"""Purpose of this file is to house trust ID schemas."""
import decimal
from flask_marshmallow import Schema
from marshmallow import pre_dump
from marshmallow.fields import List, Integer, Nested, Str, Float, Boolean
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

    class Meta:
        """Meta class to handle ordering of schema"""

        ordered = True

    disagree = Nested(RatingSchema)
    neutral = Nested(RatingSchema)
    agree = Nested(RatingSchema)


class OverallCustomerRatingSchema(Schema):
    """Overall customer rating schema"""

    total_customers = Integer(required=True, example=200)
    rating = Nested(RatingOverviewSchema)


class FactorScoreOverviewSchema(Schema):
    """Factor score overview schema"""

    class Meta:
        """Meta class for Schema"""

        ordered = True

    factor_name = Str(
        required=True,
        example="capability",
        validate=OneOf(api_c.TRUST_ID_LIST_OF_FACTORS),
    )
    factor_score = Integer(
        required=True,
        validate=Range(min_inclusive=-100, max_inclusive=100),
    )
    factor_description = Str(
        required=True,
        example="Good Quality",
    )
    overall_customer_rating = Nested(OverallCustomerRatingSchema)

    @pre_dump
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def round_up_scores(self, data: dict, many: bool = False) -> dict:
        """Round up score value to whole numbers
        Args:
            data (dict): Factor details dict
            many (bool): If multiple objects

        Returns:
            dict : Returns a factor details object
        """
        if data[api_c.TRUST_ID_FACTOR_SCORE]:
            score = decimal.Decimal(data[api_c.TRUST_ID_FACTOR_SCORE])
            decimal.getcontext().rounding = decimal.ROUND_HALF_UP
            data[api_c.TRUST_ID_FACTOR_SCORE] = round(score, 0)

        return data


class TrustIdOverviewSchema(Schema):
    """Trust ID overview Schema"""

    class Meta:
        """Meta class for Schema"""

        ordered = True

    trust_id_score = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    factors = List(Nested(FactorScoreOverviewSchema))

    @pre_dump
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def round_up_scores(self, data: dict, many: bool = False) -> dict:
        """Round up score value to whole numbers
        Args:
            data (dict): Attribute details dict
            many (bool): If multiple objects

        Returns:
            dict : Returns an attribute details object
        """
        if data[api_c.TRUST_ID_SCORE]:
            score = decimal.Decimal(data[api_c.TRUST_ID_SCORE])
            decimal.getcontext().rounding = decimal.ROUND_HALF_UP
            data[api_c.TRUST_ID_SCORE] = round(score, 0)

        return data


class TrustIdAttributesSchema(Schema):
    """Trust ID attributes Schema"""

    class Meta:
        """Meta class for Schema"""

        ordered = True

    factor_name = Str(
        required=True,
        example="capability",
        validate=OneOf(api_c.TRUST_ID_LIST_OF_FACTORS),
    )
    attribute_score = Integer(
        required=True, validate=Range(min_inclusive=-100, max_inclusive=100)
    )
    attribute_description = Str(required=True, example="Good Quality")
    attribute_short_description = Str(required=True, example="Good Quality")
    overall_customer_rating = Nested(OverallCustomerRatingSchema)

    @pre_dump
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def round_up_scores(self, data: dict, many: bool = False) -> dict:
        """Round up score value to whole numbers
        Args:
            data (dict): Attribute details dict
            many (bool): If multiple objects

        Returns:
            dict : Returns an attribute details object
        """
        if data[api_c.TRUST_ID_ATTRIBUTE_SCORE]:
            score = decimal.Decimal(data[api_c.TRUST_ID_ATTRIBUTE_SCORE])
            decimal.getcontext().rounding = decimal.ROUND_HALF_UP
            data[api_c.TRUST_ID_ATTRIBUTE_SCORE] = round(score, 0)

        return data


class AttributeScoreOverviewSchema(Schema):
    """Attribute score overview schema."""

    class Meta:
        """Meta class for Schema"""

        ordered = True

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

    @pre_dump
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def round_up_scores(self, data: dict, many: bool = False) -> dict:
        """Round up score value to whole numbers
        Args:
            data (dict): Attribute details dict
            many (bool): If multiple objects

        Returns:
            dict : Returns an attribute details object
        """
        if data[api_c.TRUST_ID_ATTRIBUTE_SCORE]:
            score = decimal.Decimal(data[api_c.TRUST_ID_ATTRIBUTE_SCORE])
            decimal.getcontext().rounding = decimal.ROUND_HALF_UP
            data[api_c.TRUST_ID_ATTRIBUTE_SCORE] = round(score, 0)

        return data


class TrustIdSegmentFilterSchema(Schema):
    """Trust ID segment filter schema"""

    class Meta:
        """Meta class for Schema"""

        ordered = True

    description = Str(example="Children count", required=True)
    type = Str(example="children_count", required=True)
    values = List(Str(example=["1", "2", "3", "4", "5+"]), default=[])
    is_boolean = Boolean(required=False, default=False)


class TrustIdSegmentSchema(Schema):
    """Trust ID segment schema"""

    class Meta:
        """Meta class for Schema"""

        ordered = True

    segment_name = Str(required=True, example="Segment 1")
    default = Boolean(default=False)
    segment_filters = List(Nested(TrustIdSegmentFilterSchema), default=[])
    attributes = List(Nested(AttributeScoreOverviewSchema), required=True)


class TrustIdComparisonSchema(Schema):
    """Trust ID comparison schema"""

    class Meta:
        """Meta class for Schema"""

        ordered = True

    segment_type = Str(
        required=True,
        example="composite & factor scores",
        validate=OneOf(api_c.TRUST_ID_SEGMENT_TYPE_MAP.values()),
    )
    segments = List(Nested(TrustIdSegmentSchema))


class TrustIdSegmentPostSchema(Schema):
    """Trust ID segment POST schema"""

    segment_name = Str(example="Segment 1", required=True)
    segment_filters = List(Nested(TrustIdSegmentFilterSchema), default=[])
