"""This script sets constants in the database"""

import logging
from enum import Enum
import huxunifylib.database.data_management as dm
import huxunifylib.database.constants as c
from database.share import get_mongo_client

# Setup logging
logging.basicConfig(level=logging.INFO)

# Set up the database client
DB_CLIENT = get_mongo_client()


class DataStorage(Enum):
    """Data storage definitions."""

    S3 = object()
    MONGODB = object()


class DataFormat(Enum):
    """Data format definitions and their file extentions."""

    CSV = "csv"
    TSV = "tsv"
    JSON = "json"


class TransformerNames(Enum):
    """Transformer names."""

    PASS_THROUGH = object()
    PASS_THROUGH_HASHED = object()

    STRIP_SPACE_LOWER_CASE = object()
    STRIP_SPACE_LOWER_CASE_HASHED = object()

    STRIP_SPACE_UPPER_CASE = object()
    STRIP_SPACE_UPPER_CASE_HASHED = object()

    FIRST_LAST_NAME = object()
    FIRST_NAME_INITIAL = object()

    CUSTOMER_ID = object()

    DOB_TO_AGE = object()
    DOB_YEAR_TO_AGE = object()

    DOB_TO_DOB_DAY = object()
    DOB_TO_DOB_MONTH = object()
    DOB_TO_DOB_YEAR = object()

    DOB_DAY = object()
    DOB_MONTH = object()
    DOB_YEAR = object()

    FACEBOOK_CITY = object()
    FACEBOOK_COUNTRY_CODE = object()
    FACEBOOK_GENDER = object()
    FACEBOOK_PHONE_NUMBER = object()
    FACEBOOK_POSTAL_CODE = object()
    FACEBOOK_STATE_OR_PROVINCE = object()

    GOOGLE_PHONE_NUMBER = object()

    GENDER = object()

    MOBILE_DEVICE_ID = object()
    POSTAL_CODE = object()
    STATE_OR_PROVINCE = object()

    TO_INTEGER = object()
    TO_FLOAT = object()
    TO_BOOLEAN = object()


# Set the list of constants and values
CONSTANTS_LIST = [
    (c.DATA_SOURCE_LOCATIONS, [DataStorage.S3.name]),
    (
        c.DATA_SOURCE_FORMATS,
        [DataFormat.CSV.name, DataFormat.TSV.name, DataFormat.JSON.name],
    ),
    (
        c.DATA_SOURCE_FIELD_MAP,
        [
            {
                c.DATA_SOURCE_FIELD_NAME: "City",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_CITY,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Country Code",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_COUNTRY_CODE,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Date of Birth",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_DOB,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Date of Birth Day",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_DOB_DAY,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Date of Birth Month",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_DOB_MONTH,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Date of Birth Year",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_DOB_YEAR,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Email Address",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_EMAIL,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "First Name",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_FIRST_NAME,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "First Name Initial",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_FIRST_NAME_INITIAL,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Gender",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_GENDER,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Last Name",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_LAST_NAME,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Mobile Device ID",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_MOBILE_DEVICE_ID,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Phone Number",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_PHONE_NUMBER,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Postal Code",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_POSTAL_CODE,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "State or Province",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_STATE_OR_PROVINCE,
            },
            {
                c.DATA_SOURCE_FIELD_NAME: "Customer ID",
                c.DATA_SOURCE_FIELD_TYPE: c.S_TYPE_CUSTOMER_ID,
            },
        ],
    ),
    (
        c.TRANSFORMATIONS,
        {
            c.S_TYPE_CITY: [
                {
                    c.TRANSFORMER: TransformerNames.PASS_THROUGH.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_CITY,
                },
            ],
            c.S_TYPE_COUNTRY_CODE: [
                {
                    c.TRANSFORMER: TransformerNames.STRIP_SPACE_UPPER_CASE.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_COUNTRY_CODE,
                },
            ],
            c.S_TYPE_DOB: [
                {
                    c.TRANSFORMER: TransformerNames.DOB_TO_AGE.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_AGE,
                },
                {
                    c.TRANSFORMER: TransformerNames.DOB_TO_DOB_DAY.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_DOB_DAY,
                },
                {
                    c.TRANSFORMER: TransformerNames.DOB_TO_DOB_MONTH.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_DOB_MONTH,
                },
                {
                    c.TRANSFORMER: TransformerNames.DOB_TO_DOB_YEAR.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_DOB_YEAR,
                },
            ],
            c.S_TYPE_DOB_DAY: [
                {
                    c.TRANSFORMER: TransformerNames.DOB_DAY.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_DOB_DAY,
                },
            ],
            c.S_TYPE_DOB_MONTH: [
                {
                    c.TRANSFORMER: TransformerNames.DOB_MONTH.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_DOB_MONTH,
                },
            ],
            c.S_TYPE_DOB_YEAR: [
                {
                    c.TRANSFORMER: TransformerNames.DOB_YEAR.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_DOB_YEAR,
                },
                {
                    c.TRANSFORMER: TransformerNames.DOB_YEAR_TO_AGE.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_AGE,
                },
            ],
            c.S_TYPE_EMAIL: [
                {
                    c.TRANSFORMER: TransformerNames.STRIP_SPACE_LOWER_CASE_HASHED.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_EMAIL,
                },
            ],
            c.S_TYPE_FIRST_NAME: [
                {
                    c.TRANSFORMER: TransformerNames.FIRST_LAST_NAME.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_FIRST_NAME,
                },
            ],
            c.S_TYPE_FIRST_NAME_INITIAL: [
                {
                    c.TRANSFORMER: TransformerNames.FIRST_NAME_INITIAL.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_FIRST_NAME_INITIAL,
                },
            ],
            c.S_TYPE_GENDER: [
                {
                    c.TRANSFORMER: TransformerNames.GENDER.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_GENDER,
                },
            ],
            c.S_TYPE_LAST_NAME: [
                {
                    c.TRANSFORMER: TransformerNames.FIRST_LAST_NAME.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_LAST_NAME,
                },
            ],
            c.S_TYPE_MOBILE_DEVICE_ID: [
                {
                    c.TRANSFORMER: TransformerNames.STRIP_SPACE_LOWER_CASE.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_MOBILE_DEVICE_ID,
                },
            ],
            c.S_TYPE_PHONE_NUMBER: [
                {
                    c.TRANSFORMER: TransformerNames.GOOGLE_PHONE_NUMBER.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_GOOGLE_PHONE_NUMBER,
                },
            ],
            c.S_TYPE_POSTAL_CODE: [
                {
                    c.TRANSFORMER: TransformerNames.POSTAL_CODE.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_POSTAL_CODE,
                },
            ],
            c.S_TYPE_STATE_OR_PROVINCE: [
                {
                    c.TRANSFORMER: TransformerNames.STATE_OR_PROVINCE.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_STATE_OR_PROVINCE,
                },
            ],
            c.S_TYPE_CUSTOMER_ID: [
                {
                    c.TRANSFORMER: TransformerNames.CUSTOMER_ID.name,
                    c.DESTINATION_COLUMN: c.S_TYPE_CUSTOMER_ID,
                },
            ],
            c.CUSTOM_TYPE_BOOL: [
                {
                    c.TRANSFORMER: TransformerNames.TO_BOOLEAN.name,
                }
            ],
            c.CUSTOM_TYPE_CAT: [
                {
                    c.TRANSFORMER: TransformerNames.PASS_THROUGH.name,
                }
            ],
            c.CUSTOM_TYPE_INT: [
                {
                    c.TRANSFORMER: TransformerNames.TO_INTEGER.name,
                }
            ],
            c.CUSTOM_TYPE_FLOAT: [
                {
                    c.TRANSFORMER: TransformerNames.TO_FLOAT.name,
                }
            ],
        },
    ),
    (
        c.STATE_ALPHA_CODE_MAPPING,
        {
            "alabama": "AL",
            "alaska": "AK",
            "arizona": "AZ",
            "arkansas": "AR",
            "california": "CA",
            "colorado": "CO",
            "connecticut": "CT",
            "delaware": "DE",
            "florida": "FL",
            "georgia": "GA",
            "hawaii": "HI",
            "idaho": "ID",
            "illinois": "IL",
            "indiana": "IN",
            "iowa": "IA",
            "kansas": "KS",
            "kentucky": "KY",
            "louisiana": "LA",
            "maine": "ME",
            "maryland": "MD",
            "massachusetts": "MA",
            "michigan": "MI",
            "minnesota": "MN",
            "mississippi": "MS",
            "missouri": "MO",
            "montana": "MT",
            "nebraska": "NE",
            "nevada": "NV",
            "new hampshire": "NH",
            "new jersey": "NJ",
            "new mexico": "NM",
            "new york": "NY",
            "north carolina": "NC",
            "north dakota": "ND",
            "ohio": "OH",
            "oklahoma": "OK",
            "oregon": "OR",
            "pennsylvania": "PA",
            "rhode island": "RI",
            "south carolina": "SC",
            "south dakota": "SD",
            "tennessee": "TN",
            "texas": "TX",
            "utah": "UT",
            "vermont": "VT",
            "virginia": "VA",
            "washington": "WA",
            "west virginia": "WV",
            "wisconsin": "WI",
            "wyoming": "WY",
            "american samoa": "AS",
            "guam": "GU",
            "northern mariana islands": "MP",
            "puerto rico": "PR",
            "virgin islands": "VI",
        },
    ),
    (c.MAX_AUDIENCE_SIZE_FOR_HASHED_FILE_DOWNLOAD, 100000),
    (c.DATA_ROUTER_BATCH_SIZE, 1000),
    (c.AUDIENCE_ROUTER_BATCH_SIZE, 5000),
    (c.AWS_BATCH_MEM_LIMIT, 2048),
    (
        c.AUDIENCE_TYPE,
        {
            c.DEFAULT_AUDIENCE: {
                c.AUDIENCE_TYPE_NAME: c.DEFAULT_AUDIENCE_STR,
                c.AUDIENCE_TYPE_DESC: "Default Audience",
            },
            c.CUSTOM_AUDIENCE: {
                c.AUDIENCE_TYPE_NAME: c.CUSTOM_AUDIENCE_STR,
                c.AUDIENCE_TYPE_DESC: "Custom Audience",
            },
            c.WIN_BACK_AUDIENCE: {
                c.AUDIENCE_TYPE_NAME: "Win-back Audience",
                c.AUDIENCE_TYPE_DESC: "No online, app, or store purchase in the past 24 months",
            },
        },
    ),
    (
        c.CUSTOM_TYPE_BOOL_MAPPING,
        {
            "YES": 1,
            "Yes": 1,
            "yes": 1,
            "Y": 1,
            "y": 1,
            "NO": 0,
            "No": 0,
            "no": 0,
            "N": 0,
            "n": 0,
            "TRUE": 1,
            "True": 1,
            "true": 1,
            "FALSE": 0,
            "False": 0,
            "false": 0,
            "0": 0,
            "1": 1,
        },
    ),
    (
        c.CUSTOM_TYPE_FRIENDLY_NAME_MAPPING,
        {
            c.CUSTOM_TYPE_BOOL: "Boolean",
            c.CUSTOM_TYPE_INT: "Numerical (Discrete)",
            c.CUSTOM_TYPE_FLOAT: "Numerical (Continuous)",
            c.CUSTOM_TYPE_CAT: "Categorical",
        },
    ),
    (
        c.CUSTOM_TYPE_FIELD_MAPPING,
        {
            c.CUSTOM_TYPE_INT: {
                c.FIELD_MAP_ORDER_QUANTITY_12M: "Order Quantity (12m)",
                c.FIELD_MAP_ORDER_QUANTITY_13M_24M: "Order Quantity (13-24m)",
            }
        },
    ),
    (
        c.AUDIENCE_FILTER_CONSTANTS,
        {
            "text_operators": {
                "contains": "Contains",
                "does_not_contain": "Does not contain",
                "equals": "Equals",
                "does_not_equal": "Does not equal",
            }
        },
    ),
]

# Loop through the list and set constants
for item in CONSTANTS_LIST:
    CONSTANT_NAME = item[0]
    CONSTANT_VALUE = item[1]

    logging.info(
        "Setting value <%s> for constant <%s>...",
        str(CONSTANT_VALUE),
        CONSTANT_NAME,
    )

    db_id = dm.set_constant(DB_CLIENT, CONSTANT_NAME, CONSTANT_VALUE)

    assert db_id

    doc = dm.get_constant(DB_CLIENT, CONSTANT_NAME)

    assert doc[c.CONSTANT_NAME] == CONSTANT_NAME
    assert doc[c.CONSTANT_VALUE] == CONSTANT_VALUE

logging.info("Done with setting the constants!")
