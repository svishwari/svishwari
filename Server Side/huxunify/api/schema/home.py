"""
Purpose of this file is to house the home schema for testing
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str


class HomeSchema(Schema):
    """
    home schema class, return the serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["message"]

    message = Str()
