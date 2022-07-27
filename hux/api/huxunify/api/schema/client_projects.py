"""Schemas for the Client Project Object."""

from flask_marshmallow import Schema
from marshmallow.fields import Str
from marshmallow.validate import OneOf

from huxunifylib.database import constants as db_c
from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api.schema.utils import (
    validate_object_id,
)


class ClientProjectGetSchema(Schema):
    """Client Project GET Schema."""

    id = Str(attribute=db_c.ID, validate=validate_object_id, required=True)
    type = Str()
    name = Str()
    description = Str()
    icon = Str()
    url = Str()
    access_level = Str(
        validate=OneOf(
            choices=[
                db_c.USER_ROLE_ADMIN,
                db_c.USER_ROLE_EDITOR,
                db_c.USER_ROLE_VIEWER,
            ]
        ),
        default=db_c.USER_ROLE_VIEWER,
        required=True,
    )
    created_by = Str(attribute=db_c.CREATED_BY, allow_none=True)
    updated_by = Str(attribute=db_c.UPDATED_BY, allow_none=True)
    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME, allow_none=True)
    update_time = DateTimeWithZ(attribute=db_c.UPDATE_TIME, allow_none=True)


class ClientProjectPatchSchema(Schema):
    """Client Project Patch Schema."""

    url = Str()


class ClientDetailsSchema(Schema):
    """Client Details Schema."""

    name = Str(required=True, example="Retail Co", default="Retail Co")
    logo = Str(required=True, example="client", default="client")
