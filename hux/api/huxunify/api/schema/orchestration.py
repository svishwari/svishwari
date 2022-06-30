"""Schemas for the Orchestration API."""
import datetime

from flask_marshmallow import Schema
from marshmallow import fields, validate
from marshmallow.fields import List, Nested, Int

from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import (
    must_not_be_blank,
    validate_object_id,
)
from huxunify.api.schema.destinations import (
    DestinationGetSchema,
)
from huxunify.api.schema.engagement import EngagementGetSchema
from huxunify.api.schema.customers import (
    CustomerOverviewSchema,
    CustomerGenderInsightsSchema,
    CustomerSpendingInsightsSchema,
    CustomerGeoVisualSchema,
)
from huxunify.api.schema.custom_schemas import DateTimeWithZ


class AudienceTagsSchema(Schema):
    """Audience tags schema class"""

    industry = fields.List(fields.String())


class LookalikeAudienceGetSchema(Schema):
    """Schema for retrieving the lookalike audience"""

    _id = fields.String(
        data_key=api_c.ID,
        required=True,
        validate=validate_object_id,
    )
    delivery_platform_id = fields.String(
        required=True, validate=validate_object_id
    )
    audience_id = fields.String(required=True, validate=validate_object_id)
    name = fields.String(required=True)
    country = fields.String()
    audience_size_percentage = fields.Float(required=True)
    size = fields.Float(default=0)
    create_time = DateTimeWithZ(required=True)
    update_time = DateTimeWithZ(required=True)
    created_by = fields.String()
    updated_by = fields.String()
    favorite = fields.Boolean(required=True)
    is_lookalike = fields.Boolean(default=True)
    status = fields.String(default=db_c.AUDIENCE_STATUS_ERROR)
    delivery_platform_link = fields.String(default=None)
    delivery_platform_name = fields.String()
    delivery_platform_type = fields.String()
    tags = fields.Nested(AudienceTagsSchema, required=False)


class AudienceDeliverySchema(Schema):
    """Audience delivery schema class"""

    delivery_platform_name = fields.String()
    delivery_platform_type = fields.String()
    last_delivered = DateTimeWithZ(attribute=db_c.UPDATE_TIME)
    status = fields.String()
    size = fields.Integer(attribute=db_c.DELIVERY_PLATFORM_AUD_SIZE, default=0)
    delivery_platform_id = fields.String(
        required=True, validate=validate_object_id
    )
    link = fields.String()
    is_ad_platform = fields.Bool()


class DeliveriesSchema(Schema):
    """Delivery schema class"""

    id = fields.String(attribute=db_c.ID)
    create_time = DateTimeWithZ()
    update_time = DateTimeWithZ()
    created_by = fields.String()
    updated_by = fields.String()
    name = fields.String()
    status = fields.String()
    size = fields.Integer(attribute=db_c.DELIVERY_PLATFORM_AUD_SIZE, default=0)
    match_rate = fields.Float(allow_none=True, example=0.21)
    delivery_platform_type = fields.String()
    delivery_platform_id = fields.String()
    is_ad_platform = fields.Bool(attribute=api_c.IS_AD_PLATFORM)
    delivery_schedule = fields.String()
    next_delivery = DateTimeWithZ()
    link = fields.String()
    replace_audience = fields.Boolean()


class EngagementDeliverySchema(EngagementGetSchema):
    """Engagement Delivery schema class"""

    deliveries = fields.Nested(DeliveriesSchema, many=True)
    last_delivered = DateTimeWithZ()
    status = fields.String()

    # TOOO - HUS-740
    next_delivery = fields.String()
    delivery_schedule = fields.String(default="Daily")


class DigitalAdvertisingMatchRates(Schema):
    """Match rates schema for digital advertising."""

    destination = fields.String(required=True, example="facebook")
    match_rate = fields.Float(allow_none=True)
    last_delivery = DateTimeWithZ(allow_none=True)


class DigitAdvertising(Schema):
    """Digital advertising schema."""

    match_rates = fields.List(fields.Nested(DigitalAdvertisingMatchRates))


class AudienceGetSchema(Schema):
    """Audience schema class"""

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
    source = fields.Dict(
        attribute=db_c.AUDIENCE_SOURCE,
        example={
            db_c.AUDIENCE_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_AMAZONS3,
            db_c.AUDIENCE_SOURCE_KEY: "bucket-name",
            db_c.AUDIENCE_SOURCE_BUCKET: "file location",
        },
    )
    tags = fields.Nested(AudienceTagsSchema, required=False)
    destinations = fields.List(fields.Nested(DestinationGetSchema))
    engagements = fields.List(fields.Nested(EngagementDeliverySchema))
    standalone_deliveries = fields.List(fields.Nested(AudienceDeliverySchema))
    audience_insights = fields.Nested(CustomerOverviewSchema)

    status = fields.String(
        attribute=api_c.STATUS,
        validate=[
            validate.OneOf(
                choices=[
                    api_c.STATUS_NOT_DELIVERED,
                    api_c.STATUS_DELIVERING,
                    api_c.STATUS_DELIVERED,
                    api_c.STATUS_DELIVERY_PAUSED,
                    api_c.STATUS_ERROR,
                ]
            )
        ],
    )

    size = fields.Int(default=0)
    last_delivered = DateTimeWithZ(attribute=api_c.AUDIENCE_LAST_DELIVERED)

    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME, allow_none=True)
    update_time = DateTimeWithZ(attribute=db_c.UPDATE_TIME, allow_none=True)
    data_added = DateTimeWithZ(attribute=db_c.DATA_ADDED, allow_none=True)

    created_by = fields.String()
    updated_by = fields.String()
    deliveries = fields.Nested(AudienceDeliverySchema, many=True)

    lookalike_audiences = fields.Nested(LookalikeAudienceGetSchema, many=True)
    is_lookalike = fields.Boolean(default=False)
    # defines if lookalikes can be created from the audience.
    lookalikeable = fields.String(default=api_c.STATUS_INACTIVE)
    source_id = fields.String(attribute=db_c.LOOKALIKE_SOURCE_AUD_ID)
    source_name = fields.String(attribute=db_c.LOOKALIKE_SOURCE_AUD_NAME)
    source_size = fields.Int(attribute=db_c.LOOKALIKE_SOURCE_AUD_SIZE)
    audience_size_percentage = fields.Float(
        attribute=db_c.LOOKALIKE_AUD_SIZE_PERCENTAGE, default=0
    )
    source_exists = fields.Boolean()
    match_rate = fields.Float(default=0)
    favorite = fields.Boolean(default=False)
    digital_advertising = fields.Nested(DigitAdvertising, allow_none=True)


class AudiencesBatchGetSchema(Schema):
    """Audiences batch schema."""

    total_records = Int(example=1)
    audiences = List(Nested(AudienceGetSchema))


class CityIncomeInsightsSchema(Schema):
    """Customer Income Insights Schema"""

    name = fields.String(required=True, example="New York", attribute="city")
    ltv = fields.Float(required=True, example=1235.31, attribute="avg_ltv")


class AudienceInsightsGetSchema(Schema):
    """Audience Insights schema class"""

    demo = fields.List(fields.Nested(CustomerGeoVisualSchema))
    income = fields.List(fields.Nested(CityIncomeInsightsSchema))
    spend = fields.Nested(CustomerSpendingInsightsSchema)
    gender = fields.Nested(CustomerGenderInsightsSchema)


class AudienceDestinationSchema(Schema):
    """Audience destination schema class"""

    id = fields.String(required=True, validate=validate_object_id)
    delivery_platform_config = fields.Dict(
        required=False,
        example={db_c.DATA_EXTENSION_NAME: "Data Extension Name"},
    )


class AudiencePutSchema(Schema):
    """Audience put schema class"""

    name = fields.String()
    destinations = fields.List(
        fields.Nested(AudienceDestinationSchema), required=False
    )
    engagement_ids = fields.List(fields.String())
    filters = fields.List(fields.Dict())
    tags = fields.Nested(AudienceTagsSchema, required=False)


class AudiencePostSchema(AudiencePutSchema):
    """Audience post schema class"""

    name = fields.String(validate=must_not_be_blank)
    destinations = fields.List(
        fields.Nested(AudienceDestinationSchema), required=False
    )
    engagements = fields.List(fields.String(), required=True)
    filters = fields.List(fields.Dict())
    tags = fields.Nested(AudienceTagsSchema, required=False)


class EngagementDeliveryHistorySchema(Schema):
    """Schema for Engagement Delivery History"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    audience = fields.Nested(
        AudienceGetSchema(
            only=(
                api_c.NAME,
                db_c.ID,
            )
        )
    )
    destination = fields.Nested(
        DestinationGetSchema(only=(api_c.NAME, api_c.TYPE, db_c.ID))
    )
    size = fields.Integer()
    match_rate = fields.Float(default=0, example=0.21)
    delivered = DateTimeWithZ(required=True, allow_none=True)


class AudienceDeliveryHistorySchema(Schema):
    """Schema for Audience Delivery History"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    engagement = fields.Nested(
        EngagementGetSchema(
            only=(
                api_c.NAME,
                db_c.ID,
            )
        )
    )
    destination = fields.Nested(
        DestinationGetSchema(only=(api_c.NAME, api_c.TYPE, db_c.ID))
    )
    size = fields.Integer()
    match_rate = fields.Float(default=0, example=0.21)
    delivered = DateTimeWithZ(required=True, allow_none=True)


class LookalikeAudiencePostSchema(Schema):
    """Schema for creating a lookalike audience"""

    audience_id = fields.String(validate=must_not_be_blank, required=True)
    name = fields.String(required=True)
    audience_size_percentage = fields.Float(required=True)
    engagement_ids = fields.List(fields.String(), required=False)
    destination_ids = fields.List(fields.String(), required=False)


class LookalikeAudiencePutSchema(Schema):
    """Schema for editing lookalike audience"""

    name = fields.String(required=False)
    tags = fields.Nested(AudienceTagsSchema, required=False)


def is_audience_lookalikeable(audience: dict) -> str:
    """Identify if an audience is able to have a lookalike created from it.
    Three possible outcomes
      - active = yes (i.e. successful facebook deliveries.)
      - inactive = no (i.e. facebook destinations, but no successful deliveries)
      - disabled = N/A (i.e. no facebook destinations)

    Args:
        audience (dict): audience document object.

    Returns:
        str: string denoting the lookalikeable status of the audience.
    """

    deliveries = []

    # if no deliveries, return disabled
    if api_c.AUDIENCE_ENGAGEMENTS in audience:
        for engagement in audience[api_c.AUDIENCE_ENGAGEMENTS]:
            if api_c.DELIVERIES in engagement:
                deliveries += engagement[api_c.DELIVERIES]

    if api_c.DELIVERIES in audience:
        deliveries += audience[api_c.DELIVERIES]

    if not deliveries:
        return api_c.STATUS_DISABLED

    # check if any of the deliveries were sent to facebook
    status = api_c.STATUS_DISABLED
    for delivery in deliveries:
        # check if delivered to facebook.
        if (
            delivery.get(db_c.DELIVERY_PLATFORM_TYPE)
            == db_c.DELIVERY_PLATFORM_FACEBOOK
        ):
            status = api_c.STATUS_INACTIVE

            # add 30 min wait time before making it lookalikable
            if (
                delivery.get(db_c.STATUS)
                in [
                    db_c.STATUS_SUCCEEDED,
                    db_c.AUDIENCE_STATUS_DELIVERED,
                ]
                and (
                    datetime.datetime.utcnow() - delivery.get(db_c.UPDATE_TIME)
                ).total_seconds()
                / 60
                > 30
            ):
                # success, break the loop and return active.
                return api_c.STATUS_ACTIVE
    return status
