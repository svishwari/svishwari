"""
Schemas for the Orchestration API
"""

from flask_marshmallow import Schema
from marshmallow import fields, post_load, post_dump
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
                api_c.DESTINATION_NAME: "destination name",
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
    audience_insights = fields.Dict(
        attribute=api_c.AUDIENCE_INSIGHTS,
        example={
            api_c.INSIGHTS_TOTAL_CUSTOMERS: 121321321,
            api_c.INSIGHTS_TOTAL_COUNTRIES: 2,
            api_c.INSIGHTS_TOTAL_US_STATES: 28,
            api_c.INSIGHTS_TOTAL_CITIES: 246,
            api_c.INSIGHTS_MIN_AGE: 34,
            api_c.INSIGHTS_MAX_AGE: 100,
            api_c.INSIGHTS_GENDER_WOMEN: 0.4651031,
            api_c.INSIGHTS_GENDER_MEN: 0.481924,
            api_c.INSIGHTS_GENDER_OTHER: 0.25219,
        },
    )
    created = fields.DateTime(attribute=db_c.CREATE_TIME, allow_none=True)
    created_by = fields.String(attribute=db_c.CREATED_BY, allow_none=True)
    updated = fields.DateTime(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = fields.String(attribute=db_c.UPDATED_BY, allow_none=True)

    @post_load()
    # pylint: disable=unused-argument, no-self-use
    def process_modified(
        self, data: dict, many: bool = False, partial: bool = False
    ) -> dict:
        """process the schema before deserializing.

        Args:
            data (dict): The audience object
            many (bool): If there are many to process
            partial (bool): Partially deserialize fields.
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

    @post_dump
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def post_serialize(self, data: dict, many=False) -> dict:
        """process the schema before serializing.
        Args:
            data (dict): The audience object
            many (bool): If there are many to process
        Returns:
            Response: Returns an audience object
        """
        # map id to audience_id
        if db_c.ID in data:
            data[api_c.AUDIENCE_ID] = str(data[db_c.ID])
            del data[db_c.ID]

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
