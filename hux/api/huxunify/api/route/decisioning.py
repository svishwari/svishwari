"""Purpose of this script is for housing the decision routes for the API"""
from random import uniform, randint
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Tuple, List

from flask import Blueprint, jsonify
from flasgger import SwaggerView
from huxunifylib.database.cache_management import (
    create_cache_entry,
    get_cache_entry,
)

from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
)
from huxunify.api.route.utils import (
    get_db_client,
)
from huxunify.api.schema.model import (
    ModelSchema,
    ModelVersionSchema,
    ModelDriftSchema,
    ModelLiftSchema,
    ModelDashboardSchema,
    FeatureSchema,
)
from huxunify.api.data_connectors import tecton
from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
    FAILED_DEPENDENCY_424_RESPONSE,
)
from huxunify.api import constants as api_c

# setup the models blueprint
model_bp = Blueprint(api_c.MODELS_ENDPOINT, import_name=__name__)


@model_bp.before_request
@secured()
def before_request():
    """Protect all of the model endpoints."""
    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(model_bp, api_c.MODELS_ENDPOINT, "ModelsView")
class ModelsView(SwaggerView):
    """Models Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of models.",
            "schema": {"type": "array", "items": ModelSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[List[dict], int]:
        """Retrieves all models.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[List[dict], int]: list containing dict of models, HTTP status code.
        """

        purchase_model = {
            api_c.TYPE: "purchase",
            api_c.FULCRUM_DATE: datetime(2021, 6, 26),
            api_c.PAST_VERSION_COUNT: 0,
            api_c.LAST_TRAINED: datetime(2021, 6, 26),
            api_c.LOOKBACK_WINDOW: 365,
            api_c.NAME: "Propensity to Purchase",
            api_c.DESCRIPTION: "Propensity of a customer making a purchase "
            "after receiving an email.",
            api_c.LATEST_VERSION: "",
            api_c.PREDICTION_WINDOW: 365,
            api_c.ID: 3,
            api_c.OWNER: "Susan Miller",
            api_c.STATUS: api_c.STATUS_PENDING,
        }
        all_models = tecton.get_models()
        all_models.append(purchase_model)
        all_models.sort(key=lambda x: x[api_c.NAME])
        return (
            jsonify(ModelSchema(many=True).dump(all_models)),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<model_id>/version-history",
    "ModelVersionView",
)
class ModelVersionView(SwaggerView):
    """Model Version Class."""

    parameters = api_c.MODEL_ID_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model version history.",
            "schema": {"type": "array", "items": ModelVersionSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self, model_id: str) -> Tuple[List[dict], int]:
        """Retrieves model version history.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.

        Returns:
            Tuple[List[dict], int]: List containing dict of model versions, HTTP status code.
        """

        # TODO Remove once Propensity to Purchase info can be retrieved from tecton
        if model_id == "3":
            version_history = [
                {
                    api_c.ID: model_id,
                    api_c.LAST_TRAINED: datetime(2021, 6, 24 + i),
                    api_c.DESCRIPTION: "Propensity of a customer making a purchase"
                    " after receiving an email.",
                    api_c.FULCRUM_DATE: datetime(2021, 6, 24 + i),
                    api_c.LOOKBACK_WINDOW: 90,
                    api_c.NAME: "Propensity to Purchase",
                    api_c.OWNER: "Susan Miller",
                    api_c.STATUS: api_c.STATUS_ACTIVE,
                    api_c.CURRENT_VERSION: f"22.8.3{i}",
                    api_c.PREDICTION_WINDOW: 90,
                }
                for i in range(3)
            ]

        else:
            version_history = tecton.get_model_version_history(model_id)

        # sort by version
        if version_history:
            version_history.sort(
                key=lambda s: [
                    int(u)
                    for u in s.get(api_c.CURRENT_VERSION).split(".")
                    if s.get(api_c.CURRENT_VERSION)
                ],
                reverse=True,
            )

        return (
            jsonify(ModelVersionSchema(many=True).dump(version_history)),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    model_bp, f"{api_c.MODELS_ENDPOINT}/<model_id>/overview", "ModelOverview"
)
class ModelOverview(SwaggerView):
    """Model Overview Class."""

    parameters = api_c.MODEL_ID_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model features.",
            "schema": ModelDashboardSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve model overview"
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self, model_id: str) -> Tuple[dict, int]:
        """Retrieves model overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.

        Returns:
            Tuple[dict, int]: dict of model features, HTTP status code.
        """

        # TODO Remove once Propensity to Purchase model data is being served
        #  from tecton.
        if model_id == "3":
            overview_data = api_c.PROPENSITY_TO_PURCHASE_MODEL_OVERVIEW_STUB
        else:
            # get model information
            model_versions = tecton.get_model_version_history(model_id)

            # if model versions not found, return not found.
            if not model_versions:
                return {}, HTTPStatus.NOT_FOUND

            # take the latest model
            latest_model = model_versions[-1]

            # generate the output
            overview_data = {
                api_c.MODEL_ID: latest_model[api_c.ID],
                api_c.MODEL_TYPE: latest_model[api_c.TYPE],
                api_c.MODEL_NAME: latest_model[api_c.NAME],
                api_c.DESCRIPTION: latest_model[api_c.DESCRIPTION],
                # get the performance metrics for a given model
                api_c.PERFORMANCE_METRIC: tecton.get_model_performance_metrics(
                    model_id,
                    latest_model[api_c.TYPE],
                    latest_model[api_c.CURRENT_VERSION],
                ),
            }

        # dump schema and return to client.
        return (
            ModelDashboardSchema().dump(overview_data),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<model_id>/drift",
    "ModelDriftView",
)
class ModelDriftView(SwaggerView):
    """Model Drift Class"""

    parameters = api_c.MODEL_ID_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model drift.",
            "schema": {"type": "array", "items": ModelDriftSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to fetch drift data",
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self, model_id: int) -> Tuple[List[dict], int]:
        """Retrieves model drift details.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.

        Returns:
            Tuple[List[dict], int]: List containing dict of model drift, HTTP status code.
        """

        # TODO Remove once Propensity to Purchase data is being served
        # from tecton
        if model_id == "3":
            drift_data = [
                {
                    api_c.DRIFT: round(uniform(0.8, 1), 2),
                    api_c.RUN_DATE: datetime(2021, 6, 1) + timedelta(i),
                }
                for i in range(4)
            ]
        else:
            # get model information
            model_versions = tecton.get_model_version_history(model_id)

            # if model versions not found, return not found.
            if not model_versions:
                return {}, HTTPStatus.NOT_FOUND

            # take the latest model
            latest_model = model_versions[-1]

            drift_data = tecton.get_model_drift(
                model_id, latest_model[api_c.TYPE]
            )

        return (
            jsonify(ModelDriftSchema(many=True).dump(drift_data)),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<model_id>/features",
    "ModelFeaturesView",
)
class ModelFeaturesView(SwaggerView):
    """Model Features Class."""

    parameters = [
        api_c.MODEL_ID_PARAMS[0],
        {
            "name": api_c.VERSION,
            "description": "Model version, if not provided, it will take the latest.",
            "type": "str",
            "in": "path",
            "required": False,
            "example": "21.7.31",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model features.",
            "schema": {"type": "array", "items": ModelVersionSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(
        self,
        model_id: str,
        model_version: str = None,
    ) -> Tuple[List[dict], int]:
        """Retrieves model features.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.
            model_version (str): Model Version.

        Returns:
            Tuple[List[dict], int]: List containing dict of model features, HTTP status code.
        """

        # TODO: Remove once this model data becomes available and can be fetched from Tecton
        # intercept to check if the model_id is for propensity_to_purchase
        # to set features with stub data
        if model_id == "3":
            features = api_c.PROPENSITY_TO_PURCHASE_FEATURES_RESPONSE_STUB
        else:
            # only use the latest version if model version is None.
            if model_version is None:
                # get latest version first
                model_version = tecton.get_model_version_history(model_id)

                # check if there is a model version we can grab, if so take the last one (latest).
                model_version = (
                    model_version[-1].get(api_c.CURRENT_VERSION)
                    if model_version
                    else ""
                )

            # check cache first
            database = get_db_client()
            features = get_cache_entry(
                database, f"features.{model_id}.{model_version}"
            )

            # if no cache, grab from Tecton and cache after.
            if not features:
                features = tecton.get_model_features(model_id, model_version)
                # create cache entry in db only if features fetched from Tecton is not empty
                if features:
                    create_cache_entry(
                        database,
                        f"features.{model_id}.{model_version}",
                        features,
                    )

        return (
            jsonify(FeatureSchema(many=True).dump(features)),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<model_id>/feature-importance",
    "ModelImportanceFeaturesView",
)
class ModelImportanceFeaturesView(SwaggerView):
    """Model Feature Importance Class."""

    parameters = [
        api_c.MODEL_ID_PARAMS[0],
        {
            "name": api_c.VERSION,
            "description": "Model version, if not provided, it will take the latest.",
            "type": "str",
            "in": "path",
            "required": False,
            "example": "21.7.31",
        },
        {
            "name": api_c.LIMIT,
            "description": "Limit of features to pull, default is 20.",
            "type": "int",
            "in": "path",
            "required": False,
            "example": 20,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model feature importance.",
            "schema": {"type": "array", "items": ModelVersionSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(
        self,
        model_id: str,
        model_version: str = None,
        limit: int = 20,
    ) -> Tuple[List[dict], int]:
        """Retrieves top model features sorted by score.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.
            model_version (str): Model Version.
            limit (int): Limit of features to return, default is 20.

        Returns:
            Tuple[List[dict], int]: List containing dict of model features, HTTP status code.
        """

        # only use the latest version if model version is None.
        if model_version is None:
            # get latest version first
            model_version = tecton.get_model_version_history(model_id)

            # check if there is a model version we can grab, if so take the last one (latest).
            model_version = (
                model_version[-1].get(api_c.CURRENT_VERSION)
                if model_version
                else ""
            )

        # check cache first
        database = get_db_client()
        features = get_cache_entry(
            database, f"features.{model_id}.{model_version}"
        )

        # if no cache, grab from Tecton and cache after.
        if not features:
            features = tecton.get_model_features(model_id, model_version)
            create_cache_entry(
                database, f"features.{model_id}.{model_version}", features
            )

        # sort the top features before serving them out
        features.sort(key=lambda x: x[api_c.SCORE], reverse=True)

        return (
            jsonify(FeatureSchema(many=True).dump(features[:limit])),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<model_id>/lift",
    "ModelLiftView",
)
class ModelLiftView(SwaggerView):
    """Model Lift Class."""

    parameters = api_c.MODEL_ID_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model lift chart.",
            "schema": {"type": "array", "items": ModelLiftSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve model lift data"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(
        self,
        model_id: int,
    ) -> Tuple[List[dict], int]:
        """Retrieves model lift data.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID

        Returns:
            Tuple[List[dict], int]: List containing adict of model lift data, HTTP status code.
        """

        # retrieves lift data
        if model_id == "3":
            lift_data = [
                {
                    api_c.PREDICTED_RATE: uniform(0.01, 0.3),
                    api_c.BUCKET: 10 * i,
                    api_c.PROFILE_SIZE_PERCENT: 0,
                    api_c.ACTUAL_VALUE: randint(1000, 5000),
                    api_c.PREDICTED_LIFT: uniform(1, 5),
                    api_c.ACTUAL_RATE: uniform(0.01, 0.3),
                    api_c.PROFILE_COUNT: randint(1000, 100000),
                    api_c.ACTUAL_LIFT: uniform(1, 5),
                    api_c.PREDICTED_LIFT: round(uniform(1000, 5000), 4),
                }
                for i in range(1, 11)
            ]
        else:
            lift_data = tecton.get_model_lift_async(model_id)
        lift_data.sort(key=lambda x: x[api_c.BUCKET])

        return (
            jsonify(ModelLiftSchema(many=True).dump(lift_data)),
            HTTPStatus.OK.value,
        )
