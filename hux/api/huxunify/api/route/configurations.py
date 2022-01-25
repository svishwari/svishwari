# pylint: disable=no-self-use,unused-argument
"""Paths for Configurations API"""
from http import HTTPStatus
from typing import Tuple
from flask import Blueprint, jsonify, request, Response
from flasgger import SwaggerView

from huxunifylib.database import (
    constants as db_c,
    collection_management,
)
from huxunify.api.schema.configurations import (
    ConfigurationsSchema,
    NavigationSettingsSchema,
)
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.route.utils import get_db_client
from huxunify.api import constants as api_c

from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
    FAILED_DEPENDENCY_424_RESPONSE,
)

# setup the configurations blueprint
configurations_bp = Blueprint(
    api_c.CONFIGURATIONS_ENDPOINT, import_name=__name__
)


@configurations_bp.before_request
@secured()
def before_request():
    """Protect all of the configurations endpoints."""

    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    configurations_bp,
    f"/{api_c.CONFIGURATIONS_ENDPOINT}/modules",
    "ConfigurationsModules",
)
class ConfigurationsModules(SwaggerView):
    """Configurations search class."""

    parameters = [
        {
            "name": api_c.STATUS,
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "description": "Configuration status.",
            "example": "Requested",
            "required": False,
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of configurations.",
            "schema": {"type": "array", "items": ConfigurationsSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CONFIGURATIONS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self) -> Tuple[Response, int]:
        """Retrieves all configurations.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[Response, int]: Response list containing dict of configurations,
                HTTP status code.
        """

        status = request.args.getlist(api_c.STATUS)
        query_filter = {
            db_c.CONFIGURATION_FIELD_TYPE: {
                "$in": [
                    db_c.CONFIGURATION_TYPE_BUSINESS_SOLUTION,
                    db_c.CONFIGURATION_TYPE_MODULE,
                ]
            }
        }
        if status:
            query_filter[db_c.STATUS] = {"$in": status}
        config_models = collection_management.get_documents(
            get_db_client(),
            db_c.CONFIGURATIONS_COLLECTION,
            query_filter=query_filter,
        )

        return (
            jsonify(
                ConfigurationsSchema(many=True).dump(
                    config_models[db_c.DOCUMENTS]
                )
            ),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    configurations_bp,
    f"/{api_c.CONFIGURATIONS_ENDPOINT}/navigation",
    "ConfigurationsNavigation",
)
class ConfigurationsNavigation(SwaggerView):
    """Configurations Navigation class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of navigation settings.",
            "schema": {"type": "array", "items": NavigationSettingsSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CONFIGURATIONS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves all configurations.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[Response, int]: Response list containing dict of configurations,
                HTTP status code.
        """

        query_filter = {
            db_c.CONFIGURATION_FIELD_TYPE: {
                "$in": [db_c.CONFIGURATION_TYPE_NAVIGATION_SETTINGS]
            }
        }
        nav_settings = collection_management.get_documents(
            get_db_client(),
            db_c.CONFIGURATIONS_COLLECTION,
            query_filter=query_filter,
        )
        return (
            jsonify(
                NavigationSettingsSchema().dump(
                    nav_settings[db_c.DOCUMENTS][0]
                )
            ),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    configurations_bp,
    f"/{api_c.CONFIGURATIONS_ENDPOINT}/navigation",
    "ConfigurationsNavigationPUT",
)
class ConfigurationsNavigationPUT(SwaggerView):
    """Configuration navigations PUT."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "description": "Settings Object.",
            "type": "object",
            "example": api_c.SAMPLE_NAVIGATION_SETTINGS,
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": NavigationSettingsSchema,
            "description": "Updated navigation settings.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update the navigation settings.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CONFIGURATIONS_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def put(self, user: dict) -> Tuple[Response, int]:
        """Set Navigation settings.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Destination doc, HTTP status code.
        """

        # load into the schema object
        body = NavigationSettingsSchema().load(request.get_json())

        database = get_db_client()
        query_filter = {
            db_c.CONFIGURATION_FIELD_TYPE: {
                "$in": [db_c.CONFIGURATION_TYPE_NAVIGATION_SETTINGS]
            }
        }

        # Fetch navigation settings document
        nav_doc = collection_management.get_document(
            database,
            db_c.CONFIGURATIONS_COLLECTION,
            query_filter=query_filter,
        )

        updated_doc = collection_management.update_document(
            database,
            db_c.CONFIGURATIONS_COLLECTION,
            nav_doc[db_c.ID],
            update_doc=body,
            username=user[api_c.USER_NAME],
        )

        return (
            jsonify(NavigationSettingsSchema().dump(updated_doc)),
            HTTPStatus.OK.value,
        )
