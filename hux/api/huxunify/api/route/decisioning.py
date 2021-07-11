"""
purpose of this script is for housing the decision routes for the API.
"""
from datetime import datetime
from random import random, randint, uniform
from http import HTTPStatus
from typing import Tuple, List, Union, Dict

from flask import Blueprint
from flask_apispec import marshal_with
from flasgger import SwaggerView

from huxunify.api.route.utils import (
    add_view_to_blueprint,
    handle_api_exception,
    secured, api_error_handler,
)
from huxunify.api.schema.model import (
    ModelSchema,
    ModelVersionSchema,
    FeatureSchema,
    PerformanceMetricSchema,
    LiftSchema,
    DriftSchema,
    FeatureImportance, ModelDashboardSchema,
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
    @marshal_with(ModelSchema(many=True))
    def get(self) -> Tuple[List[dict], int]:
        """Retrieves all models.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[List[dict], int] dict of models and http code

        """
        try:
            purchase_model = {
                "type": "purchase",
                "fulcrum_date": datetime(2021, 6, 26),
                "past_version_count": 0,
                "last_trained": datetime(2021, 6, 26),
                "lookback_window": 365,
                "name": "Propensity to Purchase",
                "description": "Propensity of a customer making a purchase after receiving an email.",
                "latest_version": " ",
                "prediction_window": 365,
                "id": 3,
                "owner": "Susan Miller",
                "status": "Active"
            }
            all_models = tecton.get_models()
            all_models.append(purchase_model)
            return all_models, HTTPStatus.OK.value

        except Exception as exc:
            raise handle_api_exception(exc, "Unable to get models.") from exc


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<name>/version-history",
    "ModelVersionView",
)
class ModelVersionView(SwaggerView):
    """
    Model Version Class
    """

    parameters = api_c.MODEL_NAME_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model version history.",
            "schema": {"type": "array", "items": ModelVersionSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(ModelVersionSchema(many=True))
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieves model version history.

        ---
        security:
            - Bearer: [Authorization]

        Args:
            name (str): model name

        Returns:
            Tuple[List[dict], int]: dict of model versions and http code

        """
        try:
            return tecton.get_model_version_history(name), HTTPStatus.OK.value

        except Exception as exc:
            raise handle_api_exception(
                exc, "Unable to get model versions."
            ) from exc


@add_view_to_blueprint(
    model_bp, f"{api_c.MODELS_ENDPOINT}/<model_type>/overview", "ModelOverview"
)
class ModelFeatureView(SwaggerView):
    """
    Model Overview Class
    """

    parameters = api_c.MODEL_TYPE_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model features.",
            "schema": ModelDashboardSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve Model Overview"
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(ModelDashboardSchema)
    def get(self, model_type: str) -> Tuple[Dict, int]:
        """Retrieves model features.

        ---
        security:
            - Bearer: [Authorization]

        Args:
            model_type (str): model type

        Returns:
            Tuple[List[dict], int]: dict of model features and http code

        """
        if model_type not in api_c.SUPPORTED_MODELS:
            return {"message": "Invalid Model Type"}, HTTPStatus.BAD_REQUEST

        output = {
            api_c.MODEL_TYPE: model_type,
            api_c.MODEL_NAME: api_c.SUPPORTED_MODELS[model_type][api_c.NAME],
            api_c.DESCRIPTION: api_c.SUPPORTED_MODELS[model_type][api_c.DESCRIPTION],
            api_c.PERFORMANCE_METRIC: {
                api_c.AUC: api_c.SUPPORTED_MODELS[model_type][api_c.DESCRIPTION],
                api_c.PRECISION: api_c.SUPPORTED_MODELS[model_type][api_c.PRECISION],
                api_c.RECALL: api_c.SUPPORTED_MODELS[model_type][api_c.RECALL],
                api_c.CURRENT_VERSION: api_c.SUPPORTED_MODELS[model_type][api_c.CURRENT_VERSION],
                api_c.RMSE: api_c.SUPPORTED_MODELS[model_type][api_c.RMSE]
            },
            api_c.FEATURE_IMPORTANCE: [
                {
                    api_c.NAME: f"feature name {x}",
                    api_c.DESCRIPTION: f"description of feature name {x}",
                    api_c.SCORE: round(random(), 2)
                }
                for x in range(1, 21)
            ],
            api_c.LIFT_DATA: [
                {
                    api_c.BUCKET: x,
                    api_c.PREDICTED_VALUE: round(uniform(100, 1000), 2),
                    api_c.ACTUAL_VALUE: round(uniform(100, 1000), 2),
                    api_c.PROFILE_COUNT: randint(1, 100),
                    api_c.PREDICTED_RATE: round(random(), 2),
                    api_c.ACTUAL_RATE: round(random(), 2),
                    api_c.PREDICTED_LIFT: round(uniform(1, 2), 2),
                    api_c.ACTUAL_LIFT: round(uniform(1, 2), 2),
                    api_c.PROFILE_SIZE_PERCENT: round(uniform(1, 100), 2),
                }
                for x in range(10, 100, 10)
            ]
        }
        return output, HTTPStatus.OK


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<name>/performance-metrics",
    "ModelMetricsView",
)
class ModelMetricsView(SwaggerView):
    """
    Model Performance Metrics Class
    """

    parameters = api_c.MODEL_NAME_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model performance metrics.",
            "schema": {"type": "array", "items": PerformanceMetricSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(PerformanceMetricSchema(many=True))
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieves model performance metrics.

        ---
        security:
            - Bearer: [Authorization]

        Args:
            name (str): model name

        Returns:
            Tuple[List[dict], int]: dict of model performance metrics and http code

        """
        try:
            return (
                tecton.get_model_performance_metrics(name),
                HTTPStatus.OK.value,
            )

        except Exception as exc:
            raise handle_api_exception(
                exc, "Unable to get model performance metrics."
            ) from exc


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<name>/feature-importance",
    "ModelFeatureImportanceView",
)
class ModelFeatureImportanceView(SwaggerView):
    """
    Model Feature Importance Class
    """

    parameters = api_c.MODEL_NAME_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model feature importance.",
            "schema": {"type": "array", "items": FeatureImportance},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(FeatureImportance(many=True))
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieves model feature importance details.

        ---
        security:
            - Bearer: [Authorization]

        Args:
            name (str): model name

        Returns:
            Tuple[List[dict], int]: dict of model feature performance and http code

        """
        try:
            return (
                tecton.get_model_feature_importance(name),
                HTTPStatus.OK.value,
            )

        except Exception as exc:
            raise handle_api_exception(
                exc, "Unable to get model feature performance."
            ) from exc


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<name>/lift",
    "ModelLiftView",
)
class ModelLiftView(SwaggerView):
    """
    Model Lift Class
    """

    parameters = api_c.MODEL_NAME_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model lift.",
            "schema": {"type": "array", "items": LiftSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(LiftSchema(many=True))
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieves model lift details.

        ---
        security:
            - Bearer: [Authorization]

        Args:
            name (str): model name

        Returns:
            Tuple[List[dict], int]: dict of model lift and http code

        """
        try:
            return tecton.get_model_lift(name), HTTPStatus.OK.value

        except Exception as exc:
            raise handle_api_exception(
                exc, "Unable to get model lift."
            ) from exc


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
