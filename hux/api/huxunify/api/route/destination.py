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
from flask import Blueprint, request, Response, jsonify
from flask_apispec import marshal_with
from botocore.exceptions import ClientError

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
from huxunifylib.database import (
    delivery_platform_management as destination_management,
    constants as db_constants,
    delete_util,
)


# setup the cdm blueprint
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
    def get(self, destination_id: str) -> Tuple[dict, Enum]:
        """Get a destination by destination ID and connection status.

        ---
        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[dict, Enum]: Destination dict, HTTP status.

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
                api_c.DESTINATION_NAME: "My destination platform",
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
            "description": "Failed to delete the destination.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    @marshal_with(DestinationPostSchema)
    def post(self) -> Tuple[dict, Enum]:
        """Creates a new destination and test the connection.

        ---
        Returns:
            Tuple[dict, Enum]: Destination created, HTTP status.

        """
        destinations_post = DestinationPostSchema()
        body = destinations_post.load(request.get_json())

        # create the destination
        destination_id = destination_management.set_delivery_platform(
            database=get_db_client(),
            delivery_platform_type=body[api_c.DESTINATION_TYPE],
            name=body[api_c.DESTINATION_NAME],
            authentication_details=None,
        )[db_constants.ID]

        # store the secrets in AWS parameter store
        authentication_parameters = set_destination_authentication_secrets(
            authentication_details=body[api_c.AUTHENTICATION_DETAILS],
            is_updated=False,
            destination_id=str(destination_id),
            destination_name=body[api_c.DESTINATION_NAME],
        )

        # store the secrets paths in database
        destination_management.set_authentication_details(
            database=get_db_client(),
            delivery_platform_id=destination_id,
            authentication_details=authentication_parameters,
        )

        # test the delivery platform connection and update connection status
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
    "DestinationDeleteView",
)
class DestinationDeleteView(SwaggerView):
    """
    Single Destination Delete view class
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
            "description": "Deleted destination by ID.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to delete the destination.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    @marshal_with(DestinationGetSchema)
    def delete(self, destination_id: str) -> Response:
        """Deletes a destination and its dependencies by ID.

        ---
        Args:
            destination_id (str): Destination ID.

        Returns:
             HTTPStatus: HTTP status.
        """

        try:
            # validate the id
            valid_id = (
                DestinationGetSchema()
                .load({api_c.DESTINATION_ID: destination_id}, partial=True)
                .get(api_c.DESTINATION_ID)
            )

            if delete_util.delete_delivery_platform(
                database=get_db_client(),
                delivery_platform_id=valid_id,
            ):
                return Response(status=HTTPStatus.OK)
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=api_c.CANNOT_DELETE_DESTINATIONS,
            )
        except Exception as exc:
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=api_c.CANNOT_DELETE_DESTINATIONS,
            ) from exc


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
                api_c.DESTINATION_NAME: "My Delivery platform",
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
    def put(self, destination_id: str) -> Tuple[dict, Enum]:
        """Updates an existing destination.

        ---
        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[dict, Enum]: Destination doc, HTTP status.

        """
        # load into the schema object
        body = DestinationPutSchema().load(request.get_json(), partial=True)

        # grab the auth details
        auth_details = body.get(api_c.AUTHENTICATION_DETAILS)
        authentication_parameters = None

        try:
            if auth_details:
                # store the secrets for the updated authentication details
                authentication_parameters = set_destination_authentication_secrets(
                    authentication_details=auth_details,
                    is_updated=True,
                    destination_id=destination_id,
                    destination_name=body.get(api_c.DESTINATION_NAME),
                )

                # TODO - implement when ORCH-94 and HUS-262 are ready
                #        need to sort out auth for parameter store.
                # test the destination connection and update connection status
                test_destination_connection(
                    destination_id=destination_id,
                    destination_type=body.get(api_c.DESTINATION_TYPE),
                    auth_details=auth_details,
                )

            # update the destination
            return (
                destination_management.update_delivery_platform(
                    database=get_db_client(),
                    delivery_platform_id=ObjectId(destination_id),
                    name=body.get(api_c.DESTINATION_NAME),
                    delivery_platform_type=body.get(api_c.DESTINATION_TYPE),
                    authentication_details=authentication_parameters,
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


@add_view_to_blueprint(dest_bp, f"/{api_c.DESTINATIONS_ENDPOINT}", "DestinationsView")
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
    def get(self) -> Tuple[list, Enum]:
        """Retrieves all the destinations.

        ---
        Returns:
            Tuple[list, Enum]: list of destinations, HTTP status.

        """

        return (
            destination_management.get_all_delivery_platforms(get_db_client()),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    dest_bp,
    f"/{api_c.DESTINATIONS_ENDPOINT}/bulk-delete",
    "DestinationsDeleteView",
)
class DestinationsBulkDeleteView(SwaggerView):
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
        HTTPStatus.BAD_REQUEST.value: {"description": "Failed to delete destinations."},
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    def post(self) -> Tuple[list, Enum]:
        """Bulk Deletes destinations by a list of IDs.

        ---
        Returns:
            Tuple[list, Enum]: list of deleted destination ids, HTTP status.

        """

        # validate the destination ids
        body = request.get_json()

        if not body:
            return [], HTTPStatus.BAD_REQUEST

        # load the IDs and validate using the destination schema
        destination_ids = [ObjectId(x) for x in body if ObjectId.is_valid(x)]

        # TODO - implement when ORCH-94 and HUS-262 are ready
        #        bulk delete resides in the huxadv.utils lib
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
    def get(self) -> Tuple[dict, Enum]:
        """Retrieves all destination constants.

        ---
        Returns:
            Tuple[dict, Enum]: dict of destination constants, HTTP status.

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


@add_view_to_blueprint(
    dest_bp,
    f"/{api_c.DESTINATIONS_ENDPOINT}/record-count",
    "DestinationRecordCountView",
)
class DestinationRecordCountView(SwaggerView):
    """
    Destination record count view class.
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "Total count of all destinations.",
            "schema": {"type": "integer"},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve the destination count.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DESTINATIONS_TAG]

    def get(self) -> Tuple[str, Enum]:
        """Retrieves the total record count of destinations.

        ---

        Returns:
            Tuple[str, Enum]: total count of destinations, HTTP status.

        """
        # TODO - implement when ORCH-94 and HUS-262 are ready
        #        bulk delete resides in the huxadv.utils lib
        destinations = destination_management.get_all_delivery_platforms(
            get_db_client()
        )

        return str(len(destinations) if destinations else 0), HTTPStatus.OK
