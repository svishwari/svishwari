"""Purpose of this file is to house all data sources tests."""
import copy
import json
from datetime import datetime
from http import HTTPStatus
from unittest import mock

from marshmallow import ValidationError

from huxunify.api.route.utils import clean_and_aggregate_datafeed_details
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
from huxunifylib.database.cdp_data_source_management import (
    create_data_source,
    bulk_write_data_sources,
)
import huxunifylib.database.constants as db_c
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.api.schema.cdp_data_source import (
    CdpDataSourceSchema,
    DataSourceDataFeedsGetSchema,
    CdpDataSourceDataFeedSchema,
    CdpConnectionsDataSourceSchema,
    DataSourceDataFeedDetailsGetSchema,
    FloatValueStandardDeviationSchema,
    IndividualDataSourceDataFeedDetailSchema,
)


class CdpDataSourcesTest(RouteTestCase):
    """Test CDP Data Sources CRUD APIs."""

    def setUp(self) -> None:
        """Setup tests."""

        self.data_sources_api_endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.CDP_DATA_SOURCES_ENDPOINT}"
        )

        super().setUp()
        self.load_test_data(self.database)

        # mock get_db_client() in cdp_data_source
        mock.patch(
            "huxunify.api.route.cdp_data_source.get_db_client",
            return_value=self.database,
        ).start()

        # Deep copy data source response object
        data_sources = copy.deepcopy(t_c.DATASOURCES_RESPONSE[api_c.BODY])[:2]
        _ = [
            data_source.update({db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 1})
            for data_source in data_sources
        ]

        # create data sources first
        self.data_sources = CdpDataSourceSchema().dump(
            bulk_write_data_sources(
                self.database,
                CdpConnectionsDataSourceSchema().load(data_sources, many=True),
            ),
            many=True,
        )

    def test_get_data_source_by_id(self):
        """Test get data source by id from DB."""

        valid_response = self.data_sources[0]

        response = self.app.get(
            f"{self.data_sources_api_endpoint}/{valid_response[api_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(CdpDataSourceSchema(), response.json)
        )
        self.assertEqual(valid_response, response.json)

    def test_get_all_data_sources_success(self):
        """Test get all data source from DB."""
        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_CONNECTIONS_ENDPOINT}/{api_c.DATASOURCES}",
            json=t_c.DATASOURCES_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            self.data_sources_api_endpoint,
            query_string={api_c.ONLY_ADDED: False},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        # verify number of data sources returned
        self.assertEqual(69, len(response.json))
        self.assertTrue(
            t_c.validate_schema(
                CdpDataSourceSchema(), response.json, is_multiple=True
            )
        )

    def test_get_all_data_sources_no_args(self):
        """Test get all data source with no args."""
        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}/"
            f"{api_c.CDM_CONNECTIONS_ENDPOINT}/{api_c.DATASOURCES}",
            json=t_c.DATASOURCES_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            self.data_sources_api_endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        # verify number of data sources returned
        self.assertEqual(69, len(response.json))
        self.assertTrue(
            t_c.validate_schema(
                CdpDataSourceSchema(), response.json, is_multiple=True
            )
        )

    def test_delete_data_sources_by_type_success(self):
        """]Test delete data sources by type from DB."""

        data_source_types = ", ".join(
            [data_source[api_c.TYPE] for data_source in self.data_sources]
        )

        valid_response = dict(
            message=api_c.DELETE_DATASOURCES_SUCCESS.format(data_source_types)
        )

        response = self.app.delete(
            f"{self.data_sources_api_endpoint}",
            query_string={api_c.DATASOURCES: data_source_types},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_create_data_sources_valid_params(self):
        """Test creating new data sources with valid params."""

        data_sources = [
            {
                api_c.NAME: "Test Data Source 1",
                api_c.TYPE: "test_data_source_type_1",
                api_c.STATUS: api_c.STATUS_ACTIVE,
                db_c.CATEGORY: db_c.CATEGORY_API,
                db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 1,
            },
            {
                api_c.NAME: "Test Data Source 2",
                api_c.TYPE: "test_data_source_type_2",
                api_c.STATUS: api_c.STATUS_PENDING,
                db_c.CATEGORY: db_c.CATEGORY_CRM,
                db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 1,
            },
        ]

        response = self.app.post(
            self.data_sources_api_endpoint,
            data=json.dumps(data_sources),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(
                CdpDataSourceSchema(), response.json, is_multiple=True
            )
        )
        self.assertEqual(len(response.json), len(data_sources))

        for data_source in response.json:
            self.assertIn(api_c.NAME, data_source)
            self.assertIn(api_c.TYPE, data_source)
            self.assertIn(api_c.STATUS, data_source)
            self.assertIn(db_c.CATEGORY, data_source)
            self.assertIn(db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT, data_source)
            self.assertIn(api_c.IS_ADDED, data_source)
            self.assertTrue(api_c.IS_ADDED)

    def test_get_data_source_by_id_invalid_id(self):
        """Test get data source with an invalid id."""

        ds_id = "XYZ"
        valid_response = {
            "message": f"Invalid CDP data source ID received {ds_id}."
        }

        response = self.app.get(
            f"{self.data_sources_api_endpoint}/{ds_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_delete_data_sources_by_type_empty_data(self):
        """Test delete data sources with empty data."""

        response = self.app.delete(
            f"{self.data_sources_api_endpoint}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(
            {api_c.MESSAGE: api_c.EMPTY_OBJECT_ERROR_MESSAGE}, response.json
        )

    def test_create_data_source_w_empty_name_string(self):
        """Test creating data sources with name set as empty string."""

        data_sources = [
            {
                api_c.NAME: "",
                api_c.TYPE: "test_data_source_type_1",
                api_c.STATUS: api_c.STATUS_ACTIVE,
            },
            {
                api_c.NAME: "Test Data Source 2",
                api_c.TYPE: "test_data_source_type_2",
                api_c.STATUS: api_c.STATUS_PENDING,
            },
        ]

        response = self.app.post(
            self.data_sources_api_endpoint,
            data=json.dumps(data_sources),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertRaises(ValidationError)

    def test_create_data_source_no_inputs(self):
        """Test creating data source without any inputs"""

        response = self.app.post(
            self.data_sources_api_endpoint,
            data=json.dumps([{}]),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertRaises(ValidationError)

    def test_create_data_source_w_no_values(self):
        """Test creating data sources with name and category set as empty
        string."""

        data_sources = [
            {
                api_c.NAME: "",
                api_c.TYPE: "",
                api_c.STATUS: api_c.STATUS_ACTIVE,
            },
            {
                api_c.NAME: "",
                api_c.TYPE: "",
                api_c.STATUS: api_c.STATUS_PENDING,
            },
        ]

        response = self.app.post(
            self.data_sources_api_endpoint,
            data=json.dumps(data_sources),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertRaises(ValidationError)

    def test_patch_data_source_valid_params(self) -> None:
        """Test patching/updating an existing data source with valid params."""

        valid_data_source = self.data_sources[0]

        response = self.app.patch(
            self.data_sources_api_endpoint,
            data=json.dumps(
                {
                    api_c.CDP_DATA_SOURCE_IDS: [valid_data_source[api_c.ID]],
                    api_c.BODY: {
                        api_c.IS_ADDED: valid_data_source[api_c.IS_ADDED],
                        api_c.STATUS: valid_data_source[api_c.STATUS],
                    },
                }
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        for record in response.json:
            self.assertTrue(t_c.validate_schema(CdpDataSourceSchema(), record))

    def test_patch_data_source_invalid_params(self) -> None:
        """Test patching/updating an existing data source with invalid params."""

        valid_data_source = self.data_sources[0]

        response = self.app.patch(
            self.data_sources_api_endpoint,
            data=json.dumps(
                {
                    api_c.CDP_DATA_SOURCE_IDS: [valid_data_source[api_c.ID]],
                }
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_get_data_source_data_feed(self) -> None:
        """Test get data source data feeds endpoint."""

        data_source_type = t_c.DATASOURCE_DATA_FEEDS_RESPONSE[api_c.BODY][0][
            api_c.DATAFEED_DATA_SOURCE_NAME
        ]
        data_source_name = t_c.DATASOURCE_DATA_FEEDS_RESPONSE[api_c.BODY][0][
            api_c.DATAFEED_DATA_SOURCE_TYPE
        ]
        # create a data source of type test_data_source
        create_data_source(
            self.database,
            name=data_source_name,
            category="",
            source_type=data_source_type,
        )

        self.request_mocker.stop()
        self.request_mocker.get(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_CONNECTIONS_ENDPOINT}/{data_source_type}/"
            f"{api_c.DATA_FEEDS}",
            json=t_c.DATASOURCE_DATA_FEEDS_RESPONSE,
        )
        self.request_mocker.start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CDP_DATA_SOURCES_ENDPOINT}/"
            f"{data_source_type}/{api_c.DATAFEEDS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(api_c.NAME, response.json)
        self.assertIn(api_c.TYPE, response.json)
        self.assertIn(api_c.DATAFEEDS, response.json)

        self.assertFalse(
            DataSourceDataFeedsGetSchema().validate(response.json)
        )
        self.assertFalse(
            CdpDataSourceDataFeedSchema().validate(
                response.json.get(api_c.DATAFEEDS), many=True
            )
        )

        for data_feed in response.json.get(api_c.DATAFEEDS):
            self.assertFalse(
                FloatValueStandardDeviationSchema().validate(
                    data_feed.get(api_c.RECORDS_PROCESSED_PERCENTAGE)
                )
            )
            self.assertFalse(
                FloatValueStandardDeviationSchema().validate(
                    data_feed.get(api_c.THIRTY_DAYS_AVG)
                )
            )

    def test_get_data_source_data_feed_details_no_status_filter(self) -> None:
        """Test get data source data feed details endpoint with no status_filter."""
        data_source_type = t_c.DATASOURCE_DATA_FEEDS_RESPONSE[api_c.BODY][0][
            api_c.DATAFEED_DATA_SOURCE_TYPE
        ]
        datafeed_name = "clicks"
        start_date = "2021-01-01"
        end_date = datetime.strftime(
            datetime.utcnow(), api_c.DEFAULT_DATE_FORMAT
        )
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_CONNECTION_SERVICE}"
            f"/{api_c.CDM_CONNECTIONS_ENDPOINT}/{api_c.DATASOURCES}/{data_source_type}/"
            f"feeds/{datafeed_name}/files",
            json=t_c.DATAFEED_FILE_DETAILS_RESPONSE,
        )
        self.request_mocker.start()

        expected_response = DataSourceDataFeedDetailsGetSchema(many=True).dump(
            sorted(
                clean_and_aggregate_datafeed_details(
                    [
                        x.copy()
                        for x in t_c.DATAFEED_FILE_DETAILS_RESPONSE[api_c.BODY]
                    ],
                    do_aggregate=True,
                ),
                key=lambda x: x[api_c.PROCESSED_START_DATE],
                reverse=True,
            )
        )
        response = self.app.get(
            f"{self.data_sources_api_endpoint}/{data_source_type}/"
            f"{api_c.DATAFEEDS}/{datafeed_name}",
            query_string={
                "start_date": start_date,
                "end_date": end_date,
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(
            DataSourceDataFeedDetailsGetSchema(many=True).validate(
                response.json
            )
        )
        self.assertEqual(len(expected_response), len(response.json))

        for df_detail in response.json:
            self.assertFalse(
                DataSourceDataFeedDetailsGetSchema().validate(df_detail)
            )
            self.assertIn(api_c.DATA_FILES, df_detail.keys())
            self.assertFalse(
                IndividualDataSourceDataFeedDetailSchema(many=True).validate(
                    df_detail[api_c.DATA_FILES]
                )
            )
