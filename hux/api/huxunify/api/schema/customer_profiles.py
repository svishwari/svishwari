"""
Schemas for the Customer Profiles API
"""


from flask_marshmallow import Schema
from marshmallow.fields import Str, Int,Float,DateTime


class CustomerProfilesOverview(Schema):
    """Customer Profile Overview Schema"""

    total_records=Int(required=True)
    match_rate=Float(required=True)
    total_unique_ids=Int(required=True)
    total_unknown_ids=Int(required=True)
    total_known_ids=Int(required=True)
    total_individual_ids=Int(required=True)
    total_household_ids=Int(required=True)
    updated=DateTime(required=True)
    total_customers=Int(required=True)
    total_countries=Int(required=True)
    total_us_states=Int(required=True)
    total_cities=Int(required=True)
    min_age=Int(required=True)
    max_age=Int(required=True)
    gender_women=Float(required=True)
    gender_men=Float(required=True)
    gender_other=Float(required=True)

