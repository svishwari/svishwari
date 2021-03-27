# pylint: disable=no-self-use
"""
Schemas for the CDM API
"""
from datetime import datetime
from typing import Union, List
from dateutil import parser
from flask_marshmallow import Schema
from marshmallow import validate, pre_dump
from marshmallow.fields import Boolean, DateTime, Int, Str, Float


DATA_TYPES: List[str] = [
    "customers",
    "orders",
    "items",
]

FEED_TYPES: List[str] = [
    "api",
    "batch",
]

FIELD_NAMES: List[str] = [
    "FNAME",
    "LNAME",
    "ADD1",
    "ADD2",
    "ADD3",
    "CITY",
    "STATE",
    "ZIP",
    "COMPANY",
    "TITLE",
    "EMAIL",
]

FILE_EXTENSIONS: List[str] = [
    "csv",
    "json",
]


def clean_date(date_obj: Union[datetime, str]) -> datetime:
    """cleans dates that come back from snowflake as strings instead of DateTimes

    Args:
        date_obj (datetime|str): A datetime or string object

    Returns:
        datetime: Returns a datetime object

    """
    # if string instance, convert to datetime.
    return parser.parse(date_obj) if isinstance(date_obj, str) else date_obj


class CdmSchema(Schema):
    """
    CDM schema class, return the serialized messages back
    """

    class Meta:
        """expose the fields for serialization"""

        # Fields to expose
        fields: List[str] = ["message"]

    message: Str = Str()


class Datafeed(Schema):
    """Datafeed schema."""

    data_source: Str = Str(required=True)
    data_type: Str = Str(required=True, validate=validate.OneOf(DATA_TYPES))
    feed_id: Int = Int(required=True, description="ID of the datafeed")
    feed_type: Str = Str(required=True, validate=validate.OneOf(FEED_TYPES))
    file_extension: Str = Str(required=True, validate=validate.OneOf(FILE_EXTENSIONS))
    is_pii: Boolean = Boolean(required=True)
    modified: DateTime = DateTime(required=True)

    @pre_dump
    # pylint: disable=unused-argument
    def process_modified(self, data: dict, many: bool = False) -> dict:
        """process the schema before serialization.
        override the serialization method from Marshmallow

        Args:
            data (dict): The datafeed object
            many (bool): If there are many to process
        Returns:
            Response: Returns a datafeed object

        """
        # snowflake sometimes returns strings in datetime fields, so we parse to ensure sanity
        if "modified" in data:
            data.update(modified=clean_date(data["modified"]))
        return data


class Fieldmapping(Schema):
    """Fieldmapping schema."""

    field_id: Int = Int(required=True)
    field_name: Str = Str(required=True, validate=validate.OneOf(FIELD_NAMES))
    field_variation: Str = Str(required=True)
    modified: DateTime = DateTime(required=True)


class ProcessedData(Schema):
    """Processed Data schema."""

    source_name: Str = Str(required=True, description="name of the data source")
    created: DateTime = DateTime(required=False)
    modified: DateTime = DateTime(required=False)
    filename: Str = Str(required=False)
    item_source: Str = Str(required=False)
    item_cost: Float = Float(required=False)

    @pre_dump
    # pylint: disable=unused-argument
    def process_modified(self, data: dict, many: bool = False) -> dict:
        """process the schema before serialization.
        override the serialization method from Marshmallow

        Args:
            data (dict): The ProcessedData object
            many (bool): If there are many to process
        Returns:
            Response: Returns a ProcessedData object

        """
        # snowflake sometimes returns strings in datetime fields, so we parse to ensure sanity
        if "modified" in data:
            data.update(modified=clean_date(data["modified"]))
        return data
