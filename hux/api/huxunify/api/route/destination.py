# pylint: disable=no-self-use
"""
Paths for destinations api
"""
import logging
from http import HTTPStatus
from typing import Tuple
from mongomock import MongoClient
from connexion.exceptions import ProblemException
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_apispec import marshal_with

from huxunifylib.database import (
    delivery_platform_management as destination_management,
    constants as db_constants,
    delete_util,
)
from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api.schema.destinations import (
    DestinationGetSchema,
    DestinationPutSchema,
    DestinationPostSchema,
    DestinationConstants,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.route.utils import add_view_to_blueprint
import huxunify.api.constants as api_c


# setup the destination blueprint
dest_bp = Blueprint(api_c.DESTINATIONS_ENDPOINT, import_name=__name__)


def get_db_client() -> MongoClient:
    """Get DB client.

    Returns:
        MongoClient: DB client
    """
    # TODO - hook-up when ORCH-94 HUS-262 are completed
    return MongoClient()


# pylint: disable=unused-argument,
def test_destination_connection(
    destination_id: str, destination_type: str, auth_details: dict
) -> dict:
    """Test the connection to the destination and update the
    connection status.

    Args:
        destination_id (str): The destination ID.
        destination_type (str): The destination type.
        auth_details (dict): The auth details dict.
    Returns:
        updated_destination (dict): The updated destination.
    """

    # TODO - hook-up when ORCH-94 HUS-262 are completed
    status = True
    # dp_connector = get_connector(
    #     destination_type=destination_type,
    #     auth_details_secrets=auth_details,
    # )
    # status = dp_connector.check_connection()

    return destination_management.set_connection_status(
        database=get_db_client(),
        delivery_platform_id=ObjectId(destination_id),
        connection_status=db_constants.STATUS_SUCCEEDED
        if status
        else db_constants.STATUS_FAILED,
    )


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

        # validate the id
        valid_id = (
            DestinationGetSchema()
            .load({api_c.DESTINATION_ID: destination_id}, partial=True)
            .get(api_c.DESTINATION_ID)
        )

        # return a bad request if invalid objectID
        if not valid_id:
            return f"Invalid ID {destination_id}.", HTTPStatus.BAD_REQUEST

        # grab the destination
        destination = destination_management.get_delivery_platform(
            get_db_client(), valid_id
        )
        return destination, HTTPStatus.OK


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

    @marshal_with(DestinationPostSchema)
    def post(self) -> Tuple[dict, int]:
        """Creates a new destination and tests the connection.

        ---
        Returns:
            Tuple[dict, int]: Destination created, HTTP status.

        """
        # TODO - implement after HUS-254 is done to grab user/okta_id
        user_id = ObjectId()

        destinations_post = DestinationPostSchema()
        body = destinations_post.load(request.get_json())

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

        # test the destination connection and update connection status
        return (
            test_destination_connection(
                destination_id=destination_id,
                destination_type=body[api_c.DESTINATION_TYPE],
                auth_details=body[api_c.AUTHENTICATION_DETAILS],
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
        body = DestinationPutSchema().load(request.get_json(), partial=True)

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

                # TODO - implement when ORCH-94 and HUS-262 are ready
                #        need to sort out auth for parameter store.
                # test the destination connection and update connection status
                test_destination_connection(
                    destination_id=destination_id,
                    destination_type=body.get(api_c.DESTINATION_TYPE),
                    auth_details=auth_details,
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
    dest_bp, f"/{api_c.DESTINATIONS_ENDPOINT}", "DestinationsView"
)
class DestinationsView(SwaggerView):
    """
    Multiple Destinations view class
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of destinations.",
            "schema": {"type": "array", "items": DestinationGetSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get all destinations."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    @marshal_with(DestinationGetSchema(many=True))
    def get(self) -> Tuple[list, int]:
        """Retrieves all the destinations.

        ---
        Returns:
            Tuple[list, int]: list of destinations, HTTP status.

        """

        return (
            destination_management.get_all_delivery_platforms(get_db_client()),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"/{api_c.DESTINATIONS_ENDPOINT}/delete",
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

        auth_details = {
            db_constants.DELIVERY_PLATFORM_FACEBOOK: {
                api_c.FACEBOOK_AD_ACCOUNT_ID: "Ad Account ID",
                api_c.FACEBOOK_APP_ID: "Facebook App ID",
                api_c.FACEBOOK_APP_SECRET: "App Secret",
                api_c.FACEBOOK_ACCESS_TOKEN: "Access Token",
            },
            db_constants.DELIVERY_PLATFORM_SFMC: {
                api_c.SFMC_CLIENT_ID: "Client ID",
                api_c.SFMC_ACCOUNT_ID: "Account ID",
                api_c.SFMC_CLIENT_SECRET: "Client Secret",
                api_c.SFMC_AUTH_BASE_URI: "Auth Base URI",
                api_c.SFMC_REST_BASE_URI: "REST Base URI",
                api_c.SFMC_SOAP_BASE_URI: "SOAP Base URI",
            },
        }

        return auth_details, HTTPStatus.OK
