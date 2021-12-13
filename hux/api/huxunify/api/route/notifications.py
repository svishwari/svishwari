# pylint: disable=no-self-use
"""Paths for Notifications API"""
import json
from http import HTTPStatus
from typing import Tuple, Generator
from time import sleep
from datetime import datetime, timedelta, timezone

import pymongo
from bson import ObjectId
from flask import Blueprint, request, Response
from flasgger import SwaggerView

from huxunifylib.util.general.logging import logger
from huxunifylib.database import (
    constants as db_c,
    notification_management,
)
from huxunify.api.schema.notifications import (
    NotificationsSchema,
    NotificationSchema,
)
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    get_user_name, requires_access_levels,
)
from huxunify.api.route.utils import get_db_client, Validation
from huxunify.api import constants as api_c
from huxunify.api.schema.errors import NotFoundError
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
    """Notifications search class."""

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
            "type": "integer",
            "description": "Number of which batch of notifications should be returned.",
            "example": "10",
            "required": False,
            "default": api_c.DEFAULT_BATCH_NUMBER,
        },
        {
            "name": api_c.QUERY_PARAMETER_NOTIFICATION_TYPES,
            "in": "query",
            "type": "string",
            "description": "Type of Notification",
            "example": "Success,Informational",
            "required": False,
        },
        {
            "name": api_c.QUERY_PARAMETER_NOTIFICATION_CATEGORY,
            "in": "query",
            "type": "string",
            "description": "Type of Notification Category",
            "example": "Delivery,Engagements",
            "required": False,
        },
        {
            "name": api_c.QUERY_PARAMETER_USERS,
            "in": "query",
            "type": "string",
            "description": "Users Filter",
            "example": "Unified-Dev Test-User",
            "required": False,
        },
        {
            "name": api_c.START_DATE,
            "in": "query",
            "type": "string",
            "description": "Start Date",
            "example": "2021-04-10",
            "required": False,
        },
        {
            "name": api_c.END_DATE,
            "in": "query",
            "type": "string",
            "description": "End Date",
            "example": "2021-04-10",
            "required": False,
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves notifications.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int] dict of notifications, HTTP status code.
        """
        batch_size = Validation.validate_integer(
            request.args.get(
                api_c.QUERY_PARAMETER_BATCH_SIZE, str(api_c.DEFAULT_BATCH_SIZE)
            )
        )

        sort_order = request.args.get(
            api_c.QUERY_PARAMETER_SORT_ORDER, db_c.PAGINATION_DESCENDING
        )

        batch_number = Validation.validate_integer(
            request.args.get(
                api_c.QUERY_PARAMETER_BATCH_NUMBER,
                str(api_c.DEFAULT_BATCH_NUMBER),
            )
        )

        notification_types = request.args.get(
            api_c.QUERY_PARAMETER_NOTIFICATION_TYPES, []
        )
        notification_types = (
            [x.lower() for x in notification_types.split(",")]
            if notification_types
            else []
        )

        if notification_types and not set(notification_types).issubset(
            set(db_c.NOTIFICATION_TYPES)
        ):
            logger.error("Invalid Notification Type")
            return {
                "message": "Invalid or incomplete arguments received"
            }, HTTPStatus.BAD_REQUEST

        notification_categories = request.args.get(
            api_c.QUERY_PARAMETER_NOTIFICATION_CATEGORY, []
        )
        notification_categories = (
            [x.lower() for x in notification_categories.split(",")]
            if notification_categories
            else []
        )

        if notification_categories and not set(
            notification_categories
        ).issubset(set(api_c.NOTIFICATION_CATEGORIES)):
            logger.error("Invalid Notification Category")
            return {
                "message": "Invalid or incomplete arguments received"
            }, HTTPStatus.BAD_REQUEST

        users = request.args.get(api_c.QUERY_PARAMETER_USERS, [])
        if users:
            users = users.split(",")

        start_date = request.args.get(api_c.START_DATE, "")
        end_date = request.args.get(api_c.END_DATE, "")
        if start_date and end_date:
            Validation.validate_date_range(start_date, end_date)
            start_date = Validation.validate_date(start_date)
            end_date = Validation.validate_date(end_date)
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
                    batch_size=batch_size,
                    sort_order=sort_order,
                    batch_number=batch_number,
                    notification_types=notification_types,
                    notification_categories=notification_categories,
                    users=users,
                    start_date=start_date,
                    end_date=end_date,
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
            Tuple[dict, int]: dict of notifications, HTTP status code.
        """

        def event_stream() -> Generator[Tuple[dict, int], None, None]:
            """Stream notifications with a generator.

            Yields:
                Generator[Tuple[dict, int], None, None]: Generator of
                    notifications.
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

        # return the event stream response
        return Response(event_stream(), mimetype="text/event-stream")


@add_view_to_blueprint(
    notifications_bp,
    f"/{api_c.NOTIFICATIONS_ENDPOINT}/<{api_c.NOTIFICATION_ID}>",
    "NotificationSearch",
)
class NotificationSearch(SwaggerView):
    """Notification search class."""

    parameters = [
        {
            "name": api_c.NOTIFICATION_ID,
            "in": "path",
            "type": "string",
            "description": "ObjectId of Notification",
            "example": "614e14bdcc267d93d62f44f4",
            "required": True,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Notification Details",
            "schema": NotificationSchema,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.NOTIFICATIONS_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, notification_id: str, user: dict) -> Tuple[dict, int]:
        """Retrieves notification.
        ---
        security:
            - Bearer: ["Authorization"]
        Args:
            notification_id (str): Notification Id
            user (dict): user object.
        Returns:
            Tuple[dict, int] dict of notifications, HTTP status code.
        """
        notification_id = ObjectId(notification_id)
        notification = notification_management.get_notification(
            get_db_client(), notification_id
        )

        if not notification:
            logger.error(
                "Could not find notification with id %s.",
                notification_id,
            )
            return {
                "message": api_c.NOTIFICATION_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        return (
            NotificationSchema().dump(notification),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    notifications_bp,
    f"{api_c.NOTIFICATIONS_ENDPOINT}/<notification_id>",
    "DeleteNotification",
)
class DeleteNotification(SwaggerView):
    """Notification Delete Class."""

    parameters = [
        {
            "name": api_c.NOTIFICATION_ID,
            "description": "Notification ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.NO_CONTENT.value: {
            "description": "Deleted Notification.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to delete the notification.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.NOTIFICATIONS_TAG]

    @api_error_handler()
    @requires_access_levels([api_c.ADMIN_LEVEL])
    def delete(
        self, notification_id: ObjectId, user: dict
    ) -> Tuple[dict, int]:
        """Deletes a notification by ID.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            notification_id (ObjectId): Notification ID.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: message, HTTP status code.
        """

        if notification_management.delete_notification(
            get_db_client(), ObjectId(notification_id)
        ):
            logger.info(
                "Successfully deleted notification %s by user %s.",
                notification_id,
                user[api_c.USER_NAME],
            )

            return {}, HTTPStatus.NO_CONTENT

        logger.info(
            "Could not delete notification with ID %s.", notification_id
        )
        return {api_c.MESSAGE: api_c.OPERATION_FAILED}, HTTPStatus.BAD_REQUEST
