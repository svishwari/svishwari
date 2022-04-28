"""Schemas for the Configurations Object"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Boolean, Nested, List, Dict

from huxunifylib.database import constants as db_c
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
    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME, allow_none=True)
    created_by = Str(attribute=db_c.CREATED_BY, allow_none=True)
    update_time = DateTimeWithZ(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = Str(attribute=db_c.UPDATED_BY, allow_none=True)


class NavigationSettings(Schema):
    """Navigation Setting"""

    name = Str()
    enabled = Boolean()
    icon = Str()
    children = List(Dict())


class NavigationSettingsSchema(Schema):
    """Navigation Settings Schema"""

    settings = List(Nested(NavigationSettings))
