# pylint: disable=no-self-use
"""
Routes for destinations api
"""
from http import HTTPStatus
from typing import Tuple
from connexion import ProblemException
from flasgger import SwaggerView
from flask import Blueprint, request, Response
from flask_apispec import marshal_with

from hux.api.huxunify.api.model.destination import DestinationModel
from hux.api.huxunify.api import utils as util
from hux.api.huxunify.api.schema.destinations import Destination, DestinationConstants

from hux.api.huxunify.api.data_connectors.aws import parameter_store
from hux.api.huxunify.api.utils import add_view_to_blueprint
import hux.api.huxunify.api.constants as constants

DESTINATIONS_TAG = "destinations"
DESTINATIONS_DESCRIPTION = "Destinations API"
DESTINATIONS_ENDPOINT = "destinations"

api_bp = Blueprint("api", import_name=__name__)


@add_view_to_blueprint(api_bp, "destinations/<destination_id>", "Destinations")
class Destination(SwaggerView):
    """
    Destinations view class.
    """

    parameters = [
        {
            "name": "destination_id",
            "description": "destination ID",
            "type": "string",
            "in": "path",
            "required": "true",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": Destination,
            "description": "destination details.",
        },
    }
    tags = [DESTINATIONS_TAG]

    @marshal_with(Destination)
    def get(self, destination_id: str) -> Tuple[dict, int]:
        """
        Retrieves destinations properties and connection status.
        """

        destinations_get = DestinationModel().get_destination_by_id(destination_id)
        return destinations_get, HTTPStatus.OK

    @marshal_with(Destination)
    def put(self, destination_id: str) -> Tuple[dict, int]:
        """
        Updates existing destinations properties.
        ---
        """

        destinations_put = Destination()
        body = destinations_put.load(request.get_json())

        if body.get(constants.AUTHENTICATION_DETAILS):
            # store the secrets for the updated authentication details
            authentication_parameters = (
                parameter_store.set_destinations_authentication_secrets(
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
            body, authentication_parameters
        )

        return updated_destinations, HTTPStatus.OK

    def delete(self, destination_id: str) -> Response:
        """
        Deletes a destinations and its dependencies by ID.
        ---
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


@add_view_to_blueprint(api_bp, "destinations", "Destinations")
class Destinations(SwaggerView):
    """
    Destinations view class.
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of destinations.",
            "schema": {"type": "array", "items": Destination},
        },
    }
    tags = [DESTINATIONS_TAG]

    @marshal_with(Destination(many=True))
    def get(self) -> Tuple[list, int]:
        """
        Retrieves all destinations.
        """
        all_destinations_collection = DestinationModel().get_destinations()
        return all_destinations_collection, HTTPStatus.OK

    @marshal_with(Destination)
    def post(self) -> Tuple[dict, int]:
        """
        Creates a new destinations.
        ---
        """

        destinations_post = Destination()
        body = destinations_post.load(request.get_json())

        # create the destinations
        destinations_id = DestinationModel().create_destination(body)

        # test the destinations connection and update connection status
        created_destinations = util.test_destinations_connection(
            destinations_id=destinations_id,
            platform_type=body[constants.DESTINATION_TYPE],
            auth_details=body[constants.AUTHENTICATION_DETAILS],
        )

        return created_destinations, HTTPStatus.OK


@add_view_to_blueprint(api_bp, "destinations/constants", "DestinationsConstants")
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
        """Retrieves all destinations related constants."""

        return DestinationModel().get_destination_constants(), HTTPStatus.OK
