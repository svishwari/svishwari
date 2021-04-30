"""
Schemas for the Audience API
"""

from flask_marshmallow import Schema
from marshmallow import fields, post_load
from marshmallow.validate import OneOf
from bson import ObjectId
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import (
    must_not_be_blank,
    validate_object_id,
)


class AudienceGetSchema(Schema):
    """
    Audience schema class
    """

    audience_id = fields.String(
        attribute=api_c.AUDIENCE_ID,
        example="585t749997acad4bac4373b",
        required=True,
        validate=validate_object_id,
    )
    audience_name = fields.String(
        attribute=api_c.AUDIENCE_NAME, example="My audience"
    )
    audience_status = fields.String(
        attribute=api_c.AUDIENCE_STATUS,
        validate=[
            OneOf(
                choices=[
                    api_c.AUDIENCE_STATUS_ERROR,
                    api_c.AUDIENCE_STATUS_PAUSED,
                    api_c.AUDIENCE_STATUS_DRAFT,
                    api_c.AUDIENCE_STATUS_DELIVERED,
                    api_c.AUDIENCE_STATUS_DELIVERING,
                    api_c.AUDIENCE_STATUS_PENDING,
                ]
            )
        ],
    )
    audience_size = fields.Int(
        attribute=api_c.AUDIENCE_SIZE, example=763123, read_only=True
    )
    audience_filters = fields.List(
        fields.Dict(),
        attribute=api_c.AUDIENCE_FILTERS,
        example=[
            {
                api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                api_c.AUDIENCE_SECTION_FILTERS: [
                    {
                        api_c.AUDIENCE_FILTER_FIELD: "filter_field",
                        api_c.AUDIENCE_FILTER_TYPE: "type",
                        api_c.AUDIENCE_FILTER_VALUE: "value",
                    }
                ],
            }
        ],
    )
    audience_destinations = fields.List(
        fields.Dict(),
        attribute=api_c.AUDIENCE_DESTINATIONS,
        example=[
            {
                api_c.DESTINATION_ID: "destination id",
                api_c.DESTINATION_NAME: "destinations name",
            }
        ],
    )
    audience_engagements = fields.List(
        fields.Dict(),
        attribute=api_c.AUDIENCE_ENGAGEMENTS,
        example=[
            {
                api_c.ENGAGEMENT_ID: "Engagement id",
                api_c.ENGAGEMENT_NAME: "Engagement name",
            }
        ],
    )
    created = fields.DateTime(attribute=db_c.CREATE_TIME, allow_none=True)
    created_by = fields.String(attribute=db_c.CREATED_BY, allow_none=True)
    updated = fields.DateTime(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = fields.String(attribute=db_c.UPDATED_BY, allow_none=True)

    @post_load()
    # pylint: disable=unused-argument, no-self-use
    def process_modified(
        self,
        data: dict,
    ) -> dict:
        """process the schema before deserializing.

        Args:
            data (dict): The audience object
            many (bool): If there are many to process
        Returns:
            Response: Returns a audience object

        """
        # set the input ID to an object ID
        if api_c.AUDIENCE_ID in data:
            # if a valid ID, map it
            if ObjectId.is_valid(data[api_c.AUDIENCE_ID]):
                data.update(audience_id=ObjectId(data[api_c.AUDIENCE_ID]))
            else:
                # otherwise map to None
                data.update(audience_id=None)
        return data


class AudiencePutSchema(Schema):
    """
    Audience put schema class
    """

    audience_name = fields.String()
    audience_destinations = fields.List(fields.String())
    audience_engagements = fields.List(fields.String())
    audience_filters = fields.List(fields.Dict())


class AudiencePostSchema(AudiencePutSchema):
    """
    Audience post schema class
    """

    audience_name = fields.String(validate=must_not_be_blank)
    audience_destinations = fields.List(fields.String())
    audience_engagements = fields.List(fields.String())
    audience_filters = fields.List(fields.Dict())
