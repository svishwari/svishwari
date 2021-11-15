"""Schemas for the Configurations Object"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Boolean

from huxunifylib.database import constants as c
from huxunify.api.schema.custom_schemas import DateTimeWithZ


class ConfigurationsSchema(Schema):
    """Configurations Schema"""

    id = Str()
    name = Str(required=True)
    icon = Str()
    type = Str()
    description = Str()
    status = Str()
    enabled = Boolean()
    roadmap = Boolean()
    create_time = DateTimeWithZ(attribute=c.CREATE_TIME, allow_none=True)
    created_by = Str(attribute=c.CREATED_BY, allow_none=True)
    update_time = DateTimeWithZ(attribute=c.UPDATE_TIME, allow_none=True)
    updated_by = Str(attribute=c.UPDATED_BY, allow_none=True)
