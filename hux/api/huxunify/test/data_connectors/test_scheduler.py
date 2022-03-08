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

monthly_schedule_list = [
    {
        "periodicity": "Monthly",
        "every": 2,
        "hour": 11,
        "minute": 15,
        "period": "PM",
        "day_of_month": ["1", "2"],
        "monthly_period_items": ["Day"],
        "month": "*",
        "day_of_week": "*",
    },
    {
        "periodicity": "Monthly",
        "every": 1,
        "hour": 11,
        "minute": 15,
        "period": "PM",
        "monthly_period_items": ["First"],
        "day_of_month": ["Tuesday", "Monday"],
    },
    {
        "periodicity": "Monthly",
        "every": 1,
        "hour": 11,
        "minute": 15,
        "period": "PM",
        "monthly_period_items": ["Last", "First"],
        "day_of_month": ["Monday"],
    },
    {
        "periodicity": "Monthly",
        "every": 1,
        "hour": 11,
        "minute": 15,
        "period": "PM",
        "monthly_period_items": ["First", "Last", "Third"],
        "day_of_month": ["Day"],
    },
]


class SchedulerTest(unittest.TestCase):
    """Class for Scheduler Test."""

    def test_generate_cron(self):
        """Test for generating cron from scheduler module."""

        self.assertEqual("15 23 ? * sun,mon *", generate_cron(weekly_schedule))
        self.assertEqual("15 23 */2 * ? *", generate_cron(daily_schedule))

        self.assertEqual(
            "15 23 1,2 */2 ? *", generate_cron(monthly_schedule_list[0])
        )

        self.assertEqual(
            "15 23 * * 2#1,1#1 *", generate_cron(monthly_schedule_list[1])
        )

        self.assertEqual(
            "15 23 1,L,3 * ? *", generate_cron(monthly_schedule_list[3])
        )
