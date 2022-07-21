"""Purpose of this file is to house all tests related to configurations."""
from unittest import mock
from http import HTTPStatus

from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
from huxunifylib.database import constants as db_c
from huxunifylib.database import (
    collection_management as cmg,
)
from huxunifylib.database.user_management import (
    set_user,
    update_user,
)
import huxunify.test.constants as t_c
from huxunify.api.schema.configurations import (
    ConfigurationsSchema,
)
from huxunify.api import constants as api_c


class ConfigurationsTests(RouteTestCase):
    """Tests for configurations."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        super().setUp()

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
            t_c.VALID_INTROSPECTION_RESPONSE.get(api_c.OKTA_UID),
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
            db_c.CONFIGURATION_FIELD_NAME: "Navigation Settings",
            db_c.CONFIGURATION_FIELD_TYPE: db_c.CONFIGURATION_TYPE_NAVIGATION_SETTINGS,
            db_c.CONFIGURATION_FIELD_SETTINGS: api_c.SAMPLE_NAVIGATION_SETTINGS[
                db_c.CONFIGURATION_FIELD_SETTINGS
            ],
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

    def test_success_get_configurations_modules_with_status(self):
        """Test get configurations modules with status."""

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
        """Test get navigation configuration."""

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

    def test_success_get_navigation_healthcare_user_demo_config(self):
        """Test get navigation configuration for user set with healthcare
        demo config."""

        # update the user with alert configurations
        update_user(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            update_doc={
                **{db_c.USER_DEMO_CONFIG: api_c.USER_DEMO_CONFIG_SAMPLE},
                **{
                    db_c.UPDATED_BY: self.user_doc[db_c.USER_DISPLAY_NAME],
                },
            },
        )

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CONFIGURATIONS_ENDPOINT}/navigation",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(response.json[db_c.CONFIGURATION_FIELD_SETTINGS])
        insights_nav_setting_names = [
            insights_nav_setting[db_c.CONFIGURATION_FIELD_NAME]
            for nav_setting in response.json[db_c.CONFIGURATION_FIELD_SETTINGS]
            if nav_setting[db_c.CONFIGURATION_FIELD_NAME]
            == api_c.INSIGHTS.title()
            for insights_nav_setting in nav_setting[
                db_c.CONFIGURATION_FIELD_CHILDREN
            ]
        ]
        self.assertIn("Patients", insights_nav_setting_names)
        self.assertNotIn("Customers", insights_nav_setting_names)

    def test_success_get_navigation_default_user_demo_config(self):
        """Test get navigation configuration for user set with no demo
        config."""

        # update the user with alert configurations
        update_user(
            database=self.database,
            okta_id=self.user_doc[db_c.OKTA_ID],
            update_doc={
                **{db_c.USER_DEMO_CONFIG: {api_c.USER_DEMO_MODE: False}},
                **{
                    db_c.UPDATED_BY: self.user_doc[db_c.USER_DISPLAY_NAME],
                },
            },
        )

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CONFIGURATIONS_ENDPOINT}/navigation",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(response.json[db_c.CONFIGURATION_FIELD_SETTINGS])
        insights_nav_setting_names = [
            insights_nav_setting[db_c.CONFIGURATION_FIELD_NAME]
            for nav_setting in response.json[db_c.CONFIGURATION_FIELD_SETTINGS]
            if nav_setting[db_c.CONFIGURATION_FIELD_NAME]
            == api_c.INSIGHTS.title()
            for insights_nav_setting in nav_setting[
                db_c.CONFIGURATION_FIELD_CHILDREN
            ]
        ]
        self.assertIn("Customers", insights_nav_setting_names)
        self.assertNotIn("Patients", insights_nav_setting_names)

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
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0][
                db_c.CONFIGURATION_FIELD_CHILDREN
            ][0][api_c.ENABLED]
        )
        self.assertTrue(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0][
                db_c.CONFIGURATION_FIELD_CHILDREN
            ][1][api_c.ENABLED]
        )

    def test_success_get_empty_industrytags(self):
        """Test get  industry tags."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CONFIGURATIONS_ENDPOINT}/industrytags",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(response.json)

    def test_success_put_industrytags(self):
        """Test get  industry tags."""

        industrytags = {
            "settings": [
                {
                    "name": "Automotive",
                    "label": "Automotive",
                    "enabled": False,
                }
            ]
        }

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.CONFIGURATIONS_ENDPOINT}/industrytags",
            json=industrytags,
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(response.json[db_c.CONFIGURATION_FIELD_SETTINGS])
        self.assertTrue(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0][api_c.NAME]
        )
        self.assertEqual(
            response.json[db_c.CONFIGURATION_FIELD_SETTINGS][0][api_c.NAME],
            "Automotive",
        )
