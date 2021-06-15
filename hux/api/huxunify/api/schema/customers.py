# pylint: disable=no-self-use
"""
Schemas for the Customers API
"""
from datetime import datetime
from dateutil import parser
from flask_marshmallow import Schema
from marshmallow import pre_dump
from marshmallow.fields import (
    Str,
    Int,
    Float,
    DateTime,
    Boolean,
    List,
    Nested,
    Integer,
    Dict,
)
from huxunify.api.schema.utils import (
    validate_object_id,
)
import huxunify.api.constants as api_c


class DataSource(Schema):
    """Data Source Schema"""

    id = Str(validate=validate_object_id, required=True)
    name = Str(required=True)
    type = Str(required=True)
    percentage = Float(required=True)


class Resolution(Schema):
    """Resolution Schema"""

    percentage = Float(required=True)
    data_sources = List(cls_or_instance=Nested(DataSource), required=True)


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

    @pre_dump
    # pylint: disable=unused-argument
    def pre_process_details(self, data, **kwarg):
        """process the schema before serializing.

        Args:
            data (dict): The CustomerProfile data source object
            many (bool): If there are many to process
        Returns:
            Response: Returns a CustomerProfile data source object

        """

        # resolve datetime fields
        # TODO HUS-360 - this should not be an issue when we pull from CDM.
        for field in [
            "last_click",
            "last_purchase",
            "last_email_open",
            "since",
            "conversion_time",
        ]:
            # convert the string to datetime as marshmallow is expecting a
            # datetime obj.
            if field in data and not isinstance(data[field], datetime):
                data[field] = parser.parse(data[field])

        return data


class CustomerOverviewSchema(Schema):
    """Customer Profile Overview Schema"""

    total_records = Integer(required=True)
    match_rate = Float(required=True)
    total_unique_ids = Integer(required=True)
    total_unknown_ids = Integer(required=True)
    total_known_ids = Integer(required=True)
    total_individual_ids = Integer(required=True)
    total_household_ids = Integer(required=True)
    updated = DateTime(required=True)
    total_customers = Integer(required=True)
    total_countries = Integer(required=True)
    total_us_states = Integer(required=True)
    total_cities = Integer(required=True)
    min_age = Integer(required=True)
    max_age = Integer(required=True)
    gender_women = Float(required=True)
    gender_men = Float(required=True)
    gender_other = Float(required=True)
    min_ltv_predicted = Float(required=True)
    max_ltv_predicted = Float(required=True)
    min_ltv_actual = Float(required=True)
    max_ltv_actual = Float(required=True)


class CustomersSchema(Schema):
    """Customers Schema"""

    total_customers = Integer(required=True, example=827438924)
    customers = List(
        Dict(),
        example=[
            {
                api_c.ID: "1531-2039-22",
                api_c.FIRST_NAME: "Bertie",
                api_c.LAST_NAME: "Fox",
                api_c.MATCH_CONFIDENCE: 0.96666666661,
            }
        ],
    )
