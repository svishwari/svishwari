"""
Purpose of this file is to house the advertising schema
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str


class AdvertisingSchema(Schema):
    """
    advertising schema class, return the serialized messages back
    """
    class Meta:
        """expose the fields for serialization"""
        # Fields to expose
        fields = ["message"]

    message = Str()
