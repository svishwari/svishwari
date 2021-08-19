"""Customer data related schema tests"""
from datetime import datetime
from unittest import TestCase

from huxunifylib.database import constants as db_c

from huxunify.api import constants as api_c
from huxunify.api.schema.customers import (
    DataFeedSchema,
    TotalCustomersInsightsSchema,
)


class CustomerSchemaTest(TestCase):
    """
    Test customer data related schemas
    """

    def test_idr_datafeed_schema(self) -> None:
        """Test idr datafeed schema.

        Args:

        Returns:
            None
        """

        doc = dict(
            datafeed_id="60e879d270815aade4d6c4fb",
            datafeed_name="Really_long_Feed_Name_106",
            data_source_type=db_c.DELIVERY_PLATFORM_SFMC,
            new_ids_generated=21,
            num_records_processed=2000000,
            match_rate=0.98,
            last_run=datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        )

        datafeed = DataFeedSchema().load(doc)

        self.assertIsInstance(datafeed["last_run"], datetime)
        self.assertFalse(DataFeedSchema().validate(doc))

    def test_total_customer_insights_schema(self) -> None:
        """Test total customers insights schema.

        Args:

        Returns:
            None
        """

        customer_count_doc = {
            api_c.DATE: "2021-04-01T00:00:00.000Z",
            api_c.TOTAL_CUSTOMERS: 105080,
            api_c.NEW_CUSTOMERS_ADDED: 4321,
        }

        self.assertFalse(
            TotalCustomersInsightsSchema().validate(customer_count_doc)
        )
