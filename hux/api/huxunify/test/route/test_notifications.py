"""Purpose of this file is to house all the notification API tests."""
import json
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
    """Test Notifications class."""

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

        # mock get db client from notifications
        mock.patch(
            "huxunify.api.route.notifications.get_db_client",
            return_value=self.database,
        ).start()

        # mock get db client from decorators
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

        # mock get db client from utils
        mock.patch(
            "huxunify.api.route.utils.get_db_client",
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
                "username": "random_user_name",
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
        """Test get notifications."""

        params = {
            api_c.QUERY_PARAMETER_BATCH_SIZE: api_c.DEFAULT_BATCH_SIZE,
            api_c.QUERY_PARAMETER_SORT_ORDER: db_c.PAGINATION_DESCENDING,
            api_c.QUERY_PARAMETER_BATCH_NUMBER: api_c.DEFAULT_BATCH_NUMBER,
        }

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}",
            data=params,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(self.notifications), response.json[api_c.TOTAL])
        self.assertCountEqual(
            self.notifications, response.json[api_c.NOTIFICATIONS_TAG]
        )

    def test_get_notification(self):
        """Test get notification."""
        notification_id = self.notifications[0][api_c.ID]

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}/{notification_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(NotificationSchema().validate(response.json))

    def test_get_notification_with_username(self):
        """Test get notification."""
        notification_id = self.notifications[0][api_c.ID]

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}/{notification_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(
            response.json["username"], ["random_user_name", "unknown"]
        )

    def test_get_notifications_default_params(self):
        """Test get notifications failure."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}",
            data={},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(self.notifications), response.json[api_c.TOTAL])
        self.assertCountEqual(
            self.notifications, response.json[api_c.NOTIFICATIONS_TAG]
        )

    def test_get_notifications_bad_params(self):
        """Test get notifications by setting batch size, batch number to
        incorrect values."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}?"
            f"{api_c.QUERY_PARAMETER_BATCH_SIZE}="
            f"{t_c.BATCH_SIZE_BAD_PARAM}&"
            f"{api_c.QUERY_PARAMETER_SORT_ORDER}="
            f"{db_c.PAGINATION_DESCENDING}&"
            f"{api_c.QUERY_PARAMETER_BATCH_NUMBER}={t_c.BATCH_NUMBER_BAD_PARAM}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_get_notifications_stream(self):
        """Test streaming notifications."""

        # create the test notification
        create_notification(
            database=self.database,
            notification_type=db_c.NOTIFICATION_TYPE_SUCCESS,
            description="Successfully delivered audience to platform A.",
        )

        with self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}/stream",
            headers=t_c.STANDARD_HEADERS,
        ) as stream:
            for line in stream.iter_encoded():
                self.assertTrue(line)

                # load the response into a list of notifications.
                notifications = json.loads(line)
                self.assertIn(db_c.NOTIFICATIONS_COLLECTION, notifications)
                self.assertEqual(notifications[api_c.TOTAL], 1)

                for notification in notifications[
                    db_c.NOTIFICATIONS_COLLECTION
                ]:
                    self.assertEqual(
                        notification[api_c.NOTIFICATION_TYPE],
                        db_c.NOTIFICATION_TYPE_SUCCESS.title(),
                    )
                break

    def test_delete_notification_valid_id(self):
        """Test delete notification API with valid ID."""

        notifcation_id = self.notifications[0][api_c.ID]

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}/{notifcation_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(notifcation_id, response.json[api_c.ID])

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}/{notifcation_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}/{notifcation_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_delete_notification_invalid_id(self):
        """Test delete notification API with invalid ID."""

        notifcation_id = "some_random_id"

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}/{notifcation_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
