"""Notification Schema Tests"""
from datetime import datetime
from unittest import TestCase
from bson import ObjectId

from huxunifylib.database import constants as db_c

from huxunify.api.schema.notifications import NotificationSchema


class TestNotificationSchema(TestCase):
    """
    Test notification schema
    """

    def test_notification_schema(self):
        """
        Test notification schema
        """
        doc = dict(
            id=str(ObjectId()),
            notification_type=db_c.NOTIFICATION_TYPE_SUCCESS,
            description="Successfully delivered",
            created=datetime.strftime(
                datetime.utcnow(), "%Y-%m-%d %H:%M:%S.%f"
            ),
        )

        res = NotificationSchema().load(doc)
        self.assertEqual({}, NotificationSchema().validate(doc))
        self.assertIsInstance(res["created"], datetime)
