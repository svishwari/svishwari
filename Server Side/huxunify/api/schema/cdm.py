"""
Purpose of this file is to house the CDM Schema
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str


class CdmSchema(Schema):
    """
    CDM schema class, return the serialized messages back
    """
    class Meta:
        """expose the fields for serialization"""
        # Fields to expose
        fields = ["message"]

    message = Str()
