import inspect
import json
from pprint import pprint
from datetime import datetime
from typing import Tuple

import requests
from huxmodelclient import api_client, configuration
from huxmodelclient.api import DefaultApi as dec_client
from huxunify.api.config import get_config
import huxunify.api.constants as api_c


token = "eyJraWQiOiJoTjFIeDl6ZGVyZWVDbmRlU2dfWGZjRzJtZDhIZGFVYUk4MkRKRFltV0dZIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIwMHVhNjB6ZjFpMm1OakhzSzJwNyIsIm5hbWUiOiJKaW0gTWNNYWhvbiIsImVtYWlsIjoiamltY21haG9uQGRlbG9pdHRlLmNvbSIsInZlciI6MSwiaXNzIjoiaHR0cHM6Ly9kZWxvaXR0ZWRpZ2l0YWwtbXMub2t0YS5jb20iLCJhdWQiOiIwb2FiZWxjMGh5Z3BteDRPVDJwNyIsImlhdCI6MTY1MTg3OTIxNiwiZXhwIjoxNjUxODgyODE2LCJqdGkiOiJJRC4tcy15MF83WmtIX1hZQVBDc3BVVUFYaV94NkxVeDRWVlJoX1dZOVJ3aHE4IiwiYW1yIjpbInN3ayIsInB3ZCIsIm1mYSJdLCJpZHAiOiIwb2FmZHVzNGhyM01pRGZ0QjJwNiIsIm5vbmNlIjoiemJnRVQ3UkFEUnlyRnRZVXJaWUkwakd0OWxkZzVqV3VzVmVpMVlGT0gwQTlNNXR3OXA5UXM4c3NUMWlMM1ZNcyIsInByZWZlcnJlZF91c2VybmFtZSI6ImppbWNtYWhvbkBkZWxvaXR0ZS5jb20iLCJhdXRoX3RpbWUiOjE2NTE4NzkyMDUsImF0X2hhc2giOiJiWnlHT0YxS2htQWtIY1hwZ0R6RHR3In0.EaJAnmSQSEF59t0F5mgzdk2VDBs2pYUnkU89qE6L1WhHaqLo0pq3ZMLt6HyT-PftosxNErYmQu__v-Tv5Xq9Pf4eE3vnNqYX6D8IS5hTjgc3EwAFdcYFWKw1biMFAIndj3oKQwU1uGXFnymtbMCtq6PPoeS499zUSBhu_7FS_0t5N6bxd_eHFUZiwtu2cEOlJ1CySY6hnfXd9dFY4A0MeBBz7LSWp5x8xOXb0JYsPmUvuM3JSYMqPMaajaTBlUzA6wzFdfj6vrINwfmjb0rK6Ux1jqWtMV5GflB-eqO55_9IVKhsjjfDMsEnarqfM2i-4v3BddcGUFDmwDnLpJb3NQ"


def dec_call(url: str):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url=url, headers=headers).json()


class Decisioning:
    def __init__(self, token: str):
        self.token = token
        config = configuration.Configuration(
            host="https://hux-model-api-dec.decisioning-pendleton.in"
        )
        # config = configuration.Configuration(get_config().DECISIONING_URL)
        self.decisioning_client = dec_client(
            api_client=api_client.ApiClient(
                configuration=config,
                header_name="Authorization",
                header_value=f"Bearer {token}",
            )
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
                if info.model_metrics["version_number"] == model_version:
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

    # TODO need to sort this out with no token
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

        # return self.decisioning_client.healthz_api_v1alpha1_healthz_get()

    # TODO good
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
                    "id": model_info.model_id,
                    "name": model_info.model_metadata.model_name,
                    "description": model_info.model_metadata.description,
                    "status": model_info.model_metadata.status.lower(),
                    "latest_version": model_info.model_version,
                    "owner": model_info.model_metadata.owner,
                    "lookback_window": model_info.model_metadata.lookback_days,
                    "prediction_window": model_info.model_metadata.prediction_days,
                    "fulcrum_date": model_info.model_metadata.fulcrum_date,
                    "last_trained": model_info.scheduled_date,
                    "type": model_info.model_metadata.model_type.lower(),
                    "category": model_info.model_metadata.model_type.lower(),
                    "past_version_count": model_info.past_version_count,
                    "is_enabled": True,
                    "is_added": True,
                }
            )

        return models

    # TODO good
    def get_model_overview(self, model_id: str) -> dict:
        """Get the feature importance for a model

        Args:
            model_id (str): ID of the model.

        Returns:
            list: feature importance statistics for the model.
        """
        model_info = self.get_model_info(model_id)
        rmse = model_info.model_metrics.get("rmse", None)

        return {
            "model_type": model_info.model_metadata.model_type,
            "model_name": model_info.model_metadata.model_name,
            "description": model_info.model_metadata.description,
            "performance_metric": {
                "rmse": rmse if rmse else -1.0,
                "auc": model_info.model_metrics["AUC"],
                "precision": model_info.model_metrics["precision"],
                "recall": model_info.model_metrics["recall"],
                "current_version": model_info.model_version,
            },
        }

    # TODO good (limit)
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
                    "id": feature["model_id"],
                    "name": feature["model_name"],
                    "description": feature["feature_description"],
                    "feature_type": feature["model_type"],
                    "records_not_null": "-",
                    "feature_importance": "-",
                    "mean": "-",
                    "min": "-",
                    "max": "-",
                    "unique_values": "-",
                    "lcuv": "-",
                    "mcuv": "-",
                }
            )

        return features

    # TODO good
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
                    "id": model_info.model_id,
                    "name": model_info.model_metadata.model_name,
                    "description": model_info.model_metadata.description,
                    "status": model_info.model_metadata.status,
                    "version": model_info.model_version,
                    "trained_date": model_info.scheduled_date,
                    "owner": model_info.model_metadata.owner,
                    "lookback_window": model_info.model_metadata.lookback_days,
                    "prediction_window": model_info.model_metadata.prediction_days,
                    "fulcrum_date": model_info.model_metadata.fulcrum_date,
                }
            )

        return feature_history

    # TODO HUS-2969
    def get_model_pipeline_performance(self, model_id: str) -> dict:
        """Get the model performance of a model.

        Args:
            model_id (str): ID of the model.

        Returns:
            dict: pipeline performance statistics.
        """

        return {
            "training": {
                "id": model_id,
                "most_recent_run_duration": "-",
                "run_duration": [
                    {
                        "status": "-",
                        "timestamp": "-",
                        "duration": "-",
                    }
                ],
                "last_run": "-",
                "frequency": "-",
                "total_runs": "-",
            },
            "scoring": {
                "most_recent_run_duration": "-",
                "run_duration": [
                    {
                        "status": "-",
                        "timestamp": "-",
                        "duration": "-",
                    }
                ],
                "last_run": "-",
                "frequency": "-",
                "total_runs": "-",
            },
        }

    # TODO good
    def get_model_lift(self, model_id: str) -> list:
        """Get the lift statics of a model.

        Args:
            model_id (str): ID of the model.

        Returns:
            list: lift statistics.
        """
        lift_stats = []
        model_info = self.get_model_info(model_id)

        for lift_info in model_info.lift_chart:
            lift_stats.append(
                {
                    api_c.BUCKET: lift_info["bucket"],
                    api_c.PREDICTED_VALUE: lift_info["predicted"],
                    api_c.ACTUAL_VALUE: lift_info["actual"],
                    api_c.PROFILE_COUNT: lift_info["profiles"],
                    api_c.PREDICTED_RATE: lift_info["rate_predicted"],
                    api_c.ACTUAL_RATE: lift_info["rate_actual"],
                    api_c.PREDICTED_LIFT: lift_info["lift_predicted"],
                    api_c.ACTUAL_LIFT: lift_info["lift_actual"],
                    api_c.PROFILE_SIZE_PERCENT: lift_info["size_profile"],
                }
            )

        return lift_stats

    # TODO test (cant use version here?)
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
            drift_data.append(
                {
                    api_c.DRIFT: model_info.model_metrics["AUC"],
                    api_c.RUN_DATE: datetime.strptime(
                        model_info.scheduled_date, "%Y-%m-%d"
                    ),
                }
            )

        return drift_data


if __name__ == "__main__":
    model_id = "model-Propensity_ctg_tk_blanket-v5-dev"
    print(Decisioning(token).get_health_status())
    # print(Decisioning(token).get_model_drift(model_id))
    # print(Decisioning().get_all_models())
    # print(Decisioning().get_health_status()
