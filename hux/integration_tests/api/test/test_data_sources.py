"""Purpose of this file is to test data sources."""
from unittest import TestCase
import pytest
import requests
from hux.integration_tests.api.test.conftest import Crud


class TestDataSources(TestCase):
    """Test Datasources."""

    DATA_SOURCES = "data-sources"
    COLLECTION = "cdp_data_sources"

    def test_create(self):
        """Test creating a datasource."""

        # setup the request mock post
        response = requests.post(
            f"{pytest.API_URL}/{self.DATA_SOURCES}",
            json=[
                {
                    "name": "E2E Test Data source",
                    "type": "dataSource",
                    "status": "Active",
                    "category": "CRM",
                }
            ],
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(200, response.status_code)

        # add the crud object to pytest for cleaning after.
        pytest.CRUD_OBJECTS += [
            Crud(self.COLLECTION, response.json()[0]["id"])
        ]
