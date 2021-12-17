"""Scheduled Delivery related schema tests."""
from random import sample
from unittest import TestCase

from hypothesis import given, strategies as st

from huxunify.api import constants as api_c
from huxunify.api.schema.destinations import (
    DeliveryScheduleDailySchema,
    DeliveryScheduleWeeklySchema,
    DeliveryScheduleMonthlySchema,
)


class DeliveryScheduleSchemaTest(TestCase):
    """Test Delivery Schedule Schemas."""

    @given(
        days=st.integers(min_value=1, max_value=7),
        hours=st.integers(min_value=1, max_value=12),
        minutes=st.integers(min_value=0, max_value=45),
        meridiem=st.sampled_from(["AM", "PM"]),
    )
    def test_daily_schema(
        self, days: int, hours: int, minutes: int, meridiem: str
    ) -> None:
        """Test DeliveryScheduleDailySchema.

        Args:
            days (int): Day of delivery.
            hours (int): Hour of delivery.
            minutes (int): Minute of delivery.
            meridiem (str): Meridiem of delivery.

        """

        doc = {
            api_c.PERIODICIY: "Daily",
            api_c.EVERY: days,
            api_c.HOUR: hours,
            api_c.MINUTE: minutes,
            api_c.PERIOD: meridiem,
        }

        daily_schedule = DeliveryScheduleDailySchema().load(doc)
        for value in daily_schedule.values():
            self.assertIn(type(value), [int, str])
        self.assertEqual(daily_schedule[api_c.PERIODICIY], api_c.DAILY)
        self.assertFalse(DeliveryScheduleDailySchema().validate(doc))

    @given(
        weeks=st.integers(min_value=1, max_value=4),
        hours=st.integers(min_value=1, max_value=12),
        minutes=st.integers(min_value=0, max_value=45),
        meridiem=st.sampled_from([api_c.AM, api_c.PM]),
        day_of_week=st.integers(min_value=1, max_value=7),
    )
    def test_weekly_schema(
        self,
        weeks: int,
        hours: int,
        minutes: int,
        meridiem: str,
        day_of_week: int,
    ) -> None:
        """Test DeliveryScheduleWeeklySchema.

        Args:
            weeks (int): Day of delivery.
            hours (int): Hour of delivery.
            minutes (int): Minute of delivery.
            meridiem (str): Meridiem of delivery.
            day_of_week (int): Day of the week.

        """

        doc = {
            api_c.PERIODICIY: "Weekly",
            # sample twice to force an in place shuffle.
            api_c.DAY_OF_WEEK: sample(
                sample(api_c.DAY_LIST, day_of_week), day_of_week
            ),
            api_c.EVERY: weeks,
            api_c.HOUR: hours,
            api_c.MINUTE: minutes,
            api_c.PERIOD: meridiem,
        }

        weekly_schedule = DeliveryScheduleWeeklySchema().load(doc)
        for value in weekly_schedule.values():
            self.assertIn(type(value), [int, str, list])
        self.assertEqual(weekly_schedule[api_c.PERIODICIY], api_c.WEEKLY)
        self.assertFalse(DeliveryScheduleWeeklySchema().validate(doc))

    @given(
        months=st.integers(min_value=1, max_value=12),
        hours=st.integers(min_value=1, max_value=12),
        minutes=st.integers(min_value=0, max_value=45),
        meridiem=st.sampled_from([api_c.AM, api_c.PM]),
        monthly_period=st.sampled_from(api_c.MONTHLY_PERIOD_LIST),
        days=st.sampled_from(api_c.DAY_OF_MONTH_LIST),
    )
    def test_monthly_schema(
        self,
        months: int,
        hours: int,
        minutes: int,
        meridiem: str,
        monthly_period: str,
        days: str,
    ) -> None:
        """Test DeliveryScheduleMonthlySchema.

        Args:
            months (int): Day of delivery.
            hours (int): Hour of delivery.
            minutes (int): Minute of delivery.
            meridiem (str): Meridiem of delivery.
            monthly_period (str): Monthly period.
            days (str): String Day of the month.

        """

        doc = {
            api_c.PERIODICIY: "Monthly",
            api_c.EVERY: months,
            api_c.HOUR: hours,
            api_c.MINUTE: minutes,
            api_c.PERIOD: meridiem,
            api_c.MONTHLY_PERIOD_ITEMS: [monthly_period],
            api_c.DAY_OF_MONTH: [days],
        }

        monthly_schedule = DeliveryScheduleMonthlySchema().load(doc)
        for value in monthly_schedule.values():
            self.assertIn(type(value), [int, str, list])
        self.assertEqual(monthly_schedule[api_c.PERIODICIY], api_c.MONTHLY)
        self.assertFalse(DeliveryScheduleMonthlySchema().validate(doc))
