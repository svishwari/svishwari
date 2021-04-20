# pylint: disable=no-self-use
"""
Paths for destinations api
"""
import logging
from http import HTTPStatus
from typing import Tuple
from enum import Enum
from mongomock import MongoClient
from connexion.exceptions import ProblemException
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, request, Response
from flask_apispec import marshal_with
from botocore.exceptions import ClientError

from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api.model.destination import DestinationModel
from huxunify.api.schema.destinations import (
    DestinationGetSchema,
    DestinationPutSchema,
    DestinationPostSchema,
    DestinationConstants,
)
from huxunify.api.schema.utils import UnAuth401Schema


from huxunify.api.route.utils import add_view_to_blueprint
import huxunify.api.constants as api_c
from huxunifylib.database import (
    delivery_platform_management as destination_management,
    constants as db_constants,
)

DESTINATIONS_TAG = "destinations"
DESTINATIONS_DESCRIPTION = "Destinations API"
DESTINATIONS_ENDPOINT = "destinations"

# setup the cdm blueprint
dest_bp = Blueprint("destinations", import_name=__name__)


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
):
    """Test the connection to the destination and update the
    connection status.
    Args:
        destination_id (str): The destination ID.
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


def set_destination_authentication_secrets(
    authentication_details: dict,
    is_updated: bool,
    destination_id: str,
    destination_name: str,
) -> dict:
    """Save authentication details in AWS Parameter Store.
    Args:
        authentication_details (dict): The key/secret pair to store away.
        is_updated (bool): Flag to update the secrets in the AWS Parameter Store.
        destination_id (str): Destination ID.
        destination_name (str): Destination name.
    Returns:
        ssm_params (dict): The key/path to where the parameters are stored.
    """
    ssm_params = {}
    # TODO - clarify the secret store with adperf team
    path = f"/adperf/{destination_id}"

    for parameter_name, secret in authentication_details.items():
        ssm_params[parameter_name] = (
            path + "/" + parameter_name if path else parameter_name
        )
        try:
            parameter_store.store_secret(
                name=parameter_name,
                secret=secret,
                overwrite=is_updated,
                path=path,
            )
        except ClientError as exc:
            logging.error("%s: %s", exc.__class__, exc)
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=f"There was a problem saving your authentication details for"
                f" Destination: '{destination_name}'. Details:"
                f" {api_c.CANNOT_STORE_SECRETS_PARAMETER_STORE}",
            ) from exc

    return ssm_params


@add_view_to_blueprint(
    dest_bp, f"{DESTINATIONS_ENDPOINT}/<destination_id>", "DestinationView"
)
class DestinationView(SwaggerView):
    """
    Single Destination view class
    """

    parameters = [
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.UNAUTHORIZED.value: {
            "schema": UnAuth401Schema,
            "description": "Access token is missing or invalid",
        },
    }
    tags = [DESTINATIONS_TAG]

    @marshal_with(DestinationGetSchema)
    def get(self, destination_id: str) -> Tuple[dict, int]:
        """Get a destination by destination ID and connection status

        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[dict, Enum]: Destination dict, HTTP status.

        ---
        responses:
          200:
            description: Retrieved destination details.
            schema:
              id: DestinationSchema
          400:
             description: failed to retrieve the destination
             schema: Null
        """
        destination = destination_management.get_delivery_platform(
            get_db_client(), ObjectId(destination_id)
        )
        return destination, HTTPStatus.OK

    @marshal_with(DestinationPutSchema)
    def put(self, destination_id: str) -> Tuple[dict, Enum]:
        """Updates an existing destination

        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[dict, Enum]: Destination doc, HTTP status.

        ---
        parameters: [
            {
                name: body,
                in: body,
                required: true,
                schema: {
                    id: DestinationPutSchema,
                    "required": "true",
                    "example": {
                        "destination_name": "My Destination,
                        "destination_type": "Facebook",
                        "authentication_details": {
                            "access_token": "MkU!3Ojgwm",
                            "app_secret": "717bdOQqZO99",
                            "app_id": "2951925002021888",
                            "ad_account_id": "111333777",
                        },
                    },
                },
            },
        ]
        responses:
             200:
               description: Destination updated
             400:
               description: failed to update the destination
        """
        # TODO - handle serialization
        destinations_put = DestinationPutSchema()
        body = destinations_put.load(request.get_json())

        if body.get(api_c.AUTHENTICATION_DETAILS):
            # store the secrets for the updated authentication details
            authentication_parameters = set_destination_authentication_secrets(
                authentication_details=body[api_c.AUTHENTICATION_DETAILS],
                is_updated=True,
                destination_id=destination_id,
                destination_name=body[db_constants.DELIVERY_PLATFORM_NAME],
            )

            # test the destination connection and update connection status
            test_destination_connection(
                destination_id=destination_id,
                destination_type=body[db_constants.DELIVERY_PLATFORM_TYPE],
                auth_details=body[api_c.AUTHENTICATION_DETAILS],
            )
        else:
            authentication_parameters = None

        # update the destination
        updated_destination = destination_management.update_delivery_platform(
            database=get_db_client(),
            delivery_platform_id=ObjectId(destination_id),
            name=body[db_constants.DELIVERY_PLATFORM_NAME],
            delivery_platform_type=body[db_constants.DELIVERY_PLATFORM_TYPE],
            authentication_details=authentication_parameters,
        )

        return updated_destination, HTTPStatus.OK

    def delete(self, destination_id: str) -> Response:
        """Deletes a destination and its dependencies by ID.

        Args:
            destination_id (str): Destination ID.

        Returns:
             HTTPStatus: HTTP status.
        ---
           responses:
             200:
               description: Deleted destination by ID
               schema: Null
             400:
               description: failed to delete the destination
               schema: Null
        """

        try:
            # TODO - handle serialization
            if DestinationModel().delete_destination_by_id(destination_id):
                return Response(status=HTTPStatus.OK)
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=f"{api_c.CANNOT_DELETE_DESTINATIONS}.",
            )
        except Exception as exc:
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=f"{api_c.CANNOT_DELETE_DESTINATIONS}.",
            ) from exc

    @marshal_with(DestinationPostSchema)
    def post(self) -> Tuple[dict, Enum]:
        """Creates a new destination and test the connection.

        Returns:
            Tuple[dict, Enum]: Destination created, HTTP status.

        ---
        parameters: [
            {
                name: "body",
                in: "body",
                required: true,
                schema: {
                    id: DestinationPostSchema,
                    required: true,
                    example: {
                        "destination_name": "My Destination",
                        "destination_type": "Facebook",
                        "authentication_details": {
                            "access_token": "MkU!3Ojgwm",
                            "app_secret": "717bdOQqZO99",
                            "app_id": "2951925002021888",
                            "ad_account_id": "111333777",
                        },
                    },
                },
            },
        ]
        responses:
            201:
                description: Destination created
                schema:
                    id: DestinationSchema
        """
        # TODO - handle serialization
        destinations_post = DestinationPostSchema()
        body = destinations_post.load(request.get_json())

        # create the destinations
        destination_id = DestinationModel().create_destination(body)

        # test the destination connection and update connection status
        created_destinations = test_destination_connection(
            destination_id=destination_id,
            destination_type=body[api_c.DESTINATION_TYPE],
            auth_details=body[api_c.AUTHENTICATION_DETAILS],
        )

        return created_destinations, HTTPStatus.OK


@add_view_to_blueprint(dest_bp, f"/{DESTINATIONS_ENDPOINT}", "DestinationsView")
class DestinationsView(SwaggerView):
    """
    Multiple Destinations view class.
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of destinations.",
            "schema": {"type": "array", "items": DestinationGetSchema},
        },
        HTTPStatus.UNAUTHORIZED.value: {
            "schema": UnAuth401Schema,
            "description": "Access token is missing or invalid",
        },
    }
    tags = [DESTINATIONS_TAG]

    @marshal_with(DestinationGetSchema(many=True))
    def get(self) -> Tuple[list, int]:
        """Retrieves all the destinations

        ---

        Returns:
            Tuple[list, int]: list of destinations, HTTP status.

        """

        all_destinations = destination_management.get_all_delivery_platforms(
            get_db_client()
        )

        return all_destinations, HTTPStatus.OK


@add_view_to_blueprint(
    dest_bp, f"/{DESTINATIONS_ENDPOINT}/bulk-delete", "DestinationsDeleteView"
)
class DestinationsDeleteView(SwaggerView):
    """
    DestinationsDeleteView view class.
    delete multiple destinations at once
    """

    parameters = [
        {
            "type": "array",
            "in": "body",
            "description": "List of destination IDs to be deleted.",
            "required": "true",
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
        HTTPStatus.BAD_REQUEST.value: {"description": "Failed to delete destinations."},
        HTTPStatus.UNAUTHORIZED.value: {
            "schema": UnAuth401Schema,
            "description": "Access token is missing or invalid",
        },
    }
    tags = [DESTINATIONS_TAG]

    def post(self) -> Tuple[list, int]:
        """Bulk Deletes destinations by a list of IDs.

        ---

        Returns:
            Tuple[list, int]: list of deleted destination ids, HTTP status.

        """
        # TODO - handle serialization
        destination_ids = request.get_json()
        mongo_ids = [
            ObjectId(destination_id)
            for destination_id in destination_ids
            if destination_ids
        ]

        # TODO - implement when ORCH-94 and HUS-262 are ready
        #   bulk delete resides in the huxadv.utils lib
        return mongo_ids, HTTPStatus.OK


@add_view_to_blueprint(
    dest_bp, f"{DESTINATIONS_ENDPOINT}/constants", "DestinationsConstants"
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
    }
    tags = [DESTINATIONS_TAG]

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


# get record count
@add_view_to_blueprint(
    dest_bp,
    f"/{DESTINATIONS_ENDPOINT}/record-count",
    "DestinationRecordCountView",
)
class DestinationRecordCountView(SwaggerView):
    """
    Destination record count view class.
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "Total count of all destinations",
            "schema": {"type": "integer"},
        },
    }
    tags = [DESTINATIONS_TAG]

    def get(self) -> Tuple[int, Enum]:
        """Retrieves the total record count of destinations

        ---

        Returns:
            Tuple[int, Enum]: total count of destinations, HTTP status.

        """
        all_destinations = destination_management.get_all_delivery_platforms(
            get_db_client()
        )

        return all_destinations, HTTPStatus.OK
