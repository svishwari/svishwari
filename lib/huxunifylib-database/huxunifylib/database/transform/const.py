"""Data Router transformer constants."""

from enum import Enum

import huxunifylib.database.constants as dc


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


class FileMatchType(Enum):
    """Upload file match type."""

    EMAIL = object()
    PHONE = object()
    MAILING_ADDRESS = object()
    MOBILE_DEVICE_ID = object()

    EMAIL_ADDRESS_PHONE = object()


FILE_UPLOAD_GOOGLE_FIELD_MAP = {
    FileMatchType.EMAIL.name: {dc.S_TYPE_EMAIL_HASHED: "Email"},
    FileMatchType.PHONE.name: {dc.S_TYPE_PHONE_NUMBER_HASHED: "Phone"},
    FileMatchType.MAILING_ADDRESS.name: {
        dc.S_TYPE_FIRST_NAME_HASHED: "First Name",
        dc.S_TYPE_FIRST_NAME_INITIAL_HASHED: "First Name",
        dc.S_TYPE_LAST_NAME_HASHED: "Last Name",
        dc.S_TYPE_COUNTRY_CODE_HASHED: "Country",
        dc.S_TYPE_POSTAL_CODE_HASHED: "Zip",
    },
    FileMatchType.MOBILE_DEVICE_ID.name: {
        dc.S_TYPE_MOBILE_DEVICE_ID: "Mobile Device ID"
    },
}

FILE_UPLOAD_AMAZON_FIELD_MAP = {
    FileMatchType.EMAIL_ADDRESS_PHONE.name: {
        dc.S_TYPE_EMAIL_HASHED: "email",
        dc.S_TYPE_PHONE_NUMBER_HASHED: "phone",
        dc.S_TYPE_FIRST_NAME_HASHED: "first_name",
        dc.S_TYPE_LAST_NAME_HASHED: "last_name",
        dc.S_TYPE_POSTAL_CODE_HASHED: "zip",
        dc.S_TYPE_STATE_OR_PROVINCE_HASHED: "state",
        dc.S_TYPE_ADDRESS: "address",
    },
}
