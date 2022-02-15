# pylint: disable=too-many-lines,unused-argument
"""Purpose of this script is for housing the
decision routes for the API"""
from random import uniform, randint
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Tuple, List

from flask import Blueprint, jsonify, request
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

from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.route.utils import (
    get_db_client,
    get_required_shap_data,
)
from huxunify.api.schema.model import (
    ModelSchema,
    ModelVersionSchema,
    ModelDriftSchema,
    ModelLiftSchema,
    ModelDashboardSchema,
    FeatureSchema,
    ModelRequestPostSchema,
    ModelUpdatePatchSchema,
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
    def get(self, user: dict) -> Tuple[List[dict], int]:
        """Retrieves all models.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[List[dict], int]: list containing dict of models,
                HTTP status code.
        """

        # convert all statuses to lower case
        status = [
            status.lower() for status in request.args.getlist(api_c.STATUS)
        ]
        all_models = Tecton().get_models()

        purchase_model = {
            api_c.TYPE: "Classification",
            api_c.CATEGORY: "Email",
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
        all_models.append(purchase_model)

        for model in all_models:
            if api_c.CATEGORY not in model:
                model[api_c.CATEGORY] = api_c.UNCATEGORIZED

        database = get_db_client()
        unified_models = collection_management.get_documents(
            database, db_c.MODELS_COLLECTION
        ).get(db_c.DOCUMENTS)
        all_models.extend(unified_models)

        config_models = collection_management.get_documents(
            get_db_client(),
            db_c.CONFIGURATIONS_COLLECTION,
            {db_c.TYPE: api_c.MODELS_TAG},
        )
        if config_models.get(db_c.DOCUMENTS):
            for model in all_models:
                matched_model = next(
                    (
                        item
                        for item in config_models[db_c.DOCUMENTS]
                        if item[api_c.NAME] == model[api_c.NAME]
                    ),
                    None,
                )
                if matched_model is not None:
                    model[api_c.STATUS] = matched_model[api_c.STATUS]

        if status:
            # match status is lower case
            all_models = [
                model
                for model in all_models
                if model[api_c.STATUS].lower() in status
            ]

        all_models.sort(key=lambda x: x[api_c.NAME])

        return (
            jsonify(ModelSchema(many=True).dump(all_models)),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(model_bp, api_c.MODELS_ENDPOINT, "SetModelStatus")
class SetModelStatus(SwaggerView):
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
                api_c.MODELS,
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
                api_c.MODELS,
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
    f"{api_c.MODELS_ENDPOINT}",
    "UpdateModels",
)
class UpdateModels(SwaggerView):
    """Class to partially update models."""

    parameters = [
        {
            "name": api_c.BODY,
            "in": api_c.BODY,
            "type": "object",
            "description": "Input model body.",
            "example": [
                {
                    api_c.ID: "f561bcc9a68f4e959cc6479fcff5a3a1",
                    api_c.TYPE: db_c.MODEL_TYPE_CLASSIFICATION,
                    api_c.NAME: "Propensity to Purchase",
                    api_c.CATEGORY: db_c.MODEL_CATEGORY_EMAIL,
                    api_c.DESCRIPTION: "Likelihood of customer to purchase",
                    api_c.STATUS: api_c.REQUESTED,
                    api_c.IS_ADDED: True,
                }
            ],
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Model updated.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update model.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @requires_access_levels(api_c.USER_ROLE_ALL)
    @api_error_handler()
    def patch(self, user: dict) -> Tuple[list, int]:
        """Updates a model.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[list, int]: List of updated requested models,
                HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        models = ModelUpdatePatchSchema(many=True).load(request.json)

        updated_models = []

        database = get_db_client()
        for model in models:
            # check if document exists in configurations collection
            model_document = collection_management.get_document(
                database,
                db_c.CONFIGURATIONS_COLLECTION,
                {
                    db_c.OBJECT_ID: model.get(api_c.ID),
                    db_c.NAME: model.get(api_c.NAME),
                },
            )

            if model_document:
                # update the document
                updated_models.append(
                    collection_management.update_document(
                        database,
                        db_c.CONFIGURATIONS_COLLECTION,
                        model_document[db_c.ID],
                        model,
                        user[api_c.USER_NAME],
                    )
                )

        return (
            jsonify(ModelSchema().dump(updated_models, many=True)),
            HTTPStatus.OK,
        )


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
    def get(self, model_id: str, user: dict) -> Tuple[List[dict], int]:
        """Retrieves model version history.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.
            user (dict): User object

        Returns:
            Tuple[List[dict], int]: List containing dict of model versions,
                HTTP status code.
        """

        # TODO Remove once Propensity to Purchase info
        #  can be retrieved from tecton
        if model_id == "3":
            version_history = [
                {
                    api_c.ID: model_id,
                    api_c.LAST_TRAINED: datetime(2021, 6, 24 + i),
                    api_c.DESCRIPTION: "Propensity of a customer making "
                    "a purchase after receiving an email.",
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
            version_history = Tecton().get_model_version_history(model_id)

        return (
            jsonify(ModelVersionSchema(many=True).dump(version_history)),
            HTTPStatus.OK.value,
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
            "schema": ModelDashboardSchema,
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
    def get(self, model_id: str, user: dict) -> Tuple[dict, int]:
        """Retrieves model overview.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.
            user (dict): User object.

        Returns:
            Tuple[dict, int]: dict of model features, HTTP status code.
        """

        # TODO Remove once Propensity to Purchase model data is being served
        #  from tecton.
        if model_id == "3":
            overview_data = api_c.PROPENSITY_TO_PURCHASE_MODEL_OVERVIEW_STUB
        else:
            version = None
            tecton = Tecton()
            for version in tecton.get_model_version_history(model_id):
                current_version = version.get(api_c.CURRENT_VERSION)

                # try to get model performance
                performance_metrics = tecton.get_model_performance_metrics(
                    model_id,
                    version[api_c.TYPE],
                    current_version,
                )

                if request.args.get(api_c.VERSION) is not None:
                    if (
                        current_version == request.args.get(api_c.VERSION)
                        and performance_metrics
                    ):
                        break

                if (
                    request.args.get(api_c.VERSION) is None
                    and performance_metrics
                ):
                    break
            else:
                # if model versions not found, return not found.
                return {}, HTTPStatus.NOT_FOUND

            # generate the output
            overview_data = {
                api_c.MODEL_ID: version.get(api_c.ID),
                api_c.MODEL_TYPE: version.get(
                    api_c.TYPE, db_c.CATEGORY_UNKNOWN
                ),
                api_c.MODEL_NAME: version.get(
                    api_c.NAME, db_c.CATEGORY_UNKNOWN
                ),
                api_c.DESCRIPTION: version.get(api_c.DESCRIPTION, ""),
                api_c.MODEL_SHAP_DATA: get_required_shap_data(
                    api_c.MODEL_ONE_SHAP_DATA
                    if model_id == "17e1565dbd2821adaf88fd26658744aba9419a6f"
                    else api_c.MODEL_TWO_SHAP_DATA,
                ),
                api_c.PERFORMANCE_METRIC: performance_metrics,
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
    responses.update(EMPTY_RESPONSE_DEPENDENCY_404_RESPONSE)
    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, model_id: str, user: dict) -> Tuple[List[dict], int]:
        """Retrieves model drift details.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID.
            user (dict): User object.

        Returns:
            Tuple[List[dict], int]: List containing dict of model drift,
                HTTP status code.
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
            tecton = Tecton()

            # get model information
            model_versions = tecton.get_model_version_history(model_id)

            # if model versions not found, return not found.
            if not model_versions:
                return {}, HTTPStatus.NOT_FOUND

            # take the latest model
            latest_model = model_versions[0]

            drift_data = tecton.get_model_drift(
                model_id, latest_model[api_c.TYPE], model_versions
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
            "description": "Model version, if not provided, "
            "it will take the latest.",
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
    responses.update(EMPTY_RESPONSE_DEPENDENCY_404_RESPONSE)

    tags = [api_c.MODELS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(
        self,
        user: dict,
        model_id: str,
        model_version: str = None,
    ) -> Tuple[List[dict], int]:
        """Retrieves model features.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.
            model_id (str): Model ID.
            model_version (str): Model Version.

        Returns:
            Tuple[List[dict], int]: List containing dict of model features,
                HTTP status code.
        """

        # TODO: Remove once this model data becomes
        #  available and can be fetched from Tecton
        # intercept to check if the model_id is for propensity_to_purchase
        # to set features with stub data
        if model_id == "3":
            features = api_c.PROPENSITY_TO_PURCHASE_FEATURES_RESPONSE_STUB
        else:
            tecton = Tecton()

            # get model versions
            model_versions = (
                [{api_c.CURRENT_VERSION: model_version}]
                if model_version
                else tecton.get_model_version_history(model_id)
            )
            database = get_db_client()

            if not model_versions:
                return jsonify([]), HTTPStatus.NOT_FOUND

            # loop versions until the latest version is found
            for version in model_versions:
                current_version = version.get(api_c.CURRENT_VERSION)

                # check cache first
                features = get_cache_entry(
                    database, f"features.{model_id}.{current_version}"
                )
                if features:
                    break

                # if no cache, grab from Tecton and cache after.
                features = tecton.get_model_features(model_id, current_version)

                # create cache entry in db only if features fetched from Tecton is not empty
                if features:
                    create_cache_entry(
                        database,
                        f"features.{model_id}.{current_version}",
                        features,
                    )
                    break

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
            "description": "Model version, if not provided, "
            "it will take the latest.",
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(
        self,
        user: dict,
        model_id: str,
        model_version: str = None,
        limit: int = 20,
    ) -> Tuple[List[dict], int]:
        """Retrieves top model features sorted by score.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.
            model_id (str): Model ID.
            model_version (str): Model Version.
            limit (int): Limit of features to return, default is 20.

        Returns:
            Tuple[List[dict], int]: List containing dict of model features,
                HTTP status code.
        """

        tecton = Tecton()

        model_versions = (
            [{api_c.CURRENT_VERSION: model_version}]
            if model_version
            else tecton.get_model_version_history(model_id)
        )

        if not model_versions:
            return jsonify([]), HTTPStatus.NOT_FOUND

        database = get_db_client()
        for version in model_versions:
            current_version = version.get(api_c.CURRENT_VERSION)

            # check cache first
            features = get_cache_entry(
                database, f"features.{model_id}.{current_version}"
            )
            if features:
                break

            # if no cache, grab from Tecton and cache after.
            features = tecton.get_model_features(model_id, current_version)
            if features:
                create_cache_entry(
                    database,
                    f"features.{model_id}.{current_version}",
                    features,
                )
                break

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

    parameters = [
        api_c.MODEL_ID_PARAMS[0],
        {
            "name": api_c.VERSION,
            "description": "Model version, if not provided, "
            "it will take the latest.",
            "type": "str",
            "in": "path",
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
        model_version: str = None,
    ) -> Tuple[List[dict], int]:
        """Retrieves model lift data.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            model_id (str): Model ID
            user (dict): User object.
            model_version (str): Model version

        Returns:
            Tuple[List[dict], int]: List containing a dict of model lift data,
                HTTP status code.
        """

        # TODO Remove once Tecton serves lift data for model id 3

        if model_id == "3":
            lift_data = [
                {
                    api_c.PREDICTED_RATE: uniform(0.01, 0.3),
                    api_c.BUCKET: 10 * i,
                    api_c.PROFILE_SIZE_PERCENT: 0,
                    api_c.ACTUAL_VALUE: randint(1000, 5000),
                    api_c.ACTUAL_RATE: uniform(0.01, 0.3),
                    api_c.PROFILE_COUNT: randint(1000, 100000),
                    api_c.ACTUAL_LIFT: uniform(1, 5),
                }
                for i in range(1, 11)
            ]
        else:
            tecton = Tecton()
            # get model versions
            model_versions = (
                [{api_c.CURRENT_VERSION: model_version}]
                if model_version
                else tecton.get_model_version_history(model_id)
            )

            if not model_versions:
                return jsonify([]), HTTPStatus.NOT_FOUND

            # loop versions until the latest version is found
            for version in model_versions:
                current_version = version.get(api_c.CURRENT_VERSION)

                lift_data = tecton.get_model_lift_async(
                    model_id, current_version
                )

                if lift_data:
                    break

        if not lift_data:
            return jsonify([]), HTTPStatus.NOT_FOUND

        lift_data.sort(key=lambda x: x[api_c.BUCKET])

        return (
            jsonify(ModelLiftSchema(many=True).dump(lift_data)),
            HTTPStatus.OK.value,
        )


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
