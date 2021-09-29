# pylint: disable=no-self-use
"""Paths for destinations API"""
from http import HTTPStatus
from typing import Tuple
from flasgger import SwaggerView
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from huxunifylib.util.general.logging import logger
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database import (
    delivery_platform_management as destination_management,
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
)
from huxunify.api.data_connectors.aws import (
    parameter_store,
    get_auth_from_parameter_store,
)
from huxunify.api.schema.destinations import (
    DestinationGetSchema,
    DestinationPutSchema,
    DestinationConstantsSchema,
    DestinationValidationSchema,
    DestinationDataExtPostSchema,
    DestinationDataExtGetSchema,
    SFMCAuthCredsSchema,
    FacebookAuthCredsSchema,
    SendgridAuthCredsSchema,
    GoogleAdsAuthCredsSchema,
    QualtricsAuthCredsSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    validate_destination,
    get_user_name,
)
from huxunify.api.route.utils import (
    get_db_client,
)
import huxunify.api.constants as api_c


# setup the destination blueprint
dest_bp = Blueprint(api_c.DESTINATIONS_ENDPOINT, import_name=__name__)


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
    def get(self, destination_id: str) -> Tuple[dict, int]:
        """Retrieves a destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.

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
    def get(self) -> Tuple[list, int]:  # pylint: disable=no-self-use
        """Retrieves all destinations.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: list of destinations, HTTP status code.
        """

        destinations = destination_management.get_all_delivery_platforms(
            get_db_client()
        )
        return (
            jsonify(DestinationGetSchema().dump(destinations, many=True)),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/<destination_id>",
    "DestinationPutView",
)
class DestinationPutView(SwaggerView):
    """Destination Put view class."""

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
            "example": {
                api_c.AUTHENTICATION_DETAILS: {
                    api_c.FACEBOOK_ACCESS_TOKEN: "MkU3Ojgwm",
                    api_c.FACEBOOK_APP_SECRET: "717bdOQqZO99",
                    api_c.FACEBOOK_APP_ID: "2951925002021888",
                    api_c.FACEBOOK_AD_ACCOUNT_ID: "111333777",
                },
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": DestinationGetSchema,
            "description": "Updated destination.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update the destination.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": api_c.DESTINATION_NOT_FOUND
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    # pylint: disable=unexpected-keyword-arg
    # pylint: disable=too-many-return-statements
    @api_error_handler(
        custom_message={
            ValidationError: {"message": api_c.INVALID_AUTH_DETAILS}
        }
    )
    @validate_destination()
    @get_user_name()
    def put(self, destination_id: str, user_name: str) -> Tuple[dict, int]:
        """Updates a destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.
            user_name (str): user_name extracted from Okta.

        Returns:
            Tuple[dict, int]: Destination doc, HTTP status code.
        """

        # load into the schema object
        body = DestinationPutSchema().load(request.get_json(), partial=True)

        # grab the auth details
        auth_details = body.get(api_c.AUTHENTICATION_DETAILS)
        performance_de = None
        authentication_parameters = None
        database = get_db_client()

        # check if destination exists
        destination = destination_management.get_delivery_platform(
            database, destination_id
        )
        platform_type = destination.get(db_c.DELIVERY_PLATFORM_TYPE)
        if platform_type == db_c.DELIVERY_PLATFORM_SFMC:
            SFMCAuthCredsSchema().load(auth_details)
            performance_de = body.get(
                api_c.SFMC_PERFORMANCE_METRICS_DATA_EXTENSION
            )
            if not performance_de:
                logger.error("%s", api_c.PERFORMANCE_METRIC_DE_NOT_ASSIGNED[0])
                return (
                    {"message": api_c.PERFORMANCE_METRIC_DE_NOT_ASSIGNED},
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
                    user_name=user_name,
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
    def get(self) -> Tuple[dict, int]:
        """Retrieves all destination constants.

        ---
        security:
            - Bearer: ["Authorization"]

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
            "example": {
                api_c.DESTINATION_TYPE: "facebook",
                api_c.AUTHENTICATION_DETAILS: {
                    api_c.FACEBOOK_ACCESS_TOKEN: "MkU3Ojgwm",
                    api_c.FACEBOOK_APP_SECRET: "717bdOQqZO99",
                    api_c.FACEBOOK_APP_ID: "2951925002021888",
                    api_c.FACEBOOK_AD_ACCOUNT_ID: "111333777",
                },
            },
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
    def post(self) -> Tuple[dict, int]:
        """Validates the credentials for a destination.

        ---
        security:
            - Bearer: ["Authorization"]

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
            SendgridConnector(
                auth_details={
                    SendgridCredentials.SENDGRID_AUTH_TOKEN.value: body.get(
                        api_c.AUTHENTICATION_DETAILS
                    ).get(api_c.SENDGRID_AUTH_TOKEN),
                },
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
    def get(self, destination_id: str) -> Tuple[list, int]:
        """Retrieves destination data extensions.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[list, int]: List of data extensions, HTTP status code.
        """

        destination = destination_management.get_delivery_platform(
            get_db_client(), destination_id
        )

        if not destination:
            logger.error(
                "Destination does not exist: %s",
                destination_id,
            )
            return {
                "message": api_c.DESTINATION_NOT_FOUND,
            }, HTTPStatus.NOT_FOUND

        if api_c.AUTHENTICATION_DETAILS not in destination:
            logger.error(
                "Destination Authentication for %s failed since authentication "
                "details missing.",
                destination_id,
            )
            return {
                "message": api_c.DESTINATION_AUTHENTICATION_FAILED
            }, HTTPStatus.BAD_REQUEST

        ext_list = []

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

            ext_list = sfmc_connector.get_list_of_data_extensions()
            logger.info(
                "Found %s data extensions for %s.",
                len(ext_list),
                destination_id,
            )

        else:
            logger.error(api_c.DATA_EXTENSION_NOT_SUPPORTED)
            return {
                "message": api_c.DATA_EXTENSION_NOT_SUPPORTED
            }, HTTPStatus.BAD_REQUEST

        return (
            jsonify(
                sorted(
                    DestinationDataExtGetSchema().dump(ext_list, many=True),
                    key=lambda i: i[api_c.NAME].lower(),
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
            "description": "Input Audience body.",
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
    def post(self, destination_id: str) -> Tuple[dict, int]:
        """Creates a destination data extension.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[dict, int]: Data Extension ID, HTTP status code.
        """

        database = get_db_client()
        destination = destination_management.get_delivery_platform(
            database, destination_id
        )

        if not destination:
            logger.error(
                "Destination does not exist: %s",
                destination_id,
            )
            return {
                "message": api_c.DESTINATION_NOT_FOUND,
            }, HTTPStatus.NOT_FOUND

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
                extension = sfmc_connector.create_data_extension(
                    body.get(api_c.DATA_EXTENSION)
                )
                # pylint: disable=too-many-function-args
                create_notification(
                    database,
                    db_c.NOTIFICATION_TYPE_SUCCESS,
                    (
                        f"New data extension named"
                        f'"{body.get(api_c.DATA_EXTENSION)}" created in '
                        f'destination "{destination[db_c.NAME]}" '
                        f"by {get_user_name()}."
                    ),
                    api_c.DESTINATIONS_TAG,
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
