"""Schemas for the Configurations Object"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Boolean
from marshmallow.validate import OneOf

from huxunifylib.database import constants as db_c

from huxunify.api.constants import APPLICATION_CATEGORIES, UNCATEGORIZED
from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api.schema.utils import (
    validate_object_id,
)


class ApplicationsPostSchema(Schema):
    """Applications post schema class"""

    category = Str(required=True, validate=OneOf(APPLICATION_CATEGORIES))
    name = Str(required=True)
    url = Str(required=True)


class ApplicationsGETSchema(Schema):
    """Applications GET Schema"""

    id = Str(attribute=db_c.ID, validate=validate_object_id, required=True)
    category = Str()
    name = Str()
    url = Str()
    type = Str(default=UNCATEGORIZED)
    is_added = Boolean()
    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME, allow_none=True)
    update_time = DateTimeWithZ(attribute=db_c.UPDATE_TIME, allow_none=True)


class ApplicationsPatchSchema(Schema):
    """Applications Patch Schema"""

    url = Str()
    is_added = Boolean(default=True)
