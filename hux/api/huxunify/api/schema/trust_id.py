"""Purpose of this file is to house trust ID schemas."""

from flask_marshmallow import Schema
from marshmallow.fields import List, Dict, Integer, Nested, Str, Float
from marshmallow.validate import Range, OneOf

from huxunify.api import constants as api_c


class SignalScoreOverviewSchema(Schema):
    """Signal score overview schema"""

    capability = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    humanity = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    reliability = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    transparency = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )


class AttributeScoreOverviewSchema(Schema):
    """Attribute score overview schema."""

    name_of_signal = Str(
        required=True,
        example="capability",
        validate=OneOf(api_c.LIST_OF_SIGNALS),
    )
    attribute_score = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    attribute_description = Str(required=True, example="Good Quality")


class TrustIdOverviewSchema(Schema):
    """Trust ID overview Schema"""

    allowed_filters = List(Dict(), optional=True)
    trust_id_score_overview = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    signal_scores_overview = Nested(SignalScoreOverviewSchema)
    attribute_scores = List(Nested(AttributeScoreOverviewSchema))


class RatingSchema(Schema):
    """Rating Schema"""

    percentage = Float(
        required=True, validate=Range(min_inclusive=0, max_inclusive=100)
    )
    count = Integer(required=True, example=100)


class RatingOverviewSchema(Schema):
    """Rating overview schema"""

    agree = Nested(RatingSchema)
    neutral = Nested(RatingSchema)
    disagree = Nested(RatingSchema)


class OverallCustomerRatingSchema(Schema):
    """Overall customer rating schema"""

    total_customers = Integer(required=True, example=200)
    rating = Nested(RatingOverviewSchema)


class CustomerAttributeRatingsSchema(Schema):
    """Customer attribute ratings schema"""

    attribute_description = Str(required=True, example="Good quality")
    attribute_score = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    overall_customer_rating = Nested(OverallCustomerRatingSchema)


class SignalOverviewSchema(Schema):
    """Signal overview schema"""

    signal_name = Str(
        required=True,
        example="capability",
        validate=OneOf(api_c.LIST_OF_SIGNALS),
    )
    signal_score = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    overall_customer_rating = Nested(OverallCustomerRatingSchema)
    customer_attribute_ratings = List(Nested(CustomerAttributeRatingsSchema))
