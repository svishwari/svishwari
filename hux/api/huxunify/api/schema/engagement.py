# pylint: disable=no-self-use
"""
Schemas for the Engagements API
"""
from flask_marshmallow import Schema
from marshmallow import fields, validate
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import must_not_be_blank, validate_object_id


class DeliverySchedule(Schema):
    """
    Delivery Schedule schema
    """

    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)


class EngagementGetSchema(Schema):
    """
    Engagement get schema class
    """

    _id = fields.String(
        data_key=api_c.ENGAGEMENT_ID,
        example="5f5f7262997acad4bac4373b",
        required=True,
        validate=validate_object_id,
    )
    name = fields.String(attribute=api_c.ENGAGEMENT_NAME, required=True)
    description = fields.String(attribute=api_c.ENGAGEMENT_DESCRIPTION)
    # TODO return empty list for now
    audiences = fields.List(
        cls_or_instance=fields.String,
        attribute=api_c.ENGAGEMENT_AUDIENCES,
        required=True,
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
    enabled = fields.Bool(attribute=db_c.ENABLED, required=True)


class EngagementPostSchema(Schema):
    """
    Engagement post schema class
    """

    name = fields.String(required=True, validate=must_not_be_blank)
    description = fields.String()
    delivery_schedule = fields.Nested(DeliverySchedule)
    audiences = fields.List(cls_or_instance=fields.String)


class EngagementPutSchema(Schema):
    """
    Engagement put schema class
    """

    name = fields.String(required=False)
    description = fields.String(required=False)
    audiences = fields.List(cls_or_instance=fields.String, required=False)
    delivery_schedule = fields.Nested(DeliverySchedule, required=False)
