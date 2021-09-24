"""Purpose of this file is to house all the route/utils tests"""
from datetime import datetime, timedelta
from unittest import TestCase
from bson import ObjectId
from marshmallow import ValidationError

from huxunify.api.route.utils import (
    get_friendly_delivered_time,
    update_metrics,
    Validation,
)
from huxunify.api import constants


class TestRouteUtils(TestCase):
    """Test routes utils"""

    def test_get_friendly_delivery_time(self):
        """Test get friendly delivered time"""

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

    def test_update_metrics(self):
        """Test update metrics"""

        target_id = ObjectId()
        perf_metric = update_metrics(
            target_id, "test_name", [], [], constants.DISPLAY_ADS
        )

        self.assertEqual(str(target_id), perf_metric.get(constants.ID))
        self.assertEqual("test_name", perf_metric.get(constants.NAME))

    def test_validate_integer(self):
        """Tests the Validation class static method validate_integer"""

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_integer("a")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_integer("1.1")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_integer("-1")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_integer("0")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_integer("12341234567123456")

        Validation.validate_integer("1")
        Validation.validate_integer("12345")

    def test_validate_boolean(self):
        """Tests the Validation class static method validate_boolean"""

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_bool("tru")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_bool("0")

        Validation.validate_bool("true")
        Validation.validate_bool("false")
        Validation.validate_bool("TRUE")
        Validation.validate_bool("FALSE")
        Validation.validate_bool("TrUe")
        Validation.validate_bool("fAlSe")

    def test_validate_date(self):
        """Tests the Validation class static method validate_date"""

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_date("2021-09-111")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_date("2021-09-aa")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_date("2021-09-111")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_date("2021-13-1")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_date("20212-13-1")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_date("1969-0009-0001")

        Validation.validate_date("2021-12-1")
        Validation.validate_date("2021-09-01")
        Validation.validate_date("1969-9-1")

    def test_validate_date_range(self):
        """Tests the Validation class static method validate_date_range"""

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_date_range("2021-09-11", "2021-09-11")

        with self.assertRaises(expected_exception=ValidationError):
            Validation.validate_date_range("2021-09-11", "2021-13-11")

        Validation.validate_date_range("2021-9-11", "2021-9-12")
