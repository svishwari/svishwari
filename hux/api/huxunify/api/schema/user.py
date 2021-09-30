"""Schemas for the User API"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, validate, List, Nested, Dict

from huxunifylib.database.constants import USER_ROLES
from huxunify.api.schema.utils import validate_object_id
from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api import constants as api_c


class Favorites(Schema):
    """Favorites Schema"""

    campaigns = List(Str())
    audiences = List(Str())
    destinations = List(Str())
    engagements = List(Str())


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
    role = Str(required=True, validate=validate.OneOf(USER_ROLES))
    organization = Str()
    subscriptions = List(Str())
    dashboard_configuration = Dict()
    favorites = Nested(Favorites, required=True)
    profile_photo = Str()
    login_count = Int()
    modified = DateTimeWithZ(required=True)
