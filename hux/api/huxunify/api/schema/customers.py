# pylint: disable=no-self-use
"""
Schemas for the Customers API
"""
from datetime import datetime

from flask_marshmallow import Schema
from marshmallow.fields import (
    Str,
    Float,
    Boolean,
    List,
    Nested,
    Integer,
    Dict,
)
from huxunifylib.database import constants as db_c
from huxunify.api.schema.utils import (
    validate_object_id,
)
from huxunify.api.schema.custom_schemas import DateTimeWithZ
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

    hux_id = Str(required=True, attribute=api_c.ID)
    first_name = Str(required=True)
    last_name = Str(required=True)
    match_confidence = Float(required=True)
    since = DateTimeWithZ(required=True)
    ltv_actual = Float(required=True)
    ltv_predicted = Float(required=True)
    conversion_time = Float(required=True)
    churn_rate = Float(required=True)
    last_click = DateTimeWithZ(required=True)
    last_purchase = DateTimeWithZ(required=True)
    last_email_open = DateTimeWithZ(required=True)
    email = Str(required=True)
    phone = Str(required=True)
    # redacted age to a string.
    age = Str(required=True)
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


class CustomerOverviewSchema(Schema):
    """Customer Profile Overview Schema"""

    total_records = Integer(required=True)
    match_rate = Float(required=True)
    total_unique_ids = Integer(required=True)
    total_unknown_ids = Integer(required=True)
    total_known_ids = Integer(required=True)
    total_individual_ids = Integer(required=True)
    total_household_ids = Integer(required=True)
    updated = DateTimeWithZ(required=True)
    total_customers = Integer(required=True)
    total_countries = Integer(required=True)
    total_us_states = Integer(required=True)
    total_cities = Integer(required=True)
    min_age = Integer(required=True)
    max_age = Integer(required=True)
    avg_age = Integer(required=True)
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
                api_c.HUX_ID: "1531-2039-22",
                api_c.FIRST_NAME: "Bertie",
                api_c.LAST_NAME: "Fox",
                api_c.MATCH_CONFIDENCE: 0.96666666661,
            }
        ],
    )


class DataFeedSchema(Schema):
    """
    Customer Datafeed Schema
    """

    datafeed_id = Str(example="60e879d270815aade4d6c4fb")
    datafeed_name = Str(example="Really_long_Feed_Name_106")
    data_source_type = Str(example=db_c.DELIVERY_PLATFORM_SFMC)
    new_ids_generated = Integer(example=21)
    num_records_processed = Integer(example=2000000)
    match_rate = Float(example=0.98)
    last_run = DateTimeWithZ()


class DataFeedPinning(Schema):
    """IDR Data feed pinning schema"""

    input_records = Integer(required=True, example=2)
    output_records = Integer(required=True, example=2)
    empty_records = Integer(required=True, example=0)
    individual_id_match = Integer(required=True, example=1)
    household_id_match = Integer(required=True, example=1)
    company_id_match = Integer(required=True, example=1)
    address_id_match = Integer(required=True, example=1)
    db_reads = Integer(required=True, example=1)
    db_writes = Integer(required=True, example=1)
    filename = Str(required=True, example="Input.csv")
    new_individual_ids = Integer(required=True, example=1)
    new_household_ids = Integer(required=True, example=1)
    new_company_ids = Integer(required=True, example=1)
    new_address_ids = Integer(required=True, example=1)
    process_time = Float(required=True, example=6.43)
    date_time = DateTimeWithZ(required=True, example=datetime.now())


class DataFeedStitched(Schema):
    """IDR Data feed stitched schema"""

    digital_ids_added = Integer(required=True, example=3)
    digital_ids_merged = Integer(required=True, example=6)
    match_rate = Float(required=True, example=0.6606)
    merge_rate = Float(required=True, example=0.0)
    records_source = Str(required=True, example="Input Waterfall")
    time_stamp = DateTimeWithZ(required=True, example=datetime.now())


class DataFeedDetailsSchema(Schema):
    """IDR Data feed schema"""

    pinning = Nested(DataFeedPinning, required=True)
    stitched = Nested(DataFeedStitched, required=True)


class CustomerGeoVisualSchema(Schema):
    """Customer Geographic Visual Schema"""

    class Meta:
        """Meta class for Schema"""

        ordered = True

    name = Str(required=True, example="California")
    population_percentage = Float(required=True, example=0.3031)
    size = Integer(required=True, example=28248560)
    gender_women = Float(required=True, example=0.50)
    gender_men = Float(required=True, example=0.49)
    gender_other = Float(required=True, example=0.01)
    ltv = Float(required=True, example=3848.50)


class GenderMetrics(Schema):
    """Gender metrics schema"""

    population_percentage = Float(required=True, example=0.4601)
    size = Integer(required=True, example=123456)


class CustomerGenderInsightsSchema(Schema):
    """Customer Gender Insights Schema"""

    gender_women = Nested(GenderMetrics, required=True)
    gender_men = Nested(GenderMetrics, required=True)
    gender_other = Nested(GenderMetrics, required=True)


class CustomerIncomeInsightsSchema(Schema):
    """Customer Income Insights Schema"""

    name = Str(required=True, example="New York")
    ltv = Float(required=True, example=1235.31)


class CustomerSpendSchema(Schema):
    """Customer Spend Schema"""

    date = DateTimeWithZ(required=True)
    ltv = Float(required=True, example=1235.31)


class CustomerSpendingInsightsSchema(Schema):
    """Customer Spending Insights Schema"""

    gender_women = List(Nested(CustomerSpendSchema))
    gender_men = List(Nested(CustomerSpendSchema))
    gender_other = List(Nested(CustomerSpendSchema))


class CustomerDemographicInsightsSchema(Schema):
    """Customer Demographic Insights Schema"""

    gender = Nested(CustomerGenderInsightsSchema)
    income = List(Nested(CustomerIncomeInsightsSchema))
    spend = Nested(CustomerSpendingInsightsSchema)


class MatchingTrendsSchema(Schema):
    """IDR Matching Trends Schema"""

    class Meta:
        """Meta class for Schema"""

        ordered = True

    date = DateTimeWithZ(required=True)
    known_ids = Integer(required=True, example=100000)
    unique_hux_ids = Integer(required=True, example=100000)
    anonymous_ids = Integer(required=True, example=100000)


class CustomerEventCountSchema(Schema):
    """Customer Event with Count Schema"""

    class Meta:
        """Meta class for Schema"""

        ordered = True

    abandoned_cart = Integer(required=True, example=1)
    viewed_cart = Integer(required=True, example=1)
    customer_login = Integer(required=True, example=1)
    viewed_checkout = Integer(required=True, example=1)
    viewed_sale_item = Integer(required=True, example=1)
    item_purchased = Integer(required=True, example=1)
    trait_computed = Integer(required=True, example=1)


class CustomerEventsSchema(Schema):
    """Customer Events Schema"""

    date = DateTimeWithZ(required=True)
    total_event_count = Integer(required=True, example=5)
    event_type_counts = Nested(CustomerEventCountSchema)


class TotalCustomersInsightsSchema(Schema):
    """Total customer insights Schema"""

    class Meta:
        """Meta class for Schema"""

        ordered = True

    date = DateTimeWithZ(required=True, attribute=api_c.RECORDED)
    total_customers = Integer(
        required=True, attribute=api_c.TOTAL_COUNT, example=5
    )
    new_customers_added = Integer(
        required=True, attribute=api_c.DIFFERENCE_COUNT, example=5
    )


class CustomersInsightsCitiesSchema(Schema):
    """City-level customer insights schema"""

    city = Str(required=True, example="New York City")
    state = Str(required=True, example="NY")
    size = Integer(
        attribute=api_c.CUSTOMER_COUNT, required=True, default=0, example=1234
    )
    spending = Float(
        attribute=api_c.AVG_LTV, required=True, default=0.0, example=123.231
    )


class CustomersInsightsStatesSchema(Schema):
    """State-level customer insights schema"""

    state = Str(attribute=api_c.NAME, required=True, example="New York")
    size = Integer(required=True, default=0, example=1234)
    spending = Float(
        attribute=api_c.LTV, required=True, default=0.0, example=123.2345
    )
