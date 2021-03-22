"""
Schemas for the CDM API
"""
from http import HTTPStatus
from dateutil import parser
from flask_marshmallow import Schema
from marshmallow import validate, pre_dump
from marshmallow.fields import Boolean, DateTime, Int, Str


DATAFEEDS_TAG = "datafeeds"

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
    def process_modified(self, data, many=False):  # pylint: disable=unused-argument
        """process the schema before serialization.
        override the serialization method from Marshmallow

        ---

        Args:
            data (obj): The datafeed object

        Returns:
            Response: Returns a datafeed object

        """
        # issue in code when dumping, when of the records in snowflake
        # 2021-01-21T05:30:48.301000 has time zone defined,
        if "modified" in data:
            data.update(modified=self.clean_date(data["modified"]))
        return data

    @staticmethod
    def clean_date(date_obj):
        """cleans dates that come back from snowflake as strings instead of DateTimes

        ---

        Args:
            date_obj (datetime): A datetime object

        Returns:
            Response: Returns a datetime object

        """
        # if string instance, convert to datetime.
        return parser.parse(date_obj) if isinstance(date_obj, str) else date_obj


# TODO - find a home for this, perhaps we can generate this even more dynamically.
DATAFEED_SPECS = {
    "description": "Retrieves the data feed configuration by ID.",
    "tags": [DATAFEEDS_TAG],
    "parameters": [
        {
            "name": "feed_id",
            "description": "ID of the datafeed",
            "type": "integer",
            "in": "path",
            "required": "true",
        }
    ],
    "responses": {
        HTTPStatus.OK.value: {
            "schema": Datafeed,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": Datafeed,
        },
    },
}


class Fieldmapping(Schema):
    """Fieldmapping schema."""

    field_id = Int(required=True)
    field_name = Str(required=True, validate=validate.OneOf(FIELD_NAMES))
    field_variation = Str(required=True)
    modified = DateTime(required=True)
