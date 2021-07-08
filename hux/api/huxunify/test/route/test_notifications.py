"""
Purpose of this file is to house all the notification api tests
"""

from unittest import TestCase, mock
from http import HTTPStatus

import requests_mock
import mongomock
from huxunifylib.database.client import DatabaseClient
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.app import create_app


class TestNotificationRoutes(TestCase):
    """Test Notifications Tests"""

    def setUp(self) -> None:
        """
        Setup resources before each test

        Args:

        Returns:
        """

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

        # mock get db client from notifications
        mock.patch(
            "huxunify.api.route.notifications.get_db_client",
            return_value=self.database,
        ).start()

        self.notifications = [
            {
                "notification_type": "Alert",
                "description": "description 1",
                "created": 0,
            },
            {
                "notification_type": "Alert",
                "description": "description 2",
                "created": 0,
            },
            {
                "notification_type": "Alert",
                "description": "description 3",
                "created": 0,
            },
        ]

        self.addCleanup(mock.patch.stopall)

    def test_get_notifications(self):
        """
        Test get notifications

        Returns:

        """

        mock.patch(
            "huxunify.api.route.notifications.notification_management.get_notifications",
            return_value=self.notifications,
        ).start()

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}"
            f"?batch_size=5&sort_order=ascending&batch_number=2",
            headers=t_c.STANDARD_HEADERS,
        )

        mock.patch.stopall()

        self.assertEqual(HTTPStatus.OK, response.status_code)
