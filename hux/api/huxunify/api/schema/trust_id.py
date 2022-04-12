"""Purpose of this file is to house trust ID schemas."""

from flask_marshmallow import Schema
from marshmallow.fields import List, Integer, Nested, Str, Float
from marshmallow.validate import Range, OneOf

from huxunify.api import constants as api_c


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


class SignalScoreOverviewSchema(Schema):
    """Signal score overview schema"""

    signal_name = Str(
        required=True,
        example="capability",
        validate=OneOf(api_c.LIST_OF_SIGNALS),
    )
    signal_score = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    signal_description = Str(required=True, example="Good Quality")
    overall_customer_rating = Nested(OverallCustomerRatingSchema)


class TrustIdOverviewSchema(Schema):
    """Trust ID overview Schema"""

    trust_id_score = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    signals = List(Nested(SignalScoreOverviewSchema))


class TrustIdAttributesSchema(Schema):
    """Trust ID attributes Schema"""

    signal_name = Str(
        required=True,
        example="capability",
        validate=OneOf(api_c.LIST_OF_SIGNALS),
    )
    attribute_score = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    attribute_description = Str(required=True, example="Good Quality")
    overall_customer_rating = Nested(OverallCustomerRatingSchema)


class AttributeScoreOverviewSchema(Schema):
    """Attribute score overview schema."""

    attribute_type = Str(
        required=True,
        example="trust_id",
    )
    attribute_name = Str(
        required=True,
    )
    attribute_score = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    attribute_description = Str(required=True, example="Good Quality")


class SegmentFilterSchema(Schema):
    """Trust ID segment filter schema"""

    type = Str(example="age", required=True)
    description = Str(example="Age", required=True)
    values = List(Str())


class TrustIdSegmentSchema(Schema):
    """Trust ID segment schema"""

    segment_name = Str(required=True, example="Segment 1")
    segment_filters = List(Nested(SegmentFilterSchema), default=[])
    attributes = List(Nested(AttributeScoreOverviewSchema), required=True)


class TrustIdComparisonSchema(Schema):
    """Trust ID comparison schema"""

    segment_type = Str(
        required=True,
        example="composite & signal scores",
        validate=OneOf(api_c.SEGMENT_TYPES),
    )
    segments = List(Nested(TrustIdSegmentSchema))


class TrustIdSegmentFilterSchema(Schema):
    """Trust ID segment filter schema"""

    type = Str(example="children_count", required=True)
    description = Str(example="Children count", required=True)
    values = List(Str(example=["1", "2", "3", "4", "5+"]), default=[])


class TrustIdSegmentPostSchema(Schema):
    """Trust ID segment POST schema"""

    segment_name = Str(example="Segment 1", required=True)
    segment_filters = List(Nested(TrustIdSegmentFilterSchema), default=[])
