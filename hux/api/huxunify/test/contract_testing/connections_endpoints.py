"""Tests to generate contracts for  CDP Connections/Identity API endpoints."""
import unittest
import atexit
from datetime import datetime
from pathlib import Path

import requests
from dateutil.relativedelta import relativedelta
from pact import Consumer, Provider, EachLike, Like
from pact.matchers import get_generated_values

import huxunify.test.constants as t_c
import huxunify.api.constants as api_c

# Folder where generated pacts are saved
CONTRACTS_FOLDER = (
    Path(__file__)
    .parent.joinpath(t_c.CONTRACTS_DIR)
    .joinpath(t_c.CDP_CONNECTIONS_CONTRACTS_DIR)
)

# Initializing pact
PACT = Consumer(t_c.HUX).has_pact_with(
    Provider(t_c.CDP_CONNECTIONS), pact_dir=str(CONTRACTS_FOLDER)
)
PACT.start_service()

atexit.register(PACT.stop_service)


class CDPConnectionsContracts(unittest.TestCase):
    """Generate pact contracts for CDP connections endpoints."""

    def setUp(self) -> None:
        """Setup tests."""

        self.data_source_name = "bluecore"
        self.data_source_label = "Bluecore"
        self.data_source_status = "Active"
        self.data_source_data_feed_name = "bluecore_email_clicks"
        self.timestamp = "2021-08-16T12:17:24.628Z"

    def test_get_data_sources(self):
        """Test get data sources endpoint to generate pact contract."""

        expected = {
            "code": 200,
            "message": "Data Sources Fetched successfully",
            "body": EachLike(
                {
                    "name": Like(self.data_source_name),
                    "label": Like(self.data_source_label),
                    "status": Like(self.data_source_status),
                }
            ),
        }

        (
            PACT.given("No filters passed.")
            .upon_receiving("A request to get data sources.")
            .with_request(
                method="GET",
                path=t_c.CDP_CONNECTIONS_DATA_SOURCES_ENDPOINT,
                body={},
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with PACT:
            result = requests.get(
                PACT.uri + t_c.CDP_CONNECTIONS_DATA_SOURCES_ENDPOINT,
                json={},
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))

    def test_get_data_source_data_feeds(self):
        """Test get data source's data feeds endpoint to generate pact
        contract."""

        expected = {
            "code": 200,
            "message": "Data Feed Fetched successfully",
            "body": EachLike(
                {
                    "datasource_name": Like(self.data_source_name),
                    "datasource_label": Like(self.data_source_label),
                    "name": Like(self.data_source_data_feed_name),
                    "records_received": Like(2000000),
                    "records_processed": Like(1800000),
                    "thirty_days_avg": Like(75),
                    "processed_at": Like(self.timestamp),
                    "status": Like(self.data_source_status),
                }
            ),
        }

        (
            PACT.given("Valid data source name exists.")
            .upon_receiving("A request to get data source's data feeds.")
            .with_request(
                method="GET",
                path=t_c.CDP_CONNECTIONS_DATA_SOURCE_DATA_FEEDS_ENDPOINT.format(
                    data_source_name=self.data_source_name
                ),
                body={},
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with PACT:
            result = requests.get(
                PACT.uri
                + t_c.CDP_CONNECTIONS_DATA_SOURCE_DATA_FEEDS_ENDPOINT.format(
                    data_source_name=self.data_source_name
                ),
                json={},
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))


class CDPIdentityContracts(unittest.TestCase):
    """Generate pact contracts for CDP Identity endpoints."""

    def setUp(self) -> None:
        """Setup tests."""

        self.feed_id = "3"
        self.data_source_name = "bluecore"
        self.data_source_label = "Bluecore"
        self.data_source_data_feed_name = "bluecore_email_clicks"
        self.timestamp = "2021-08-05T14:44:42.694Z"
        self.filters = {
            api_c.START_DATE: (
                datetime.utcnow().date() - relativedelta(months=1)
            ).strftime(api_c.DEFAULT_DATE_FORMAT),
            api_c.END_DATE: (datetime.utcnow().date()).strftime(
                api_c.DEFAULT_DATE_FORMAT
            ),
        }

    def test_get_data_feeds(self):
        """Test get identity data feeds to generate pact contract."""

        expected = {
            "code": 200,
            "message": "ok",
            "body": EachLike(
                {
                    "id": Like(self.feed_id),
                    "name": Like(self.data_source_data_feed_name),
                    "datasource_name": Like(self.data_source_name),
                    "new_ids_generated": Like(1159),
                    "total_rec_processed": Like(1159),
                    "match_rate": Like(0.888),
                    "timestamp": Like(self.timestamp),
                    "datasource_label": Like(self.data_source_label),
                }
            ),
        }

        (
            PACT.given("Start date and end date passed as filters.")
            .upon_receiving("A request to get identity data feeds.")
            .with_request(
                method="POST",
                path=t_c.CDP_IDENTITY_DATA_FEEDS_ENDPOINT,
                body=self.filters,
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with PACT:
            result = requests.post(
                PACT.uri + t_c.CDP_IDENTITY_DATA_FEEDS_ENDPOINT,
                json=self.filters,
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))

    def test_get_data_feeds_feed_id(self):
        """Test get identity data feeds by feed ID to generate pact contract."""

        expected = {
            "code": 200,
            "message": "ok",
            "body": Like(
                {
                    "pinning": Like(
                        {
                            "input_records": Like(38),
                            "output_records": Like(28),
                            "empty_records": Like(5),
                            "individual_id_match": Like(5),
                            "household_id_match": Like(6),
                            "company_id_match": Like(47),
                            "address_id_match": Like(35),
                            "db_reads": Like(9),
                            "db_writes": Like(21),
                            "filename": Like(
                                "email_analytics_extract_clicks_2021841437.csv"
                            ),
                            "new_individual_ids": Like(27),
                            "new_household_ids": Like(34),
                            "new_company_ids": Like(46),
                            "new_address_ids": Like(27),
                            "process_time": Like(1.46),
                            "pinning_timestamp": Like(self.timestamp),
                        }
                    ),
                    "stitched": Like(
                        {
                            "digital_ids_added": Like(12),
                            "digital_ids_merged": Like(21),
                            "match_rate": Like(0.66),
                            "merge_rate": Like(0.46),
                            "records_source": Like("input waterfall"),
                            "stitched_timestamp": Like(self.timestamp),
                        }
                    ),
                }
            ),
        }

        (
            PACT.given("Valid data feeds feed ID exists.")
            .upon_receiving("A request to get identity data feeds by feed ID.")
            .with_request(
                method="GET",
                path=t_c.CDP_IDENTITY_DATA_FEEDS_FEED_ID_ENDPOINT.format(
                    feed_id=self.feed_id
                ),
                body={},
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with PACT:
            result = requests.get(
                PACT.uri
                + t_c.CDP_IDENTITY_DATA_FEEDS_FEED_ID_ENDPOINT.format(
                    feed_id=self.feed_id
                ),
                json={},
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))

    def test_identity_count_by_day(self):
        """Test get identity data count by day to generate pact contract."""

        expected = {
            "code": 200,
            "message": "ok",
            "body": EachLike(
                {
                    "day": Like(
                        datetime.utcnow()
                        .date()
                        .strftime(api_c.DEFAULT_DATE_FORMAT)
                    ),
                    "unique_hux_ids": Like(1029),
                    "anonymous_ids": Like(130),
                    "known_ids": Like(1029),
                }
            ),
        }

        (
            PACT.given("Start date and end date passed as filters.")
            .upon_receiving("A request to get identity count by day.")
            .with_request(
                method="POST",
                path=t_c.CDP_IDENTITY_ID_COUNT_BY_DAY_ENDPOINT,
                body=self.filters,
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with PACT:
            result = requests.post(
                PACT.uri + t_c.CDP_IDENTITY_ID_COUNT_BY_DAY_ENDPOINT,
                json=self.filters,
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))
