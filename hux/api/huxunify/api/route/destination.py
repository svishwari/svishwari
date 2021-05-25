# pylint: disable=no-self-use
"""
Paths for destinations api
"""
import logging
from http import HTTPStatus
from typing import Tuple
from connexion.exceptions import ProblemException
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_apispec import marshal_with
from marshmallow import ValidationError

from huxunifylib.database import (
    delivery_platform_management as destination_management,
    constants as db_constants,
)
from huxunifylib.connectors.facebook_connector import FacebookConnector
from huxunifylib.util.general.const import FacebookCredentials
from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api.schema.destinations import (
    DestinationGetSchema,
    DestinationPutSchema,
    DestinationConstants,
    DestinationValidationSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
)
import huxunify.api.constants as api_c


# setup the destination blueprint
dest_bp = Blueprint(api_c.DESTINATIONS_ENDPOINT, import_name=__name__)


@dest_bp.before_request
@secured()
def before_request():
    """Protect all of the destinations endpoints."""
    pass  # pylint: disable=unnecessary-pass


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
    }
    responses.update(AUTH401_RESPONSE)

    tags = [api_c.DESTINATIONS_TAG]

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
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        # grab the destination
        destination = destination_management.get_delivery_platform(
            get_db_client(), ObjectId(destination_id)
        )
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
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    @marshal_with(DestinationPutSchema)
    def put(self, destination_id: str) -> Tuple[dict, int]:
        """Updates a destination.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[dict, int]: Destination doc, HTTP status.

        """

        # TODO - implement after HUS-254 is done to grab user/okta_id
        user_id = ObjectId()

        # load into the schema object
        try:
            body = DestinationPutSchema().load(
                request.get_json(), partial=True
            )
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        # grab the auth details
        auth_details = body.get(api_c.AUTHENTICATION_DETAILS)
        authentication_parameters = None

        try:
            if auth_details:
                # store the secrets for the updated authentication details
                authentication_parameters = (
                    parameter_store.set_destination_authentication_secrets(
                        authentication_details=auth_details,
                        is_updated=True,
                        destination_id=destination_id,
                    )
                )
                is_added = True

            # TODO - provide input user-id to delivery platform
            #       create the destination after the PR 171 is merged
            # update the destination
            return (
                destination_management.update_delivery_platform(
                    database=get_db_client(),
                    delivery_platform_id=ObjectId(destination_id),
                    authentication_details=authentication_parameters,
                    added=is_added,
                    user_id=user_id,
                ),
                HTTPStatus.OK,
            )

        except Exception as exc:
            logging.error(
                "%s: %s. Reason:[%s: %s].",
                api_c.CANNOT_UPDATE_DESTINATIONS,
                destination_id,
                exc.__class__,
                exc,
            )
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=api_c.CANNOT_UPDATE_DESTINATIONS,
            ) from exc


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
            "schema": DestinationConstants,
            "description": "Retrieved destination constants.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve the destination constants.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    @marshal_with(DestinationConstants)
    def get(self) -> Tuple[dict, int]:
        """Retrieves all destination constants.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: dict of destination constants, HTTP status.

        """
        return api_c.DESTINATION_CONSTANTS, HTTPStatus.OK


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
                api_c.DESTINATION_TYPE: "Facebook",
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

        try:
            # test the destination connection and update connection status
            if (
                body.get(api_c.DESTINATION_TYPE)
                == db_constants.DELIVERY_PLATFORM_FACEBOOK
            ):
                destination_connector = FacebookConnector(
                    auth_details={
                        FacebookCredentials.FACEBOOK_AD_ACCOUNT_ID.name: body.get(
                            api_c.AUTHENTICATION_DETAILS
                        ).get(
                            api_c.FACEBOOK_AD_ACCOUNT_ID
                        ),
                        FacebookCredentials.FACEBOOK_APP_ID.name: body.get(
                            api_c.AUTHENTICATION_DETAILS
                        ).get(api_c.FACEBOOK_APP_ID),
                        FacebookCredentials.FACEBOOK_APP_SECRET.name: body.get(
                            api_c.AUTHENTICATION_DETAILS
                        ).get(api_c.FACEBOOK_APP_SECRET),
                        FacebookCredentials.FACEBOOK_ACCESS_TOKEN.name: body.get(
                            api_c.AUTHENTICATION_DETAILS
                        ).get(
                            api_c.FACEBOOK_ACCESS_TOKEN
                        ),
                    },
                )
            else:
                return {
                    "message": api_c.DESTINATION_NOT_SUPPORTED
                }, HTTPStatus.BAD_REQUEST
            # TODO : Add support for other connectors like SFMC
            if destination_connector.check_connection():
                return {
                    "message": api_c.DESTINATION_AUTHENTICATION_SUCCESS
                }, HTTPStatus.OK

        except Exception as exc:
            logging.error(
                "%s. Reason:[%s: %s].",
                api_c.DESTINATION_AUTHENTICATION_FAILED,
                exc.__class__,
                exc,
            )
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=api_c.DESTINATION_AUTHENTICATION_FAILED,
            ) from exc

        return {
            "message": api_c.DESTINATION_AUTHENTICATION_FAILED
        }, HTTPStatus.BAD_REQUEST
