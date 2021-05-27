"""
Schemas for the Customer Profiles API
"""


from flask_marshmallow import Schema
from marshmallow import fields


class CustomerProfilesOverviewSchema(Schema):
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
