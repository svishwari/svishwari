"""
Schemas for the User API
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, validate, List, DateTime, Boolean, Nested

ROLES = ["user", "super-admin", "admin", "viewer"]


class Favorites(Schema):
    """Favorites Schema"""

    campaigns = List(Str())
    audiences = List(Str())
    destinations = List(Str())


class DashBoardConfiguration(Schema):
    """Dashboard Schema"""

    configure_hux = Boolean(required=True)
    activity = Boolean(required=True)
    data_mgmt_overview = Boolean(required=True)
    key_perf_insights = Boolean(required=True)
    customer_insights = Boolean(required=True)


class User(Schema):
    """User Schema"""

    email = Str(required=True)
    display_name = Str(required=True)
    role = Str(required=True, validate=validate.OneOf(ROLES))
    organization = Str(required=True)
    # subscriptions = List(Str())
    dashboard_configuration = Nested(DashBoardConfiguration, required=True)
    favorites = Nested(Favorites, required=True)
    profile_photo = Str()
    login_count = Int()
    modified = DateTime(required=True)
