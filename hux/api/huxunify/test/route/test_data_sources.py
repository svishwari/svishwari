import json
from unittest import TestCase

import mongomock
import requests_mock
from huxunifylib.database.cdp_data_source_management import create_data_source
from requests_mock import Mocker
from flask import Flask

import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunify.api import constants as api_c


class DataSourcesTest(TestCase):
    """
    Test Data Sources CRUD APIs
    """

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.data_sources_api_endpoint = f'/api/v1{api_c.CDP_DATA_SOURCES_ENDPOINT}/'

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        data_sources_list = [
            {
                "name": "TestDataSource1",
                "category": "Web Events"
            },
            {
                "name": "TestDataSource2",
                "category": "Web Events"
            }
        ]

        self.data_sources = []
        for ds in data_sources_list:
            self.data_sources.append(create_data_source(
                self.database,
                ds["name"],
                ds["category"]
            ))

    @requests_mock.Mocker()
    def test_get_data_source_by_id_valid_request(self, request_mocker: Mocker):
        """Test get data source by id from DB

        Args:

        Returns:

        """
        valid_response = self.data_sources[0]

        request_mocker.get(
            f'{self.data_sources_api_endpoint}/{valid_response["_id"]}',
            json=json.dumps(valid_response)
        )

        with Flask("valid_request").test_request_context():
            def demo_endpoint():
                return True

            # true means the endpoint and token call were successfully passed.
            self.assertTrue(demo_endpoint())

    @requests_mock.Mocker()
    def test_get_all_data_sources_valid_request(self, request_mocker: Mocker):
        """Test get all data source from DB

        Args:

        Returns:

        """
        valid_response = self.data_sources

        request_mocker.get(
            f'{self.data_sources_api_endpoint}',
            json=json.dumps(valid_response)
        )

        with Flask("valid_request").test_request_context():
            def demo_endpoint():
                return True

            # true means the endpoint and token call were successfully passed.
            self.assertTrue(demo_endpoint())

    @requests_mock.Mocker()
    def test_delete_data_source_by_id_valid_request(self, request_mocker: Mocker):
        """Test delete data source by id from DB

        Args:

        Returns:

        """
        valid_response = self.data_sources[0]

        request_mocker.delete(
            f'{self.data_sources_api_endpoint}/{valid_response["_id"]}',
            json=json.dumps(valid_response)
        )

        with Flask("valid_request").test_request_context():
            def demo_endpoint():
                return True

            # true means the endpoint and token call were successfully passed.
            self.assertTrue(demo_endpoint())
