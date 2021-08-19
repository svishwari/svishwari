"""
purpose of this script is for housing the decision routes for the API.
"""
from datetime import datetime
from http import HTTPStatus
from typing import Tuple, List

from flask import Blueprint, jsonify
from flask_apispec import marshal_with
from flasgger import SwaggerView
from huxunifylib.database.cache_management import (
    create_cache_entry,
    get_cache_entry,
)

from huxunify.api.route.utils import (
    add_view_to_blueprint,
    handle_api_exception,
    secured,
    api_error_handler,
    get_db_client,
)
from huxunify.api.schema.model import (
    ModelSchema,
    ModelVersionSchema,
    DriftSchema,
    ModelDashboardSchema,
    FeatureSchema,
)
from huxunify.api.data_connectors import tecton
from huxunify.api.schema.utils import AUTH401_RESPONSE
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
    """
    Models Class
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of models.",
            "schema": {"type": "array", "items": ModelSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[List[dict], int]:
        """Retrieves all models.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[List[dict], int] dict of models and http code

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
    """
    Model Version Class
    """

    parameters = api_c.MODEL_ID_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model version history.",
            "schema": {"type": "array", "items": ModelVersionSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self, model_id: int) -> Tuple[List[dict], int]:
        """Retrieves model version history.

        ---
        security:
            - Bearer: [Authorization]

        Args:
            model_id (int): model id

        Returns:
            Tuple[List[dict], int]: dict of model versions and http code

        """
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
    """
    Model Overview Class
    """

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
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self, model_id: int) -> Tuple[dict, int]:
        """Retrieves model overview.

        ---
        security:
            - Bearer: [Authorization]

        Args:
            model_id (int): model id

        Returns:
            Tuple[dict, int]: dict of model features and http code

        """
        model_id = int(model_id)

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
            # TODO - HUS-894, return Drift/Lift data.
            api_c.LIFT_DATA: [
                {
                    api_c.BUCKET: api_c.SUPPORTED_MODELS[model_id][
                        api_c.LIFT_DATA
                    ][api_c.BUCKET][x],
                    api_c.PREDICTED_VALUE: api_c.SUPPORTED_MODELS[model_id][
                        api_c.LIFT_DATA
                    ][api_c.PREDICTED_VALUE][x],
                    api_c.ACTUAL_VALUE: api_c.SUPPORTED_MODELS[model_id][
                        api_c.LIFT_DATA
                    ][api_c.ACTUAL_VALUE][x],
                    api_c.PROFILE_COUNT: api_c.SUPPORTED_MODELS[model_id][
                        api_c.LIFT_DATA
                    ][api_c.PROFILE_COUNT][x],
                    api_c.PREDICTED_RATE: api_c.SUPPORTED_MODELS[model_id][
                        api_c.LIFT_DATA
                    ][api_c.PREDICTED_RATE][x],
                    api_c.ACTUAL_RATE: api_c.SUPPORTED_MODELS[model_id][
                        api_c.LIFT_DATA
                    ][api_c.ACTUAL_RATE][x],
                    api_c.PREDICTED_LIFT: api_c.SUPPORTED_MODELS[model_id][
                        api_c.LIFT_DATA
                    ][api_c.PREDICTED_LIFT][x],
                    api_c.ACTUAL_LIFT: api_c.SUPPORTED_MODELS[model_id][
                        api_c.LIFT_DATA
                    ][api_c.ACTUAL_LIFT][x],
                    api_c.PROFILE_SIZE_PERCENT: api_c.SUPPORTED_MODELS[
                        model_id
                    ][api_c.LIFT_DATA][api_c.PROFILE_SIZE_PERCENT][x],
                }
                for x in range(10)
            ],
        }

        # dump schema and return to client.
        return (
            ModelDashboardSchema().dump(overview_data),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<name>/drift",
    "ModelDriftView",
)
class ModelDriftView(SwaggerView):
    """
    Model Drift Class
    """

    parameters = api_c.MODEL_NAME_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model drift.",
            "schema": {"type": "array", "items": DriftSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(DriftSchema(many=True))
    @api_error_handler()
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieves model drift details.

        ---
        security:
            - Bearer: [Authorization]

        Args:
            name (str): model name

        Returns:
            Tuple[List[dict], int]: dict of model drift and http code

        """
        try:
            return tecton.get_model_drift(name), HTTPStatus.OK.value

        except Exception as exc:
            raise handle_api_exception(
                exc, "Unable to get model drift."
            ) from exc


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<model_id>/features",
    "ModelFeaturesView",
)
class ModelFeaturesView(SwaggerView):
    """
    Model Features Class
    """

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
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(
        self,
        model_id: int,
        model_version: str = None,
    ) -> Tuple[List[dict], int]:
        """Retrieves model features.

        ---
        security:
            - Bearer: [Authorization]

        Args:
            model_id (int): model id
            model_version (str): model version.

        Returns:
            Tuple[List[dict], int]: dict of model features and http code

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
        features = get_cache_entry(database, f"features.{1}.{model_version}")

        # if no cache, grab from Tecton and cache after.
        if not features:
            features = tecton.get_model_features(model_id, model_version)
            create_cache_entry(
                database, f"features.{1}.{model_version}", features
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
    """
    Model Feature Importance Class
    """

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
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(
        self,
        model_id: int,
        model_version: str = None,
        limit: int = 20,
    ) -> Tuple[List[dict], int]:
        """Retrieves top model features sorted by score.

        ---
        security:
            - Bearer: [Authorization]

        Args:
            model_id (int): model id
            model_version (str): model version.
            limit (int): Limit of features to return, default is 20.

        Returns:
            Tuple[List[dict], int]: dict of model features and http code

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
