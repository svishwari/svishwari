"""
Purpose of this file is to house the Decision schema for testing
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, List, String
from marshmallow.validate import Length


class DecisionSchema(Schema):
    """
    Decision schema class, return the serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["message"]

    message = Str()


class CustomerFeatureSchema(Schema):
    """
    Decision schema class, return the serialized messages back
    """

    # define parameters
    predictions = List(
        String(),
        required=True,
        validate=Length(max=1000),
        example=[
            {"feature_name": "imps_count_1d_1d", "predictions": [1, 2, 3]},
            {"feature_name": "imps_count_2d_1d", "predictions": [3, 1, 0]},
            {"feature_name": "imps_count_3d_1d", "predictions": [5, 7, 9]},
        ],
    )

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["predictions"]

    message = Str()
