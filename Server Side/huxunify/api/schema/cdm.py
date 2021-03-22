"""
Schemas for the CDM API
"""

from flask_marshmallow import Schema
from marshmallow import validate
from marshmallow.fields import Boolean, DateTime, Int, Str


DATA_TYPES = [
    "customers",
    "orders",
    "items",
]

FEED_TYPES = [
    "api",
    "batch",
]

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

FILE_EXTENSIONS = [
    "csv",
    "json",
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


class Datafeed(Schema):
    """Datafeed schema."""

    data_source = Str(required=True)
    data_type = Str(required=True, validate=validate.OneOf(DATA_TYPES))
    feed_id = Int(required=True)
    feed_type = Str(required=True, validate=validate.OneOf(FEED_TYPES))
    file_extension = Str(required=True, validate=validate.OneOf(FILE_EXTENSIONS))
    is_pii = Boolean(required=True)
    modified = DateTime(required=True)


class Fieldmapping(Schema):
    """Fieldmapping schema."""

    field_id = Int(required=True)
    field_name = Str(required=True, validate=validate.OneOf(FIELD_NAMES))
    field_variation = Str(required=True)
    modified = DateTime(required=True)
