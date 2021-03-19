"""
Schemas for the CDM API
"""

from flask_marshmallow import Schema
from marshmallow import validate
from marshmallow.fields import Str, Int, DateTime


FIELD_NAMES = [
    "FNAME",
    "LNAME",
    "ADD1",
    "ADD2",
    "ADD3",
    "CITY",
    "STATE",
    "ZIP",
    "COMPANY",
    "TITLE",
    "EMAIL",
]


class CdmSchema(Schema):
    """
    CDM schema class, return the serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields = ["message"]

    message = Str()


class Fieldmapping(Schema):
    """Fieldmapping schema."""

    field_id = Int(required=True)
    field_name = Str(required=True, validate=validate.OneOf(FIELD_NAMES))
    field_variation = Str(required=True)
    modified = DateTime(required=True)
