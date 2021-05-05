"""
Schemas for cdp data sources API
"""

from flask_marshmallow import Schema
from marshmallow import post_dump
from marshmallow.fields import Str, Int
from huxunifylib.database.constants import ID, CDP_DATA_SOURCE_ID
from huxunify.api.schema.utils import validate_object_id, must_not_be_blank


class CdpDataSourcePostSchema(Schema):
    """
    CdpDataSourcePostSchema.
    """

    name = Str(required=True, validate=must_not_be_blank)
    category = Str(required=True, validate=must_not_be_blank)


class CdpDataSourceSchema(Schema):
    """
    CdpDataSourceSchema
    """

    data_source_id = Str(required=True, validate=validate_object_id)
    name = Str(required=True)
    category = Str(required=True)
    feed_count = Int()
    status = Str()

    @post_dump
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def post_serialize(self, data: dict, many=False) -> dict:
        """process the schema before serializing.

        Args:
            data (dict): The CDP data source object
            many (bool): If there are many to process
        Returns:
            Response: Returns a CDP data source object

        """
        # map id to data_source_id
        if ID in data:
            data[CDP_DATA_SOURCE_ID] = str(data[ID])
            del data[ID]

        return data
