"""Util module for route testcases"""
from unittest import TestCase, mock

import mongomock
import requests_mock

from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.app import create_app
from huxunify.test import constants as t_c
from huxunify.test.route.route_test_util.test_data_loading.data_sources import (
    load_data_sources,
)
from huxunify.test.route.route_test_util.test_data_loading.destinations import (
    load_destinations,
)
from huxunify.test.route.route_test_util.test_data_loading.users import (
    load_users,
)
from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient

# pylint: disable=attribute-defined-outside-init
class RouteTestCase(TestCase):
    """Base class for route test case"""

    def setUp(self) -> None:
        """Performs the proper mocks for all all unit tests

        Returns:

        """
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.config = get_config(api_c.TEST_MODE)

        # mock get_db_client() in utils
        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() in decorators
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

        # mock request for introspect call
        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(
            t_c.INTROSPECT_CALL, json=t_c.VALID_INTROSPECTION_RESPONSE
        )
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.get(
            t_c.CDM_HEALTHCHECK_CALL, json=t_c.CDM_HEALTHCHECK_RESPONSE
        )
        self.request_mocker.start()

        # stop all mocks in cleanup
        self.addCleanup(mock.patch.stopall)

        # setup the flask test client
        self.app = create_app().test_client()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.user_name = "Joe Smithers"

    # pylint:disable=no-self-use
    def load_test_data(self, database: DatabaseClient):
        """Load test data into the database.

        Args:
            database (DatabaseClient): A database client.

        Returns:

        """

        load_destinations(database)
        load_data_sources(database)
        load_users(database)
