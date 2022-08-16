"""Purpose of this file is to test data sources."""
from http import HTTPStatus
from time import time
from unittest import TestCase
import pytest
import requests
from conftest import Crud
from prometheus_metrics import record_test_result, HttpMethod, Endpoints


class TestDataSources(TestCase):
    """Test Data Sources."""

    DATA_SOURCES = "data-sources"
    COLLECTION = "cdp_data_sources"

    @record_test_result(
        HttpMethod.POST, Endpoints.DATA_SOURCES.POST_CREATE_DATA_SOURCE
    )
    def test_create_data_source(self):
        """Test creating a data source."""

        # set up the request post
        response = requests.post(
            f"{pytest.API_URL}/{self.DATA_SOURCES}",
            json=[
                {
                    "name": f"E2E test_data_sources Integration Test-{int(time() * 1000)}",
                    "type": f"E2E-test_data_sources-dataSource-{int(time() * 1000)}",
                    "status": "Active",
                    "category": "CRM",
                }
            ],
            headers=pytest.HEADERS,
        )

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [
            Crud(self.COLLECTION, response.json()[0]["id"])
        ]

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 1)

    @record_test_result(
        HttpMethod.DELETE, Endpoints.DATA_SOURCES.DELETE_DATA_SOURCE
    )
    def test_delete_data_source(self):
        """Test deleting a data source."""

        data_source_type = (
            f"E2E-test_data_sources-dataSource-{int(time() * 1000)}"
        )

        # set up the request post to create a test data source that is to be
        # deleted
        create_response = requests.post(
            f"{pytest.API_URL}/{self.DATA_SOURCES}",
            json=[
                {
                    "name": f"E2E test_data_sources Integration Test-{int(time() * 1000)}",
                    "type": data_source_type,
                    "status": "Active",
                    "category": "CRM",
                }
            ],
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, create_response.status_code)
        self.assertIsInstance(create_response.json(), list)
        self.assertEqual(len(create_response.json()), 1)

        # request to delete the E2E integration data source created above
        delete_response = requests.delete(
            f"{pytest.API_URL}/{self.DATA_SOURCES}?datasources={data_source_type}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, delete_response.status_code)
        self.assertIsInstance(delete_response.json(), dict)

    @record_test_result(
        HttpMethod.GET, Endpoints.DATA_SOURCES.GET_DATA_SOURCES
    )
    def test_get_all_data_sources(self):
        """Test get all data sources."""

        # set up the request to get all data sources
        response = requests.get(
            f"{pytest.API_URL}/{self.DATA_SOURCES}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)

    @record_test_result(HttpMethod.GET, Endpoints.DATA_SOURCES.GET_DATA_SOURCE)
    def test_get_data_source(self):
        """Test get data source by ID."""

        # set up the request to get all data sources
        get_all_response = requests.get(
            f"{pytest.API_URL}/{self.DATA_SOURCES}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, get_all_response.status_code)
        self.assertIsInstance(get_all_response.json(), list)
        self.assertGreaterEqual(len(get_all_response.json()), 1)

        get_individual_response = requests.get(
            f"{pytest.API_URL}/{self.DATA_SOURCES}/"
            f'{get_all_response.json()[0]["id"]}',
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, get_individual_response.status_code)
        self.assertIsInstance(get_individual_response.json(), dict)

    @record_test_result(
        HttpMethod.GET, Endpoints.DATA_SOURCES.GET_DATA_SOURCE_DATAFEEDS
    )
    def test_get_data_feeds_of_data_source(self):
        """Test get data feeds of a data source."""

        # set up the request to get data feeds of a data source
        response = requests.get(
            f"{pytest.API_URL}/{self.DATA_SOURCES}/bluecore/datafeeds",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.GET, Endpoints.DATA_SOURCES.GET_DATA_SOURCE_DATAFEEDS
    )
    def test_get_data_feeds_of_data_source_data_feed(self):
        """Test get data feeds of a data source's data feed."""

        # set up the request to get data feeds of a data source
        data_source_data_feeds_response = requests.get(
            f"{pytest.API_URL}/{self.DATA_SOURCES}/bluecore/datafeeds",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(
            HTTPStatus.OK, data_source_data_feeds_response.status_code
        )
        self.assertIsInstance(data_source_data_feeds_response.json(), dict)
        self.assertIsInstance(
            data_source_data_feeds_response.json()["datafeeds"], list
        )
        self.assertGreaterEqual(
            len(data_source_data_feeds_response.json()["datafeeds"]), 1
        )

        # set up the request to get data feeds of a data source's data feed
        data_source_data_feed_data_feeds_response = requests.get(
            f"{pytest.API_URL}/{self.DATA_SOURCES}/bluecore/datafeeds/"
            f'{data_source_data_feeds_response.json()["datafeeds"][0]["name"]}',
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(
            HTTPStatus.OK,
            data_source_data_feed_data_feeds_response.status_code,
        )
        self.assertIsInstance(
            data_source_data_feed_data_feeds_response.json(), list
        )

    @record_test_result(
        HttpMethod.PATCH, Endpoints.DATA_SOURCES.PATCH_UPDATE_DATA_SOURCES
    )
    def test_update_data_source(self):
        """Test updating a data source."""

        # set up the request post to create a data source for updating
        create_response = requests.post(
            f"{pytest.API_URL}/{self.DATA_SOURCES}",
            json=[
                {
                    "name": f"E2E test_data_sources Integration Test-{int(time() * 1000)}",
                    "type": f"E2E-test_data_sources-dataSource-{int(time() * 1000)}",
                    "status": "Active",
                    "category": "CRM",
                }
            ],
            headers=pytest.HEADERS,
        )

        data_source_id_to_update = create_response.json()[0]["id"]

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [
            Crud(self.COLLECTION, data_source_id_to_update)
        ]

        # test create success
        self.assertEqual(HTTPStatus.OK, create_response.status_code)
        self.assertIsInstance(create_response.json(), list)
        self.assertEqual(len(create_response.json()), 1)

        # set up the request patch to update the data source created above
        update_response = requests.patch(
            f"{pytest.API_URL}/{self.DATA_SOURCES}",
            json={
                "data_source_ids": [data_source_id_to_update],
                "body": {"is_added": True, "status": "Pending"},
            },
            headers=pytest.HEADERS,
        )

        # test update success
        self.assertEqual(HTTPStatus.OK, update_response.status_code)
        self.assertIsInstance(update_response.json(), list)
        self.assertEqual(len(update_response.json()), 1)
        self.assertEqual(
            data_source_id_to_update, update_response.json()[0]["id"]
        )
        self.assertEqual("Pending", update_response.json()[0]["status"])
