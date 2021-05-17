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
    delete_util,
)
from huxunifylib.connectors.facebook_connector import FacebookConnector
from huxunifylib.util.general.const import FacebookCredentials
from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api.schema.destinations import (
    DestinationGetSchema,
    DestinationPutSchema,
    DestinationPostSchema,
    DestinationConstants,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.route.utils import add_view_to_blueprint, get_db_client
import huxunify.api.constants as api_c


# setup the destination blueprint
dest_bp = Blueprint(api_c.DESTINATIONS_ENDPOINT, import_name=__name__)


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

    @marshal_with(DestinationGetSchema)
    def get(self, destination_id: str) -> Tuple[dict, int]:
        """Get a destination by destination ID.

        ---
        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[dict, int]: Destination dict, HTTP status.

        """

        try:
            # validate the id
            valid_id = (
                DestinationGetSchema()
                .load({api_c.DESTINATION_ID: destination_id}, partial=True)
                .get(api_c.DESTINATION_ID)
            )
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        # grab the destination
        destination = destination_management.get_delivery_platform(
            get_db_client(), valid_id
        )
        return destination, HTTPStatus.OK


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

    @marshal_with(DestinationGetSchema(many=True))
    def get(self) -> Tuple[list, int]:  # pylint: disable=no-self-use
        """Retrieves all destinations.

        ---
        Returns:
            Tuple[list, int]: list of destinations, HTTP status.

        """

        destinations = destination_management.get_all_delivery_platforms(
            get_db_client()
        )

        return (
            destinations,
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"{api_c.DESTINATIONS_ENDPOINT}",
    "DestinationPostView",
)
class DestinationPostView(SwaggerView):
    """
    Single Destination Post view class
    """

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input destination body.",
            "example": {
                api_c.DESTINATION_NAME: "My destination",
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
        HTTPStatus.CREATED.value: {
            "schema": DestinationGetSchema,
            "description": "Destination created.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create the destination.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    def post(self) -> Tuple[dict, int]:
        """Creates a new destination and tests the connection.

        ---
        Returns:
            Tuple[dict, int]: Destination created, HTTP status.

        """
        # TODO - implement after HUS-254 is done to grab user/okta_id
        user_id = ObjectId()

        try:
            body = DestinationPostSchema().load(request.get_json())
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        destination_id = destination_management.set_delivery_platform(
            database=get_db_client(),
            delivery_platform_type=body[api_c.DESTINATION_TYPE],
            name=body[api_c.DESTINATION_NAME],
            authentication_details=None,
            user_id=user_id,
        )[db_constants.ID]

        # store the secrets in AWS parameter store
        authentication_parameters = (
            parameter_store.set_destination_authentication_secrets(
                authentication_details=body[api_c.AUTHENTICATION_DETAILS],
                is_updated=False,
                destination_id=str(destination_id),
                destination_name=body[api_c.DESTINATION_NAME],
            )
        )

        # store the secrets paths in database
        destination_management.set_authentication_details(
            database=get_db_client(),
            delivery_platform_id=destination_id,
            authentication_details=authentication_parameters,
        )

        # A destination can only be created if the authentication is validated.
        # So update the connection status to SUCCESS.
        return (
            destination_management.set_connection_status(
                database=get_db_client(),
                delivery_platform_id=ObjectId(destination_id),
                connection_status=db_constants.STATUS_SUCCEEDED,
            ),
            HTTPStatus.CREATED,
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
                api_c.DESTINATION_NAME: "My destination",
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
        """Updates an existing destination.

        ---
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
                        destination_name=body.get(api_c.DESTINATION_NAME),
                    )
                )

            # TODO - provide input user-id to delivery platform
            #       create the destination after the PR 171 is merged
            # update the destination
            return (
                destination_management.update_delivery_platform(
                    database=get_db_client(),
                    delivery_platform_id=ObjectId(destination_id),
                    name=body.get(api_c.DESTINATION_NAME),
                    delivery_platform_type=body.get(api_c.DESTINATION_TYPE),
                    authentication_details=authentication_parameters,
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
    api_c.DESTINATIONS_ENDPOINT,
    "DestinationsDeleteView",
)
class DestinationsDeleteView(SwaggerView):
    """
    DestinationsDeleteView view class
    Delete multiple destinations at once.
    """

    parameters = [
        {
            "in": "body",
            "name": "destination_ids",
            "description": "List of destination IDs to be deleted.",
            "schema": {
                "type": "array",
                "items": {"type": "string"},
                "example": [
                    "603e112b53594f0228bd79ef",
                    "603e112c53594f0228bd79f5",
                ],
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Deleted destinations.",
            "schema": {
                "type": "array",
                "items": {"type": "string"},
                "example": [
                    "603e112b53594f0228bd79ef",
                    "603e112c53594f0228bd79f5",
                ],
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to delete destinations."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    def delete(self) -> Tuple[list, int]:
        """Delete destination by a list of ID(s).
        Ability to delete one or multiple.

        ---
        Returns:
            Tuple[list, int]: list of deleted destination ids, HTTP status.

        """

        # validate the destination ids
        body = request.get_json()

        if not body:
            return [], HTTPStatus.BAD_REQUEST

        # load the IDs and validate using the destination schema
        destination_ids = [ObjectId(x) for x in body if ObjectId.is_valid(x)]

        try:
            if delete_util.delete_delivery_platforms_bulk(
                database=get_db_client(), delivery_platform_ids=destination_ids
            ):
                # return list of string IDs
                return (
                    jsonify([str(x) for x in destination_ids]),
                    HTTPStatus.OK,
                )
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=api_c.CANNOT_DELETE_DESTINATIONS,
            )
        except Exception as exc:
            logging.error(
                "%s: %s. Reason:[%s: %s].",
                api_c.CANNOT_DELETE_DESTINATIONS,
                destination_ids,
                exc.__class__,
                exc,
            )
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=api_c.CANNOT_DELETE_DESTINATIONS,
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
        """Authenticates the destination with given credentials.

        ---
        Returns:
            Tuple[dict, int]: Message indicating connection
                            success/failure, HTTP Status.

        """

        try:
            body = DestinationPostSchema().load(request.get_json())
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
