# pylint: disable=no-self-use
"""
Schemas for the Customers API
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, Float, DateTime, Boolean, List, Nested
from huxunify.api.schema.utils import (
    validate_object_id,
)


class DataSource(Schema):
    """Data Source Schema"""

    id = Str(validate=validate_object_id, required=True)
    name = Str(required=True)
    type = Str(required=True)
    percentage = Float(required=True)


class Resolution(Schema):
    """Resolution Schema"""

    percentage = Float(required=True)
    data_sources = List(cls_or_instance=DataSource, required=True)


class IdentityResolution(Schema):
    """Identity Resolution Schema"""

    name = Nested(Resolution, required=True)
    address = Nested(Resolution, required=True)
    email = Nested(Resolution, required=True)
    phone = Nested(Resolution, required=True)
    cookie = Nested(Resolution, required=True)


class CustomerProfileSchema(Schema):
    """Customer Profile Schema"""

    id = Str(required=True)
    first_name = Str(required=True)
    last_name = Str(required=True)
    match_confidence = Float(required=True)
    since = DateTime(required=True)
    ltv_actual = Float(required=True)
    ltv_predicted = Float(required=True)
    conversion_time = DateTime(required=True)
    churn_rate = Float(required=True)
    last_click = DateTime(required=True)
    last_purchase = DateTime(required=True)
    last_email_open = DateTime(required=True)
    email = Str(required=True)
    phone = Str(required=True)
    age = Int(required=True)
    gender = Str(required=True)
    address = Str(required=True)
    city = Str(required=True)
    state = Str(required=True)
    zip = Str(required=True)
    preference_email = Boolean(required=True)
    preference_push = Boolean(required=True)
    preference_sms = Boolean(required=True)
    preference_in_app = Boolean(required=True)
    identity_resolution = Nested(IdentityResolution, required=True)
    propensity_to_unsubscribe = Float(required=True)
    propensity_to_purchase = Float(required=True)
