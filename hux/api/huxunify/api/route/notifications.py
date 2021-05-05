# pylint: disable=no-self-use
"""
Paths for Notifications API
"""
from http import HTTPStatus
from typing import Tuple

import pymongo
from bson import ObjectId
from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView

from pymongo import MongoClient

from huxunify.api.schema.notifications import NotificationSchema
from huxunify.api.route.utils import add_view_to_blueprint
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunifylib.database import (
    constants as db_constants,
    notification_management,
)

NOTIFICATIONS_TAG = "notifications"
NOTIFICATIONS_DESCRIPTION = "Notifications API"
NOTIFICATIONS_ENDPOINT = "notifications"

# setup the notifications blueprint
notifications_bp = Blueprint(NOTIFICATIONS_ENDPOINT, import_name=__name__)


def get_db_client() -> MongoClient:
    """Get DB client.
    Returns:
        MongoClient: DB client
    """
    # TODO - hook-up when ORCH-94 HUS-262 are completed
    return MongoClient()


@add_view_to_blueprint(
    notifications_bp, f"/{NOTIFICATIONS_ENDPOINT}", "NotificationsSearch"
)
class NotificationsSearch(SwaggerView):
    """
    Notifications search class
    """

    # TODO how to put in Keyword url args into parameters here
    parameters = [
        {
            "name": db_constants.NOTIFICATION_QUERY_PARAMETER_PAGE_SIZE,
            "in": "query",
            "type": "integer",
            "description": "Max number of notifications to be returned.",
            "example": "5",
            "required": True,
        },
        {
            "name": db_constants.NOTIFICATION_QUERY_PARAMETER_ORDER,
            "in": "query",
            "type": "string",
            "description": "Order of the records to be returned.",
            "example": "ascending",
            "required": True,
        },
        {
            "name": db_constants.NOTIFICATION_QUERY_PARAMETER_START_ID,
            "in": "query",
            "type": "string",
            "description": "Start ID of notification to begin the next query from.",
            "example": "10",
            "required": False,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of notifications.",
            "schema": {"type": "array", "items": NotificationSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [NOTIFICATIONS_TAG]

    @marshal_with(NotificationSchema(many=True))
    def get(self) -> Tuple[dict, int]:
        """Retrieves a set of requested notifications

        ---

        Returns:
            Tuple[dict, int] dict of notifications and http code
        """

        page_size = request.args.get("page_size")
        order = request.args.get("order")
        start_id = request.args.get("start_id")

        if page_size is None or (
            order.lower() != db_constants.PAGINATION_ASCENDING
            and order.lower() != db_constants.PAGINATION_DESCENDING
        ):
            return {
                "message": "Invalid or incomplete arguments received"
            }, HTTPStatus.BAD_REQUEST

        order = (
            pymongo.ASCENDING
            if order.lower() == db_constants.PAGINATION_ASCENDING
            else pymongo.DESCENDING
        )

        if start_id is not None:
            if not ObjectId.is_valid(start_id):
                return {
                    "message": "Invalid start_id received."
                }, HTTPStatus.BAD_REQUEST

        response = notification_management.get_notifications(
            get_db_client(),
            page_size=int(page_size),
            order=order,
            start_id=start_id,
        )

        return response, HTTPStatus.OK
