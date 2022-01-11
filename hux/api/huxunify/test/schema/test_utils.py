"""Purpose of this file is to test the utils schemas"""
import datetime
from unittest import TestCase
from hypothesis import given, strategies as st

from huxunify.api import constants as api_c
from huxunify.api.schema.utils import get_next_schedule


class TestUtilsSchemas(TestCase):
    """Utils Schema test class."""

    @given(
        minute=st.sampled_from(list(range(60))),
        hour=st.sampled_from(list(range(24))),
        day=st.sampled_from(list(range(1, 32))),
    )
    def test_get_next_schedule(self, minute: int, hour: int, day: int):
        """Test get next schedule.

        Args:
            minute (int): Minute of hour
            hour (int): Hour of the day
            day (int): Day of the month
        """
        cron_expression = f"{minute} {hour} {day} * ? *"
        start_date = datetime.datetime.today()

        next_schedule = get_next_schedule(cron_expression, start_date)
        self.assertEqual(day, next_schedule.day)
        self.assertEqual(hour, next_schedule.hour)
        self.assertEqual(minute, next_schedule.minute)

    @given(
        minute=st.integers(min_value=60),
        hour=st.integers(min_value=24),
        day=st.integers(min_value=32, max_value=99),
    )
    def test_get_next_schedule_bad_cron_error(
        self, minute: int, hour: int, day: int
    ):
        """Test get next schedule throwing CroniterBadCronError.

        Args:
            minute (int): Minute of hour
            hour (int): Hour of the day
            day (int): Day of the month
        """
        cron_expression = f"{minute} {hour} {day} * ? *"
        start_date = datetime.datetime.today()

        next_schedule = get_next_schedule(cron_expression, start_date)
        self.assertIsNone(next_schedule)

    @given(
        minute=st.sampled_from(list(range(60))),
        hour=st.sampled_from(list(range(24))),
        day_of_week=st.sampled_from(["abc", "def"]),
    )
    def test_get_next_schedule_not_alpha_error(
        self, minute: int, hour: int, day_of_week: str
    ):
        """Test get next schedule throwing CroniterNotAlphaError.

        Args:
            minute (int): Minute of hour
            hour (int): Hour of the day
            day_of_week (str): Day of the week
        """
        cron_expression = f"{minute} {hour} * * {day_of_week} *"
        start_date = datetime.datetime.today()

        next_schedule = get_next_schedule(cron_expression, start_date)
        self.assertIsNone(next_schedule)

    def test_get_next_schedule_invalid_params(self):
        """Test get next schedule with invalid params."""
        invalid_cron_expressions = [123, True, 12.234, datetime.date.today()]
        start_date = datetime.datetime.strftime(
            datetime.datetime.today(), api_c.DEFAULT_DATE_FORMAT
        )

        for cron_expression in invalid_cron_expressions:
            next_schedule = get_next_schedule(cron_expression, start_date)
            self.assertIsNone(next_schedule)
