"""
purpose of this file is to house schema utilities
"""
import uuid
from datetime import datetime, timedelta
import random
from flask_marshmallow import Schema
from marshmallow.fields import Boolean, DateTime, Int, Str, Float


# get random data back based on marshmallow field type
SPEC_TYPE_LOOKUP: dict = {
    Boolean: bool(random.getrandbits(1)),
    DateTime: datetime.now() + timedelta(random.randint(0, 1e4)),
    Int: random.randint(0, 1e4),
    Str: str(uuid.uuid4()),
    Float: random.random(),
}


def generate_synthetic_marshmallow_data(schema_obj: Schema) -> Schema:
    """This function generates synthetic data for marshmallow

    Args:
        schema_obj (Schema): a marshmallow schema object

    Returns:
        Response: dynamic object based on schema

    """
    # get random data based on marshmallow type
    return {
        field: SPEC_TYPE_LOOKUP[type(val)] for field, val in schema_obj().fields.items()
    }
