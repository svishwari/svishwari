# pylint: disable=no-self-use
"""
Schemas for the Engagements API
"""
from bson import ObjectId
from flask_marshmallow import Schema
from marshmallow import fields, post_load
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import (
    must_not_be_blank,
    validate_object_id,
    validate_object_id_list,
)


class EngagementGetSchema(Schema):
    """
    Engagement get schema class
    """

    engagement_id = fields.String(
        attribute=api_c.ENGAGEMENT_ID,
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
    size = fields.Int(attribute=api_c.ENGAGEMENT_SIZE, allow_none=True)
    # TODO note, what does this delivery schedule need to look like?
    delivery_schedule = fields.List(
        cls_or_instance=fields.String,
        attribute=api_c.ENGAGEMENT_DELIVERY_SCHEDULE,
        allow_none=True,
    )
    created = fields.DateTime(attribute=db_c.CREATE_TIME, allow_none=True)
    created_by = fields.String(attribute=db_c.CREATED_BY, allow_none=True)
    updated = fields.DateTime(attribute=db_c.UPDATE_TIME, allow_none=True)

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

        # set the audiences list str list to an object id list
        if api_c.ENGAGEMENT_AUDIENCES in data:
            id_list = []
            for audience_id in data[api_c.ENGAGEMENT_AUDIENCES]:
                id_list.append(ObjectId(audience_id))
            data.update(audiences=id_list)
        else:
            data.update(audiences=None)

        return data


class EngagementPostSchema(Schema):
    """
    Engagement post schema class
    """

    name = fields.String(required=True, validate=must_not_be_blank)
    description = fields.String()
    created_by = fields.String(required=True, validate=must_not_be_blank)
    # TODO delivery schedule needs to be here as well after structure is addressed
    audiences = fields.List(
        cls_or_instance=fields.String,
        validate=validate_object_id_list
    )


class EngagementPutSchema(Schema):
    """
    Engagement put schema class
    """

    name = fields.String()
    audiences = fields.List(cls_or_instance=fields.String)
    delivery_schedule = fields.List(cls_or_instance=fields.String)
