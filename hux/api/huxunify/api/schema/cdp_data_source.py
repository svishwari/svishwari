"""
Schemas for cdp data sources API
"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Int

from huxunify.api.schema.utils import validate_object_id, must_not_be_blank


class CdpDataSourcePostSchema(Schema):
    name = Str(required=True, validate=must_not_be_blank)
    category = Str(required=True, validate=must_not_be_blank)


class CdpDataSourceSchema(Schema):
    data_source_id = Str(required=True, validate=validate_object_id)
    name = Str(required=True)
    category = Str(required=True)
    feed_count = Int()
    status = Str()
