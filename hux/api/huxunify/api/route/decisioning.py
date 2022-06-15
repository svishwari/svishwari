# pylint: disable=too-many-lines,unused-argument
"""Purpose of this script is for housing the
decision routes for the API"""
from random import uniform, randint, choice
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Tuple

from flask import Blueprint, jsonify, request, Response
from flasgger import SwaggerView
from huxunifylib.util.general.logging import logger
from huxunifylib.database.cache_management import (
    create_cache_entry,
    get_cache_entry,
)
from huxunifylib.database import (
    collection_management,
    notification_management,
)
from huxunifylib.database import constants as db_c

from huxunify.api.config import get_config
from huxunify.api.data_connectors.cache import Caching
from huxunify.api.data_connectors.decisioning import Decisioning

from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.route.return_util import HuxResponse
from huxunify.api.route.utils import (
    get_db_client,
)
from huxunify.api.schema.model import (
    ModelSchema,
    ModelVersionSchema,
    ModelDriftSchema,
    ModelLiftSchema,
    ModelOverviewSchema,
    FeatureSchema,
    ModelRequestPostSchema,
    ModelPipelinePerformanceSchema,
)
from huxunify.api.schema.configurations import ConfigurationsSchema
from huxunify.api.data_connectors.tecton import Tecton
from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
    FAILED_DEPENDENCY_424_RESPONSE,
    EMPTY_RESPONSE_DEPENDENCY_404_RESPONSE,
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

    parameters = [
        {
            "name": api_c.STATUS,
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "description": "Model status.",
            "example": "Requested",
            "required": False,
        }
    ]

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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves all models.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[Response, int]: list containing dict of models,
                HTTP status code.
        """
        token = request.headers.get("authorizationden")
        all_models = Caching.check_and_return_cache(
            "all_models.info",
            Decisioning(token).get_all_models,
            {},
        )

        all_models.sort(key=lambda x: x[api_c.NAME])
        all_models = list(
            filter(
                lambda model: not model.get(api_c.NAME, "")
                .lower()
                .__contains__("pendleton"),
                all_models,
            )
        )

        return HuxResponse.OK(data=all_models, data_schema=ModelSchema())


@add_view_to_blueprint(model_bp, api_c.MODELS_ENDPOINT, "SetModelStatus")
class RequestModel(SwaggerView):
    """Class to request a model."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Models request body.",
            "example": [
                {
                    api_c.TYPE: "purchase",
                    api_c.NAME: "Propensity to Purchase",
                    api_c.ID: "9a44c346ba034ac8a699ae0ab3314003",
                    api_c.STATUS: api_c.REQUESTED,
                },
                {
                    api_c.TYPE: "unsubscribe",
                    api_c.NAME: "Propensity to Unsubscribe",
                    api_c.ID: "eb5f35e34c0047d3b9022ef330952dd1",
                    api_c.STATUS: api_c.REQUESTED,
                },
            ],
        }
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": {
                "example": {api_c.MESSAGE: api_c.OPERATION_SUCCESS},
            },
            "description": "Successfully requested the model.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to request the model.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels([api_c.ADMIN_LEVEL, api_c.EDITOR_LEVEL])
    def post(self, user: dict) -> Tuple[dict, int]:
        """Request a model.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[dict, int]: Model Requested, HTTP status code.
        """
        models = ModelRequestPostSchema().load(
            request.get_json(), unknown=True, many=True
        )
        database = get_db_client()

        configurations = []
        for model in models:
            # set source of configuration as model
            model[db_c.TYPE] = api_c.MODELS_TAG

            # check if document exists
            model_document = collection_management.get_document(
                database,
                db_c.CONFIGURATIONS_COLLECTION,
                {db_c.OBJECT_ID: model.get(db_c.OBJECT_ID)},
            )

            if model_document:
                # TODO: TEMPORARILY update document.
                logger.warning(
                    "Requested model already exists %s.", model.get(db_c.NAME)
                )
                # update the document
                configurations.append(
                    collection_management.update_document(
                        database,
                        db_c.CONFIGURATIONS_COLLECTION,
                        model_document[db_c.ID],
                        model,
                        user[api_c.USER_NAME],
                    )
                )
                continue

            configurations.append(
                collection_management.create_document(
                    database=database,
                    collection=db_c.CONFIGURATIONS_COLLECTION,
                    new_doc=model,
                    username=user[api_c.USER_NAME],
                )
            )
            notification_management.create_notification(
                database,
                db_c.NOTIFICATION_TYPE_SUCCESS,
                f'Model requested "{model[db_c.NAME]}" '
                f"by {user[api_c.USER_NAME]}.",
                db_c.NOTIFICATION_CATEGORY_MODELS,
                user[api_c.USER_NAME],
            )
            logger.info(
                "User with username %s successfully requested model %s.",
                user[api_c.USER_NAME],
                model.get(db_c.NAME),
            )

        return (
            jsonify(ConfigurationsSchema(many=True).dump(configurations)),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(model_bp, api_c.MODELS_ENDPOINT, "RemoveRequestedModel")
class RemoveRequestedModel(SwaggerView):
    """Class to remove a requested model."""

    parameters = [
        {
            "name": api_c.MODEL_ID,
            "in": "query",
            "type": "string",
            "description": "Model ID.",
            "required": True,
            "example": "61928a4dce8aa67b888826f5",
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "example": {api_c.MESSAGE: api_c.OPERATION_SUCCESS},
            },
            "description": "Successfully removed the requested model.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to remove the requested model.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def delete(self, user: dict) -> Tuple[dict, int]:
        """Remove a requested model.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[dict, int]: Model Removed, HTTP status code.
        """
        database = get_db_client()

        if not request.args:
            return {
                api_c.MESSAGE: api_c.EMPTY_OBJECT_ERROR_MESSAGE
            }, HTTPStatus.BAD_REQUEST

        model_id = request.args.get(api_c.MODEL_ID)

        # get the model
        model = collection_management.get_document(
            database,
            db_c.CONFIGURATIONS_COLLECTION,
            {db_c.OBJECT_ID: model_id},
        )

        deletion_status = collection_management.delete_document(
            database=database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            query_filter={db_c.OBJECT_ID: model_id},
            hard_delete=True,
            username=user[api_c.USER_NAME],
        )

        if deletion_status:
            notification_management.create_notification(
                database,
                db_c.NOTIFICATION_TYPE_SUCCESS,
                f'Requested model "{model[db_c.NAME]}" removed by {user[api_c.USER_NAME]}.',
                db_c.NOTIFICATION_CATEGORY_MODELS,
                user[api_c.USER_NAME],
            )
            logger.info(
                "User with username %s successfully removed model %s.",
                user[api_c.USER_NAME],
                model_id,
            )
            return {api_c.MESSAGE: api_c.OPERATION_SUCCESS}, HTTPStatus.OK

        return {api_c.MESSAGE: api_c.OPERATION_FAILED}, HTTPStatus.NOT_FOUND


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<model_id>/version-history",
    "ModelVersionHistoryView",
)
class ModelVersionHistoryView(SwaggerView):
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
    responses.update(EMPTY_RESPONSE_DEPENDENCY_404_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, model_id: str, user: dict) -> Tuple[Response, int]:
        """Retrieves model version history.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.
            user (dict): User object

        Returns:
            Tuple[Response, int]: List containing dict of model versions,
                HTTP status code.
        """
        # Dec API only available in stg, all other environments are mocked
        token = request.headers.get("authorizationden")
        version_history = Caching.check_and_return_cache(
            f"model_version_history.{model_id}",
            Decisioning(token).get_model_version_history,
            {
                "model_id": model_id,
            },
        )
        return HuxResponse.OK(
            data=version_history, data_schema=ModelVersionSchema()
        )


@add_view_to_blueprint(
    model_bp, f"{api_c.MODELS_ENDPOINT}/<model_id>/overview", "ModelOverview"
)
class ModelOverview(SwaggerView):
    """Model Overview Class."""

    parameters = [
        {
            "name": api_c.MODEL_ID,
            "description": "Model id",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "1",
        },
        {
            "name": api_c.VERSION,
            "description": "Version id",
            "type": "string",
            "in": "query",
            "required": False,
            "example": "1.0.0",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model features.",
            "schema": ModelOverviewSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve model overview"
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    responses.update(EMPTY_RESPONSE_DEPENDENCY_404_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, model_id: str, user: dict) -> Tuple[Response, int]:
        """Retrieves model overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.
            user (dict): User object.

        Returns:
            Tuple[Response, int]: dict of model features, HTTP status code.
        """

        # Dec API only available in stg, all other environments are mocked
        token = request.headers.get("authorizationden")
        model_overview = Caching.check_and_return_cache(
            f"model_overview.{model_id}",
            Decisioning(token).get_model_overview,
            {
                "model_id": model_id,
                "model_version": request.args.get(api_c.VERSION, default=None),
            },
        )
        return HuxResponse.OK(
            data=model_overview, data_schema=ModelOverviewSchema()
        )


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<model_id>/drift",
    "ModelDriftView",
)
class ModelDriftView(SwaggerView):
    """Model Drift Class"""

    parameters = [
        api_c.MODEL_ID_PARAMS[0],
        {
            "name": api_c.VERSION,
            "description": "Model version, if not provided, "
            "it will take the latest.",
            "type": "str",
            "in": "query",
            "required": False,
            "example": "21.7.31",
        },
    ]
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
    responses.update(EMPTY_RESPONSE_DEPENDENCY_404_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict, model_id: str) -> Tuple[Response, int]:
        """Retrieves model drift details.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.
            model_id (str): Model ID.

        Returns:
            Tuple[Response, int]: List containing dict of model drift,
                HTTP status code.
        """

        token = request.headers.get("authorizationden")
        drift_data = Caching.check_and_return_cache(
            f"drift.{model_id}.{request.args.get(api_c.VERSION, 'current')}",
            Decisioning(token).get_model_drift,
            {
                "model_id": model_id,
                "model_version": request.args.get(api_c.VERSION, None),
            },
        )
        return HuxResponse.OK(data=drift_data, data_schema=ModelDriftSchema())


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
            "description": "Model version, if not provided, "
            "it will take the latest.",
            "type": "str",
            "in": "query",
            "required": False,
            "example": "21.7.31",
        },
        {
            "name": api_c.LIMIT,
            "description": "Limit of features to pull, default is 20.",
            "type": "int",
            "in": "query",
            "required": False,
            "example": 20,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model features.",
            "schema": {"type": "array", "items": FeatureSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    responses.update(EMPTY_RESPONSE_DEPENDENCY_404_RESPONSE)

    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(
        self,
        user: dict,
        model_id: str,
    ) -> Tuple[Response, int]:
        """Retrieves model features.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.
            model_id (str): Model ID.

        Returns:
            Tuple[Response, int]: List containing dict of model features,
                HTTP status code.
        """
        limit = int(request.args.get(api_c.LIMIT, 20))

        token = request.headers.get("authorizationden")
        features = Caching.check_and_return_cache(
            f"features.{model_id}.{request.args.get(api_c.VERSION, 'current')}",
            Decisioning(token).get_model_features,
            {
                "model_id": model_id,
                "model_version": request.args.get(api_c.VERSION, None),
            },
        )
        return HuxResponse.OK(
            data=features[:limit], data_schema=FeatureSchema()
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
            "description": "Model version, if not provided, "
            "it will take the latest.",
            "type": "str",
            "in": "query",
            "required": False,
            "example": "21.7.31",
        },
        {
            "name": api_c.LIMIT,
            "description": "Limit of features to pull, default is 20.",
            "type": "int",
            "in": "query",
            "required": False,
            "example": 20,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model feature importance.",
            "schema": {"type": "array", "items": FeatureSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(
        self,
        user: dict,
        model_id: str,
    ) -> Tuple[Response, int]:
        """Retrieves top model features sorted by score.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.
            model_id (str): Model ID.

        Returns:
            Tuple[Response, int]: List containing dict of model features,
                HTTP status code.
        """
        model_version = request.args.get(api_c.VERSION, None)

        token = request.headers.get("authorizationden")
        version_cache_key = model_version if model_version else "current"
        features = Caching.check_and_return_cache(
            f"features.{model_id}.{version_cache_key}",
            Decisioning(token).get_model_features,
            {
                "model_id": model_id,
                "model_version": model_version,
            },
        )
        return HuxResponse.OK(data=features, data_schema=FeatureSchema())


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<model_id>/lift",
    "ModelLiftView",
)
class ModelLiftView(SwaggerView):
    """Model Lift Class."""

    parameters = [
        api_c.MODEL_ID_PARAMS[0],
        {
            "name": api_c.VERSION,
            "description": "Model version, if not provided, "
            "it will take the latest.",
            "type": "str",
            "in": "query",
            "required": False,
            "example": "21.7.31",
        },
    ]
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(
        self,
        model_id: str,
        user: dict,
    ) -> Tuple[Response, int]:
        """Retrieves model lift data.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID
            user (dict): User object.

        Returns:
            Tuple[Response, int]: List containing a dict of model lift data,
                HTTP status code.
        """

        # Dec API only available in stg, all other environments are mocked
        token = request.headers.get("authorizationden")
        model_version = (
            request.args.get(api_c.VERSION)
            if request.args.get(api_c.VERSION)
            else None
        )
        lift_data = Caching.check_and_return_cache(
            f"lift.{model_id}",
            Decisioning(token).get_model_lift,
            {"model_id": model_id, "model_version": model_version},
        )
        lift_data.sort(key=lambda x: x[api_c.BUCKET])
        return HuxResponse.OK(data=lift_data, data_schema=ModelLiftSchema())


@add_view_to_blueprint(
    model_bp,
    f"{api_c.MODELS_ENDPOINT}/<model_id>/pipeline-performance",
    "ModelPipelinePerformance",
)
class ModelPipelinePerformance(SwaggerView):
    """Model Pipeline Performance Class."""

    parameters = [
        {
            "name": api_c.MODEL_ID,
            "description": "Model id",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "1",
        },
        {
            "name": api_c.VERSION,
            "description": "Version id",
            "type": "string",
            "in": "query",
            "required": False,
            "example": "1.0.0",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Model pipeline performance.",
            "schema": ModelPipelinePerformanceSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve model pipeline performance"
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    responses.update(EMPTY_RESPONSE_DEPENDENCY_404_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, model_id: str, user: dict) -> Tuple[dict, int]:
        """Retrieves model pipeline performance.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.
            user (dict): User object.

        Returns:
            Tuple[dict, int]: dict of model pipeline performance, HTTP status code.
        """

        return (
            jsonify(
                ModelPipelinePerformanceSchema().dump(
                    api_c.MODEL_PIPELINE_PERFORMANCE_STUB
                )
            ),
            HTTPStatus.OK.value,
        )
