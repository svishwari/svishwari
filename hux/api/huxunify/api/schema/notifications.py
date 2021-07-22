"""
Schemas for the notifications API
"""

from flask_marshmallow import Schema
from marshmallow import post_dump
from marshmallow.fields import Str
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
        validate=[
            OneOf(
                choices=[
                    api_c.DESTINATIONS_TAG,
                    api_c.MODELS_TAG,
                    api_c.ENGAGEMENT_TAG,
                    api_c.DELIVERY_TAG,
                    api_c.ORCHESTRATION_TAG,
                    api_c.CUSTOMERS_TAG,
                ]
            )
        ],
        required=False,
        example=api_c.DELIVERY_TAG,
    )

    @post_dump
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def post_serialize(self, data: dict, many=False) -> dict:
        """process the schema before serializing.

        Args:
            data (dict): The notification object
            many (bool): If there are many to process

        Returns:
            Response: Returns a notification object

        """
        # change notification type and category to title case
        if data.get(db_c.NOTIFICATION_FIELD_CATEGORY):
            data[db_c.NOTIFICATION_FIELD_CATEGORY] = data[
                db_c.NOTIFICATION_FIELD_CATEGORY
            ].title()
        data[api_c.NOTIFICATION_TYPE] = data[api_c.NOTIFICATION_TYPE].title()

        return data
