"""
Schemas for the Customer Profiles API
"""


from flask_marshmallow import Schema
from marshmallow import fields
from huxunify.api import constants as api_c


class CustomerOverviewSchema(Schema):
    """Customer Profile Overview Schema"""

    total_records = fields.Integer(required=True)
    match_rate = fields.Float(required=True)
    total_unique_ids = fields.Integer(required=True)
    total_unknown_ids = fields.Integer(required=True)
    total_known_ids = fields.Integer(required=True)
    total_individual_ids = fields.Integer(required=True)
    total_household_ids = fields.Integer(required=True)
    updated = fields.DateTime(required=True)
    total_customers = fields.Integer(required=True)
    total_countries = fields.Integer(required=True)
    total_us_states = fields.Integer(required=True)
    total_cities = fields.Integer(required=True)
    min_age = fields.Integer(required=True)
    max_age = fields.Integer(required=True)
    gender_women = fields.Float(required=True)
    gender_men = fields.Float(required=True)
    gender_other = fields.Float(required=True)
    min_ltv_predicted = fields.Float(required=True)
    max_ltv_predicted = fields.Float(required=True)
    min_ltv_actual = fields.Float(required=True)
    max_ltv_actual = fields.Float(required=True)


class CustomersSchema(Schema):
    """Customers Schema"""

    total_customers = fields.Integer(required=True, example=827438924)
    customers = fields.List(
        fields.Dict(),
        example=[
            {
                api_c.ID: "1531-2039-22",
                api_c.FIRST_NAME: "Bertie",
                api_c.LAST_NAME: "Fox",
                api_c.MATCH_CONFIDENCE: 0.96666666661,
            }
        ],
    )
