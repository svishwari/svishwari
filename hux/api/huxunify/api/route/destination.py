# pylint: disable=no-self-use,too-many-lines,unused-argument
"""Paths for destinations API"""
import datetime
from threading import Thread
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from flasgger import SwaggerView
from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError

from huxunifylib.util.general.logging import logger
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database import (
    delivery_platform_management as destination_management,
)
from huxunifylib.database.engagement_management import (
    remove_destination_from_all_engagements,
)
from huxunifylib.database.collection_management import (
    get_documents,
    delete_document,
)
import huxunifylib.database.constants as db_c
from huxunifylib.util.general.const import (
    FacebookCredentials,
    SFMCCredentials,
    SendgridCredentials,
    GoogleCredentials,
    QualtricsCredentials,
)
from huxunifylib.connectors import (
    FacebookConnector,
    SFMCConnector,
    SendgridConnector,
    GoogleConnector,
    QualtricsConnector,
    AudienceAlreadyExists,
    AuthenticationFailed,
)
from huxunifylib.connectors import connector_sfmc
from huxunify.api.data_connectors.aws import (
    get_auth_from_parameter_store,
    parameter_store,
)
from huxunify.api.data_connectors.jira import JiraConnection
from huxunify.api.schema.destinations import (
    DestinationGetSchema,
    DestinationPatchSchema,
    DestinationConstantsSchema,
    DestinationValidationSchema,
    DestinationDataExtPostSchema,
    DestinationDataExtGetSchema,
    DestinationRequestSchema,
    SFMCAuthCredsSchema,
    DestinationDataExtConfigSchema,
    FacebookAuthCredsSchema,
    SendgridAuthCredsSchema,
    QualtricsAuthCredsSchema,
    GoogleAdsAuthCredsSchema,
    DestinationPutSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    validate_destination,
    requires_access_levels,
)
from huxunify.api.route.utils import (
    get_db_client,
)
import huxunify.api.constants as api_c


# setup the destination blueprint
dest_bp = Blueprint(api_c.DESTINATIONS_ENDPOINT, import_name=__name__)

facebook_auth_example = {
    api_c.AUTHENTICATION_DETAILS: {
        api_c.FACEBOOK_ACCESS_TOKEN: "ABCD",
        api_c.FACEBOOK_APP_SECRET: "1234",
        api_c.FACEBOOK_APP_ID: "1234",
        api_c.FACEBOOK_AD_ACCOUNT_ID: "1234",
    },
}


@dest_bp.before_request
@secured()
def before_request():
    """Protect all of the destinations endpoints."""

    pass  # pylint: disable=unnecessary-pass


def set_sfmc_auth_details(sfmc_auth: dict) -> dict:
    """Set SFMC auth details.

    Args:
        sfmc_auth (dict): Auth details.

    Returns:
        SFMC auth (dict): SFMC auth dict containing SFMC credentials.
    """

    return {
        SFMCCredentials.SFMC_ACCOUNT_ID.value: sfmc_auth.get(
            api_c.SFMC_ACCOUNT_ID
        ),
        SFMCCredentials.SFMC_AUTH_URL.value: sfmc_auth.get(
            api_c.SFMC_AUTH_BASE_URI
        ),
        SFMCCredentials.SFMC_CLIENT_ID.value: sfmc_auth.get(
            api_c.SFMC_CLIENT_ID
        ),
        SFMCCredentials.SFMC_CLIENT_SECRET.value: sfmc_auth.get(
            api_c.SFMC_CLIENT_SECRET
        ),
        SFMCCredentials.SFMC_SOAP_ENDPOINT.value: sfmc_auth.get(
            api_c.SFMC_SOAP_BASE_URI
        ),
        SFMCCredentials.SFMC_URL.value: sfmc_auth.get(
            api_c.SFMC_REST_BASE_URI
        ),
    }


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/<destination_id>",
    "DestinationGetView",
)
class DestinationGetView(SwaggerView):
    """Single Destination Get view class."""

    parameters = [
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": DestinationGetSchema,
            "description": "Retrieved destination details.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve the destination.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": api_c.DESTINATION_NOT_FOUND,
        },
    }
    responses.update(AUTH401_RESPONSE)

    tags = [api_c.DESTINATIONS_TAG]

    @api_error_handler()
    @validate_destination()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, destination_id: str, user: dict) -> Tuple[dict, int]:
        """Retrieves a destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Destination dict, HTTP status code.
        """

        destination = destination_management.get_delivery_platform(
            get_db_client(), destination_id
        )

        return DestinationGetSchema().dump(destination), HTTPStatus.OK


@add_view_to_blueprint(
    dest_bp, api_c.DESTINATIONS_ENDPOINT, "DestinationsView"
)
class DestinationsView(SwaggerView):
    """Destinations view class."""

    parameters = [
        {
            "name": api_c.DESTINATION_REFRESH,
            "description": "Refresh all.",
            "type": "boolean",
            "in": "query",
            "required": False,
            "example": "False",
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of all destinations",
            "schema": {"type": "array", "items": DestinationGetSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get all destinations."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(
        self, user: dict
    ) -> Tuple[Response, int]:  # pylint: disable=no-self-use
        """Retrieves all destinations.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Response list of destinations, HTTP status code.
        """
        database = get_db_client()
        destinations = destination_management.get_all_delivery_platforms(
            database
        )

        refresh_all = request.args.get(
            api_c.DESTINATION_REFRESH,
            False,
            type=lambda v: v.lower() == "true",
        )

        connector_dict = {
            db_c.DELIVERY_PLATFORM_FACEBOOK: FacebookConnector,
            db_c.DELIVERY_PLATFORM_SFMC: SFMCConnector,
            db_c.DELIVERY_PLATFORM_QUALTRICS: QualtricsConnector,
            db_c.DELIVERY_PLATFORM_SENDGRID: SendgridConnector,
            db_c.DELIVERY_PLATFORM_TWILIO: SendgridConnector,
            db_c.DELIVERY_PLATFORM_GOOGLE: GoogleConnector,
        }

        # Map db status values to api status values
        status_mapping = {
            db_c.STATUS_SUCCEEDED: api_c.STATUS_ACTIVE,
            db_c.STATUS_PENDING: api_c.STATUS_PENDING,
            db_c.STATUS_FAILED: api_c.STATUS_ERROR,
            db_c.STATUS_REQUESTED: api_c.STATUS_REQUESTED,
        }

        for destination in destinations:
            if refresh_all:
                if destination[api_c.DELIVERY_PLATFORM_TYPE] in connector_dict:
                    try:
                        connector_dict[
                            destination[api_c.DELIVERY_PLATFORM_TYPE]
                        ](
                            auth_details=get_auth_from_parameter_store(
                                destination[api_c.AUTHENTICATION_DETAILS],
                                destination[api_c.DELIVERY_PLATFORM_TYPE],
                            )
                        )
                        destination[
                            db_c.DELIVERY_PLATFORM_STATUS
                        ] = db_c.STATUS_SUCCEEDED
                    # pylint: disable=broad-except
                    except Exception as exception:
                        logger.error(
                            "%s: %s while connecting to destination %s.",
                            exception.__class__,
                            str(exception),
                            destination[api_c.DELIVERY_PLATFORM_TYPE],
                        )
                        destination[
                            db_c.DELIVERY_PLATFORM_STATUS
                        ] = db_c.STATUS_FAILED

                    destination_management.update_delivery_platform(
                        database=database,
                        delivery_platform_id=destination[db_c.ID],
                        name=destination[db_c.DELIVERY_PLATFORM_NAME],
                        delivery_platform_type=destination[
                            db_c.DELIVERY_PLATFORM_TYPE
                        ],
                        status=destination[db_c.DELIVERY_PLATFORM_STATUS],
                    )
            destination[db_c.DELIVERY_PLATFORM_STATUS] = status_mapping[
                destination[db_c.DELIVERY_PLATFORM_STATUS]
            ]
        return (
            jsonify(DestinationGetSchema().dump(destinations, many=True)),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/<destination_id>/authentication",
    "DestinationAuthenticationPostView",
)
class DestinationAuthenticationPostView(SwaggerView):
    """Destination Authentication post view class."""

    parameters = [
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "description": "Destination Object.",
            "type": "object",
            "example": facebook_auth_example,
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": DestinationGetSchema,
            "description": "Updated destination.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update the authentication details of the destination.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": api_c.DESTINATION_NOT_FOUND
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    @api_error_handler(
        custom_message={
            ValidationError: {"message": api_c.INVALID_AUTH_DETAILS}
        }
    )
    @validate_destination()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def put(self, destination_id: ObjectId, user: dict) -> Tuple[dict, int]:
        """Sets a destination's authentication details.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (ObjectId): Destination ID.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Destination doc, HTTP status code.
        """

        # load into the schema object
        body = DestinationPutSchema().load(request.get_json(), partial=True)

        # grab the auth details
        auth_details = body.get(api_c.AUTHENTICATION_DETAILS)
        performance_de = None
        campaign_de = None
        authentication_parameters = None
        database = get_db_client()

        # check if destination exists
        destination = destination_management.get_delivery_platform(
            database, destination_id
        )
        platform_type = destination.get(db_c.DELIVERY_PLATFORM_TYPE)
        if platform_type == db_c.DELIVERY_PLATFORM_SFMC:
            SFMCAuthCredsSchema().load(auth_details)
            sfmc_config = body.get(db_c.CONFIGURATION)
            if not sfmc_config or not isinstance(sfmc_config, dict):
                logger.error("%s", api_c.SFMC_CONFIGURATION_MISSING)
                return (
                    {"message": api_c.SFMC_CONFIGURATION_MISSING},
                    HTTPStatus.BAD_REQUEST,
                )

            performance_de = sfmc_config.get(
                api_c.SFMC_PERFORMANCE_METRICS_DATA_EXTENSION
            )
            if not performance_de:
                logger.error("%s", api_c.PERFORMANCE_METRIC_DE_NOT_ASSIGNED)
                return (
                    {"message": api_c.PERFORMANCE_METRIC_DE_NOT_ASSIGNED},
                    HTTPStatus.BAD_REQUEST,
                )
            campaign_de = sfmc_config.get(
                api_c.SFMC_CAMPAIGN_ACTIVITY_DATA_EXTENSION
            )
            if not campaign_de:
                logger.error("%s", api_c.CAMPAIGN_ACTIVITY_DE_NOT_ASSIGNED)
                return (
                    {"message": api_c.CAMPAIGN_ACTIVITY_DE_NOT_ASSIGNED},
                    HTTPStatus.BAD_REQUEST,
                )
            DestinationDataExtConfigSchema().load(sfmc_config)
            if performance_de == campaign_de:
                logger.error("%s", api_c.SAME_PERFORMANCE_CAMPAIGN_ERROR)
                return (
                    {"message": api_c.SAME_PERFORMANCE_CAMPAIGN_ERROR},
                    HTTPStatus.BAD_REQUEST,
                )
        elif platform_type == db_c.DELIVERY_PLATFORM_FACEBOOK:
            FacebookAuthCredsSchema().load(auth_details)
        elif platform_type in [
            db_c.DELIVERY_PLATFORM_SENDGRID,
            db_c.DELIVERY_PLATFORM_TWILIO,
        ]:
            SendgridAuthCredsSchema().load(auth_details)
        elif platform_type == db_c.DELIVERY_PLATFORM_QUALTRICS:
            QualtricsAuthCredsSchema().load(auth_details)
        elif platform_type == db_c.DELIVERY_PLATFORM_GOOGLE:
            GoogleAdsAuthCredsSchema().load(auth_details)

        if auth_details:
            # store the secrets for the updated authentication details
            authentication_parameters = (
                parameter_store.set_destination_authentication_secrets(
                    authentication_details=auth_details,
                    is_updated=True,
                    destination_id=destination_id,
                    destination_type=platform_type,
                )
            )
            is_added = True

        return (
            DestinationGetSchema().dump(
                destination_management.update_delivery_platform(
                    database=database,
                    delivery_platform_id=destination_id,
                    delivery_platform_type=destination[
                        db_c.DELIVERY_PLATFORM_TYPE
                    ],
                    name=destination[db_c.DELIVERY_PLATFORM_NAME],
                    authentication_details=authentication_parameters,
                    added=is_added,
                    performance_de=performance_de,
                    campaign_de=campaign_de,
                    user_name=user[api_c.USER_NAME],
                    status=db_c.STATUS_SUCCEEDED,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/constants",
    "DestinationsConstants",
)
class DestinationsConstants(SwaggerView):
    """Destinations Constants view class."""

    responses = {
        HTTPStatus.OK.value: {
            "schema": DestinationConstantsSchema,
            "description": "Retrieve destination constants.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve the destination constants.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves all destination constants.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: dict of destination constants, HTTP status code.
        """

        return (
            DestinationConstantsSchema().dump(api_c.DESTINATION_CONSTANTS),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/validate",
    "DestinationValidatePostView",
)
class DestinationValidatePostView(SwaggerView):
    """Destination Validation Post view class."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Validate destination body.",
            "example": facebook_auth_example,
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Validated destination successfully.",
            "schema": {
                "example": {
                    "message": "Destination is validated successfully"
                },
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to validate the destination.",
            "schema": {
                "example": {"message": "Destination can not be validated"},
            },
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    # pylint: disable=bare-except,too-many-return-statements
    @api_error_handler(
        custom_message={"message": api_c.DESTINATION_AUTHENTICATION_FAILED}
    )
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def post(self, user: dict) -> Tuple[dict, int]:
        """Validates the credentials for a destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Message indicating connection success/failure,
                HTTP status code.
        """

        body = DestinationValidationSchema().load(request.get_json())
        platform_type = body.get(api_c.TYPE)

        # test the destination connection and update connection status
        if platform_type == db_c.DELIVERY_PLATFORM_FACEBOOK:
            logger.info("Trying to connect to Facebook.")
            destination_connector = FacebookConnector(
                auth_details={
                    FacebookCredentials.FACEBOOK_AD_ACCOUNT_ID.name: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.FACEBOOK_AD_ACCOUNT_ID),
                    FacebookCredentials.FACEBOOK_APP_ID.name: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.FACEBOOK_APP_ID),
                    FacebookCredentials.FACEBOOK_APP_SECRET.name: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.FACEBOOK_APP_SECRET),
                    FacebookCredentials.FACEBOOK_ACCESS_TOKEN.name: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.FACEBOOK_ACCESS_TOKEN),
                },
            )
            if destination_connector.check_connection():
                logger.info("Facebook destination validated successfully.")
                return {
                    "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS
                }, HTTPStatus.OK
            logger.error("Could not validate Facebook successfully.")
        elif platform_type == db_c.DELIVERY_PLATFORM_SFMC:
            logger.info("Validating SFMC destination.")
            connector = SFMCConnector(
                auth_details=set_sfmc_auth_details(
                    body.get(api_c.AUTHENTICATION_DETAILS)
                )
            )

            ext_list = sorted(
                DestinationDataExtGetSchema().dump(
                    connector.get_list_of_data_extensions(), many=True
                ),
                key=lambda i: i[api_c.NAME].lower(),
            )
            logger.info("Successfully validated SFMC destination.")
            return {
                "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS,
                api_c.SFMC_PERFORMANCE_METRICS_DATA_EXTENSIONS: ext_list,
            }, HTTPStatus.OK
        elif platform_type in [
            db_c.DELIVERY_PLATFORM_SENDGRID,
            db_c.DELIVERY_PLATFORM_TWILIO,
        ]:
            sendgrid_connector = SendgridConnector(
                auth_details={
                    SendgridCredentials.SENDGRID_AUTH_TOKEN.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.SENDGRID_AUTH_TOKEN),
                },
            )
            if sendgrid_connector.check_connection():
                logger.info(
                    "%s destination validated successfully.",
                    platform_type.capitalize(),
                )
                return {
                    "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS
                }, HTTPStatus.OK
        elif platform_type == db_c.DELIVERY_PLATFORM_QUALTRICS:
            qualtrics_connector = QualtricsConnector(
                auth_details={
                    QualtricsCredentials.QUALTRICS_API_TOKEN.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.QUALTRICS_API_TOKEN),
                    QualtricsCredentials.QUALTRICS_DATA_CENTER.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.QUALTRICS_DATA_CENTER),
                    QualtricsCredentials.QUALTRICS_OWNER_ID.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.QUALTRICS_OWNER_ID),
                    QualtricsCredentials.QUALTRICS_DIRECTORY_ID.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(
                        api_c.QUALTRICS_DIRECTORY_ID
                    ),
                }
            )
            if qualtrics_connector.check_connection():
                logger.info("Qualtrics destination validated successfully.")
                return {
                    "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS
                }, HTTPStatus.OK

            logger.error("Could not validate Qualtrics successfully.")
        elif platform_type == db_c.DELIVERY_PLATFORM_GOOGLE:
            google_connector = GoogleConnector(
                auth_details={
                    GoogleCredentials.GOOGLE_DEVELOPER_TOKEN.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.GOOGLE_DEVELOPER_TOKEN),
                    GoogleCredentials.GOOGLE_REFRESH_TOKEN.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.GOOGLE_REFRESH_TOKEN),
                    GoogleCredentials.GOOGLE_CLIENT_CUSTOMER_ID.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(
                        api_c.GOOGLE_CLIENT_CUSTOMER_ID
                    ),
                    GoogleCredentials.GOOGLE_CLIENT_ID.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.GOOGLE_CLIENT_ID),
                    GoogleCredentials.GOOGLE_CLIENT_SECRET.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.GOOGLE_CLIENT_SECRET),
                }
            )
            if google_connector.check_connection():
                logger.info("Google Ads destination validated successfully.")
                return {
                    "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS
                }, HTTPStatus.OK

            logger.error("Could not validate Google Ads successfully.")

        else:
            logger.error(
                "Destination type %s not supported yet.", body.get(db_c.TYPE)
            )
            return {
                "message": api_c.DESTINATION_NOT_SUPPORTED
            }, HTTPStatus.BAD_REQUEST

        logger.error(
            "Could not validate destination type %s.", body.get(db_c.TYPE)
        )
        return (
            {"message": api_c.DESTINATION_AUTHENTICATION_FAILED},
            HTTPStatus.FORBIDDEN,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/<destination_id>/{api_c.DATA_EXTENSIONS}",
    "DestinationDataExtView",
)
class DestinationDataExtView(SwaggerView):
    """Destination Data Extension view class."""

    parameters = [
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieved destination data extensions.",
            "schema": {"type": "array", "items": DestinationDataExtGetSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve destination data extensions.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    @api_error_handler()
    @validate_destination()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, destination_id: str, user: dict) -> Tuple[Response, int]:
        """Retrieves destination data extensions.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.
            user (dict): user object.


        Returns:
            Tuple[Response, int]: Response list of data extensions, HTTP status code.
        """

        destination = destination_management.get_delivery_platform(
            get_db_client(), destination_id
        )

        if api_c.AUTHENTICATION_DETAILS not in destination:
            logger.error(
                "Destination authentication for %s failed since authentication "
                "details missing.",
                destination_id,
            )
            return (
                jsonify({"message": api_c.DESTINATION_AUTHENTICATION_FAILED}),
                HTTPStatus.BAD_REQUEST,
            )

        if (
            destination[api_c.DELIVERY_PLATFORM_TYPE]
            == db_c.DELIVERY_PLATFORM_SFMC
        ):
            try:
                sfmc_connector = SFMCConnector(
                    auth_details=get_auth_from_parameter_store(
                        destination[api_c.AUTHENTICATION_DETAILS],
                        destination[api_c.DELIVERY_PLATFORM_TYPE],
                    )
                )
                ext_list = sfmc_connector.get_list_of_data_extensions()
                logger.info(
                    "Found %s data extensions for %s.",
                    len(ext_list),
                    destination_id,
                )
            except AuthenticationFailed:
                return (
                    jsonify(
                        {"message": api_c.DESTINATION_AUTHENTICATION_FAILED}
                    ),
                    HTTPStatus.FORBIDDEN,
                )

        else:
            logger.error(api_c.DATA_EXTENSION_NOT_SUPPORTED)
            return (
                jsonify({"message": api_c.DATA_EXTENSION_NOT_SUPPORTED}),
                HTTPStatus.BAD_REQUEST,
            )

        return (
            jsonify(
                sorted(
                    DestinationDataExtGetSchema().dump(ext_list, many=True),
                    key=lambda i: i[db_c.CREATE_TIME],
                    reverse=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/<destination_id>/{api_c.DATA_EXTENSIONS}",
    "DestinationDataExtPostView",
)
class DestinationDataExtPostView(SwaggerView):
    """Destination Data Extension Post class."""

    parameters = [
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Destination body.",
            "example": {api_c.DATA_EXTENSION: "data_ext_name"},
        },
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "description": "Created destination data extension successfully.",
            "schema": DestinationDataExtGetSchema,
        },
        HTTPStatus.OK.value: {
            "description": "Destination data extension already exists.",
            "schema": DestinationDataExtGetSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create destination data extension.",
            "schema": {
                "example": {
                    "message": "Destination data extension cannot be created."
                },
            },
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    # pylint: disable=too-many-return-statements
    @api_error_handler()
    @validate_destination()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def post(self, destination_id: str, user: dict) -> Tuple[dict, int]:
        """Creates a destination data extension.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.
            user (dict): User object.

        Returns:
            Tuple[dict, int]: Data Extension ID, HTTP status code.
        """

        database = get_db_client()
        destination = destination_management.get_delivery_platform(
            database, destination_id
        )

        if api_c.AUTHENTICATION_DETAILS not in destination:
            logger.error(api_c.DATA_EXTENSION_NOT_SUPPORTED)
            return {
                "message": api_c.DATA_EXTENSION_NOT_SUPPORTED
            }, HTTPStatus.BAD_REQUEST

        body = DestinationDataExtPostSchema().load(
            request.get_json(), partial=True
        )

        if (
            destination[api_c.DELIVERY_PLATFORM_TYPE]
            == db_c.DELIVERY_PLATFORM_SFMC
        ):

            sfmc_connector = SFMCConnector(
                auth_details=get_auth_from_parameter_store(
                    destination[api_c.AUTHENTICATION_DETAILS],
                    destination[api_c.DELIVERY_PLATFORM_TYPE],
                )
            )

            if not sfmc_connector.check_connection():
                logger.info("Could not validate SFMC successfully.")
                return {
                    "message": api_c.DESTINATION_AUTHENTICATION_FAILED
                }, HTTPStatus.FORBIDDEN

            status_code = HTTPStatus.CREATED

            try:
                # work around to handle connector issue - deep copy list
                # pylint: disable=unnecessary-comprehension
                sfmc_cdp_prop_list = [
                    x for x in connector_sfmc.SFMC_CDP_PROPERTIES_LIST
                ]

                extension = sfmc_connector.create_data_extension(
                    body.get(api_c.DATA_EXTENSION)
                )

                # work around to handle connector issue - set list back
                connector_sfmc.SFMC_CDP_PROPERTIES_LIST = sfmc_cdp_prop_list

                # pylint: disable=too-many-function-args
                create_notification(
                    database,
                    db_c.NOTIFICATION_TYPE_SUCCESS,
                    (
                        f"New data extension named"
                        f'"{body.get(api_c.DATA_EXTENSION)}" created in '
                        f'destination "{destination[db_c.NAME]}" '
                        f"by {user[api_c.USER_NAME]}."
                    ),
                    api_c.DESTINATIONS_TAG,
                    user[api_c.USER_NAME],
                )
            except AudienceAlreadyExists:
                # TODO - this is a work around until ORCH-288 is done
                status_code = HTTPStatus.OK
                extension = {}
                for ext in sfmc_connector.get_list_of_data_extensions():
                    if ext["CustomerKey"] == body.get(api_c.DATA_EXTENSION):
                        extension = ext
            return DestinationDataExtGetSchema().dump(extension), status_code

        logger.error(api_c.DATA_EXTENSION_NOT_SUPPORTED)
        return {
            "message": api_c.DATA_EXTENSION_NOT_SUPPORTED
        }, HTTPStatus.BAD_REQUEST


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/<destination_id>",
    "DestinationPatchView",
)
class DestinationPatchView(SwaggerView):
    """Destination Patch class."""

    parameters = [
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Destination body.",
            "example": {db_c.ENABLED: False},
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Destination updated.",
            "schema": DestinationDataExtGetSchema,
        },
        HTTPStatus.UNPROCESSABLE_ENTITY.value: {
            "description": "Failed to patch destination data.",
            "schema": {
                "example": {
                    "message": api_c.DESTINATION_INVALID_PATCH_MESSAGE
                },
            },
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    # pylint: disable=unexpected-keyword-arg
    # pylint: disable=too-many-return-statements
    @api_error_handler()
    @validate_destination()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def patch(self, destination_id: str, user: dict) -> Tuple[dict, int]:
        """Updates a destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Destination doc, HTTP status code.
        """

        # get update fields
        patch_dict = {
            k: v
            for k, v in (
                request.get_json() if request.get_json() else {}
            ).items()
            if k in api_c.DESTINATION_PATCH_FIELDS
        }

        if not patch_dict:
            logger.info("Could not patch destination.")
            return {
                "message": api_c.DESTINATION_INVALID_PATCH_MESSAGE
            }, HTTPStatus.UNPROCESSABLE_ENTITY

        # validate the schema first.
        DestinationPatchSchema().validate(patch_dict)

        database = get_db_client()

        updated_destination = (
            destination_management.update_delivery_platform_doc(
                database,
                destination_id,
                {
                    **patch_dict,
                    **{
                        db_c.UPDATED_BY: user[api_c.USER_NAME],
                        db_c.UPDATE_TIME: datetime.datetime.utcnow(),
                    },
                },
            )
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f"{user[api_c.USER_NAME]} successfully updated"
                f' "{updated_destination[db_c.NAME]}" destination.'
            ),
            api_c.DESTINATION,
            user[api_c.USER_NAME],
        )

        if not updated_destination.get(db_c.ADDED):
            # TODO: HUS-1749 - remove destinations from standalone audiences.
            # remove from any engagement audiences
            Thread(
                target=remove_destination_from_all_engagements,
                args=[
                    database,
                    destination_id,
                    user[api_c.USER_NAME],
                ],
            ).start()

        # update the document
        return (
            DestinationGetSchema().dump(updated_destination),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/request",
    "DestinationsRequestView",
)
class DestinationsRequestView(SwaggerView):
    """Destinations Request view class."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "schema": {"id": "DestinationRequestSchema"},
            "description": "Input Destination body.",
            "example": DestinationRequestSchema,
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Destination.",
            "schema": DestinationGetSchema,
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": api_c.DESTINATION_NOT_FOUND,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    # pylint: disable=too-many-return-statements
    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def post(self, user: dict) -> Tuple[list, int]:
        """Requests an unsupported destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Destination doc, HTTP status code.
        """

        destination_request = DestinationRequestSchema().load(
            request.get_json(), partial=True
        )

        # check if destination name already exists
        database = get_db_client()
        destinations = get_documents(
            database,
            db_c.DELIVERY_PLATFORM_COLLECTION,
            {
                db_c.NAME: {
                    "$regex": destination_request[db_c.NAME],
                    "$options": "i",
                }
            },
            batch_size=1,
        )

        # check if any found documents
        destinations = (
            destinations.get(db_c.DOCUMENTS, []) if destinations else []
        )

        # check if it was requested
        if destinations:
            destination = destinations[0]
            if destination.get(db_c.DELIVERY_PLATFORM_STATUS) in [
                db_c.STATUS_REQUESTED,
                db_c.STATUS_FAILED,
                db_c.STATUS_SUCCEEDED,
            ]:
                # return already requested, return 409, with message.
                return {
                    api_c.MESSAGE: "Destination already present."
                }, HTTPStatus.CONFLICT
            # otherwise set the status to requested
            destination = destination_management.update_delivery_platform_doc(
                database,
                destination[db_c.ID],
                {
                    db_c.DELIVERY_PLATFORM_STATUS: db_c.STATUS_REQUESTED,
                    db_c.ADDED: True,
                },
            )
        else:
            # create a destination object and set the status to requested.
            destination = destination_management.set_delivery_platform(
                database=database,
                delivery_platform_type=api_c.GENERIC_DESTINATION,
                name=destination_request[api_c.NAME],
                user_name=user[api_c.USER_NAME],
                status=db_c.STATUS_REQUESTED,
                enabled=False,
                added=True,
            )

            destination_request.update(
                {
                    "Requested By": user[api_c.USER_NAME],
                    "Environment": request.url_root,
                }
            )

            # create JIRA ticket for the request.
            JiraConnection().create_jira_issue(
                api_c.TASK,
                f"Requested Destination '{destination_request[api_c.NAME]}'.",
                "\n".join(
                    f"{key.title()}: {value}"
                    for key, value in destination_request.items()
                ),
            )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f"{user[api_c.USER_NAME]} successfully requested"
                f' "{destination[db_c.NAME]}" destination.'
            ),
            api_c.DESTINATION,
            user[api_c.USER_NAME],
        )

        return (
            DestinationGetSchema().dump(destination),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/<destination_id>",
    "DestinationDeleteView",
)
class DestinationDeleteView(SwaggerView):
    """Destination Delete class."""

    parameters = [
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        },
    ]

    responses = {
        HTTPStatus.NO_CONTENT.value: {
            "description": "Destination deleted.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    @api_error_handler()
    @requires_access_levels([api_c.ADMIN_LEVEL])
    def delete(self, destination_id: str, user: dict) -> Tuple[dict, int]:
        """Deletes a destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Destination doc, HTTP status code.
        """
        database = get_db_client()

        destination = destination_management.get_delivery_platform(
            database, ObjectId(destination_id)
        )

        if not destination:
            create_notification(
                database,
                db_c.NOTIFICATION_TYPE_SUCCESS,
                (
                    f"{user[api_c.USER_NAME]} requested delete for "
                    f"{destination_id} that does not exist."
                ),
                api_c.DESTINATION,
                user[api_c.USER_NAME],
            )
            return {}, HTTPStatus.NO_CONTENT

        deleted_flag = delete_document(
            database,
            db_c.DELIVERY_PLATFORM_COLLECTION,
            {db_c.ID: ObjectId(destination_id)},
            True,
            user[api_c.USER_NAME],
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f"{user[api_c.USER_NAME]} {'deleted' if deleted_flag else 'failed to delete'}"
                f' "{destination[db_c.NAME]}" destination.'
            ),
            api_c.DESTINATION,
            user[api_c.USER_NAME],
        )

        return {}, HTTPStatus.NO_CONTENT
