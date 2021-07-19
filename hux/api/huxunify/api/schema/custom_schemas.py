"""
Creating this file to have modifications to default schema fields
"""
import datetime
import logging
import pytz
from marshmallow.fields import DateTime


class DateTimeWithZ(DateTime):
    """
    This class is to modify serialization of datetime
    We need
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        try:
            if value.tzinfo:
                # time zone aware
                if value.utcoffset() != datetime.timedelta(
                    days=0, hours=0, minutes=0, seconds=0
                ):
                    # no need to convert if already in utc
                    print(value.astimezone(pytz.UTC))
                return value.isoformat(
                    sep="T", timespec="milliseconds"
                ).replace("+00:00", "Z")
            return value.isoformat(sep="T", timespec="milliseconds") + "Z"

        except Exception as exc:  # pylint: disable=broad-except
            logging.warning(
                "Failed to convert to isoformat %s: %s.",
                exc.__class__,
                exc,
            )
            return None
