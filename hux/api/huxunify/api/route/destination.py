# pylint: disable=no-self-use
"""
Paths for destinations api
"""
from http import HTTPStatus
from typing import Tuple
from enum import Enum
from connexion.exceptions import ProblemException
from flasgger import SwaggerView
from flask import Blueprint, request, Response
from flask_apispec import marshal_with

from huxunify.api.model.destination import DestinationModel
from huxunify.api.route import utils as util
from huxunify.api.schema.destinations import (
    DestinationSchema,
    DestinationConstants,
)
from huxunify.api.schema.utils import UnAuth401Schema

from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api.route.utils import add_view_to_blueprint
import huxunify.api.constants as constants

DESTINATIONS_TAG = "destinations"
DESTINATIONS_DESCRIPTION = "Destinations API"
DESTINATIONS_ENDPOINT = "destinations"

# setup the cdm blueprint
dest_bp = Blueprint("destinations", import_name=__name__)


@add_view_to_blueprint(
    dest_bp, f"{DESTINATIONS_ENDPOINT}/<destination_id>", "DestinationView"
)
class DestinationView(SwaggerView):
    """
    Destinations view class. Ability to process a single Destination.
    """

    parameters = [
        {
            "name": "destination_id",
            "description": "ID of the destination",
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

    @marshal_with(DestinationSchema)
    def get(self, destination_id: str) -> Tuple[dict, Enum]:
        """Get a destination by destination ID.

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

        destinations_get = DestinationModel().get_destination_by_id(destination_id)
        return destinations_get, HTTPStatus.OK

    @marshal_with(DestinationSchema)
    def put(self, destination_id: str) -> Tuple[dict, Enum]:
        """Updates an existing destination

        Args:
            destination_id (str): Destination ID.

        Returns:
            Tuple[dict, Enum]: Destination doc, HTTP status.

        ---
           responses:
             200:
               description: Destination Updated
             400:
               description: failed to update the destination
        """

        destinations_put = DestinationSchema()
        body = destinations_put.load(request.get_json())

        if body.get(constants.AUTHENTICATION_DETAILS):
            # store the secrets for the updated authentication details
            authentication_parameters = (
                parameter_store.set_destination_authentication_secrets(
                    authentication_details=body[constants.AUTHENTICATION_DETAILS],
                    is_updated=True,
                    destination_id=destination_id,
                    destination_name=body[constants.DESTINATION_NAME],
                )
            )
        else:
            authentication_parameters = None

        # update the platform
        updated_destinations = DestinationModel().update_destination(
            destination_id, body, authentication_parameters
        )

        return updated_destinations, HTTPStatus.OK

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
            if DestinationModel().delete_destination_by_id(destination_id):
                return Response(status=HTTPStatus.OK)
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=f"{constants.CANNOT_DELETE_DESTINATIONS}.",
            )
        except Exception as exc:
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=f"{constants.CANNOT_DELETE_DESTINATIONS}.",
            ) from exc

    @marshal_with(DestinationSchema)
    def post(self) -> Tuple[dict, Enum]:
        """Creates a new destination and tests the connection.

        Returns:
            Tuple[dict, Enum]: Destination Created, HTTP status.

        ---
           responses:
             201:
               description: Destination Created
               schema:
                    id: DestinationSchema
        """

        destinations_post = DestinationSchema()
        body = destinations_post.load(request.get_json())

        # create the destinations
        destination_id = DestinationModel().create_destination(body)

        # test the destinations connection and update connection status
        created_destinations = util.test_destinations_connection(
            destination_id=destination_id,
            platform_type=body[constants.DESTINATION_TYPE],
            auth_details=body[constants.AUTHENTICATION_DETAILS],
        )

        return created_destinations, HTTPStatus.OK


@add_view_to_blueprint(dest_bp, f"/{DESTINATIONS_ENDPOINT}", "DestinationsView")
class DestinationsView(SwaggerView):
    """
    Destinations view class. Ability to process multiple Destinations.
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of destinations.",
            "schema": {"type": "array", "items": DestinationSchema},
        },
        HTTPStatus.UNAUTHORIZED.value: {
            "schema": UnAuth401Schema,
            "description": "Access token is missing or invalid",
        },
    }
    tags = [DESTINATIONS_TAG]

    @marshal_with(DestinationSchema(many=True))
    def get(self) -> Tuple[list, int]:
        """Retrieves all the destinations

        ---

        Returns:
            Tuple[list, int]: list of destinations, HTTP status.

        """
        all_destinations_collection = DestinationModel().get_destinations()
        return all_destinations_collection, HTTPStatus.OK


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
            "description": "Retrieved destinations related constants.",
        },
    }
    tags = [DESTINATIONS_TAG]

    @marshal_with(DestinationConstants)
    def get(self) -> Tuple[dict, int]:
        """Retrieves all destination related constants.

        ---

        Returns:
            Tuple[dict, int]: dict of destination constants, HTTP status.

        """
        return DestinationModel().get_destination_constants(), HTTPStatus.OK


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
        all_destinations_collection = DestinationModel().get_destinations()
        return all_destinations_collection, HTTPStatus.OK
