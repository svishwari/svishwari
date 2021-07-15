"""
Creating this file to have modifications to default schema fields
"""
import logging
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
            return value.isoformat(sep="T", timespec="milliseconds") + "Z"
        except Exception as exc:  # pylint: disable=broad-except
            logging.warning(
                "Failed to convert to isoformat  %s: %s.",
                exc.__class__,
                exc,
            )
            return None
