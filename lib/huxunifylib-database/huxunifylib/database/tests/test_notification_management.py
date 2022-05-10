"""Database client notification management tests."""
from unittest import TestCase
from datetime import datetime
from dateutil.relativedelta import relativedelta

import mongomock
import pymongo
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database import constants as db_c
from huxunifylib.database import notification_management as nmg


class NotificationManagementTest(TestCase):
    """Test notification management."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):
        """Setup resources before each test."""

        self.database = DatabaseClient(host="localhost", port=27017).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        self.test_username = "test_user"

        notifications = [
            {
                "notification_type": db_c.NOTIFICATION_TYPE_SUCCESS,
                "description": "Successfully completed delivery",
                "category": db_c.NOTIFICATION_CATEGORY_DELIVERY,
                "username": self.test_username,
            },
            {
                "notification_type": db_c.NOTIFICATION_TYPE_CRITICAL,
                "description": "Delivery Failed",
                "category": db_c.NOTIFICATION_CATEGORY_DELIVERY,
                "username": self.test_username,
            },
        ]

        self.notifications = [
            nmg.create_notification(database=self.database, **notification)
            for notification in notifications
        ]

    def test_create_notification_informational(self):
        """Test creating a informational notification."""

        notification = nmg.create_notification(
            database=self.database,
            notification_type=db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            description="Some Information",
            username=self.test_username,
            category=db_c.NOTIFICATION_CATEGORY_DELIVERY,
            platform=db_c.AZURE_COSMOS_DB,
        )

        self.assertIsNotNone(notification)
        self.assertIn(db_c.ID, notification)
        self.assertIn(db_c.NOTIFICATION_FIELD_CREATE_TIME, notification)
        self.assertEqual(
            db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            notification[db_c.NOTIFICATION_FIELD_TYPE],
        )
        self.assertEqual(
            "Some Information",
            notification[db_c.NOTIFICATION_FIELD_DESCRIPTION],
        )
        self.assertEqual(
            self.test_username, notification[db_c.NOTIFICATION_FIELD_USERNAME]
        )
        self.assertIsInstance(notification[db_c.TTL], int)

    def test_create_notification_success(self):
        """Test creating a notification."""

        notification = nmg.create_notification(
            database=self.database,
            notification_type=db_c.NOTIFICATION_TYPE_SUCCESS,
            description="Some Information",
            category=db_c.NOTIFICATION_CATEGORY_DELIVERY,
            username=self.test_username,
        )

        current_time = datetime.utcnow()
        upper_bound = current_time + relativedelta(weeks=1) + relativedelta(minutes=1)
        lower_bound = current_time + relativedelta(weeks=1) - relativedelta(minutes=1)

        self.assertIsNotNone(notification)
        self.assertIn(db_c.ID, notification)
        self.assertIn(db_c.NOTIFICATION_FIELD_CREATE_TIME, notification)
        self.assertEqual(
            db_c.NOTIFICATION_TYPE_SUCCESS,
            notification[db_c.NOTIFICATION_FIELD_TYPE],
        )
        self.assertEqual(
            "Some Information",
            notification[db_c.NOTIFICATION_FIELD_DESCRIPTION],
        )
        self.assertEqual(
            self.test_username, notification[db_c.NOTIFICATION_FIELD_USERNAME]
        )
        self.assertLess(notification[db_c.EXPIRE_AT], upper_bound)
        self.assertGreater(notification[db_c.EXPIRE_AT], lower_bound)

    def test_create_notification_critical(self):
        """Test creating a critical notification."""

        notification = nmg.create_notification(
            database=self.database,
            notification_type=db_c.NOTIFICATION_TYPE_CRITICAL,
            description="Some Information",
            category=db_c.NOTIFICATION_CATEGORY_DELIVERY,
            username=self.test_username,
        )

        current_time = datetime.utcnow()
        upper_bound = current_time + relativedelta(weeks=4) + relativedelta(minutes=1)
        lower_bound = current_time + relativedelta(weeks=4) - relativedelta(minutes=1)

        self.assertIsNotNone(notification)
        self.assertIn(db_c.ID, notification)
        self.assertIn(db_c.NOTIFICATION_FIELD_CREATE_TIME, notification)
        self.assertEqual(
            db_c.NOTIFICATION_TYPE_CRITICAL,
            notification[db_c.NOTIFICATION_FIELD_TYPE],
        )
        self.assertEqual(
            "Some Information",
            notification[db_c.NOTIFICATION_FIELD_DESCRIPTION],
        )
        self.assertEqual(
            self.test_username, notification[db_c.NOTIFICATION_FIELD_USERNAME]
        )
        self.assertLess(notification[db_c.EXPIRE_AT], upper_bound)
        self.assertGreater(notification[db_c.EXPIRE_AT], lower_bound)

    # TODO just use validation error when deprecation warning is removed
    # def test_create_notification_bad_category(self):
    #     """Test creating a notification with an invalid category."""
    #
    #     with self.assertRaises(ValueError):
    #         nmg.create_notification(
    #             database=self.database,
    #             notification_type=db_c.NOTIFICATION_TYPE_CRITICAL,
    #             description="Some Information",
    #             category="Invalid category",
    #             username=self.test_username,
    #         )

    def test_create_notification_bad_type(self):
        """Test creating a notification with a invalid type."""

        with self.assertRaises(ValueError):
            nmg.create_notification(
                database=self.database,
                notification_type="Bad type",
                description="Some Information",
                category=db_c.NOTIFICATION_CATEGORY_DELIVERY,
                username=self.test_username,
            )

    def test_get_notifications_batch(self):
        """Test get all notifications via batch."""

        notifications = nmg.get_notifications_batch(
            database=self.database,
            batch_size=10,
            sort_order=pymongo.DESCENDING,
            batch_number=1,
            notification_types=[],
            notification_categories=[],
            users=[],
            start_date="",
            end_date="",
        )

        self.assertCountEqual(
            self.notifications, notifications[db_c.NOTIFICATIONS_COLLECTION]
        )
        self.assertEqual(len(self.notifications), notifications["total_records"])

    def test_get_notifications_same_day_batch(self):
        """Test get all notifications via batch for a single day."""

        notifications = nmg.get_notifications_batch(
            database=self.database,
            batch_size=10,
            sort_order=pymongo.DESCENDING,
            batch_number=1,
            notification_types=[],
            notification_categories=[],
            users=[],
            start_date=datetime.combine(datetime.utcnow().date(), datetime.min.time()),
            end_date=datetime.combine(datetime.utcnow().date(), datetime.min.time()),
        )

        self.assertCountEqual(
            self.notifications, notifications[db_c.NOTIFICATIONS_COLLECTION]
        )
        self.assertEqual(len(self.notifications), notifications["total_records"])
        for notification in notifications["notifications"]:
            self.assertEqual(
                datetime.utcnow().date(),
                notification.get(db_c.NOTIFICATION_FIELD_CREATE_TIME).date(),
            )

    def test_get_notifications(self):
        """Test get all notifications with a filter."""

        notifications = nmg.get_notifications(
            self.database, {db_c.TYPE: db_c.NOTIFICATION_TYPE_CRITICAL}
        )

        self.assertTrue(notifications[db_c.NOTIFICATIONS_COLLECTION])
        self.assertEqual(1, len(notifications[db_c.NOTIFICATIONS_COLLECTION]))
        self.assertEqual(
            db_c.NOTIFICATION_TYPE_CRITICAL,
            notifications[db_c.NOTIFICATIONS_COLLECTION][0][db_c.TYPE],
        )

    def test_delete_notification(self):
        """Test deleting a notification"""
        notification = nmg.create_notification(
            database=self.database,
            notification_type=db_c.NOTIFICATION_TYPE_CRITICAL,
            description="Delivery Failed",
            category=db_c.NOTIFICATION_CATEGORY_DELIVERY,
            username=self.test_username,
        )

        self.assertIsNotNone(notification)

        self.assertTrue(
            nmg.delete_notification(
                database=self.database, notification_id=notification[db_c.ID]
            )
        )

        notification = nmg.get_notification(self.database, notification[db_c.ID])
        self.assertIsNone(notification)

    def test_hard_delete_notification(self):
        """Test hard deleting a notification"""
        notification = nmg.create_notification(
            database=self.database,
            notification_type=db_c.NOTIFICATION_TYPE_CRITICAL,
            description="Delivery Failed",
            category=db_c.NOTIFICATION_CATEGORY_DELIVERY,
            username=self.test_username,
        )

        self.assertIsNotNone(notification)

        self.assertTrue(
            nmg.delete_notification(
                database=self.database,
                notification_id=notification[db_c.ID],
                hard_delete=True,
            )
        )

        notification = nmg.get_notification(self.database, notification[db_c.ID])
        self.assertIsNone(notification)

    def test_get_notification(self):
        """Test to get notification."""
        notifications = nmg.get_notifications(
            self.database, {db_c.TYPE: db_c.NOTIFICATION_TYPE_CRITICAL}
        )
        notification = nmg.get_notification(
            self.database,
            notification_id=notifications[db_c.NOTIFICATIONS_COLLECTION][0][db_c.ID],
        )
        self.assertTrue(notification)
        self.assertFalse(notification[db_c.DELETED])
        self.assertEqual(
            notifications[db_c.NOTIFICATIONS_COLLECTION][0][db_c.TYPE],
            notification[db_c.TYPE],
        )
