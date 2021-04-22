"""
Schemas for the User API
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, validate, List, DateTime, Nested, Dict

from huxunify.api.schema.utils import validate_object_id
from huxunifylib.database.constants import USER_ROLES


class Favorites(Schema):
    """Favorites Schema"""

    campaigns = List(Str())
    audiences = List(Str())
    destinations = List(Str())


class UserSchema(Schema):
    """User Schema"""

    user_id = Str(required=True, validate=validate_object_id)
    email = Str(required=True)
    first_name = Str()
    last_name = Str()
    role = Str(required=True, validate=validate.OneOf(USER_ROLES))
    organization = Str()
    subscriptions = List(Str())
    dashboard_configuration = Dict()
    favorites = Nested(Favorites, required=True)
    profile_photo = Str()
    login_count = Int()
    modified = DateTime(required=True)
