"""
Schemas for cdp data sources API
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int, validate, List, DateTime, Nested, Dict


class CdpDataSourceSchema(Schema):
    name = Str(required=True)
    category = Str(required=True)
    feed_count = Int()
    status = Str()
