"""Notification Schema Tests."""
from datetime import datetime
from unittest import TestCase
from bson import ObjectId

from huxunifylib.database import constants as db_c

from huxunify.api import constants as api_c
from huxunify.api.schema.notifications import NotificationSchema


class TestNotificationSchema(TestCase):
    """Test Notification related schemas."""

    def test_notification_schema(self):
        """Test NotificationSchema."""

        current_time = datetime.utcnow()
        doc = dict(
            _id=str(ObjectId()),
            type=db_c.NOTIFICATION_TYPE_SUCCESS,
            description="Successfully delivered",
            created=current_time,
            category=api_c.DELIVERY_TAG,
        )

        res = NotificationSchema().dump(doc)

        self.assertEqual(
            res["notification_type"], doc[db_c.NOTIFICATION_FIELD_TYPE].title()
        )
        self.assertEqual(
            res[db_c.NOTIFICATION_FIELD_CATEGORY],
            doc[db_c.NOTIFICATION_FIELD_CATEGORY].title(),
        )
        self.assertIsInstance(res[db_c.NOTIFICATION_FIELD_CREATED], str)
