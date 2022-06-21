"""This module holds the decisioning class that connects to the decisioning
metrics API."""
from datetime import datetime
from typing import Tuple

from huxmodelclient import api_client, configuration
from huxmodelclient.api import DefaultApi as dec_client

from huxunifylib.database import constants as db_c
import huxunify.api.constants as api_c
from huxunify.api.config import get_config
from huxunify.api.prometheus import record_health_status, Connections
from huxunify.api.data_connectors import den_stub


class DotNotationDict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def convert_model_to_dot_notation(model_info) -> DotNotationDict:
    """Convert a model to dot notation to simulate the DEN response.

    Args:
        model_info (dict): input model dict.

    Returns:
       DotNotationDict: converted model den object.
    """
    # pylint: disable=attribute-defined-outside-init
    # convert model to dot notation dict
    model = DotNotationDict(model_info)
    model.model_metadata = DotNotationDict(model.model_metadata)
    model.model_metrics = DotNotationDict(model.model_metrics)
    model.important_features = [
        DotNotationDict(x) for x in model.important_features
    ]
    model.lift_chart = [DotNotationDict(x) for x in model.lift_chart]
    return model


class DenStubClient:
    """class used to simulate the den stub client."""

    @staticmethod
    def get_models_api_v1alpha1_models_get() -> DotNotationDict:
        """get models simulation.

        Returns:
            DotNotationDict: model dictionary.
        """
        return [DotNotationDict(x) for x in den_stub.MODEL_ID_RESPONSE]

    @staticmethod
    def get_model_info_api_v1alpha1_models_model_id_get(
        model_id,
    ) -> DotNotationDict:
        """get the model info data lookup based on model IDs above.

        Args:
            model_id (str): model id.

        Returns:
            DotNotationDict: model info dictionary.
        """

        # convert to an attr dict.
        return [
            convert_model_to_dot_notation(x)
            for x in den_stub.MODEL_INFO_RESPONSE.get(model_id, [])
        ]


# pylint: disable=redefined-outer-name
class Decisioning:
    """Decisioning metrics connector class"""

    def __init__(self, token: str):
        self.token = token
        self.decisioning_client = (
            dec_client(
                api_client=api_client.ApiClient(
                    configuration=configuration.Configuration(
                        host=get_config().DECISIONING_URL
                    ),
                    header_name="Authorization",
                    header_value=self.token,
                )
            )
            if get_config().ENV_NAME == api_c.STAGING_ENV
            else DenStubClient()
        )

    def get_all_model_ids(self) -> list:
        """Gets a list of all models from decisioning.

        Returns:
            list: list of model names.
        """
        resp = self.decisioning_client.get_models_api_v1alpha1_models_get()
        return [model.model_id for model in resp]

    def get_model_info(self, model_id: str, model_version: str = None) -> dict:
        """Gets the current info for a model from decisioning.

        If model_version is provided the function will try to find
        that version. If it is not found, the most recent version
        is returned. If model_version is not provided the most
        recent version is returned.

        Args:
            model_id (str): ID of the model.
            model_version (str): version of the model.

        Returns:
            dict: model info dictionary.
        """
        model_infos = self.decisioning_client.get_model_info_api_v1alpha1_models_model_id_get(
            model_id
        )
        desired_info = None
        if model_version:
            for info in model_infos:
                if info.model_metrics[api_c.VERSION_NUMBER] == model_version:
                    desired_info = info
                    break
        if not desired_info:
            desired_info = max(
                model_infos,
                key=lambda info: datetime.strptime(
                    info.scheduled_date, "%Y-%m-%d"
                ),
            )
        desired_info.past_version_count = len(model_infos)
        return desired_info

    def get_model_info_history(self, model_id: str) -> list:
        """Gets current and previous info objects for a model from decisioning.

        Args:
            model_id (str): ID of the model.

        Returns:
            list: list of model info.
        """
        return self.decisioning_client.get_model_info_api_v1alpha1_models_model_id_get(
            model_id
        )

    # pylint: disable=no-member, broad-except
    @record_health_status(Connections.DECISIONING)
    def get_health_status(self) -> Tuple[bool, str]:
        """Get the health status of the Decisioning API

        Returns:
            Tuple[bool, str]: Returns if the connection is valid, and the message.
        """
        try:
            health = self.decisioning_client.healthz_api_v1alpha1_healthz_get()
            if health.status == "Ok":
                return True, "Decisioning Metrics API available"
        except Exception as exc:
            if exc.status:
                if exc.status == 401:
                    return True, "Decisioning Metrics API available"

        return False, "Decisioning Metrics API unavailable"

    def get_all_models(self) -> list:
        """Gets a list of all models

        Returns:
            list: list of all models
        """
        models = []
        model_ids = self.get_all_model_ids()
        for model_id in model_ids:
            model_info = self.get_model_info(model_id)

            models.append(
                {
                    api_c.ID: model_id,
                    api_c.NAME: model_info.model_metadata.model_name,
                    api_c.DESCRIPTION: model_info.model_metadata.description,
                    api_c.STATUS: model_info.model_metadata.status.title(),
                    api_c.LATEST_VERSION: model_info.model_metrics[
                        api_c.VERSION_NUMBER
                    ],
                    api_c.OWNER: model_info.model_metadata.owner,
                    api_c.LOOKBACK_WINDOW: model_info.model_metadata.lookback_days,
                    api_c.PREDICTION_WINDOW: model_info.model_metadata.prediction_days,
                    api_c.FULCRUM_DATE: datetime.strptime(
                        model_info.model_metadata.fulcrum_date, "%Y-%M-%d"
                    ),
                    api_c.LAST_TRAINED: datetime.strptime(
                        model_info.scheduled_date, "%Y-%M-%d"
                    ),
                    api_c.TYPE: model_info.model_metadata.model_type.lower(),
                    api_c.CATEGORY: model_info.model_metadata.model_type.lower(),
                    api_c.PAST_VERSION_COUNT: model_info.past_version_count,
                    db_c.ENABLED: True,
                    db_c.ADDED: True,
                    api_c.TAGS: api_c.MODEL_NAME_TAGS_MAP.get(
                        model_info.model_metadata.model_name, None
                    ),
                }
            )

        return models

    def get_model_overview(self, model_id: str, model_version: str) -> dict:
        """Get the feature importance for a model

        Args:
            model_id (str): ID of the model.
            model_version (str): Version of the model.

        Returns:
            list: feature importance statistics for the model.
        """
        model_info = self.get_model_info(model_id, model_version)

        return {
            api_c.MODEL_TYPE: model_info.model_metadata.model_type,
            api_c.MODEL_NAME: model_info.model_metadata.model_name,
            api_c.DESCRIPTION: model_info.model_metadata.description,
            api_c.PERFORMANCE_METRIC: {
                api_c.RMSE: model_info.model_metrics.get(
                    api_c.RMSE.upper(), -1
                ),
                api_c.AUC: model_info.model_metrics.get(api_c.AUC.upper(), -1),
                api_c.PRECISION: model_info.model_metrics.get(
                    api_c.PRECISION, -1
                ),
                api_c.RECALL: model_info.model_metrics.get(api_c.RECALL, -1),
                api_c.CURRENT_VERSION: model_info.model_metrics[
                    api_c.VERSION_NUMBER
                ],
            },
        }

    def get_model_features(
        self, model_id: str, model_version: str = None
    ) -> list:
        """Get the features for a model.

        Args:
            model_id (str): ID of the model.
            model_version (str): Version of the model.

        Returns:
            list: feature statistics for the model.
        """
        features = []
        model_info = self.get_model_info(model_id, model_version)

        for feature in model_info.important_features:
            features.append(
                {
                    api_c.ID: feature[api_c.MODEL_ID],
                    # make the feature name unique
                    api_c.NAME: f"{feature[api_c.MODEL_NAME]}-{feature.rank}",
                    api_c.DESCRIPTION: feature[api_c.FEATURE_DESCRIPTION],
                    api_c.FEATURE_TYPE: feature[api_c.MODEL_TYPE],
                    api_c.RECORDS_NOT_NULL: 0,
                    api_c.FEATURE_IMPORTANCE: 1,
                    api_c.MEAN: 0,
                    api_c.MIN: 0,
                    api_c.MAX: 0,
                    api_c.UNIQUE_VALUES: 1,
                    api_c.LCUV: "",
                    api_c.MCUV: "",
                    api_c.SCORE: feature.lift,
                }
            )

        return features

    def get_model_version_history(self, model_id: str) -> list:
        """Get the feature importance for a model

        Args:
            model_id (str): ID of the model.

        Returns:
            list: feature importance statistics for the model.
        """
        model_infos = self.get_model_info_history(model_id)

        feature_history = []

        for model_info in model_infos:
            feature_history.append(
                {
                    api_c.ID: model_info.model_id,
                    api_c.NAME: model_info.model_metadata.model_name,
                    api_c.DESCRIPTION: model_info.model_metadata.description,
                    api_c.STATUS: model_info.model_metadata.status,
                    api_c.CURRENT_VERSION: model_info.model_metrics[
                        api_c.VERSION_NUMBER
                    ],
                    api_c.LAST_TRAINED: model_info.scheduled_date,
                    api_c.OWNER: model_info.model_metadata.owner,
                    api_c.LOOKBACK_WINDOW: model_info.model_metadata.lookback_days,
                    api_c.PREDICTION_WINDOW: model_info.model_metadata.prediction_days,
                    api_c.FULCRUM_DATE: model_info.model_metadata.fulcrum_date,
                }
            )

        return feature_history

    # TODO HUS-2969
    # pylint: disable=no-self-use, unused-argument
    def get_model_pipeline_performance(
        self, model_id: str, model_version: str
    ) -> dict:
        """Get the model performance of a model.

        Args:
            model_id (str): ID of the model.
            model_version (str): Version of the model.

        Returns:
            dict: pipeline performance statistics.
        """

        return {
            "training": {
                "id": model_id,
                "most_recent_run_duration": None,
                "run_duration": [
                    {
                        "status": None,
                        "timestamp": None,
                        "duration": None,
                    }
                ],
                "last_run": None,
                "frequency": None,
                "total_runs": None,
            },
            "scoring": {
                "most_recent_run_duration": None,
                "run_duration": [
                    {
                        "status": None,
                        "timestamp": None,
                        "duration": None,
                    }
                ],
                "last_run": None,
                "frequency": None,
                "total_runs": None,
            },
        }

    def get_model_lift(self, model_id: str, model_version: str) -> list:
        """Get the lift statics of a model.

        Args:
            model_id (str): ID of the model.
            model_version (str): Version of the model.

        Returns:
            list: lift statistics.
        """
        lift_stats = []
        model_info = self.get_model_info(model_id, model_version)

        for lift_info in model_info.lift_chart:
            lift_stats.append(
                {
                    api_c.BUCKET: lift_info[api_c.BUCKET],
                    api_c.PREDICTED_VALUE: lift_info[api_c.PREDICTED],
                    api_c.ACTUAL_VALUE: lift_info[api_c.ACTUAL],
                    api_c.PROFILE_COUNT: lift_info[api_c.PROFILES],
                    api_c.PREDICTED_RATE: lift_info[api_c.RATE_PREDICTED],
                    api_c.ACTUAL_RATE: lift_info[api_c.RATE_ACTUAL],
                    api_c.PREDICTED_LIFT: lift_info[api_c.LIFT_PREDICTED],
                    api_c.ACTUAL_LIFT: lift_info[api_c.LIFT_ACTUAL],
                    api_c.PROFILE_SIZE_PERCENT: lift_info[api_c.SIZE_PROFILE],
                }
            )

        return lift_stats

    # pylint: disable=unused-argument
    def get_model_drift(
        self, model_id: str, model_version: str = None
    ) -> list:
        """Get the drift statics of a model.

        Args:
            model_id (str): ID of the model.
            model_version (str): Version of the model.

        Returns:
            list: list of drift statistics.
        """
        model_infos = self.get_model_info_history(model_id)
        drift_data = []

        for model_info in model_infos:
            # get metric based on model type
            metric_type = (
                api_c.AUC.upper()
                if api_c.AUC.upper() in model_info.model_metrics
                else api_c.RMSE.upper()
            )
            drift_data.append(
                {
                    api_c.DRIFT: model_info.model_metrics.get(metric_type, -1),
                    api_c.RUN_DATE: datetime.strptime(
                        model_info.scheduled_date, "%Y-%m-%d"
                    ),
                }
            )

        return drift_data
