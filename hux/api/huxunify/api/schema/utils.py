"""
purpose of this file is to house schema utilities
"""
import uuid
from datetime import datetime, timedelta
import random
from flask_marshmallow import Schema
from marshmallow.fields import Boolean, DateTime, Int, Str, Float


# get random data back based on marshmallow field type
SPEC_TYPE_LOOKUP = {
    Boolean: bool(random.getrandbits(1)),
    DateTime: datetime.now() + timedelta(random.randint(0, 1e4)),
    Int: random.randint(0, 1e4),
    Str: str(uuid.uuid4()),
    Float: random.random(),
}


def generate_synthetic_marshmallow_data(schema_obj: Schema) -> dict:
    """This function generates synthetic data for marshmallow

    Args:
        schema_obj (Schema): a marshmallow schema object

    Returns:
        dict: a dictionary that simulates the passed in marshmallow schema obj

    """
    # get random data based on marshmallow type
    return {
        field: SPEC_TYPE_LOOKUP[type(val)] for field, val in schema_obj().fields.items()
    }


class UnAuth401Schema(Schema):
    """Datafeed schema."""

    # data_source = Str(required=True)
    # data_type = Str(required=True, validate=validate.OneOf(DATA_TYPES))
    # feed_id = Int(required=True, description="ID of the datafeed")
    # feed_type = Str(required=True, validate=validate.OneOf(FEED_TYPES))
    # file_extension = Str(required=True, validate=validate.OneOf(FILE_EXTENSIONS))
    code = Int(name="code", example=401)
    message = Str(name="message", example="Access token is missing or invalid")
