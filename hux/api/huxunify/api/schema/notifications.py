"""
Schemas for the notifications API
"""

from flask_marshmallow import Schema
from marshmallow import post_dump
from marshmallow.fields import Str, DateTime
from marshmallow.validate import OneOf

from huxunifylib.database import constants as db_c

from hux.api.huxunify.api import constants as api_c


class NotificationSchema(Schema):
    """Notifications Schema"""

    id = Str(attribute=db_c.ID, example="60e5c7be3b080a75959d6282")
    notification_type = Str(
        attribute="type",
        validate=[OneOf(choices=db_c.NOTIFICATION_TYPES)],
        required=True,
        example=db_c.NOTIFICATION_TYPE_SUCCESS,
    )
    description = Str(
        attribute="description",
        required=True,
        example="Facebook Delivery Stopped",
    )
    created = DateTime(
        attribute="created",
        required=True,
        allow_none=False,
    )
    category = Str(
        attribute="category",
        validate=[
            OneOf(
                choices=[
                    api_c.CATEGORY_ORCHESTRATION,
                    api_c.CATEGORY_DATA_MANAGEMENT,
                    api_c.CATEGORY_DECISIONING,
                ]
            )
        ],
        required=True,
        example=api_c.CATEGORY_ORCHESTRATION,
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
        # change notification_type to title case
        if data.get(db_c.NOTIFICATION_FIELD_CATEGORY):
            data[db_c.NOTIFICATION_FIELD_CATEGORY] = data[
                db_c.NOTIFICATION_FIELD_CATEGORY
            ].title()
        data["notification_type"] = data["notification_type"].title()

        return data
