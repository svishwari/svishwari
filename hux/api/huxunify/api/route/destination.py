# pylint: disable=no-self-use
"""
Paths for destinations api
"""
from http import HTTPStatus
from typing import Tuple
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_apispec import marshal_with
from marshmallow import ValidationError

from huxunifylib.database import (
    delivery_platform_management as destination_management,
)
import huxunifylib.database.constants as db_c
from huxunifylib.util.general.const import FacebookCredentials, SFMCCredentials
from huxunifylib.connectors.facebook_connector import FacebookConnector
from huxunifylib.connectors.connector_sfmc import SFMCConnector
from huxunifylib.connectors.connector_exceptions import AudienceAlreadyExists
from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api.schema.destinations import (
    DestinationGetSchema,
    DestinationPutSchema,
    DestinationConstantsSchema,
    DestinationValidationSchema,
    DestinationDataExtPostSchema,
    DestinationDataExtGetSchema,
    SFMCAuthCredsSchema,
    FacebookAuthCredsSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
    get_user_name,
    set_sfmc_auth_from_parameter_store,
    api_error_handler,
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
    """Set SFMC auth details
    ---

        Args:
            sfmc_auth (dict): Auth details.

        Returns:
            Auth Object (dict): SFMC auth object.

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
    """
    Single Destination Get view class
    """

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
    def get(self, destination_id: str) -> Tuple[dict, int]:
        """Retrieves a destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[dict, int]: Destination dict, HTTP status.

        """

        if not ObjectId.is_valid(destination_id):
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        # grab the destination
        destination = destination_management.get_delivery_platform(
            get_db_client(), ObjectId(destination_id)
        )

        if not destination:
            return {
                "message": api_c.DESTINATION_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        return DestinationGetSchema().dump(destination), HTTPStatus.OK


@add_view_to_blueprint(
    dest_bp, api_c.DESTINATIONS_ENDPOINT, "DestinationsView"
)
class DestinationsView(SwaggerView):
    """
    Destinations view class
    """

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
            Tuple[list, int]: list of destinations, HTTP status.

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
    """
    Destination Put view class
    """

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
    @marshal_with(DestinationPutSchema)
    @api_error_handler()
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
            Tuple[dict, int]: Destination doc, HTTP status.

        """

        if not ObjectId.is_valid(destination_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        # load into the schema object
        try:
            body = DestinationPutSchema().load(
                request.get_json(), partial=True
            )
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        # grab the auth details
        auth_details = body.get(api_c.AUTHENTICATION_DETAILS)
        performance_de = None
        authentication_parameters = None
        destination_id = ObjectId(destination_id)

        database = get_db_client()

        # check if destination exists
        destination = destination_management.get_delivery_platform(
            database, destination_id
        )
        if not destination:
            return {
                "message": api_c.DESTINATION_NOT_FOUND
            }, HTTPStatus.NOT_FOUND
        if (
            destination[db_c.DELIVERY_PLATFORM_TYPE]
            == db_c.DELIVERY_PLATFORM_SFMC
        ):
            try:
                SFMCAuthCredsSchema().load(auth_details)
                performance_de = body.get(
                    api_c.SFMC_PERFORMANCE_METRICS_DATA_EXTENSION
                )
                if not performance_de:
                    return (
                        {"message": api_c.PERFORMANCE_METRIC_DE_NOT_ASSIGNED},
                        HTTPStatus.BAD_REQUEST,
                    )
            except ValidationError:
                return (
                    {"message": api_c.INVALID_AUTH_DETAILS},
                    HTTPStatus.BAD_REQUEST,
                )
        elif (
            destination[db_c.DELIVERY_PLATFORM_TYPE]
            == db_c.DELIVERY_PLATFORM_FACEBOOK
        ):
            try:
                FacebookAuthCredsSchema().load(auth_details)
            except ValidationError:
                return (
                    {"message": api_c.INVALID_AUTH_DETAILS},
                    HTTPStatus.BAD_REQUEST,
                )

        if auth_details:
            # store the secrets for the updated authentication details
            authentication_parameters = (
                parameter_store.set_destination_authentication_secrets(
                    authentication_details=auth_details,
                    is_updated=True,
                    destination_id=destination_id,
                    destination_type=destination[db_c.DELIVERY_PLATFORM_TYPE],
                )
            )
            is_added = True

        # update the destination
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
    """
    DestinationsConstants view class.
    """

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
            Tuple[dict, int]: dict of destination constants, HTTP status.

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
    """
    Destination Validation Post view class
    """

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

    @api_error_handler()
    def post(self) -> Tuple[dict, int]:
        """Validates the credentials for a destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: Message indicating connection
                success/failure, HTTP Status.

        """

        try:
            body = DestinationValidationSchema().load(request.get_json())
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        # test the destination connection and update connection status
        if body.get(db_c.TYPE) == db_c.DELIVERY_PLATFORM_FACEBOOK:
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
                return {
                    "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS
                }, HTTPStatus.OK
        elif body.get(api_c.DESTINATION_TYPE) == db_c.DELIVERY_PLATFORM_SFMC:
            connector = SFMCConnector(
                auth_details=set_sfmc_auth_details(
                    body.get(api_c.AUTHENTICATION_DETAILS)
                )
            )

            ext_list = DestinationDataExtGetSchema().dump(
                connector.get_list_of_data_extensions(), many=True
            )

            return {
                "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS,
                api_c.SFMC_PERFORMANCE_METRICS_DATA_EXTENSIONS: ext_list,
            }, HTTPStatus.OK
        else:
            return {
                "message": api_c.DESTINATION_NOT_SUPPORTED
            }, HTTPStatus.BAD_REQUEST

        return (
            {"message": api_c.DESTINATION_AUTHENTICATION_FAILED},
            HTTPStatus.BAD_REQUEST,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/<destination_id>/{api_c.DATA_EXTENSIONS}",
    "DestinationDataExtView",
)
class DestinationDataExtView(SwaggerView):
    """
    Destination Data Extension view class
    """

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
    def get(self, destination_id: str) -> Tuple[list, int]:
        """Retrieves destination data extensions.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[list, int]: List of data extensions, HTTP Status.

        """

        if destination_id is None or not ObjectId.is_valid(destination_id):
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        destination = destination_management.get_delivery_platform(
            get_db_client(), ObjectId(destination_id)
        )

        if not destination:
            return {
                "message": api_c.DESTINATION_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        if (
            api_c.AUTHENTICATION_DETAILS not in destination
            or api_c.DELIVERY_PLATFORM_TYPE not in destination
        ):
            return {
                "message": api_c.DESTINATION_AUTHENTICATION_FAILED
            }, HTTPStatus.BAD_REQUEST

        ext_list = []

        if (
            destination[api_c.DELIVERY_PLATFORM_TYPE]
            == db_c.DELIVERY_PLATFORM_SFMC
        ):
            connector = SFMCConnector(
                auth_details=set_sfmc_auth_from_parameter_store(
                    destination[api_c.AUTHENTICATION_DETAILS]
                )
            )
            ext_list = connector.get_list_of_data_extensions()

        return (
            jsonify(DestinationDataExtGetSchema().dump(ext_list, many=True)),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}/<destination_id>/{api_c.DATA_EXTENSIONS}",
    "DestinationDataExtPostView",
)
class DestinationDataExtPostView(SwaggerView):
    """
    Destination Data Extension Post class
    """

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
    def post(self, destination_id: str) -> Tuple[dict, int]:
        """Creates a destination data extension.
        ---
        security:
            - Bearer: ["Authorization"]
        Args:
            destination_id (str): Destination ID.
        Returns:
            Tuple[dict, int]: Data Extension ID, HTTP Status.
        """

        if destination_id is None or not ObjectId.is_valid(destination_id):
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        destination = destination_management.get_delivery_platform(
            get_db_client(), ObjectId(destination_id)
        )

        if not destination:
            return {
                "message": api_c.DESTINATION_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        if (
            api_c.AUTHENTICATION_DETAILS not in destination
            or api_c.DELIVERY_PLATFORM_TYPE not in destination
        ):
            return {
                "message": api_c.DESTINATION_AUTHENTICATION_FAILED
            }, HTTPStatus.BAD_REQUEST

        try:
            body = DestinationDataExtPostSchema().load(
                request.get_json(), partial=True
            )
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        if (
            destination[api_c.DELIVERY_PLATFORM_TYPE]
            == db_c.DELIVERY_PLATFORM_SFMC
        ):
            connector = SFMCConnector(
                auth_details=set_sfmc_auth_from_parameter_store(
                    destination[api_c.AUTHENTICATION_DETAILS]
                )
            )
            status_code = HTTPStatus.CREATED

            try:
                extension = connector.create_data_extension(
                    body.get(api_c.DATA_EXTENSION)
                )
            except AudienceAlreadyExists:
                # TODO - this is a work around until ORCH-288 is done
                status_code = HTTPStatus.OK
                extension = {}
                for ext in connector.get_list_of_data_extensions():
                    if ext["CustomerKey"] == body.get(api_c.DATA_EXTENSION):
                        extension = ext

            return DestinationDataExtGetSchema().dump(extension), status_code

        return {"message": api_c.OPERATION_FAILED}, HTTPStatus.BAD_REQUEST
