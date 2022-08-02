# pylint: disable=no-self-use,unused-argument,too-many-lines
"""Paths for the User API."""
import random
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from connexion.exceptions import ProblemException
from dateutil.parser import parse, ParserError
from flask import Blueprint, request, jsonify, Response
from flasgger import SwaggerView

from huxunifylib.util.general.logging import logger

from huxunifylib.database import constants as db_c
from huxunifylib.database.collection_management import get_document
from huxunifylib.database.user_management import (
    manage_user_favorites,
    get_all_users,
    update_user,
    get_user,
    delete_user,
)
from huxunify.api.config import get_config
from huxunify.api.exceptions.integration_api_exceptions import (
    FailedAPIDependencyError,
)
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.route.return_util import HuxResponse
from huxunify.api.route.utils import (
    get_db_client,
    get_user_from_db,
    create_description_for_user_request,
    filter_team_member_requests,
    Validation as validation,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.schema.user import (
    UserSchema,
    UserPatchSchema,
    UserPreferencesSchema,
    TicketSchema,
    TicketGetSchema,
    NewUserRequest,
    RequestedUserSchema,
    RBACMatrixSchema,
)
from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
    FAILED_DEPENDENCY_424_RESPONSE,
)
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
    user_bp, f"{api_c.USER_ENDPOINT}/{api_c.PROFILE}", "UserProfile"
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
    @requires_access_levels(api_c.COMMON_USER_ROLE)
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

            logger.info(
                "User with username %s has attempted to login.",
                user[api_c.USER_NAME],
            )

            # get access token from request and set it to a variable for it to
            # be used in subsequent requests
            access_token = get_token_from_request(request)[0]

            okta_id = introspect_token(access_token).get(
                api_c.OKTA_USER_ID, None
            )

            # return unauthorized response if no valid okta_id is fetched by
            # introspecting the access_token
            if okta_id is None:
                logger.error(
                    "Unauthorized login since OKTA ID from access token for "
                    "user %s is not fetched.",
                    user[api_c.USER_NAME],
                )
                return {
                    "message": api_c.AUTH401_ERROR_MESSAGE
                }, HTTPStatus.UNAUTHORIZED

            # get the new user value right here since the decorator
            # requires_access_levels that is wrapped around this endpoint
            # would have set the user in DB if new
            is_user_new = user.get(api_c.IS_USER_NEW, False)

            # get the user info and the corresponding user document from db
            # from the access_token
            user_response = get_user_from_db(access_token)

            # if the user_response object is of type tuple, then return it as
            # such since a failure must have occurred while fetching user data
            # from db
            if isinstance(user_response, tuple):
                return user_response

            # check and set the last known release version of the user right
            # here before updating the user document in DB below
            config = get_config()
            show_latest_release_notes = (
                config.RELEASE_VERSION_LATEST
                != user.get(db_c.USER_LAST_KNOWN_RELEASE_VERSION, "")
            )
            release_notes_latest = config.RELEASE_NOTES_LATEST

            # update user record's login_count and update_time in DB and return
            # the updated record
            user = update_user(
                get_db_client(),
                okta_id=okta_id,
                update_doc={
                    db_c.USER_LOGIN_COUNT: (
                        user_response.get(db_c.USER_LOGIN_COUNT, 0) + 1
                    ),
                    db_c.USER_LAST_KNOWN_RELEASE_VERSION: config.RELEASE_VERSION_LATEST,
                },
            )

            user[api_c.IS_USER_NEW] = is_user_new
            user[api_c.SHOW_LATEST_RELEASE_NOTES] = show_latest_release_notes
            user[api_c.LINK_LATEST_RELEASE_NOTES] = release_notes_latest

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
    f"{api_c.USER_ENDPOINT}/seen_notifications",
    "SeenNotifications",
)
class SeenNotifications(SwaggerView):
    """Seen Notifications API Class"""

    parameters = [
        {
            "name": api_c.RESET,
            "description": "Reset Flag for Seen Notifications",
            "in": "query",
            "type": "boolean",
            "required": False,
            "default": False,
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Seen Notification Flag or Reset Flag",
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(
        self,
        user: dict,
    ) -> Tuple[dict, int]:
        """Gets and Resets Seen Notifications.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.


        Returns:
            Tuple[dict, int]: Seen Notification dict, HTTP status code.
        """

        okta_id = introspect_token(get_token_from_request(request)[0]).get(
            api_c.OKTA_USER_ID
        )

        if request.args.get(api_c.RESET) and validation.validate_bool(
            request.args.get(api_c.RESET)
        ):
            user_details = update_user(
                get_db_client(),
                okta_id=okta_id,
                update_doc={db_c.SEEN_NOTIFICATIONS: True},
            )
            if user_details:
                return HuxResponse.OK(data={db_c.SEEN_NOTIFICATIONS: True})
        user = get_user(database=get_db_client(), okta_id=okta_id)
        return HuxResponse.OK(
            data={
                db_c.SEEN_NOTIFICATIONS: user.get(
                    db_c.SEEN_NOTIFICATIONS, False
                )
            }
        )


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
    @requires_access_levels(api_c.USER_ROLE_ALL)
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
            userinfo[api_c.USER_ACCESS_LEVEL] = api_c.USER_DISPLAY_ROLES.get(
                userinfo[db_c.USER_ROLE]
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
                db_c.USER_DEMO_CONFIG: api_c.USER_DEMO_CONFIG_SAMPLE,
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
                },
            },
        )

        if db_c.USER_ROLE in body:
            logger.info(
                "User with display name %s role changed from %s to %s by user with username %s",
                updated_user[api_c.DISPLAY_NAME],
                userinfo[0][db_c.USER_ROLE],
                updated_user[db_c.USER_ROLE],
                user[api_c.USER_NAME],
            )

        # update the document
        return HuxResponse.OK(data=updated_user, data_schema=UserSchema())


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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
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
                f"Reported By: {user[api_c.USER_NAME]} "
                f"({user[api_c.USER_EMAIL_ADDRESS]})\n"
                f"Environment: {request.url_root}"
            ),
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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
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
            {
                api_c.REQUESTED_BY: f"{user.get(api_c.USER_NAME)} "
                f"({user[api_c.USER_EMAIL_ADDRESS]})"
            }
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

        return (
            TicketGetSchema().dump(new_issue),
            HTTPStatus.CREATED,
        )


@add_view_to_blueprint(
    user_bp, f"{api_c.USER_ENDPOINT}/tickets", "UserTickets"
)
class UserTickets(SwaggerView):
    """User Tickets Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieves tickets reported by user",
            "schema": {"type": "array", "items": TicketGetSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get tickets created by user."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves tickets reported by user.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Response list of user's tickets,
                HTTP status code.

        Raises:
            FailedAPIDependencyError: Exception raised due to unexpected return
                field format in JIRA API response.
        """

        matching_tickets = (
            JiraConnection()
            .search_jira_issues(
                jql_suffix=f'{api_c.DESCRIPTION}~"{user[api_c.USER_EMAIL_ADDRESS]}"',
                return_fields=[
                    api_c.ID,
                    api_c.KEY,
                    api_c.SUMMARY,
                    api_c.STATUS,
                    api_c.CREATED,
                ],
                order_by_field=api_c.KEY,
                sort_order="DESC",
            )
            .get(api_c.ISSUES)
        )

        if not matching_tickets:
            logger.info(
                "No matching tickets found for user with user name %s.",
                user[api_c.USER_NAME],
            )
            return HuxResponse.OK("No matching tickets found for user")

        my_tickets = []
        # set the dict in ticket by rearranging the needed values as received
        # in the jira response as per the required response schema
        try:
            for ticket in matching_tickets:
                my_tickets.append(
                    {
                        api_c.ID: ticket.get(api_c.ID),
                        api_c.KEY: ticket.get(api_c.KEY),
                        api_c.SUMMARY: ticket.get(api_c.FIELDS).get(
                            api_c.SUMMARY
                        ),
                        api_c.CREATED: parse(
                            ticket.get(api_c.FIELDS).get(api_c.CREATED)
                        ),
                        api_c.STATUS: ticket.get(api_c.FIELDS)
                        .get(api_c.STATUS)
                        .get(api_c.NAME),
                    }
                )
        except ParserError as error:
            logger.error("%s: %s.", error.__class__, error)
            raise FailedAPIDependencyError(
                "CREATED field not in expected format in JIRA API response",
                error.__class__,
            ) from error

        return HuxResponse.OK(data=my_tickets, data_schema=TicketGetSchema())


@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}/{api_c.USER_PREFERENCES}",
    "UserPreferencesView",
)
class UserPreferencesView(SwaggerView):
    """User Preferences class."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input user preferences body.",
            "example": api_c.ALERT_SAMPLE_RESPONSE,
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "User preferences updated.",
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def put(self, user: dict) -> Tuple[dict, int]:
        """Updates a user preferences.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[dict, int]: User doc, HTTP status code.
        """

        body = UserPreferencesSchema().load(request.get_json())

        if not body:
            return {
                api_c.MESSAGE: "No alert body provided."
            }, HTTPStatus.BAD_REQUEST

        updated_user = update_user(
            get_db_client(),
            okta_id=user[db_c.OKTA_ID],
            update_doc={
                **body,
                **{
                    db_c.UPDATED_BY: user[api_c.USER_NAME],
                },
            },
        )

        # update the document
        return (
            UserSchema().dump(updated_user),
            HTTPStatus.OK,
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

    @api_error_handler()
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

        jira_issues = (
            JiraConnection()
            .search_jira_issues(
                jql_suffix=f"{api_c.COMPONENT}={get_config().JIRA_PROJECT_KEY}"
                f" AND {api_c.SUMMARY}~{summary} "
                f"AND {api_c.STATUS}!={api_c.STATE_DONE}",
                return_fields=[
                    api_c.DESCRIPTION,
                    api_c.STATUS,
                    api_c.CREATED,
                    api_c.UPDATED,
                ],
                order_by_field=api_c.UPDATED,
                sort_order="DESC",
            )
            .get(api_c.ISSUES)
        )

        if not jira_issues:
            logger.info(
                "No user requests found for user with user name %s.",
                user[api_c.USER_NAME],
            )
            return {"message": "No user requests found."}, HTTPStatus.OK

        return (
            jsonify(
                RequestedUserSchema().dump(
                    filter_team_member_requests(jira_issues),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}/{api_c.RBAC_MATRIX}",
    "UsersRBACMatrix",
)
class UsersRBACMatrix(SwaggerView):
    """User RBAC Matrix Class."""

    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve RBAC Matrix.",
            "schema": RBACMatrixSchema,
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
        """Retrieves RBAC matrix for users.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: dict of requested users, HTTP status code.
        """

        # Fetch rbac matrix settings document from configurations collection
        database = get_db_client()
        query_filter = {
            db_c.CONFIGURATION_FIELD_TYPE: {
                "$in": [db_c.CONFIGURATION_TYPE_RBAC_MATRIX]
            }
        }
        rbac_matrix = get_document(
            database=database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            query_filter=query_filter,
        )

        if not rbac_matrix:
            logger.error(
                "RBAC matrix document not found in configurations collection."
            )
            return HuxResponse.NOT_FOUND(
                "RBAC matrix document not found in configurations collection."
            )

        return HuxResponse.OK(
            data=rbac_matrix[db_c.CONFIGURATION_FIELD_SETTINGS],
            data_schema=RBACMatrixSchema(),
        )


@add_view_to_blueprint(
    user_bp,
    f"{api_c.USER_ENDPOINT}/<user_id>",
    "DeleteUser",
)
class DeleteUser(SwaggerView):
    """Delete User Class."""

    responses = {
        HTTPStatus.NO_CONTENT.value: {
            "description": "Indicates a successful deletion.",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {
            "description": "Indicates a failed deletion.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.USER_TAG]

    @api_error_handler()
    @requires_access_levels([api_c.ADMIN_LEVEL])
    def delete(self, user_id: str, user: dict) -> Tuple[Response, int]:
        """Deletes a user from the database.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user_id (str): user ID of the user to be deleted.
            user (dict): user object.

        Returns:
            Tuple[Response, int]: message dict, HTTP status code.
        """

        database = get_db_client()

        deleted_user = get_user(database, user_id=ObjectId(user_id))

        if delete_user(database, user_id=ObjectId(user_id)):
            if deleted_user:
                logger.info(
                    "%s deleted the user %s.",
                    user[db_c.USER_NAME],
                    deleted_user[db_c.USER_DISPLAY_NAME],
                )
            return HuxResponse.NO_CONTENT()

        return HuxResponse.INTERNAL_SERVER_ERROR("Failed to delete this user.")
