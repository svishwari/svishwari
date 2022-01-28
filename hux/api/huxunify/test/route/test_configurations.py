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
)
import huxunify.test.constants as t_c
from huxunify.api.schema.configurations import ConfigurationsSchema
from huxunify.api import constants as api_c


class ConfigurationsTests(RouteTestCase):
    """Tests for configurations."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        super().setUp()

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

    def test_success_get_configurations(self):
        """Test get configurations."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.CONFIGURATIONS_ENDPOINT}",
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
            f"{api_c.CONFIGURATIONS_ENDPOINT}?{api_c.STATUS}=active",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertTrue(
            t_c.validate_schema(ConfigurationsSchema(), response.json, True)
        )

        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0][api_c.NAME], "Data management")
        self.assertEqual(response.json[0][api_c.TYPE], "module")
