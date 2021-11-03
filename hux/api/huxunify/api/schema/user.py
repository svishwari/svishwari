"""Schemas for the User API"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, validate, List, Nested, Dict, Bool
from marshmallow.validate import OneOf

from huxunifylib.database import constants as db_c
from huxunify.api.schema.utils import validate_object_id
from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api import constants as api_c


class Favorites(Schema):
    """Favorites Schema"""

    campaigns = List(Str(), default=[])
    audiences = List(Str(), default=[])
    destinations = List(Str(), default=[])
    engagements = List(Str(), default=[])


class UserSchema(Schema):
    """User Schema"""

    _id = Str(
        data_key=api_c.ID,
        example="5f5f7262997acad4bac4373b",
        required=True,
        validate=validate_object_id,
    )
    email = Str(required=True, attribute="email_address")
    display_name = Str(example="Joe M")
    first_name = Str()
    last_name = Str()
    phone_number = Str()
    access_level = Str()
    role = Str(required=True, validate=validate.OneOf(db_c.USER_ROLES))
    pii_access = Bool(default=False)
    organization = Str()
    subscriptions = List(Str())
    dashboard_configuration = Dict()
    favorites = Nested(Favorites, required=True)
    profile_photo = Str()
    login_count = Int(required=True, default=0, example=10)
    last_login = DateTimeWithZ(required=True, attribute=db_c.UPDATE_TIME)
    modified = DateTimeWithZ(required=True)


class UserPatchSchema(Schema):
    """User patch schema"""

    role = Str(required=False)
    display_name = Str(required=False)
    dashboard_configuration = Dict(required=False)
    pii_access = Bool(required=False)


class TicketSchema(Schema):
    """Ticket schema"""

    type = Str(required=True, validate=OneOf([api_c.TICKET_TYPE_BUG]))
    summary = Str(required=True)
    description = Str(required=False)


class TicketGetSchema(Schema):
    """Ticket get schema"""

    id = Int(example=1)
    key = Str(example="ABC-123")
    type = Str(example=api_c.TICKET_TYPE_BUG)
    summary = Str(example="Audience and Engagement Dashboard not loading")
    description = Str(example="Description of the issue.")
