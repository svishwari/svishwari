"""Schemas for the Configurations Object"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Boolean

from huxunifylib.database import constants as db_c
from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api.schema.utils import (
    validate_object_id,
)


class ApplicationsPostSchema(Schema):
    """Applications post schema class"""

    category = Str(required=True)
    type = Str(required=True)
    name = Str(required=True)
    url = Str(required=True)


class ApplicationsGETSchema(Schema):
    """Applications GET Schema"""

    id = Str(attribute=db_c.ID, validate=validate_object_id, required=True)
    category = Str()
    type = Str()
    name = Str()
    url = Str()
    status = Str()
    added = Boolean()
    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME, allow_none=True)
    created_by = Str(attribute=db_c.CREATED_BY, allow_none=True)
    update_time = DateTimeWithZ(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = Str(attribute=db_c.UPDATED_BY, allow_none=True)


class ApplicationsPatchSchema(Schema):
    """Applications Patch Schema"""

    url = Str()
