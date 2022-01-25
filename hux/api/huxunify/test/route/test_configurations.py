"""Purpose of this file is to house all tests related to configurations."""
from unittest import TestCase, mock
from http import HTTPStatus

import requests_mock
import mongomock

from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database import (
    collection_management as cmg,
)
from huxunifylib.database.user_management import (
    set_user,
)
import huxunify.test.constants as t_c
from huxunify.api.schema.configurations import (
    ConfigurationsSchema,
)
from huxunify.api import constants as api_c
from huxunify.app import create_app


class ConfigurationsTests(TestCase):
    """Tests for configurations."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        # mock request for introspect call
        request_mocker = requests_mock.Mocker()
        request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        request_mocker.get(t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE)
        request_mocker.start()

        self.app = create_app().test_client()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

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

        mock.patch(
            "huxunify.api.route.configurations.get_db_client",
            return_value=self.database,
        ).start()

        # write a user to the database
        self.user_name = t_c.VALID_USER_RESPONSE.get(api_c.NAME)
        self.user_doc = set_user(
            self.database,
            t_c.VALID_RESPONSE.get(api_c.OKTA_UID),
            t_c.VALID_USER_RESPONSE.get(api_c.EMAIL),
            display_name=self.user_name,
        )

        configurations = [
            {
                "id": "3",
                "name": "Data management",
                "type": "module",
                "status": "active",
                "description": "Data management.",
                "enabled": True,
            },
            {
                "id": "3",
                "name": "Trust ID",
                "type": "business_solution",
                "status": "pending",
                "description": "Trust ID.",
                "enabled": True,
            },
        ]

        self.configurations = []
        for configuration in configurations:
            self.configurations.append(
                cmg.create_document(
                    self.database,
                    db_c.CONFIGURATIONS_COLLECTION,
                    configuration,
                )
            )

        navigation_settings = {
            "name": "Navigation Settings",
            "type": "navigation_settings",
            "settings": api_c.SAMPLE_NAVIGATION_SETTINGS["settings"],
        }
        cmg.create_document(
            self.database,
            db_c.CONFIGURATIONS_COLLECTION,
            navigation_settings,
        )

        self.addCleanup(mock.patch.stopall)

    def test_success_get_configurations_modules(self):
        """Test get configurations."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CONFIGURATIONS_ENDPOINT}/modules",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            t_c.validate_schema(ConfigurationsSchema(), response.json, True)
        )

        self.assertEqual(
            [x[api_c.NAME] for x in response.json],
            sorted([x[api_c.NAME] for x in self.configurations]),
        )

    def test_success_get_models_with_status(self):
        """Test get models from Tecton with status."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}"
            f"{api_c.CONFIGURATIONS_ENDPOINT}/modules?{api_c.STATUS}=active",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertTrue(
            t_c.validate_schema(ConfigurationsSchema(), response.json, True)
        )

        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0][api_c.NAME], "Data management")
        self.assertEqual(response.json[0][api_c.TYPE], "module")

    def test_success_get_configurations_navigation(self):
        """Test get configurations."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CONFIGURATIONS_ENDPOINT}/navigation",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(response.json[db_c.CONFIGURATION_FIELD_SETTINGS])
        self.assertTrue(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0][api_c.NAME]
        )
        self.assertEqual(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0][api_c.NAME],
            "Data Management",
        )
        self.assertTrue(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0][api_c.ENABLED]
        )

    def test_success_put_configurations_navigation(self):
        """Test get configurations."""

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.CONFIGURATIONS_ENDPOINT}/navigation",
            json=t_c.TEST_NAVIGATION_SETTINGS,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        self.assertTrue(response.json[db_c.CONFIGURATION_FIELD_SETTINGS])
        self.assertTrue(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0][api_c.NAME]
        )
        self.assertEqual(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0][api_c.NAME],
            "Data Management",
        )
        self.assertTrue(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0][api_c.ENABLED]
        )
        self.assertFalse(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0]["children"][0][
                api_c.ENABLED
            ]
        )
        self.assertTrue(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0]["children"][1][
                api_c.ENABLED
            ]
        )
