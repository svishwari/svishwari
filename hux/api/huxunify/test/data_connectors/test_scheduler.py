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
    "day_of_week": ["SUN", "MON"],
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

        self.assertEqual(generate_cron(weekly_schedule), "15 23 * * SUN,MON")
        self.assertEqual(generate_cron(daily_schedule), "15 23 */2 * *")

        self.assertEqual("15 23 1 */2 *", generate_cron(monthly_schedule))
