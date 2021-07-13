"""
Schemas for the Orchestration API
"""

from flask_marshmallow import Schema
from marshmallow import fields
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import (
    must_not_be_blank,
    validate_object_id,
)
from huxunify.api.schema.destinations import DestinationGetSchema


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

    destinations = fields.List(fields.Nested(DestinationGetSchema))
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
    last_delivered = fields.DateTime(attribute=api_c.AUDIENCE_LAST_DELIVERED)

    create_time = fields.DateTime(attribute=db_c.CREATE_TIME, allow_none=True)
    update_time = fields.DateTime(attribute=db_c.UPDATE_TIME, allow_none=True)
    created_by = fields.String()
    updated_by = fields.String()


class AudiencePutSchema(Schema):
    """
    Audience put schema class
    """

    name = fields.String()
    destinations = fields.List(fields.Dict())
    engagement_ids = fields.List(fields.String())
    filters = fields.List(fields.Dict())


class AudiencePostSchema(AudiencePutSchema):
    """
    Audience post schema class
    """

    name = fields.String(validate=must_not_be_blank)
    destinations = fields.List(
        fields.Dict(),
        attribute=api_c.DESTINATIONS,
        example=[
            {
                api_c.ID: "60ae035b6c5bf45da27f17d6",
                api_c.DATA_EXTENSION_ID: "data_extension_id",
            }
        ],
    )
    engagements = fields.List(fields.String(), required=True)
    filters = fields.List(fields.Dict())


class DeliveryHistorySchema(Schema):
    """
    Schema for Engagement Delivery History
    """

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    audience = fields.Nested(
        AudienceGetSchema(
            only=(
                "name",
                "_id",
            )
        )
    )
    destination = fields.Nested(
        DestinationGetSchema(only=("name", "type", "_id"))
    )
    size = fields.Integer()
    delivered = fields.DateTime(required=True, allow_none=True)
