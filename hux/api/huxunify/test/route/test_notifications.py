"""Purpose of this file is to house all the notification API tests."""
from datetime import datetime
import json
from unittest import mock
from http import HTTPStatus

from dateutil.relativedelta import relativedelta

from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
from huxunifylib.database import constants as db_c
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database.user_management import set_user, update_user
import huxunify.test.constants as t_c
from huxunify.api import constants as api_c
from huxunify.api.schema.notifications import NotificationSchema


class TestNotificationRoutes(RouteTestCase):
    """Test Notifications class."""

    def setUp(self) -> None:
        """Setup resources before each test."""

        super().setUp()

        # mock get db client from notifications
        mock.patch(
            "huxunify.api.route.notifications.get_db_client",
            return_value=self.database,
        ).start()

        self.test_username = "test_user"

        notifications = [
            {
                "notification_type": db_c.NOTIFICATION_TYPE_SUCCESS,
                "description": "description 1",
                "category": db_c.NOTIFICATION_CATEGORY_DELIVERY,
                "username": self.test_username,
            },
            {
                "notification_type": db_c.NOTIFICATION_TYPE_INFORMATIONAL,
                "description": "description 2",
                "category": db_c.NOTIFICATION_CATEGORY_MODELS,
                "username": self.test_username,
            },
            {
                "notification_type": db_c.NOTIFICATION_TYPE_CRITICAL,
                "description": "description 3",
                "category": db_c.NOTIFICATION_CATEGORY_AUDIENCES,
                "username": self.test_username,
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

    def test_create_notification(self):
        """Test create notification"""
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}",
            json={
                "type": db_c.NOTIFICATION_TYPE_SUCCESS,
                "category": db_c.NOTIFICATION_CATEGORY_DELIVERY,
                "description": "Successful delivery",
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        # assert that the return json body is successfully validated to return
        # an empty dict
        self.assertFalse(NotificationSchema().validate(response.json))

    def test_create_notification_invalid_category(self):
        """Test create notification"""
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}",
            json={
                "type": db_c.NOTIFICATION_TYPE_SUCCESS,
                "category": "invalid_category",
                "description": "Successful delivery",
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_create_notification_invalid_type(self):
        """Test create notification"""
        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}",
            json={
                "type": "invalid_type",
                "category": db_c.NOTIFICATION_CATEGORY_DELIVERY,
                "description": "Successful delivery",
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

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
        # assert that the return json body is successfully validated to return
        # an empty dict
        self.assertFalse(NotificationSchema().validate(response.json))

    def test_get_notification_with_username(self):
        """Test get notification."""
        notification_id = self.notifications[0][api_c.ID]

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}/{notification_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(self.test_username, response.json["username"])

    def test_get_notification_users(self):
        """Test get notification users."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}/{api_c.USERS}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(len(response.json), 1)
        self.assertIn("test_user", response.json)

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

    def test_get_notifications_custom_date_params(self):
        """Test get notifications failure."""

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}",
            query_string={
                api_c.START_DATE: datetime.strftime(
                    datetime.utcnow() - relativedelta(days=2),
                    api_c.DEFAULT_DATE_FORMAT,
                ),
                api_c.END_DATE: datetime.strftime(
                    datetime.utcnow(),
                    api_c.DEFAULT_DATE_FORMAT,
                ),
                db_c.NOTIFICATION_QUERY_PARAMETER_BATCH_SIZE: 10,
                db_c.NOTIFICATION_QUERY_PARAMETER_BATCH_NUMBER: 1,
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(self.notifications), response.json[api_c.TOTAL])
        self.assertCountEqual(
            self.notifications, response.json[api_c.NOTIFICATIONS_TAG]
        )

    def test_get_notifications_custom_params(self):
        """Test get notifications with filters."""

        expected_notification_types = ",".join(db_c.NOTIFICATION_TYPES[:-1])
        expected_notification_categories = ",".join(db_c.NOTIFICATION_CATEGORIES[:-1])
        expected_notifications = [
            x
            for x in self.notifications
            if x[api_c.NOTIFICATION_TYPE] in expected_notification_types.split(",")
            and x[db_c.CATEGORY] in expected_notification_categories.split(",")
        ]
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}",
            query_string={
                api_c.START_DATE: datetime.strftime(
                    datetime.utcnow() - relativedelta(days=2),
                    api_c.DEFAULT_DATE_FORMAT,
                ),
                api_c.END_DATE: datetime.strftime(
                    datetime.utcnow(),
                    api_c.DEFAULT_DATE_FORMAT,
                ),
                db_c.NOTIFICATION_QUERY_PARAMETER_BATCH_SIZE: 10,
                db_c.NOTIFICATION_QUERY_PARAMETER_BATCH_NUMBER: 1,
                api_c.QUERY_PARAMETER_NOTIFICATION_TYPES: expected_notification_types,
                api_c.QUERY_PARAMETER_NOTIFICATION_CATEGORY: expected_notification_categories,
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(expected_notifications), response.json[api_c.TOTAL])
        self.assertCountEqual(
            expected_notifications, response.json[api_c.NOTIFICATIONS_TAG]
        )
        for notification in response.json[api_c.NOTIFICATIONS_TAG]:
            self.assertIn(
                notification[api_c.NOTIFICATION_TYPE],
                expected_notification_types,
            )
            self.assertIn(
                notification[db_c.CATEGORY],
                expected_notification_categories,
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
            category=db_c.NOTIFICATION_CATEGORY_DELIVERY,
            username=self.test_username,
        )

        # write a user to the database
        user = set_user(
            database=self.database,
            okta_id=t_c.VALID_USER_RESPONSE[api_c.OKTA_ID_SUB],
            email_address=t_c.VALID_USER_RESPONSE[api_c.EMAIL],
            display_name=t_c.VALID_USER_RESPONSE[api_c.NAME],
            role=t_c.VALID_USER_RESPONSE[api_c.ROLE],
        )
        # update the user with alert configurations
        user = update_user(
            database=self.database,
            okta_id=user[db_c.OKTA_ID],
            update_doc={
                **api_c.ALERT_SAMPLE_RESPONSE,
                **{
                    db_c.UPDATED_BY: user[db_c.USER_DISPLAY_NAME],
                },
            },
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

                for notification in notifications[db_c.NOTIFICATIONS_COLLECTION]:
                    self.assertEqual(
                        notification[api_c.NOTIFICATION_TYPE],
                        db_c.NOTIFICATION_TYPE_SUCCESS,
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

        notification_id = "some_random_id"

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.NOTIFICATIONS_ENDPOINT}/{notification_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
