"""Database client notification management tests"""
from unittest import TestCase

import mongomock
import pymongo
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database import constants as db_c
from huxunifylib.database import notification_management as nmg


class NotificationManagementTest(TestCase):
    """Test notification management"""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):
        """Setup resources before each test"""
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        notifications = [
            {
                "notification_type": db_c.NOTIFICATION_TYPE_SUCCESS,
                "description": "Successfully completed",
            },
            {
                "notification_type": db_c.NOTIFICATION_TYPE_CRITICAL,
                "description": "Delivery Failed",
            },
        ]

        self.notifications = [
            nmg.create_notification(database=self.database, **notification)
            for notification in notifications
        ]

    def test_create_notification(self):
        """Test creating a notification"""
        notification = nmg.create_notification(
            database=self.database,
            notification_type=db_c.NOTIFICATION_TYPE_CRITICAL,
            description="Delivery Failed",
        )

        self.assertTrue(notification is not None)

    def test_get_notifications_batch(self):
        """Test get all notifications via batch"""
        notifications = nmg.get_notifications_batch(
            database=self.database,
            batch_size=10,
            sort_order=pymongo.DESCENDING,
            batch_number=1,
        )

        self.assertCountEqual(
            self.notifications, notifications["notifications"]
        )
        self.assertEqual(
            len(self.notifications), notifications["total_records"]
        )

    def test_get_notifications(self):
        """Test get all notifications with a filter."""
        notifications = nmg.get_notifications(
            self.database, {db_c.TYPE: db_c.NOTIFICATION_TYPE_CRITICAL}
        )

        self.assertTrue(notifications[db_c.NOTIFICATIONS_COLLECTION])
        self.assertEqual(1, len(notifications[db_c.NOTIFICATIONS_COLLECTION]))
        self.assertEqual(
            notifications[db_c.NOTIFICATIONS_COLLECTION][0][db_c.TYPE],
            db_c.NOTIFICATION_TYPE_CRITICAL,
        )

    def test_delete_notification(self):
        """Test deleting a notification"""
        notification = nmg.create_notification(
            database=self.database,
            notification_type=db_c.NOTIFICATION_TYPE_CRITICAL,
            description="Delivery Failed",
        )

        self.assertTrue(notification is not None)

        self.assertTrue(
            nmg.delete_notification(
                database=self.database, notification_id=notification[db_c.ID]
            )
        )
