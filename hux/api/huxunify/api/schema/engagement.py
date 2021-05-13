# pylint: disable=no-self-use
"""
Schemas for the Engagements API
"""
from bson import ObjectId
from flask_marshmallow import Schema
from marshmallow import fields, post_load, validate
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import (
    must_not_be_blank,
    validate_object_id,
    validate_object_id_list,
)


class DeliverySchedule(Schema):
    """
    Delivery Schedule schema
    """

    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)


class EngagementSchema(Schema):
    """
    engagement schema class, return serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = [
            "name",
            "description",
            "audiences",
            "status",
            "delivery_schedule",
            "created_time",
            "created_by",
            "updated_time",
            "updated_by"
        ]

    name = fields.Str()
    description = fields.Str()
    audiences = fields.List(cls_or_instance=fields.Str())
    status = fields.Str()
    delivery_schedule = fields.Nested(DeliverySchedule)
    created_time = fields.DateTime()
    created_by = fields.DateTime()
    update_time = fields.DateTime()
    updated_by = fields.DateTime()


engagement_schema = EngagementSchema()
engagements_schema = EngagementSchema(many=True)


class EngagementGetSchema(Schema):
    """
    Engagement get schema class
    """

    e_id = fields.String(
        attribute=db_c.ID,
        example="5f5f7262997acad4bac4373b",
        required=True,
        validate=validate_object_id,
    )
    name = fields.String(attribute=api_c.ENGAGEMENT_NAME, required=True)
    description = fields.String(attribute=api_c.ENGAGEMENT_DESCRIPTION)
    audiences = fields.List(
        cls_or_instance=fields.String,
        attribute=api_c.ENGAGEMENT_AUDIENCES,
        required=True,
        validate=validate_object_id_list,
    )
    status = fields.String(
        attribute=api_c.ENGAGEMENT_STATUS,
        required=True,
        validate=validate.OneOf(api_c.ENGAGEMENT_STATUSES),
    )
    delivery_schedule = fields.Nested(
        DeliverySchedule,
        required=True,
        attribute=api_c.ENGAGEMENT_DELIVERY_SCHEDULE,
    )
    created_time = fields.DateTime(attribute=db_c.CREATE_TIME)
    created_by = fields.String(attribute=db_c.CREATED_BY)
    updated_time = fields.DateTime(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = fields.DateTime(attribute=db_c.UPDATED_BY, allow_none=True)

    @post_load()
    def process_modified(self, data: dict) -> dict:
        """Process the schema before deserialization

        Args:
            data (dict): the engagement object

        Returns:
            Response: Returns an engagement object

        """

        # set the input ID to an object ID
        if api_c.ENGAGEMENT_ID in data:
            # if a valid ID, map it
            if ObjectId.is_valid(data[api_c.ENGAGEMENT_ID]):
                data.update(engagement_id=ObjectId(data[api_c.ENGAGEMENT_ID]))
            else:
                # otherwise map to None
                data.update(engagement_id=None)

        return data


class EngagementPostSchema(Schema):
    """
    Engagement post schema class
    """

    name = fields.String(required=True, validate=must_not_be_blank)
    description = fields.String()
    created_by = fields.String(required=True, validate=must_not_be_blank)
    delivery_schedule = fields.Nested(DeliverySchedule)
    audiences = fields.List(
        cls_or_instance=fields.String, validate=validate_object_id_list
    )


class EngagementPutSchema(Schema):
    """
    Engagement put schema class
    """

    name = fields.String(required=False)
    description = fields.String(required=False)
    audiences = fields.List(cls_or_instance=fields.String, required=False)
    delivery_schedule = fields.Nested(DeliverySchedule, required=False)
