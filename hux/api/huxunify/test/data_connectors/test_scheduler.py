"""Purpose of this file is to park all tests for scheduler."""
import unittest
from huxunify.api.data_connectors.scheduler import generate_cron

weekly_schedule = {
    "periodicity": "Weekly",
    "every": 1,
    "hour": 11,
    "minute": 15,
    "period": "PM",
    "day_of_month": "*",
    "month": "*",
    "day_of_week": ["sun", "mon"],
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

monthly_schedule = {
    "periodicity": "Monthly",
    "every": 2,
    "hour": 11,
    "minute": 15,
    "period": "PM",
    "day_of_month": "1",
    "month": "*",
    "day_of_week": "*",
}


class SchedulerTest(unittest.TestCase):
    """Class for Scheduler Test."""

    def test_generate_cron(self):
        """Test for generating cron from scheduler module."""

        self.assertEqual("15 23 ? * sun,mon *", generate_cron(weekly_schedule))
        self.assertEqual("15 23 */2 * ? *", generate_cron(daily_schedule))

        self.assertEqual("15 23 1 */2 ? *", generate_cron(monthly_schedule))
