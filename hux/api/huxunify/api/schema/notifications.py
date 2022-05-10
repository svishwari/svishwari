"""Schemas for the notifications API."""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, List, Nested, Bool
from marshmallow.validate import OneOf

from huxunifylib.database import constants as db_c

from huxunify.api import constants as api_c
from huxunify.api.schema.custom_schemas import DateTimeWithZ


class NotificationSchema(Schema):
    """Notification Schema class."""

    id = Str(attribute=db_c.ID, example="60e5c7be3b080a75959d6282")
    notification_type = Str(
        attribute="type",
        validate=[OneOf(choices=db_c.NOTIFICATION_TYPES)],
        required=True,
        example=db_c.NOTIFICATION_TYPE_CRITICAL,
    )
    description = Str(
        attribute="description",
        required=True,
        example="Facebook Delivery Stopped",
    )
    create_time = DateTimeWithZ(
        attribute="create_time",
        required=True,
        allow_none=False,
    )
    category = Str(
        attribute="category",
        validate=[OneOf(choices=db_c.NOTIFICATION_CATEGORIES)],
        required=True,
        example=db_c.NOTIFICATION_CATEGORY_DELIVERY,
    )
    username = Str(
        attribute="username",
        required=True,
        example="Username",
        allow_none=False,
    )


class NotificationsSchema(Schema):
    """Notifications get schema"""

    total = Int(
        attribute=api_c.TOTAL_RECORDS,
        example=1,
    )
    seen_notifications = Bool(default=False)
    notifications = List(
        Nested(NotificationSchema),
        example=[
            {
                api_c.ID: "60e5c7be3b080a75959d6282",
                api_c.NOTIFICATION_TYPE: db_c.NOTIFICATION_TYPE_CRITICAL,
                api_c.DESCRIPTION: "Facebook Delivery Stopped",
                db_c.NOTIFICATION_FIELD_CATEGORY: db_c.NOTIFICATION_CATEGORY_DELIVERY,
                db_c.NOTIFICATION_FIELD_CREATE_TIME: "2021-08-09T12:35:24.915Z",
            },
        ],
    )


class NotificationPostSchema(Schema):
    """Notification POST schema"""

    type = Str(validate=OneOf(db_c.NOTIFICATION_TYPES))
    category = Str(validate=OneOf(db_c.NOTIFICATION_CATEGORIES))
    description = Str()
