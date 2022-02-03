"""Schemas for email deliverability  API"""

from flask_marshmallow import Schema
from marshmallow.fields import Integer, Float, Str, List, Nested
from marshmallow.validate import Range, OneOf

from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api import constants as api_c


class DomainDataPercentageSchema(Schema):
    """Schema for percentage data representation for all domains."""

    domain_1 = Float(
        validate=Range(min_inclusive=0.0, max_inclusive=1.0), example=0.1
    )
    domain_2 = Float(
        validate=Range(min_inclusive=0.0, max_inclusive=1.0), example=0.1
    )
    domain_3 = Float(
        validate=Range(min_inclusive=0.0, max_inclusive=1.0), example=0.1
    )
    date = DateTimeWithZ(required=True)


class DomainDataCountSchema(Schema):
    """Schema for count data representation for all domains."""

    domain_1 = Integer(example=10)
    domain_2 = Integer(example=10)
    domain_3 = Integer(example=10)
    date = DateTimeWithZ(required=True)


class EmailDeliverabiliyDomainsSchema(Schema):
    """Schema for data for each domain's email deliverability."""

    interval = Str(
        default=api_c.DAILY,
        validate=OneOf([api_c.DAILY, api_c.WEEKLY, api_c.MONTHLY]),
    )

    sent = List(Nested(DomainDataCountSchema), required=True)
    delivered_rate = List(Nested(DomainDataPercentageSchema), required=True)
    open_rate = List(Nested(DomainDataPercentageSchema), required=True)
    click_rate = List(Nested(DomainDataPercentageSchema), required=True)
    unsubscribe_rate = List(Nested(DomainDataPercentageSchema), required=True)
    complaints_rate = List(Nested(DomainDataPercentageSchema), required=True)


class SendingDomainsOverviewSchema(Schema):
    """Schema for sending domain overview."""

    domain_name = Str(example="domain1", required=True)
    sent = Integer(example=1, required=True)
    bounce_rate = Float(
        validate=Range(min_inclusive=0.0, max_inclusive=1.0), example=0.1
    )
    open_rate = Float(
        validate=Range(min_inclusive=0.0, max_inclusive=1.0), example=0.1
    )
    click_rate = Float(
        validate=Range(min_inclusive=0.0, max_inclusive=1.0), example=0.1
    )


class DeliveredOpenRateOverviewSchema(Schema):
    """Schema for Delivered count and Open rate data."""

    date = DateTimeWithZ(required=True)
    open_rate = Float(
        validate=Range(min_inclusive=0.0, max_inclusive=1.0), example=0.1
    )
    delivered_count = Integer(example=2)


class EmailDeliverabilityOverviewSchema(Schema):
    """Schema for email deliverability overview."""

    overall_inbox_rate = Float(example=0.8, required=True)
    interval = Str(
        default=api_c.DAILY,
        validate=OneOf([api_c.DAILY, api_c.WEEKLY, api_c.MONTHLY]),
    )
    sending_domains_overview = List(Nested(SendingDomainsOverviewSchema))
    delivered_open_rate_overview = List(
        Nested(DeliveredOpenRateOverviewSchema)
    )
