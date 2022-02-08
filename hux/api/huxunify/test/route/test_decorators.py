"""Purpose of this file is to house tests for standalone decorators."""
from http import HTTPStatus
from unittest import mock

from huxunify.api.route.decorators import requires_access_policy
from huxunify.api import constants as api_c
from huxunify.app import create_app
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase

from huxunifylib.database import constants as db_c
from huxunifylib.database.orchestration_management import create_audience

import huxunify.test.constants as t_c


class TestDecorators(RouteTestCase):
    """Purpose of this class is to test Decorators."""

    def setUp(self) -> None:
        """Initialize resources before each test."""

        super().setUp()

        mock.patch(
            "huxunify.api.route.decorators.get_token_from_request",
            return_value=tuple([t_c.TEST_AUTH_TOKEN.split()[1], 200]),
        ).start()

        self.user_name = t_c.VALID_USER_RESPONSE.get(api_c.NAME, "")

        self.user = {
            api_c.USER_NAME: self.user_name,
            api_c.USER_ACCESS_LEVEL: db_c.USER_ROLE_ADMIN,
            api_c.USER_PII_ACCESS: True,
            db_c.USER_DISPLAY_NAME: self.user_name,
        }

    def tearDown(self) -> None:
        """Tear down after tests."""

        mock.patch.stopall()

    def test_requires_access_policy(self):
        """Test requires_access_policy decorators"""
        audience = create_audience(
            database=self.database,
            name="Test Audience",
            audience_filters=[],
            user_name=self.user_name,
        )

        with create_app().test_request_context():

            @requires_access_policy(
                access_rule=api_c.RESOURCE_OWNER,
                resource_attributes={api_c.NAME: api_c.AUDIENCE},
                access_levels=[api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL],
            )
            def sample_audience_manipulation(
                audience_id: str, user: dict
            ) -> tuple:
                """A sample function for audience manipulation.

                Args:
                    audience_id (str): ID of the audience to be manipulated.
                    user (dict): Info of user requesting the operation.

                Returns:
                    tuple: User Info, Audience ID or Unauthorized Message, Code
                """
                return user, audience_id

        response = sample_audience_manipulation(
            audience_id=str(audience.get(db_c.ID)), user={}
        )
        self.assertEqual(response[0][api_c.DISPLAY_NAME], self.user_name)

    def test_requires_access_policy_user_not_owner(self):
        """Test requires_access_policy decorator for unauthorized access."""
        audience = create_audience(
            database=self.database,
            name="Test Audience",
            audience_filters=[],
            user_name=self.user_name,
        )

        test_user = {
            api_c.USER_NAME: t_c.TEST_USER_NAME,
            api_c.USER_ACCESS_LEVEL: db_c.USER_ROLE_VIEWER,
            api_c.USER_PII_ACCESS: False,
            db_c.USER_DISPLAY_NAME: t_c.TEST_USER_NAME,
        }
        mock.patch(
            "huxunify.api.route.decorators.get_user_from_db",
            return_value=test_user,
        ).start()

        with create_app().test_request_context():

            @requires_access_policy(
                access_rule=api_c.RESOURCE_OWNER,
                resource_attributes={api_c.NAME: api_c.AUDIENCE},
                access_levels=[api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL],
            )
            def sample_audience_manipulation(
                audience_id: str, user: dict
            ) -> tuple:
                """A sample function for audience manipulation.

                Args:
                    audience_id (str): ID of audience to be manipulated.
                    user (dict): Info of user requesting the operation.

                Returns:
                    tuple: User Info, Audience ID or Unauthorized Message, Code
                """
                return user, audience_id

        response = sample_audience_manipulation(
            audience_id=str(audience.get(db_c.ID)), user={}
        )
        self.assertEqual(response[1], HTTPStatus.UNAUTHORIZED)
