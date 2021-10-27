"""Customer data related schema tests."""
from datetime import datetime
from unittest import TestCase

from huxunifylib.database import constants as db_c

from huxunify.api import constants as api_c
from huxunify.api.schema.customers import (
    CustomerOverviewSchema,
    DataFeedSchema,
    TotalCustomersInsightsSchema,
)


class CustomerSchemaTest(TestCase):
    """Test customer data related schemas."""

    def test_idr_datafeed_schema(self) -> None:
        """Test IDR DataFeedSchema."""

        doc = dict(
            datafeed_id="1",
            datafeed_name="Really_long_Feed_Name_106",
            data_source_type=db_c.CDP_DATA_SOURCE_BLUECORE,
            data_source_name=db_c.CDP_DATA_SOURCE_BLUECORE.title(),
            new_ids_generated=21,
            num_records_processed=2000000,
            match_rate=0.98,
            last_run="2021-08-05T14:44:42.694Z",
        )

        datafeed = DataFeedSchema().load(doc)

        self.assertIsInstance(datafeed["timestamp"], datetime)
        self.assertFalse(DataFeedSchema().validate(doc))

    def test_total_customer_insights_schema(self) -> None:
        """Test TotalCustomersInsightsSchema."""

        customer_count_doc = {
            api_c.DATE: "2021-04-01T00:00:00.000Z",
            api_c.TOTAL_CUSTOMERS: 105080,
            api_c.NEW_CUSTOMERS_ADDED: 4321,
            api_c.CUSTOMERS_LEFT: -4321,
        }

        self.assertFalse(
            TotalCustomersInsightsSchema().validate(customer_count_doc)
        )

    def test_customers_overview_schema(self) -> None:
        """Test CustomerOverviewSchema."""

        customer = {
            api_c.TOTAL_RECORDS: 10,
            api_c.MATCH_RATE: 0.42,
            api_c.TOTAL_UNIQUE_IDS: 10,
            api_c.TOTAL_UNKNOWN_IDS: 2,
            api_c.TOTAL_KNOWN_IDS: 8,
            api_c.TOTAL_INDIVIDUAL_IDS: 5,
            api_c.TOTAL_HOUSEHOLD_IDS: 5,
            api_c.UPDATED: "2021-04-01T00:00:00.000Z",
            api_c.TOTAL_CUSTOMERS: 105080,
            api_c.TOTAL_COUNTRIES: 1,
            api_c.TOTAL_STATES: 42,
            api_c.TOTAL_CITIES: 60,
            api_c.MIN_AGE: 23,
            api_c.MAX_AGE: 65,
            api_c.AVERAGE_AGE: 40,
            api_c.GENDER_MEN: 0.45,
            api_c.GENDER_WOMEN: 0.53,
            api_c.GENDER_OTHER: 0.2,
            api_c.GENDER_MEN_COUNT: 53001,
            api_c.GENDER_WOMEN_COUNT: 65845,
            api_c.GENDER_OTHER_COUNT: 2453,
            api_c.MIN_LTV_PREDICTED: 0.34,
            api_c.MAX_LTV_PREDICTED: 0.45,
            api_c.MIN_LTV_ACTUAL: 0.36,
            api_c.MAX_LTV_ACTUAL: 0.42,
        }

        self.assertFalse(CustomerOverviewSchema().validate(customer))
