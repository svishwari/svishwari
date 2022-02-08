# pylint: disable=no-self-use
"""Paths for applications API"""
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from flask import Blueprint, jsonify, request
from flasgger import SwaggerView

from huxunifylib.util.general.logging import logger

from huxunify.api.data_connectors.okta import (
    introspect_token,
    get_token_from_request,
)
from huxunify.api.route.return_util import HuxResponse
from huxunifylib.database.user_management import update_user
from huxunifylib.database import (
    constants as db_c,
    collection_management,
)
from huxunify.api.schema.applications import (
    ApplicationsGETSchema,
    ApplicationsPostSchema,
    ApplicationsPatchSchema,
)
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.route.utils import (
    get_db_client,
    Validation,
    get_user_from_db,
)
from huxunify.api import constants as api_c

from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
)

# setup the applications blueprint
applications_bp = Blueprint(api_c.APPLICATIONS_ENDPOINT, import_name=__name__)


@applications_bp.before_request
@secured()
def before_request():
    """Protect all of the applications endpoints."""

    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    applications_bp,
    api_c.APPLICATIONS_ENDPOINT,
    "ApplicationsGetView",
)
class ApplicationGetView(SwaggerView):
    """Applications Get view class."""

    parameters = [
        {
            "name": api_c.USER,
            "description": "Flag to specify if only user added applications "
            "are to be fetched. Otherwise, all the available "
            "applications are returned along with added field",
            "type": "boolean",
            "in": "query",
            "required": False,
            "default": False,
            "example": "false",
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": {"type": "array", "items": ApplicationsGETSchema},
            "description": "List of applications.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve applications"
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.APPLICATIONS_TAG]

    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    # pylint: disable=no-self-use
    # pylint: disable=unused-argument
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Fetch all applications.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[dict, int]: Created application, HTTP status code.
        """
        database = get_db_client()

        access_token = get_token_from_request(request)[0]
        # get the user info and the corresponding user document from db
        # from the access_token
        user_info = get_user_from_db(access_token)

        user_added = (
            Validation.validate_bool(request.args.get(api_c.USER))
            if request.args.get(api_c.USER)
            else False
        )

        # Return the applications user has already added
        if user_added:
            if (
                db_c.USER_APPLICATIONS not in user_info
                or not user_info[db_c.USER_APPLICATIONS]
            ):
                return HuxResponse.OK(api_c.EMPTY_USER_APPLICATION_RESPONSE)

            added_application_ids = [
                i[api_c.ID] for i in user_info[db_c.USER_APPLICATIONS]
            ]
            application_details = collection_management.get_documents(
                database,
                db_c.APPLICATIONS_COLLECTION,
                {db_c.ID: {"$in": added_application_ids}},
            ).get(db_c.DOCUMENTS)

            for i in application_details:
                i[api_c.URL] = next(
                    (
                        item
                        for item in user_info[db_c.USER_APPLICATIONS]
                        if item[api_c.ID] == i[db_c.ID]
                    )
                )[api_c.URL]
                i[api_c.IS_ADDED] = True

            return (
                jsonify(
                    ApplicationsGETSchema(many=True).dump(application_details)
                ),
                HTTPStatus.OK.value,
            )
        # Return all the applications user can add.
        # In this case, we do not need to show uncategorized applications
        else:
            available_applications = collection_management.get_documents(
                database,
                db_c.APPLICATIONS_COLLECTION,
                {
                    db_c.ENABLED: True,
                    db_c.CATEGORY: {
                        "$nin": ["Uncategorized", "uncategorized"]
                    },
                },
            ).get(db_c.DOCUMENTS)

            added_application_ids = (
                [i[api_c.ID] for i in user_info[db_c.USER_APPLICATIONS]]
                if db_c.USER_APPLICATIONS in user_info
                else []
            )

            for i in available_applications:
                i[api_c.IS_ADDED] = (
                    True if i[db_c.ID] in added_application_ids else False
                )

            return (
                jsonify(
                    ApplicationsGETSchema(many=True).dump(
                        available_applications
                    )
                ),
                HTTPStatus.OK.value,
            )


@add_view_to_blueprint(
    applications_bp,
    api_c.APPLICATIONS_ENDPOINT,
    "ApplicationsPostView",
)
class ApplicationsPostView(SwaggerView):
    """Applications Post view class."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Applications body.",
            "example": {
                api_c.CATEGORY: "uncategorized",
                api_c.NAME: "Custom Application",
                api_c.URL: "URL_Link",
            },
        },
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": ApplicationsGETSchema,
            "description": "Application created.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create application.",
        },
        HTTPStatus.FORBIDDEN.value: {
            "description": "Application already exists.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.APPLICATIONS_TAG]

    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def post(self, user: dict) -> Tuple[dict, int]:
        """Creates a new application.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Created application, HTTP status code.
        """

        new_application = ApplicationsPostSchema().load(
            request.get_json(),
        )
        database = get_db_client()

        access_token = get_token_from_request(request)[0]
        okta_id = introspect_token(access_token).get(api_c.OKTA_USER_ID)
        # get the user info and the corresponding user document from db
        # from the access_token
        user_info = get_user_from_db(access_token)

        existing_application = collection_management.get_document(
            database,
            db_c.APPLICATIONS_COLLECTION,
            {
                db_c.CATEGORY: new_application[api_c.CATEGORY],
                db_c.NAME: new_application[api_c.NAME],
                db_c.ENABLED: True,
            },
        )

        if existing_application is None:
            existing_application = collection_management.create_document(
                database,
                db_c.APPLICATIONS_COLLECTION,
                {
                    db_c.CATEGORY: new_application[api_c.CATEGORY],
                    db_c.NAME: new_application[api_c.NAME],
                    db_c.ENABLED: True,
                },
                user[api_c.USER_NAME],
            )

        # add applications to user doc
        updated_user_doc = (
            user_info[db_c.USER_APPLICATIONS]
            if db_c.USER_APPLICATIONS in user_info
            and user_info[db_c.USER_APPLICATIONS] is not None
            else []
        )
        user_apps = [
            d
            for d in updated_user_doc
            if d[api_c.ID] != existing_application[db_c.ID]
        ]
        user_apps.append(
            {
                api_c.ID: existing_application[db_c.ID],
                db_c.URL: new_application[api_c.URL],
            }
        )

        update_user(database, okta_id, {db_c.USER_APPLICATIONS: user_apps})

        logger.info(
            "User with username %s successfully created application %s.",
            user[api_c.USER_NAME],
            existing_application.get(db_c.NAME),
        )

        application = existing_application
        application[api_c.URL] = new_application[api_c.URL]
        return (
            jsonify(ApplicationsGETSchema().dump(application)),
            HTTPStatus.CREATED.value,
        )


@add_view_to_blueprint(
    applications_bp,
    f"{api_c.APPLICATIONS_ENDPOINT}/<application_id>",
    "ApplicationsPatchView",
)
class ApplicationsPatchView(SwaggerView):
    """Applications Patch view class."""

    parameters = [
        {
            "name": api_c.APPLICATION_ID,
            "description": "Application ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Application's fields to edit.",
            "example": {
                api_c.URL: "URL_Link",
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": ApplicationsGETSchema,
            "description": "Application patched.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to patch application.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "Failed to find application.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.APPLICATIONS_TAG]

    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def patch(self, application_id: str, user: dict) -> Tuple[dict, int]:
        """Patches an existing application.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            application_id (str): Application ID.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Updated application, HTTP status code.
        """

        if not request.json:
            logger.info("Could not patch application.")
            return {"message": "No body provided."}, HTTPStatus.BAD_REQUEST

        ApplicationsPatchSchema().validate(
            request.json,
        )
        new_application = ApplicationsPatchSchema().load(
            request.get_json(),
        )
        database = get_db_client()

        access_token = get_token_from_request(request)[0]
        okta_id = introspect_token(access_token).get(api_c.OKTA_USER_ID)
        # get the user info and the corresponding user document from db
        # from the access_token
        user_info = get_user_from_db(access_token)

        existing_application = collection_management.get_document(
            database,
            db_c.APPLICATIONS_COLLECTION,
            {db_c.ID: ObjectId(application_id)},
        )
        if not existing_application:
            return {
                "message": f"Application {application_id} not found"
            }, HTTPStatus.NOT_FOUND

        # add applications to user doc
        updated_user_doc = (
            user_info[db_c.USER_APPLICATIONS]
            if db_c.USER_APPLICATIONS in user_info
            and user_info[db_c.USER_APPLICATIONS] is not None
            else []
        )
        user_apps = [
            d
            for d in updated_user_doc
            if d[api_c.ID] != existing_application[db_c.ID]
        ]
        user_apps.append(
            {
                api_c.ID: existing_application[db_c.ID],
                db_c.URL: new_application[api_c.URL],
            }
        )

        update_user(database, okta_id, {db_c.USER_APPLICATIONS: user_apps})

        logger.info(
            "User with username %s successfully updated application %s.",
            user[api_c.USER_NAME],
            new_application.get(db_c.NAME),
        )

        application = existing_application
        application[api_c.URL] = new_application[api_c.URL]

        return (
            jsonify(ApplicationsGETSchema().dump(application)),
            HTTPStatus.OK.value,
        )
