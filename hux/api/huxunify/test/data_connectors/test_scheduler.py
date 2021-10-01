"""Purpose of this file is to park all tests for scheduler."""
import unittest
from huxunify.api.data_connectors.scheduler import generate_cron

weekend_schedule = {
    "periodicity": "Weekly",
    "every": 2,
    "hour": 11,
    "minute": 15,
    "period": "PM",
    "day_of_month": "*",
    "month": "*",
    "day_of_week": ["Weekend"],
}

daily_schedule = {
    "periodicity": "Daily",
    "every": 2,
    "hour": 11,
    "minute": 15,
    "period": "PM",
    "day_of_month": "*",
    "month": "*",
    "day_of_week": "*",
}


class SchedulerTest(unittest.TestCase):
    """Class for Scheduler Test."""

    def test_generate_cron(self):
        """Test for generating cron from scheduler module."""

        self.assertEqual(generate_cron(daily_schedule), "15 23 ? * 1/2 *")

        self.assertEqual(
            generate_cron(weekend_schedule), "15 23 ? * SAT,SUN/2 *"
        )
