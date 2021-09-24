"""Creating this file to have modifications to default schema fields"""
import datetime
import logging
from typing import Any

import pytz
from marshmallow.fields import DateTime


class DateTimeWithZ(DateTime):
    """This class is to modify serialization of datetime"""

    def _serialize(self, value: datetime.datetime, attr: str, obj: Any, **kwargs):
        """Serializes Date Time Object with Z

        Args:
            value (datetime.datetime): The value to be serialized.
            attr (str): The attribute or key on the object to be serialized.
            obj (obj): The object the value was pulled from.
            **kwargs: Field-specific keyword arguments.

        Returns:
            str: datetime value with Z

        """
        if value is None:
            return None
        try:
            if value.tzinfo:
                # time zone aware
                if value.utcoffset() != datetime.timedelta(
                    days=0, hours=0, minutes=0, seconds=0
                ):
                    # no need to convert if already in utc
                    value = value.astimezone(pytz.UTC)
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
