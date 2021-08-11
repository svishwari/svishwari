# pylint: disable=no-self-use
"""
Paths for Notifications API
"""
from http import HTTPStatus
from typing import Tuple

import pymongo
from flask import Blueprint, request
from flasgger import SwaggerView

from huxunifylib.database import (
    constants as db_c,
    notification_management,
)
from huxunify.api.schema.notifications import NotificationsSchema
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
    api_error_handler,
)
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import AUTH401_RESPONSE

# setup the notifications blueprint
notifications_bp = Blueprint(
    api_c.NOTIFICATIONS_ENDPOINT, import_name=__name__
)


@notifications_bp.before_request
@secured()
def before_request():
    """Protect all of the notifications endpoints."""
    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    notifications_bp, f"/{api_c.NOTIFICATIONS_ENDPOINT}", "NotificationsSearch"
)
class NotificationsSearch(SwaggerView):
    """
    Notifications search class
    """

    parameters = [
        {
            "name": db_c.NOTIFICATION_QUERY_PARAMETER_BATCH_SIZE,
            "in": "query",
            "type": "integer",
            "description": "Max number of notifications to be returned.",
            "example": "5",
            "required": False,
            "default": api_c.DEFAULT_ALERT_BATCH_SIZE,
        },
        {
            "name": db_c.NOTIFICATION_QUERY_PARAMETER_SORT_ORDER,
            "in": "query",
            "type": "string",
            "description": "Sort order of the records to be returned.",
            "example": "ascending",
            "required": False,
            "default": db_c.PAGINATION_DESCENDING,
        },
        {
            "name": db_c.NOTIFICATION_QUERY_PARAMETER_BATCH_NUMBER,
            "in": "query",
            "type": "string",
            "description": "Number of which batch of notifications should be returned.",
            "example": "10",
            "required": False,
            "default": api_c.DEFAULT_ALERT_BATCH_NUMBER,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of notifications with total number of notifications.",
            "schema": NotificationsSchema,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.NOTIFICATIONS_TAG]

    @api_error_handler(
        custom_message={ValueError: {"message": api_c.INVALID_BATCH_PARAMS}}
    )
    def get(self) -> Tuple[dict, int]:
        """Retrieves notifications.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] dict of notifications and http code
        """

        batch_size = (
            request.args.get("batch_size") or api_c.DEFAULT_ALERT_BATCH_SIZE
        )
        sort_order = (
            request.args.get("sort_order") or db_c.PAGINATION_DESCENDING
        )
        batch_number = (
            request.args.get("batch_number")
            or api_c.DEFAULT_ALERT_BATCH_NUMBER
        )

        if (
            batch_size is None
            or batch_number is None
            or (
                sort_order.lower()
                not in [db_c.PAGINATION_ASCENDING, db_c.PAGINATION_DESCENDING]
            )
        ):
            return {
                "message": "Invalid or incomplete arguments received"
            }, HTTPStatus.BAD_REQUEST

        sort_order = (
            pymongo.ASCENDING
            if sort_order.lower() == db_c.PAGINATION_ASCENDING
            else pymongo.DESCENDING
        )

        return (
            NotificationsSchema().dump(
                notification_management.get_notifications(
                    get_db_client(),
                    batch_size=int(batch_size),
                    sort_order=sort_order,
                    batch_number=int(batch_number),
                )
            ),
            HTTPStatus.OK,
        )
