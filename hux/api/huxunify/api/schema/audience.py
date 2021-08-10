"""
Purpose of this file is to house the audience schema
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Integer
from marshmallow.fields import List, Dict
from marshmallow.validate import Length, OneOf

import huxunify.api.constants as api_c


class AudienceSchema(Schema):
    """
    audience schema class, return the serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = [
            "audience_filters",
            "audience_name",
            "audience_type",
            "audience_id",
            "created",
        ]

    audience_filters = List(Dict())
    audience_name = Str()
    audience_type = Str()
    audience_id = Str()
    created = Str()


audience_schema = AudienceSchema()
audiences_schema = AudienceSchema(many=True)


class AudienceDeliverySchema(Schema):
    """
    audience schema class, return the serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = [
            "delivery_platform_id",
            "audience_delivery_status",
            "audience_id",
            "completed",
            "count",
            "delivery_job_id",
            "delivery_job_status",
            "created",
        ]

    delivery_platform_id = Str()
    audience_delivery_status = Str(
        attribute=api_c.STATUS,
        required=True,
        validate=OneOf(
            choices=[
                api_c.STATUS_DELIVERING,
                api_c.STATUS_DELIVERED,
                api_c.STATUS_NOT_DELIVERED,
                api_c.STATUS_DRAFT,
                api_c.STATUS_ERROR,
                api_c.STATUS_PAUSED,
            ]
        ),
        default=api_c.STATUS_DRAFT,
    )
    completed = Str()
    audience_id = Str()
    delivery_job_id = Str()
    delivery_job_status = Str()
    count = Integer()
    created = Str()


audience_delivery_schema = AudienceDeliverySchema()
audience_delivery_schemas = AudienceDeliverySchema(many=True)


class AudienceInsightsSchema(Schema):
    """
    Decision schema class, return the serialized messages back
    """

    # define parameters
    insights = List(
        Dict(),
        required=True,
        validate=Length(max=1000),
        example={
            "age": {
                "breakdown": {
                    "additionalProp1": 0,
                    "additionalProp2": 0,
                    "additionalProp3": 0,
                },
                "coverage": 70.2,
            },
            "audience_id": "5f5f7262997acad4bac4373b",
            "city": {
                "breakdown": {
                    "additionalProp1": 0,
                    "additionalProp2": 0,
                    "additionalProp3": 0,
                },
                "coverage": 70.2,
            },
            "count": 98743,
            "country_code": {
                "breakdown": {
                    "additionalProp1": 0,
                    "additionalProp2": 0,
                    "additionalProp3": 0,
                },
                "coverage": 70.2,
            },
            "gender": {
                "breakdown": {
                    "additionalProp1": 0,
                    "additionalProp2": 0,
                    "additionalProp3": 0,
                },
                "coverage": 70.2,
            },
            "mobile_device_id": {"coverage": 70.2},
            "state_or_province": {
                "breakdown": {
                    "additionalProp1": 0,
                    "additionalProp2": 0,
                    "additionalProp3": 0,
                },
                "coverage": 70.2,
            },
        },
    )

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["insights"]


audience_insights_schema = AudienceInsightsSchema()


class AudienceDeliveryInsightsSchema(Schema):
    """
    audience schema class, return the serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["audience_id", "delivery_job_id", "count"]

    delivery_job_id = Str()
    audience_id = Str()
    count = Integer()


audience_delivery_insights_schema = AudienceDeliveryInsightsSchema()
