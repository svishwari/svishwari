# pylint: disable=no-self-use
"""
Paths for Notifications API
"""
from http import HTTPStatus
from typing import Tuple

import pymongo
from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView

from huxunifylib.database import (
    constants as db_constants,
    notification_management,
)
from huxunify.api.schema.notifications import NotificationSchema
from huxunify.api.route.utils import add_view_to_blueprint, get_db_client
from huxunify.api.schema.utils import AUTH401_RESPONSE

NOTIFICATIONS_TAG = "notifications"
NOTIFICATIONS_DESCRIPTION = "Notifications API"
NOTIFICATIONS_ENDPOINT = "notifications"

# setup the notifications blueprint
notifications_bp = Blueprint(NOTIFICATIONS_ENDPOINT, import_name=__name__)


@add_view_to_blueprint(
    notifications_bp, f"/{NOTIFICATIONS_ENDPOINT}", "NotificationsSearch"
)
class NotificationsSearch(SwaggerView):
    """
    Notifications search class
    """

    parameters = [
        {
            "name": db_constants.NOTIFICATION_QUERY_PARAMETER_BATCH_SIZE,
            "in": "query",
            "type": "integer",
            "description": "Max number of notifications to be returned.",
            "example": "5",
            "required": True,
        },
        {
            "name": db_constants.NOTIFICATION_QUERY_PARAMETER_SORT_ORDER,
            "in": "query",
            "type": "string",
            "description": "Sort order of the records to be returned.",
            "example": "ascending",
            "required": True,
        },
        {
            "name": db_constants.NOTIFICATION_QUERY_PARAMETER_BATCH_NUMBER,
            "in": "query",
            "type": "string",
            "description": "Number of which batch of notifications should be returned.",
            "example": "10",
            "required": True,
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
        """Retrieves notifications.

        ---

        Returns:
            Tuple[dict, int] dict of notifications and http code
        """

        batch_size = request.args.get("batch_size")
        sort_order = request.args.get("sort_order")
        batch_number = request.args.get("batch_number")

        if (
            batch_size is None
            or batch_number is None
            or (
                sort_order.lower() != db_constants.PAGINATION_ASCENDING
                and sort_order.lower() != db_constants.PAGINATION_DESCENDING
            )
        ):
            return {
                "message": "Invalid or incomplete arguments received"
            }, HTTPStatus.BAD_REQUEST

        sort_order = (
            pymongo.ASCENDING
            if sort_order.lower() == db_constants.PAGINATION_ASCENDING
            else pymongo.DESCENDING
        )

        response = notification_management.get_notifications(
            get_db_client(),
            batch_size=int(batch_size),
            sort_order=sort_order,
            batch_number=int(batch_number),
        )

        return response, HTTPStatus.OK
