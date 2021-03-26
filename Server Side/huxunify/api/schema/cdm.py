"""
Schemas for the CDM API
"""
from dateutil import parser
from flask_marshmallow import Schema
from marshmallow import validate, pre_dump
from marshmallow.fields import Boolean, DateTime, Int, Str, Float


DATA_TYPES = [
    "customers",
    "orders",
    "items",
]

FEED_TYPES = [
    "api",
    "batch",
]

FIELD_NAMES = [
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

FILE_EXTENSIONS = [
    "csv",
    "json",
]


def clean_date(date_obj):
    """cleans dates that come back from snowflake as strings instead of DateTimes

    Args:
        date_obj (datetime): A datetime object

    Returns:
        Response: Returns a datetime object

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
        fields = ["message"]

    message = Str()


class Datafeed(Schema):
    """Datafeed schema."""

    data_source = Str(required=True)
    data_type = Str(required=True, validate=validate.OneOf(DATA_TYPES))
    feed_id = Int(required=True, description="ID of the datafeed")
    feed_type = Str(required=True, validate=validate.OneOf(FEED_TYPES))
    file_extension = Str(required=True, validate=validate.OneOf(FILE_EXTENSIONS))
    is_pii = Boolean(required=True)
    modified = DateTime(required=True)

    @pre_dump
    def process_modified(
        self, data, many=False
    ):  # pylint: disable=unused-argument,no-self-use
        """process the schema before serialization.
        override the serialization method from Marshmallow

        Args:
            data (obj): The datafeed object

        Returns:
            Response: Returns a datafeed object

        """
        # snowflake sometimes returns strings in datetime fields, so we parse to ensure sanity
        if "modified" in data:
            data.update(modified=clean_date(data["modified"]))
        return data


class Fieldmapping(Schema):
    """Fieldmapping schema."""

    field_id = Int(required=True)
    field_name = Str(required=True, validate=validate.OneOf(FIELD_NAMES))
    field_variation = Str(required=True)
    modified = DateTime(required=True)


class ProcessedData(Schema):
    """Processed Data schema."""

    source_name = Str(required=True, description="name of the data source")
    created = DateTime(required=False)
    modified = DateTime(required=False)
    filename = Str(required=False)
    item_source = Str(required=False)
    item_cost = Float(required=False)

    @pre_dump
    def process_dump(
        self, data, many=False
    ):  # pylint: disable=unused-argument,no-self-use
        """process the schema before serialization.
        override the serialization method from Marshmallow

        Args:
            data (obj): The ProcessedData object

        Returns:
            Response: Returns a ProcessedData object

        """
        # change keys to lower case
        data = {k.lower(): v for k, v in data.items()}

        # issue in code when dumping, when of the records in snowflake
        # 2021-01-21T05:30:48.301000 has time zone defined,
        if "modified" in data:
            data.update(modified=clean_date(data["modified"]))
        return data
