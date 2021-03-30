"""
Purpose of this file is to house the marketing schema
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, List, Length, Dict


class MarketingSchema(Schema):
    """
    Marketing schema class, return the serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["message"]

    message = Str()


class ModelSchema(Schema):
    """
    marketing model schema class, return the serialized messages back
    """

    # define parameters
    models = List(
        Dict(),
        required=True,
        validate=Length(max=1000),
        example=[
            {
                "name": "Churn",
                "value": 1,
            },
            {
                "name": "Propensity",
                "value": 2,
            },
            {
                "name": "LTV",
                "value": 3,
            },
        ],
    )

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["models"]

    message = Str()


class SegmentSchema(Schema):
    """
    marketing segment schema class, return the serialized messages back
    """

    segments = List(
        Dict(),
        required=True,
        validate=Length(max=10000),
        example={
            "PredictionData": [
                {
                    "User": "A5BB0719-2CE0-762B-7C68-C67361766A18",
                    "Segment": "Most Likely",
                }
            ],
            "fileURL": "s3://XXXXXXXX/customers.csv",
            "TransactionID": "260fecbf-3bd9-4a70-8c4c-0a174f708e46",
            "Scales": {
                "Churn": {
                    "Segments": {
                        "0.0-0.2": "Unlikely",
                        "0.21-0.5": "Likely",
                        "0.51-0.8": "Most likely",
                        "0.81-1.0": "Very likely",
                    },
                    "Values": {"Min": "0.0", "Max": "1.0"},
                },
                "Propensity": {
                    "Segments": {
                        "0.0-0.2": "Unlikely",
                        "0.21-0.5": "Likely",
                        "0.51-0.8": "Most likely",
                        "0.81-1.0": "Very likely",
                    },
                    "Values": {"Min": "0.0", "Max": "1.0"},
                },
            },
        },
    )

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["segments"]

    message = Str()


class SegmentFlySchema(Schema):
    """
    marketing segment schema class, return the serialized messages back
    """

    segments = List(
        Dict(),
        required=True,
        validate=Length(max=10000),
        example={
            "TransactionID": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
            "Scales": {
                "Propensity": {
                    "Segments": {
                        "0.0-0.2": "Unlikely",
                        "0.21-0.5": "Likely",
                        "0.51-0.8": "Most likely",
                        "0.81-1.0": "Very likely",
                    },
                    "Values": {"Min": "0.0", "Max": "1.0"},
                }
            },
            "Rules": [
                {
                    "Rule": [
                        {
                            "Transaction": {
                                "all": [
                                    {
                                        "all": [
                                            {
                                                "fact": "Propensity",
                                                "operator": "greaterThanInclusive",
                                                "value": 0.35,
                                            },
                                            {
                                                "fact": "Propensity",
                                                "operator": "lessThanInclusive",
                                                "value": 1,
                                            },
                                        ]
                                    }
                                ]
                            }
                        },
                        {"Values": {"Segment": "Most Likely"}},
                    ]
                }
            ],
            "PredictionData": [{"User": "1", "Segment": "Most Likely"}, {"User": "2"}],
        },
    )

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["segments"]

    message = Str()


class SegmentDeliverSchema(Schema):
    """
    Marketing schema class, return the serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["status"]

    message = Str()


class SegmentCountSchema(Schema):
    """
    Marketing schema class, return the serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["segment_count"]

    message = Str()
