"""Scheduled Delivery related schema tests"""
from unittest import TestCase


from huxunify.api import constants as api_c
from huxunify.api.schema.destinations import (
    DeliveryScheduleDailySchema,
    DeliveryScheduleWeeklySchema,
    DeliveryScheduleMonthlySchema,
)


class DeliveryScheduleSchemaTest(TestCase):
    """
    Test DeliveryScheduleDailySchema
    """

    def test_daily_schema(self) -> None:
        """Test DeliveryScheduleDailySchema.

        Args:

        Returns:
            None
        """

        doc = {
            "periodicity": "Daily",
            "every": 2,
            "hour": 11,
            "minute": 15,
            "period": "PM",
        }

        daily_schedule = DeliveryScheduleDailySchema().load(doc)
        _ = [
            self.assertIn(type(x), [int, str]) for x in daily_schedule.values()
        ]
        self.assertEqual(daily_schedule["periodicity"], api_c.DAILY)
        self.assertFalse(DeliveryScheduleDailySchema().validate(doc))

    def test_weekly_schema(self) -> None:
        """Test DeliveryScheduleWeeklySchema.

        Args:

        Returns:
            None
        """

        doc = {
            "periodicity": "Weekly",
            "every": 2,
            "hour": 11,
            "minute": 15,
            "period": "PM",
            "day_of_week": ["MON", "TUE"],
        }

        weekly_schedule = DeliveryScheduleWeeklySchema().load(doc)
        _ = [
            self.assertIn(type(x), [int, str, list])
            for x in weekly_schedule.values()
        ]
        self.assertEqual(weekly_schedule["periodicity"], api_c.WEEKLY)
        self.assertFalse(DeliveryScheduleWeeklySchema().validate(doc))

    def test_monthly_schema(self) -> None:
        """Test DeliveryScheduleMonthlySchema.

        Args:

        Returns:
            None
        """

        doc = {
            "periodicity": "Monthly",
            "every": 12,
            "hour": 11,
            "minute": 15,
            "period": "PM",
            "monthly_period_items": ["Day"],
            "day_of_month": ["1"],
        }

        monthly_schedule = DeliveryScheduleMonthlySchema().load(doc)
        _ = [
            self.assertIn(type(x), [int, str, list])
            for x in monthly_schedule.values()
        ]
        self.assertEqual(monthly_schedule["periodicity"], api_c.MONTHLY)
        self.assertFalse(DeliveryScheduleMonthlySchema().validate(doc))
