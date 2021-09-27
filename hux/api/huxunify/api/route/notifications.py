# pylint: disable=no-self-use
"""
Paths for Notifications API
"""
import json
from http import HTTPStatus
from typing import Tuple, Generator
from time import sleep
from datetime import datetime, timedelta, timezone

import pymongo
from flask import Blueprint, request, Response
from flasgger import SwaggerView

from huxunifylib.util.general.logging import logger
from huxunifylib.database import (
    constants as db_c,
    notification_management,
)
from huxunify.api.schema.notifications import NotificationsSchema
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
)
from huxunify.api.route.utils import (
    get_db_client,
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
            "default": api_c.DEFAULT_BATCH_SIZE,
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
            "default": api_c.DEFAULT_BATCH_NUMBER,
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

        batch_size = request.args.get(
            api_c.QUERY_PARAMETER_BATCH_SIZE, api_c.DEFAULT_BATCH_SIZE
        )
        sort_order = request.args.get(
            api_c.QUERY_PARAMETER_SORT_ORDER, db_c.PAGINATION_DESCENDING
        )
        batch_number = request.args.get(
            api_c.QUERY_PARAMETER_BATCH_NUMBER, api_c.DEFAULT_BATCH_NUMBER
        )

        if (
            batch_size is None
            or batch_number is None
            or (
                sort_order.lower()
                not in [db_c.PAGINATION_ASCENDING, db_c.PAGINATION_DESCENDING]
            )
        ):
            logger.error("Invalid or incomplete arguments received.")
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
                notification_management.get_notifications_batch(
                    get_db_client(),
                    batch_size=int(batch_size),
                    sort_order=sort_order,
                    batch_number=int(batch_number),
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    notifications_bp,
    f"/{api_c.NOTIFICATIONS_ENDPOINT}/stream",
    "NotificationStream",
)
class NotificationStream(SwaggerView):
    """Notifications stream class"""

    parameters = []
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of notifications with total number of notifications.",
            "schema": NotificationsSchema,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.NOTIFICATIONS_TAG]

    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Stream notifications.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int] dict of notifications and http code
        """

        def event_stream() -> Generator[Tuple[dict, int], None, None]:
            """Stream notifications with a generator.

            Returns:
                Generator[Tuple[dict, int], None, None]: Generator of notifications.

            """
            i = 0
            while True:
                # sleep each iteration, don't sleep first iteration
                sleep(0 if i == 0 else api_c.NOTIFICATION_STREAM_TIME_SECONDS)

                # increase iteration
                i += 1

                # get the previous time, take last minute.
                previous_time = datetime.utcnow().replace(
                    tzinfo=timezone.utc
                ) - timedelta(
                    minutes=int(api_c.NOTIFICATION_STREAM_TIME_SECONDS / 60)
                )

                # dump the output notification list to the notification schema.
                yield json.dumps(
                    NotificationsSchema().dump(
                        notification_management.get_notifications(
                            get_db_client(),
                            {
                                db_c.NOTIFICATION_FIELD_CREATED: {
                                    "$gt": previous_time
                                },
                                db_c.TYPE: db_c.NOTIFICATION_TYPE_SUCCESS,
                                db_c.NOTIFICATION_FIELD_DESCRIPTION: {
                                    "$regex": "^Successfully delivered audience"
                                },
                            },
                            [(db_c.NOTIFICATION_FIELD_CREATED, -1)],
                        )
                    )
                )

        # return the event stream, which returns Tuple[dict, int].
        return Response(event_stream(), mimetype="text/event-stream")
