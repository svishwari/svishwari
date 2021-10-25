"""Schemas for the User API"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, validate, List, Nested, Dict

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

    role = Str(required=False) # Should this be editable?
    organization = Str(required=False) # Should this be editable?
    subscription = List(Str(), default=[], required=False)
    profile_photo = Str(required=False) # is this going to be editable from our portal?
    dashboard_configuration = Dict(required=False) # should this be editable from this endpoint and does it have a schema?
