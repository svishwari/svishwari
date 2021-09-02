"""
Schemas for cdp data sources API
"""

from flask_marshmallow import Schema
from marshmallow import post_dump, fields
from marshmallow.validate import OneOf, Range

import huxunifylib.database.constants as db_c
from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api.schema.utils import validate_object_id, must_not_be_blank
from huxunify.api import constants as api_c


class CdpDataSourcePostSchema(Schema):
    """
    CdpDataSourcePostSchema.
    """

    name = fields.Str(required=True, validate=must_not_be_blank)
    category = fields.Str(required=True, validate=must_not_be_blank)


class CdpDataSourceSchema(Schema):
    """
    CdpDataSourceSchema
    """

    _id = fields.Str(
        data_key=api_c.ID,
        example="5f5f7262997acad4bac4373b",
        required=True,
        validate=validate_object_id,
    )
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    feed_count = fields.Int()
    status = fields.Str(
        validate=[
            OneOf(
                choices=[
                    api_c.STATUS_ACTIVE,
                    api_c.STATUS_PENDING,
                ]
            )
        ],
        default=api_c.STATUS_ACTIVE,
    )
    is_added = fields.Bool(attribute="added")
    is_enabled = fields.Bool(attribute="enabled")
    type = fields.Str()

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
        if db_c.ID in data:
            data[db_c.CDP_DATA_SOURCE_ID] = str(data[db_c.ID])
            del data[db_c.ID]

        return data


class CdpDataSourceDataFeedSchema(Schema):
    """
    Data source data feed schema
    """

    name = fields.Str()
    datasource_type = fields.Str(example=db_c.CDP_DATA_SOURCE_BLUECORE)
    records_received = fields.Int(example=345612)
    records_processed = fields.Int(example=345612)
    records_processed_percentage = fields.Float(
        validate=Range(min_inclusive=0.0, max_inclusive=1.0), example=0.9
    )
    thirty_days_avg = fields.Float(example=76.45)
    last_processed = DateTimeWithZ(
        attribute=api_c.PROCESSED_AT, example="2021-01-01T17:56:07.290Z"
    )
    status = fields.Str(
        validate=OneOf(choices=[api_c.STATUS_ACTIVE, api_c.STATUS_PENDING]),
        default=api_c.STATUS_PENDING,
    )


class DataSourceDataFeedsGetSchema(Schema):
    """
    Data source data feeds get schema
    """

    name = fields.Str()
    type = fields.Str()
    datafeeds = fields.List(fields.Nested(CdpDataSourceDataFeedSchema))
