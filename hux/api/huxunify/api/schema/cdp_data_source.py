"""Schemas for cdp data sources API"""

from flask_marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import OneOf, Range

import huxunifylib.database.constants as db_c
from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api.schema.utils import validate_object_id, must_not_be_blank
from huxunify.api import constants as api_c


class CdpDataSourcePostSchema(Schema):
    """CDP data source post schema class"""

    name = fields.Str(required=True, validate=must_not_be_blank)
    type = fields.Str(required=True, validate=must_not_be_blank)
    status = fields.Str(
        required=True,
        validate=OneOf(choices=[api_c.STATUS_ACTIVE, api_c.STATUS_PENDING]),
        default=api_c.STATUS_PENDING,
    )
    category = fields.Str(
        required=True,
        validate=OneOf(
            choices=api_c.CDP_DATA_SOURCE_CATEGORIES + [db_c.CATEGORY_UNKNOWN]
        ),
        default=db_c.CATEGORY_UNKNOWN,
        allow_none=True,
    )
    feed_count = fields.Int(required=False, default=None)


class CdpDataSourceSchema(Schema):
    """CDP data source get schema class, return the serialized messages back"""

    id = fields.Str(
        attribute=db_c.ID,
        example="5f5f7262997acad4bac4373b",
        required=False,
        validate=validate_object_id,
    )
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    category = fields.Str(
        required=True,
        validate=OneOf(
            choices=api_c.CDP_DATA_SOURCE_CATEGORIES + [db_c.CATEGORY_UNKNOWN]
        ),
        default=db_c.CATEGORY_UNKNOWN,
        allow_none=True,
    )
    feed_count = fields.Int(required=False, default=None, allow_none=True)
    status = fields.Str(
        required=True,
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
    is_added = fields.Bool(required=False, attribute=db_c.ADDED, default=False)
    is_enabled = fields.Bool(
        required=False, attribute=db_c.ENABLED, default=False
    )


class CdpConnectionsDataSourceSchema(Schema):
    """CDP connections data source get schema"""

    label = fields.Str(attribute=api_c.NAME, required=True)
    name = fields.Str(attribute=api_c.TYPE, required=True)
    status = fields.Str(
        required=True,
        validate=[
            OneOf(
                choices=[
                    api_c.STATUS_ACTIVE,
                    api_c.STATUS_PENDING,
                ]
            )
        ],
    )
    category = fields.Str(
        required=False,
        validate=OneOf(
            choices=api_c.CDP_DATA_SOURCE_CATEGORIES + [db_c.CATEGORY_UNKNOWN]
        ),
        default=db_c.CATEGORY_UNKNOWN,
        allow_none=True,
    )
    feed_count = fields.Int(required=False, default=None, allow_none=True)


class CdpDataSourceDataFeedTypeAverageSchema(Schema):
    """Data source data feed type average schema with value and flag
    indicator."""

    value = fields.Float(
        validate=Range(min_inclusive=0.0, max_inclusive=1.0), example=0.75
    )
    flag_indicator = fields.Bool(default=False)


class CdpDataSourceDataFeedSchema(Schema):
    """Data source data feed schema"""

    name = fields.Str()
    datasource_type = fields.Str(example=db_c.DATA_SOURCE_PLATFORM_BLUECORE)
    records_received = fields.Int(example=345612)
    records_processed = fields.Int(example=345612)
    records_processed_percentage = fields.Nested(
        CdpDataSourceDataFeedTypeAverageSchema,
        attribute=api_c.RECORDS_PROCESSED_PERCENTAGE,
    )
    thirty_days_avg = fields.Nested(
        CdpDataSourceDataFeedTypeAverageSchema,
        attribute=api_c.THIRTY_DAYS_AVG,
    )
    last_processed = DateTimeWithZ(
        attribute=api_c.PROCESSED_AT, example="2021-01-01T17:56:07.290Z"
    )
    status = fields.Str(
        validate=OneOf(
            choices=[
                api_c.STATUS_ACTIVE,
                api_c.STATUS_PENDING,
                api_c.STATUS_ERROR,
            ]
        ),
        default=api_c.STATUS_PENDING,
    )


class DataSourceDataFeedsGetSchema(Schema):
    """Data source data feeds get schema"""

    name = fields.Str()
    type = fields.Str()
    datafeeds = fields.List(fields.Nested(CdpDataSourceDataFeedSchema))


class IndividualDataSourceDataFeedDetailSchema(Schema):
    """Data source data feed details get schema"""

    filename = fields.Str(example="unsubscribe_1")
    last_processed = DateTimeWithZ(example="2022-01-01T01:02:03Z")
    thirty_days_avg = fields.Float(example=0.87)
    records_processed = fields.Int(example=20000)
    records_received = fields.Int(example=25000)
    records_processed_percentage = fields.Float(example=0.8)
    run_duration = fields.Str(example="01:32:45")
    status = fields.Str(
        validate=OneOf(
            [
                api_c.STATUS_SUCCESS,
                api_c.STATUS_RUNNING,
                api_c.STATUS_FAILED,
                api_c.STATUS_DISABLED,
                api_c.STATUS_CANCELLED,
            ]
        ),
        example=api_c.STATUS_SUCCESS,
    )
    sub_status = fields.Str(
        validate=OneOf(
            [
                api_c.STATUS_IN_PROGRESS,
                api_c.STATUS_PARTIAL_SUCCESS_PROGRESS,
                api_c.STATUS_WAITING,
                api_c.STATUS_PARTIAL_SUCCESS_WAITING,
                api_c.STATUS_COMPLETE,
                api_c.STATUS_FAILED,
                api_c.STATUS_CANCELLED,
                api_c.STATUS_PARTIAL_SUCCESS,
            ]
        ),
        example=api_c.STATUS_SUCCESS,
    )


class DataSourceDataFeedDetailsGetSchema(Schema):
    """Data source data feed details get schema"""

    name = DateTimeWithZ(example="2022-01-01T01:02:03Z")
    filename = fields.Str(example="unsubscribe_1")
    last_processed_start = DateTimeWithZ(example="2022-01-01T01:02:03Z")
    last_processed_end = DateTimeWithZ(example="2022-01-01T01:02:03Z")
    thirty_days_avg = fields.Float(example=0.89)
    records_processed = fields.Int(example=40000)
    records_received = fields.Int(example=50000)
    records_processed_percentage = fields.Float(example=0.8)
    status = fields.Str(
        validate=OneOf(
            [
                api_c.STATUS_COMPLETE,
                api_c.STATUS_INCOMPLETE,
                api_c.STATUS_FAILED,
                api_c.STATUS_SUCCESS,
                api_c.STATUS_RUNNING,
                api_c.STATUS_DISABLED,
                api_c.STATUS_CANCELLED,
            ]
        ),
        example=api_c.STATUS_COMPLETE,
    )
    data_files = fields.List(
        fields.Nested(IndividualDataSourceDataFeedDetailSchema)
    )
