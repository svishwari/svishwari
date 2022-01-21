# pylint: disable=no-self-use,disable=unused-argument
"""Paths for the User API."""
import datetime
import random
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from connexion.exceptions import ProblemException
from flask import Blueprint, request, jsonify
from flasgger import SwaggerView

from huxunifylib.util.general.logging import logger
from huxunifylib.database import constants as db_c
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database.user_management import (
    manage_user_favorites,
    get_all_users,
    update_user,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.route.utils import (
    get_db_client,
    get_user_from_db,
    create_description_for_user_request,
    filter_team_member_requests,
)
from huxunify.api.schema.user import (
    UserSchema,
    UserPatchSchema,
    TicketSchema,
    TicketGetSchema,
    NewUserRequest,
    RequestedUserSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.okta import (
    get_token_from_request,
    introspect_token,
)
from huxunify.api.data_connectors.jira import JiraConnection

# setup the cdm blueprint
user_bp = Blueprint(api_c.USER_ENDPOINT, import_name=__name__)


@user_bp.before_request
@secured()
def before_request():
    """Protect all of the user endpoints."""

    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    user_bp, f"{api_c.USER_ENDPOINT}/profile", "IndividualUserSearch"
)
class UserProfile(SwaggerView):
    """User Profile Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve Individual User profile",
            "schema": UserSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get user details from request."
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves a user profile.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: dict of user, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        try:
            # get access token from request and set it to a variable for it to
            # be used in subsequent requests
            access_token = get_token_from_request(request)[0]

            okta_id = introspect_token(access_token).get(
                api_c.OKTA_USER_ID, None
            )

            # return unauthorized response if no valid okta_id is fetched by
            # introspecting the access_token
            if okta_id is None:
                return {
                    "message": api_c.AUTH401_ERROR_MESSAGE
                }, HTTPStatus.UNAUTHORIZED

            # get the user info and the corresponding user document from db
            # from the access_token
            user_response = get_user_from_db(access_token)

            # if the user_response object is of type tuple, then return it as
            # such since a failure must have occurred while fetching user data
            # from db
            if isinstance(user_response, tuple):
                return user_response

            # update user record's login_count and update_time in DB and return
            # the updated record
            user = update_user(
                get_db_client(),
                okta_id=okta_id,
                update_doc={
                    db_c.USER_LOGIN_COUNT: (
                        user_response.get(db_c.USER_LOGIN_COUNT, 0) + 1
                    )
                },
            )

            # merge lookalikes if any to audiences
            if user[db_c.USER_FAVORITES]:
                user[db_c.USER_FAVORITES][db_c.AUDIENCES] = user[
                    db_c.USER_FAVORITES
                ].get(db_c.AUDIENCES, []) + user[db_c.USER_FAVORITES].get(
                    db_c.LOOKALIKE, []
                )

            return (
                UserSchema().dump(user),
                HTTPStatus.OK,
            )
        except Exception as exc:
            logger.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail="Unable to get user profile.",
            ) from exc


@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}/<component_name>/<component_id>/favorite",
    "AddUserFavorite",
)
class AddUserFavorite(SwaggerView):
    """Add user favorites class."""

    parameters = [
        {
            "name": db_c.COMPONENT_ID,
            "in": "path",
            "type": "string",
            "description": "Component ID.",
            "example": "5f5f7262997acad4bac4373b",
            "required": True,
        },
        {
            "name": db_c.COMPONENT_NAME,
            "in": "path",
            "type": "string",
            "description": "Component name.",
            "example": "audiences",
            "required": True,
        },
    ]
    responses = {
        HTTPStatus.CREATED.value: {
            "description": "User favorite created",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to add user favorite",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def post(
        self, component_name: str, component_id: str, user: dict
    ) -> Tuple[dict, int]:
        """Creates a user favorite.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            component_name (str): Component name.
            component_id (str): Component ID.
            user (dict): User object.

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status code.
        """

        okta_id = introspect_token(get_token_from_request(request)[0]).get(
            api_c.OKTA_USER_ID
        )

        if component_name not in db_c.FAVORITE_COMPONENTS:
            logger.error(
                "Component name %s not in favorite components.", component_name
            )
            return {
                "message": api_c.INVALID_COMPONENT_NAME
            }, HTTPStatus.BAD_REQUEST

        component_id = ObjectId(component_id)

        user_details = manage_user_favorites(
            get_db_client(),
            okta_id=okta_id,
            component_name=component_name,
            component_id=component_id,
        )
        if user_details:
            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.CREATED

        return {
            "message": f"{str(component_id)} already in favorites."
        }, HTTPStatus.OK


@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}/<component_name>/<component_id>/favorite",
    "DeleteUserFavorite",
)
class DeleteUserFavorite(SwaggerView):
    """Delete user favorites class."""

    parameters = [
        {
            "name": db_c.COMPONENT_ID,
            "in": "path",
            "type": "string",
            "description": "Component ID.",
            "example": "5f5f7262997acad4bac4373b",
            "required": True,
        },
        {
            "name": db_c.COMPONENT_NAME,
            "in": "path",
            "type": "string",
            "description": "Component name.",
            "example": "audiences",
            "required": True,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "User favorite deleted",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to delete user favorite",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def delete(
        self, component_name: str, component_id: str, user: dict
    ) -> Tuple[dict, int]:
        """Deletes a user favorite.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            component_name (str): Component name.
            component_id (str): Component ID.
            user(dict): User object.

        Returns:
            Tuple[dict, int]: Configuration dict, HTTP status code.
        """

        okta_id = introspect_token(get_token_from_request(request)[0]).get(
            api_c.OKTA_USER_ID
        )

        if component_name not in db_c.FAVORITE_COMPONENTS:
            logger.error(
                "Component name %s not in favorite components.", component_name
            )
            return {
                "message": api_c.INVALID_COMPONENT_NAME
            }, HTTPStatus.BAD_REQUEST

        user_details = manage_user_favorites(
            get_db_client(),
            okta_id=okta_id,
            component_name=component_name,
            component_id=ObjectId(component_id),
            delete_flag=True,
        )
        if user_details:
            logger.info(
                "Successfully deleted user favorite %s.", component_name
            )
            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK

        return {
            "message": f"{component_id} not part of user favorites"
        }, HTTPStatus.OK


@add_view_to_blueprint(user_bp, api_c.USER_ENDPOINT, "UserView")
class UserView(SwaggerView):
    """User view class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of all Users.",
            "schema": {"type": "array", "items": UserSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get all Users."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def get(
        self, user: dict
    ) -> Tuple[list, int]:  # pylint: disable=no-self-use
        """Retrieves all users.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user(dict): User object.

        Returns:
            Tuple[list, int]: list of users, HTTP status code.
        """

        # get all users
        users = get_all_users(get_db_client())

        # generate random phone number and user access level
        for userinfo in users:
            userinfo[api_c.USER_PHONE_NUMBER] = random.choice(
                ["720-025-8322", "232-823-6049", "582-313-7191"]
            )
            userinfo[api_c.USER_ACCESS_LEVEL] = random.choice(
                ["Edit", "View-only", "Admin"]
            )

        return (
            jsonify(UserSchema().dump(users, many=True)),
            HTTPStatus.OK.value,
        )


# HUS-1320 need to allow user to edit other users via RBAC
@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}",
    "UserPatchView",
)
class UserPatchView(SwaggerView):
    """User Patch class."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input user body.",
            "example": {
                db_c.USER_ROLE: "viewer",
                db_c.USER_DISPLAY_NAME: "new_display_name",
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "User updated.",
            "schema": UserSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Invalid data received.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "User not found.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    @requires_access_levels([api_c.ADMIN_LEVEL])
    def patch(self, user: dict) -> Tuple[dict, int]:
        """Updates a user.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[dict, int]: User doc, HTTP status code.
        """

        body = UserPatchSchema().load(request.get_json())

        if not body:
            return {api_c.MESSAGE: "No body provided."}, HTTPStatus.BAD_REQUEST

        database = get_db_client()

        if api_c.ID in body:
            userinfo = get_all_users(
                database, {db_c.ID: ObjectId(body.get(api_c.ID))}
            )
            del body[api_c.ID]
        else:
            userinfo = get_all_users(
                database,
                {db_c.USER_DISPLAY_NAME: user[api_c.USER_NAME]},
            )

        if not userinfo:
            return {api_c.MESSAGE: api_c.USER_NOT_FOUND}, HTTPStatus.NOT_FOUND

        # TODO Access Control Based on Roles

        updated_user = update_user(
            database,
            okta_id=userinfo[0][db_c.OKTA_ID],
            update_doc={
                **body,
                **{
                    db_c.UPDATED_BY: user[api_c.USER_NAME],
                    db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                },
            },
        )

        # update the document
        return (
            UserSchema().dump(updated_user),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    user_bp, f"{api_c.USER_ENDPOINT}/{api_c.CONTACT_US}", "CreateTicket"
)
class CreateTicket(SwaggerView):
    """Ticket creation class."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Details of the feedback/bug to be reported",
            "example": {
                api_c.ISSUE_TYPE: api_c.TICKET_TYPE_BUG,
                api_c.SUMMARY: "Summary",
                api_c.DESCRIPTION: "Description",
            },
        }
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": TicketGetSchema,
            "description": "Details of ticket created in JIRA.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to report issue."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def post(self, user: dict) -> Tuple[dict, int]:
        """Create a ticket in JIRA

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[dict, int]: dict of message, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """
        issue_details = TicketSchema().load(request.get_json())
        # JIRA automated trigger activated when it sees '[REPORTED UI ISSUE]' in the title
        new_issue = JiraConnection().create_jira_issue(
            issue_type=issue_details[api_c.ISSUE_TYPE],
            summary=f"HUS: [REPORTED UI ISSUE] {issue_details[api_c.SUMMARY]}",
            description=(
                f"{issue_details[api_c.DESCRIPTION]}\n\n"
                f"Reported By: {user[api_c.USER_NAME]}\nEnvironment: {request.url_root}"
            ),
        )

        create_notification(
            database=get_db_client(),
            notification_type=db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            description=f"{user[api_c.USER_NAME]} created a new issue"
            f"{new_issue.get(api_c.KEY)} in JIRA.",
            category=api_c.TICKET_TYPE_BUG,
            username=user[api_c.USER_NAME],
        )
        return (
            TicketGetSchema().dump(new_issue),
            HTTPStatus.CREATED,
        )


@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}/{api_c.REQUEST_NEW_USER}",
    "RequestNewUser",
)
class RequestNewUser(SwaggerView):
    """Request new user class."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Details of user to be given access.",
            "example": {
                api_c.FIRST_NAME: "Sarah",
                api_c.LAST_NAME: "Huxley",
                api_c.EMAIL: "sh@fake.com",
                api_c.USER_ACCESS_LEVEL: "admin",
                api_c.USER_PII_ACCESS: False,
                api_c.REASON_FOR_REQUEST: "New member to our team",
            },
        }
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": TicketGetSchema,
            "description": "Details of ticket created in JIRA.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to request user."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    @requires_access_levels([api_c.ADMIN_LEVEL])
    def post(self, user: dict) -> Tuple[dict, int]:
        """Create a user request ticket in JIRA

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[dict, int]: dict of message, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """
        user_request_details = NewUserRequest().load(request.get_json())
        user_request_details.update(
            {api_c.REQUESTED_BY: user.get(api_c.USER_NAME, "")}
        )
        # JIRA automated trigger activated when it sees '[NEW_USER_REQUEST]'
        # in the title
        new_issue = JiraConnection().create_jira_issue(
            issue_type=api_c.TASK,
            summary=f"{api_c.NEW_USER_REQUEST_PREFIX} for "
            f"{user_request_details.get(api_c.EMAIL, '')}",
            description=create_description_for_user_request(
                **user_request_details
            ),
        )

        create_notification(
            database=get_db_client(),
            notification_type=db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            description=f"{user[api_c.USER_NAME]} created a new issue"
            f"{new_issue.get(api_c.KEY)} in JIRA.",
            category=api_c.TICKET_TYPE_BUG,
            username=user[api_c.USER_NAME],
        )
        return (
            TicketGetSchema().dump(new_issue),
            HTTPStatus.CREATED,
        )


@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}/{api_c.REQUESTED_USERS}",
    "UsersRequested",
)
class UsersRequested(SwaggerView):
    """User Profile Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve requested users.",
            "schema": {"type": "array", "items": RequestedUserSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get requested users."
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves requested users.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: dict of requested users, HTTP status code.
        """
        summary = api_c.NEW_USER_REQUEST_PREFIX
        summary = summary.replace("[", '"').replace("]", '"')

        jira_issues = JiraConnection().get_issues(
            jql=f"summary~{summary} ORDER BY updated DESC",
            fields=f"{api_c.DESCRIPTION},{api_c.STATUS},{api_c.UPDATED},"
            f"{api_c.CREATED}",
        )

        jira_issues = jira_issues.get(api_c.ISSUES)
        if not jira_issues:
            return {"message": "No user requests found."}, HTTPStatus.OK

        return (
            jsonify(
                RequestedUserSchema().dump(
                    filter_team_member_requests(jira_issues, remove_done=True),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )
