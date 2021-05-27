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

    id = Str(validate=validate_object_id)
    name = Str()
    type = Str()
    percentage = Float()


class Resolution(Schema):
    """Resolution Schema"""

    percentage = Float()
    data_sources = List(cls_or_instance=DataSource)


class IdentityResolution(Schema):
    """Identity Resolution Schema"""

    name = Nested(Resolution)
    address = Nested(Resolution)
    email = Nested(Resolution)
    phone = Nested(Resolution)
    cookie = Nested(Resolution)


class CustomerProfileSchema(Schema):
    """Customer Profile Schema"""

    id = Str()
    first_name = Str()
    last_name = Str()
    match_confidence = Float()
    since = DateTime()
    ltv_actual = Float()
    ltv_predicted = Float()
    conversion_time = DateTime()
    churn_rate = Float()
    last_click = DateTime()
    last_purchase = DateTime()
    last_email_open = DateTime()
    email = Str()
    phone = Str()
    age = Int()
    gender = Str()
    address = Str()
    city = Str()
    state = Str()
    zip = Str()
    preference_email = Boolean()
    preference_push = Boolean()
    preference_sms = Boolean()
    preference_in_app = Boolean()
    identity_resolution = Nested(IdentityResolution)
    propensity_to_unsubscribe = Float()
    propensity_to_purchase = Float()
