"""
Schemas for the notifications API
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int


class NotificationSchema(Schema):
    """Notifications Schema"""

    notification_type = Str(required=True)
    description = Str(required=True)
    created = Int(required=True)
