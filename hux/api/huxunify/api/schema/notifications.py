"""Schemas for the notifications API"""

from flask_marshmallow import Schema
from marshmallow import post_dump
from marshmallow.fields import Str, Int, List, Nested
from marshmallow.validate import OneOf

from huxunifylib.database import constants as db_c

from huxunify.api import constants as api_c
from huxunify.api.schema.custom_schemas import DateTimeWithZ


class NotificationSchema(Schema):
    """Notifications Schema"""

    id = Str(attribute=db_c.ID, example="60e5c7be3b080a75959d6282")
    notification_type = Str(
        attribute="type",
        validate=[OneOf(choices=db_c.NOTIFICATION_TYPES)],
        required=True,
        example=db_c.NOTIFICATION_TYPE_CRITICAL.title(),
    )
    description = Str(
        attribute="description",
        required=True,
        example="Facebook Delivery Stopped",
    )
    created = DateTimeWithZ(
        attribute="created",
        required=True,
        allow_none=False,
    )
    category = Str(
        attribute="category",
        validate=[OneOf(choices=db_c.NOTIFICATION_CATEGORIES)],
        required=True,
        example=db_c.NOTIFICATION_CATEGORY_DELIVERY.title(),
    )
    username = Str(
        attribute="username",
        required=True,
        example="Username",
        allow_none=False,
    )

    @post_dump
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def post_serialize(self, data: dict, many: bool = False) -> dict:
        """process the schema before serializing.

        Args:
            data (dict): The notification object
            many (bool): If there are many to process

        Returns:
            dict: Returns a notification object

        """
        # change notification type and category to title case
        if data.get(db_c.NOTIFICATION_FIELD_CATEGORY):
            data[db_c.NOTIFICATION_FIELD_CATEGORY] = data[
                db_c.NOTIFICATION_FIELD_CATEGORY
            ].title()
        data[api_c.NOTIFICATION_TYPE] = data[api_c.NOTIFICATION_TYPE].title()

        return data


class NotificationsSchema(Schema):
    """Notifications get schema"""

    total = Int(
        attribute=api_c.TOTAL_RECORDS,
        example=1,
    )
    notifications = List(
        Nested(NotificationSchema),
        example=[
            {
                api_c.ID: "60e5c7be3b080a75959d6282",
                api_c.NOTIFICATION_TYPE: db_c.NOTIFICATION_TYPE_CRITICAL.title(),
                api_c.DESCRIPTION: "Facebook Delivery Stopped",
                db_c.NOTIFICATION_FIELD_CATEGORY: db_c.NOTIFICATION_CATEGORY_DELIVERY.title(),
                db_c.NOTIFICATION_FIELD_CREATED: "2021-08-09T12:35:24.915Z",
            },
        ],
    )


class NotificationPostSchema(Schema):
    """Notification POST schema"""

    type = Str(validate=OneOf(db_c.NOTIFICATION_TYPES))
    category = Str(validate=OneOf(db_c.NOTIFICATION_CATEGORIES))
    description = Str()
