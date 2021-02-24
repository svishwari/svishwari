"""
Purpose of this file is to house the audience schema
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str


class AudienceSchema(Schema):
    """
    audience schema class, return the serialized messages back
    """
    class Meta:
        """expose the fields for serialization"""
        # Fields to expose
        fields = ["audience_name", "audience_type"]

audience_schema = AudienceSchema()
audiences_schema = AudienceSchema(many=True)