"""
Purpose of this file is to house all the route/utils tests
"""
from datetime import datetime, timedelta
from unittest import TestCase
from huxunify.api.route.utils import get_friendly_delivered_time


class TestRouteUtils(TestCase):
    """Test routes utils"""

    def test_get_friendly_delivery_time(self):
        """
        Test get friendly delivered time

        """

        delivered_time = datetime.utcnow() - timedelta(days=2)
        response = get_friendly_delivered_time(delivered_time)
        self.assertEqual("2 days ago", response)

        delivered_time = datetime.utcnow() - timedelta(hours=5)
        response = get_friendly_delivered_time(delivered_time)
        self.assertEqual("5 hours ago", response)

        delivered_time = datetime.utcnow() - timedelta(minutes=15)
        response = get_friendly_delivered_time(delivered_time)
        self.assertEqual("15 minutes ago", response)

        delivered_time = datetime.utcnow() - timedelta(seconds=15)
        response = get_friendly_delivered_time(delivered_time)
        self.assertEqual("15 seconds ago", response)
