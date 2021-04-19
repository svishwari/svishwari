"""
Purpose of this file is testing the cdm model class
"""
from unittest import TestCase
from unittest.mock import Mock
from huxunify.api.data_connectors.snowflake_client import SnowflakeClient
from huxunify.api.model.cdm import CdmModel
from huxunify.api.schema.cdm import ProcessedData
from huxunify.api.schema.utils import generate_synthetic_marshmallow_data


class CdmTest(TestCase):
    """
    Test CDM database querying
    """

    datafeeds = [
        [
            1,
            "Batch",
            "Salesforce",
            "Customers",
            ".csv",
            "Y",
            "2021-01-21 05:30:48.301",
        ],
        [
            1,
            "adobe",
            "Salesforce",
            "Customers",
            ".csv",
            "Y",
            "2021-01-21 05:30:48.301",
        ],
    ]
    mappings = [
        [1, "FNAME", "FIRST", "2021-01-21 05:31:36.094"],
        [2, "FNAME", "FIRST_NAME", "2021-01-21 05:31:37.072"],
    ]
    datafeed_fields = [
        "feed_id",
        "feed_type",
        "data_source",
        "data_type",
        "file_extension",
        "is_pii",
        "modified",
    ]
    mapping_fields = ["field_id", "field_name", "field_variation", "modified"]

    def setUp(self):
        """
        Setup initial model and database connection
        """
        mock_client = Mock(spec=SnowflakeClient)
        self.model = CdmModel(mock_client)

    def test_get_processed_data(self):
        """Test Retrieving the processed data sources.

        Returns:
            Response: bool - pass/fail.

        """
        # fields only used for this test
        test_fields = ("created", "modified", "source_name")

        # get synth data
        processed_data = [
            generate_synthetic_marshmallow_data(ProcessedData).fromkeys(
                test_fields
            )
            for i in range(4)
        ]
        self.model.ctx.cursor().fetchall.return_value = processed_data

        # get the returned sources
        returned_sources = self.model.read_processed_sources()

        # ensure count for first test
        self.assertEqual(len(returned_sources), len(processed_data))

        # pull the keys we need and test to ensure it pulled them
        self.assertEqual(returned_sources, processed_data)

    def test_get_processed_data_by_name(self):
        """Test Retrieving the processed data source by name.

        Returns:
            Response: bool - pass/fail.

        """
        # get synth data
        processed_data = generate_synthetic_marshmallow_data(ProcessedData)
        self.model.ctx.cursor().fetchone.return_value = processed_data

        # get the returned sources
        returned_source = self.model.read_processed_source_by_name(
            processed_data["source_name"]
        )

        # ensure dict is the same
        self.assertDictEqual(returned_source, processed_data)

    def test_read_datafeeds(self):
        """
        Successfully retrieve datafeeds
        """
        self.model.ctx.cursor().fetchall.return_value = CdmTest.datafeeds
        returned_feeds = self.model.read_datafeeds()

        for feed in returned_feeds:
            self.assertCountEqual(feed, CdmTest.datafeed_fields)

        self.assertEqual(2, len(returned_feeds))
        self.assertEqual("Batch", returned_feeds[0]["feed_type"])
        self.assertEqual("adobe", returned_feeds[1]["feed_type"])

    def test_read_datafeeds_by_id(self):
        """
        Successfully retrieve single datafeed
        """
        self.model.ctx.cursor().fetchone.return_value = CdmTest.datafeeds[0]

        returned_feed = self.model.read_datafeed_by_id(1)
        self.assertCountEqual(returned_feed, CdmTest.datafeed_fields)
        self.assertEqual("Batch", returned_feed["feed_type"])

    def test_read_fieldmappings(self):
        """
        Successfully retrieve field mappings
        """
        self.model.ctx.cursor().fetchall.return_value = CdmTest.mappings

        returned_mappings = self.model.read_fieldmappings()
        for mapping in returned_mappings:
            self.assertCountEqual(mapping, CdmTest.mapping_fields)

        self.assertEqual(2, len(returned_mappings))
        self.assertEqual(1, returned_mappings[0]["field_id"])
        self.assertEqual(2, returned_mappings[1]["field_id"])

    def test_read_fieldmappings_by_id(self):
        """
        Successfully retrieve field mappings by id
        """
        self.model.ctx.cursor().fetchone.return_value = CdmTest.mappings[0]

        returned_mapping = self.model.read_fieldmapping_by_id(1)

        self.assertCountEqual(returned_mapping, CdmTest.mapping_fields)
        self.assertEqual(1, returned_mapping["field_id"])
