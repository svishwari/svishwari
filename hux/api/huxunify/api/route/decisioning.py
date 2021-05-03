"""
purpose of this script is for housing the decision routes for the API.
"""
from http import HTTPStatus
from typing import Tuple, List

from flask import Blueprint
from flask_apispec import marshal_with
from flasgger import SwaggerView

from huxunify.api.route.utils import (
    add_view_to_blueprint,
    handle_api_exception,
)
from huxunify.api.schema.model import (
    ModelSchema,
    ModelVersionSchema,
    FeatureSchema,
    PerformanceMetricSchema,
    LiftSchema,
    DriftSchema,
    FeatureImportance,
)
from huxunify.api.data_connectors import tecton
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c

MODELS_TAG = "model"
MODELS_DESCRIPTION = "MODEL API"
MODELS_ENDPOINT = "models"

# setup the models blueprint
model_bp = Blueprint(MODELS_ENDPOINT, import_name=__name__)


@add_view_to_blueprint(model_bp, f"/{MODELS_ENDPOINT}", "ModelsView")
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
    tags = [MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(ModelSchema(many=True))
    def get(self) -> Tuple[List[dict], int]:
        """Retrieves all models.

        ---

        Returns:
            Tuple[List[dict], int] dict of models and http code

        """
        try:
            return tecton.get_models(), HTTPStatus.OK.value

        except Exception as exc:
            raise handle_api_exception(exc, "Unable to get models.") from exc


@add_view_to_blueprint(
    model_bp, f"/{MODELS_ENDPOINT}/<name>/version-history", "ModelVersionView"
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
    tags = [MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(ModelVersionSchema(many=True))
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieve model versions by model name.

        ---
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
    model_bp, f"/{MODELS_ENDPOINT}/<name>/features", "ModelFeatureView"
)
class ModelFeatureView(SwaggerView):
    """
    Model Feature Class
    """

    parameters = api_c.MODEL_NAME_PARAMS
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model features.",
            "schema": {"type": "array", "items": FeatureSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(FeatureSchema(many=True))
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieve model features by model name.

        ---
        Args:
            name (str): model name

        Returns:
            Tuple[List[dict], int]: dict of model features and http code

        """
        try:
            return tecton.get_model_features(name), HTTPStatus.OK.value

        except Exception as exc:
            raise handle_api_exception(
                exc, "Unable to get model features."
            ) from exc


@add_view_to_blueprint(
    model_bp,
    f"/{MODELS_ENDPOINT}/<name>/performance-metrics",
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
    tags = [MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(PerformanceMetricSchema(many=True))
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieve model performance metrics.

        ---
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
    f"/{MODELS_ENDPOINT}/<name>/feature-importance",
    "ModelImportanceView",
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
    tags = [MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(FeatureImportance(many=True))
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieve model feature importance.

        ---
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
    f"/{MODELS_ENDPOINT}/<name>/lift",
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
    tags = [MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(LiftSchema(many=True))
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieve model lift.

        ---
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
    f"/{MODELS_ENDPOINT}/<name>/drift",
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
    tags = [MODELS_TAG]

    # pylint: disable=no-self-use
    @marshal_with(DriftSchema(many=True))
    def get(self, name: str) -> Tuple[List[dict], int]:
        """Retrieve model drift.

        ---
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
