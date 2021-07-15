"""
Creating this file to have modifications to default schema fields
"""
from marshmallow.fields import DateTime


class DateTimeWithZ(DateTime):
    """
    This class is to modify serialization of datetime
    We need
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.isoformat(sep="T", timespec="milliseconds") + "Z"
