# pylint: disable=no-self-use
"""Paths for client-projects API."""
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from flask import Blueprint, request, Response
from flasgger import SwaggerView

from huxunifylib.database import (
    constants as db_c,
    collection_management,
)
from huxunifylib.database.collection_management import get_document
from huxunifylib.util.general.logging import logger

from huxunify.api import constants as api_c
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.route.return_util import HuxResponse
from huxunify.api.route.utils import get_db_client
from huxunify.api.schema.client_projects import (
    ClientProjectGetSchema,
    ClientProjectPatchSchema,
    ClientDetailsSchema,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
)

# setup the client-projects blueprint
client_projects_bp = Blueprint(
    api_c.CLIENT_PROJECTS_ENDPOINT, import_name=__name__
)


@client_projects_bp.before_request
@secured()
def before_request():
    """Protect all the client-projects endpoints."""

    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    client_projects_bp,
    api_c.CLIENT_PROJECTS_ENDPOINT,
    "ClientProjectGetView",
)
class ClientProjectGetView(SwaggerView):
    """Client Projects Get view class."""

    responses = {
        HTTPStatus.OK.value: {
            "schema": {"type": "array", "items": ClientProjectGetSchema},
            "description": "List of client projects.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve client projects."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CLIENT_PROJECTS_TAG]

    # pylint: disable=unused-argument
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Fetch all client projects.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[Response, int]: Response list of client projects,
                HTTP status code.
        """

        client_projects = collection_management.get_documents(
            get_db_client(),
            db_c.CLIENT_PROJECTS_COLLECTION,
        ).get(db_c.DOCUMENTS)

        logger.info("Successfully retrieved all client projects.")

        return HuxResponse.OK(
            data=client_projects, data_schema=ClientProjectGetSchema()
        )


@add_view_to_blueprint(
    client_projects_bp,
    f"{api_c.CLIENT_PROJECTS_ENDPOINT}/<client_project_id>",
    "ClientProjectPatchView",
)
class ClientProjectPatchView(SwaggerView):
    """Client Project Patch view class."""

    parameters = [
        {
            "name": api_c.CLIENT_PROJECT_ID,
            "description": "Client Project ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Client Project's fields to edit.",
            "example": {
                api_c.URL: "URL_Link",
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": ClientProjectGetSchema,
            "description": "Client Project patched.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to patch client project.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "Failed to find client project.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CLIENT_PROJECTS_TAG]

    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def patch(self, client_project_id: str, user: dict) -> Tuple[dict, int]:
        """Patches an existing client project.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            client_project_id (str): Client Project ID.
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Updated client project, HTTP status code.
        """

        if not request.get_json():
            logger.error("Could not patch client project.")
            return {
                api_c.MESSAGE: "No request body provided."
            }, HTTPStatus.BAD_REQUEST

        ClientProjectPatchSchema().validate(request.get_json())

        database = get_db_client()

        if not collection_management.get_document(
            database,
            db_c.CLIENT_PROJECTS_COLLECTION,
            {db_c.ID: ObjectId(client_project_id)},
        ):
            return {
                api_c.MESSAGE: f"Client Project {client_project_id} not found"
            }, HTTPStatus.NOT_FOUND

        updated_client_project = collection_management.update_document(
            database,
            db_c.CLIENT_PROJECTS_COLLECTION,
            ObjectId(client_project_id),
            request.get_json(),
            user[api_c.USER_NAME],
        )

        logger.info(
            "Successfully updated client project %s.",
            updated_client_project.get(db_c.NAME),
        )

        return HuxResponse.OK(
            data=updated_client_project, data_schema=ClientProjectGetSchema()
        )


@add_view_to_blueprint(
    client_projects_bp,
    f"{api_c.CLIENT_ENDPOINT}",
    "ClientDetails",
)
class ClientDetails(SwaggerView):
    """User Client Details Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve Client Details.",
            "schema": ClientDetailsSchema,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CLIENT_PROJECTS_TAG]

    # pylint: disable=unused-argument
    @api_error_handler()
    @requires_access_levels(api_c.COMMON_USER_ROLE)
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves client details.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[Response, int]: dict of requested users, HTTP status code.
        """

        # Fetch client details document from configurations collection
        database = get_db_client()
        query_filter = {
            db_c.CONFIGURATION_FIELD_TYPE: db_c.CONFIGURATION_TYPE_CLIENT_DETAILS
        }

        client_details = get_document(
            database=database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            query_filter=query_filter,
        )

        return HuxResponse.OK(
            data=client_details[db_c.CONFIGURATION_FIELD_DETAILS]
            if client_details
            else {},
            data_schema=ClientDetailsSchema(),
        )
