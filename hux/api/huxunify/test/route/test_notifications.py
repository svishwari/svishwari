"""
Purpose of this file is to house all the notification api tests
"""

from unittest import TestCase, mock
from http import HTTPStatus

import requests_mock
import mongomock
from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.notification_management import create_notification
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.api.schema.notifications import NotificationSchema
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

        notifications = [
            {
                "notification_type": db_c.NOTIFICATION_TYPE_SUCCESS,
                "description": "description 1",
                "category": api_c.DELIVERY_TAG,
            },
            {
                "notification_type": db_c.NOTIFICATION_TYPE_INFORMATIONAL,
                "description": "description 2",
                "category": api_c.MODELS_TAG,
            },
            {
                "notification_type": db_c.NOTIFICATION_TYPE_CRITICAL,
                "description": "description 3",
                "category": api_c.ORCHESTRATION_TAG,
            },
        ]

        self.notifications = sorted(
            NotificationSchema().dump(
                [
                    create_notification(self.database, **notification)
                    for notification in notifications
                ],
                many=True,
            ),
            key=lambda x: x["created"],
            reverse=True,
        )

        self.addCleanup(mock.patch.stopall)

    def test_get_notifications(self):
        """
        Test get notifications

        Returns:

        """

        params = {
            db_c.NOTIFICATION_QUERY_PARAMETER_BATCH_SIZE: api_c.DEFAULT_ALERT_BATCH_SIZE,
            db_c.NOTIFICATION_QUERY_PARAMETER_SORT_ORDER: db_c.PAGINATION_DESCENDING,
            db_c.NOTIFICATION_QUERY_PARAMETER_BATCH_NUMBER: api_c.DEFAULT_ALERT_BATCH_NUMBER,
        }

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}",
            data=params,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(self.notifications), response.json["total"])
        self.assertCountEqual(
            self.notifications, response.json[api_c.NOTIFICATIONS_TAG]
        )
