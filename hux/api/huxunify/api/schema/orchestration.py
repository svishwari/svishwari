"""
Schemas for the Orchestration API
"""

from flask_marshmallow import Schema
from marshmallow import fields
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.destinations import DestinationGetSchema
from huxunify.api.schema.user import UserSchema
from huxunify.api.schema.utils import (
    must_not_be_blank,
    validate_object_id,
)


class AudienceGetSchema(Schema):
    """
    Audience schema class
    """

    _id = fields.String(
        data_key=api_c.ID,
        example="5f5f7262997acad4bac4373b",
        required=True,
        validate=validate_object_id,
    )
    name = fields.String(attribute=api_c.AUDIENCE_NAME, example="My audience")
    filters = fields.List(
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

    destinations = fields.List(
        fields.Nested(DestinationGetSchema),
        attribute=api_c.DESTINATIONS_TAG,
    )
    engagements = fields.List(
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
            api_c.TOTAL_CUSTOMERS: 121321321,
            api_c.COUNTRIES: 2,
            api_c.STATES: 28,
            api_c.CITIES: 246,
            api_c.MIN_AGE: 34,
            api_c.MAX_AGE: 100,
            api_c.GENDER_WOMEN: 0.4651031,
            api_c.GENDER_MEN: 0.481924,
            api_c.GENDER_OTHER: 0.25219,
        },
    )

    size = fields.Int(example=6173223)
    last_delivered_on = fields.DateTime(
        attribute=api_c.AUDIENCE_LAST_DELIVERED
    )

    create_time = fields.DateTime(attribute=db_c.CREATE_TIME, allow_none=True)
    update_time = fields.DateTime(attribute=db_c.UPDATE_TIME, allow_none=True)
    created_by = fields.Nested(
        UserSchema(only=("first_name", "last_name", "user_id"))
    )
    updated_by = fields.Nested(
        UserSchema(only=("first_name", "last_name", "user_id"))
    )


class AudiencePutSchema(Schema):
    """
    Audience put schema class
    """

    name = fields.String()
    destinations = fields.List(fields.String())
    engagements = fields.List(fields.String())
    filters = fields.List(fields.Dict())


class AudiencePostSchema(AudiencePutSchema):
    """
    Audience post schema class
    """

    name = fields.String(validate=must_not_be_blank)
    destinations = fields.List(fields.String())
    engagements = fields.List(fields.String())
    filters = fields.List(fields.Dict())
