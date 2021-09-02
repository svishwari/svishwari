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
            api_c.PERIODICIY: "Daily",
            api_c.EVERY: 2,
            api_c.HOUR: 11,
            api_c.MINUTE: 15,
            api_c.PERIOD: "PM",
        }

        daily_schedule = DeliveryScheduleDailySchema().load(doc)
        _ = [
            self.assertIn(type(x), [int, str]) for x in daily_schedule.values()
        ]
        self.assertEqual(daily_schedule[api_c.PERIODICIY], api_c.DAILY)
        self.assertFalse(DeliveryScheduleDailySchema().validate(doc))

    def test_weekly_schema(self) -> None:
        """Test DeliveryScheduleWeeklySchema.

        Args:

        Returns:
            None
        """

        doc = {
            api_c.PERIODICIY: "Weekly",
            api_c.EVERY: 2,
            api_c.HOUR: 11,
            api_c.MINUTE: 15,
            api_c.PERIOD: "PM",
            api_c.DAY_OF_WEEK: ["MON", "TUE"],
        }

        weekly_schedule = DeliveryScheduleWeeklySchema().load(doc)
        _ = [
            self.assertIn(type(x), [int, str, list])
            for x in weekly_schedule.values()
        ]
        self.assertEqual(weekly_schedule[api_c.PERIODICIY], api_c.WEEKLY)
        self.assertFalse(DeliveryScheduleWeeklySchema().validate(doc))

    def test_monthly_schema(self) -> None:
        """Test DeliveryScheduleMonthlySchema.

        Args:

        Returns:
            None
        """

        doc = {
            api_c.PERIODICIY: "Monthly",
            api_c.EVERY: 12,
            api_c.HOUR: 11,
            api_c.MINUTE: 15,
            api_c.PERIOD: "PM",
            api_c.MONTHLY_PERIOD_ITEMS: ["Day"],
            api_c.DAY_OF_MONTH: ["1"],
        }

        monthly_schedule = DeliveryScheduleMonthlySchema().load(doc)
        _ = [
            self.assertIn(type(x), [int, str, list])
            for x in monthly_schedule.values()
        ]
        self.assertEqual(monthly_schedule[api_c.PERIODICIY], api_c.MONTHLY)
        self.assertFalse(DeliveryScheduleMonthlySchema().validate(doc))
