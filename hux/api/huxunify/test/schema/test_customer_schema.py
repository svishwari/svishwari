"""Customer data related schema tests"""
from datetime import datetime
from unittest import TestCase

from huxunifylib.database import constants as db_c

from huxunify.api.schema.customers import DatafeedSchema


class TestIDRDatafeedSchema(TestCase):
    """
    Test customer data related schemas
    """

    def test_datafeed_schema(self) -> None:
        """
        Test datafeed schema
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

        datafeed = DatafeedSchema().load(doc)

        self.assertIsInstance(datafeed["last_run"], datetime)
        assert DatafeedSchema().validate(doc) == {}
