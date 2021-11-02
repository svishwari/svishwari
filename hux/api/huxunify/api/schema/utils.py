"""Purpose of this file is to house schema utilities"""
import uuid
from typing import AnyStr, Union
from http import HTTPStatus
from datetime import datetime, timedelta
import random
from bson import ObjectId
from flask_marshmallow import Schema
from marshmallow import ValidationError
from marshmallow.fields import Boolean, DateTime, Int, Str, Float
from croniter import croniter, CroniterNotAlphaError
from huxunifylib.database import constants as db_c
from huxunifylib.util.general.logging import logger
from huxunify.api import constants as api_c

# get random data back based on marshmallow field type
SPEC_TYPE_LOOKUP = {
    Boolean: bool(random.getrandbits(1)),
    DateTime: datetime.now() + timedelta(random.randint(0, 1e4)),
    Int: random.randint(0, 1e4),
    Str: str(uuid.uuid4()),
    Float: random.random(),
}


def generate_synthetic_marshmallow_data(schema_obj: Schema) -> dict:
    """This function generates synthetic data for marshmallow

    Args:
        schema_obj (Schema): a marshmallow schema object

    Returns:
        dict: a dictionary that simulates the passed in marshmallow schema obj

    """
    # get random data based on marshmallow type
    return {
        field: SPEC_TYPE_LOOKUP[type(val)]
        for field, val in schema_obj().fields.items()
    }


def must_not_be_blank(data: AnyStr) -> None:
    """This function validates an empty string.

    Args:
        data (AnyStr): any string

    Raises:
        ValidationError: Error for if data is empty

    """
    if not data:
        raise ValidationError(api_c.EMPTY_OBJECT_ERROR_MESSAGE)


def validate_object_id(data: AnyStr) -> None:
    """This function validates an object id.

    Args:
        data (AnyStr): any string

    """
    ObjectId(data)


def validate_dest_constants(data: dict) -> None:
    """This function validates destination auth details.

    Args:
        data (dict): input dict

    Raises:
        ValidationError:
            - raised if data is not a dict
            - raised if an account id is not in the dict
            - raised if improper fields are in the dict

    """
    # check if dictionary first
    if not isinstance(data, dict):
        raise ValidationError(api_c.INVALID_DESTINATION_AUTH)

    # check which destination auth is being set
    if api_c.FACEBOOK_APP_ID in data:
        destination_key_name = db_c.DELIVERY_PLATFORM_FACEBOOK
    elif api_c.SFMC_ACCOUNT_ID in data:
        destination_key_name = db_c.DELIVERY_PLATFORM_SFMC
    else:
        raise ValidationError(api_c.INVALID_DESTINATION_AUTH)

    # check all keys to ensure coverage by checking against destination constants
    if api_c.DESTINATION_CONSTANTS[destination_key_name].keys() != data.keys():
        raise ValidationError(api_c.INVALID_DESTINATION_AUTH)


class UnAuth401Schema(Schema):
    """401 schema."""

    code = Int(name="code", example=401)
    message = Str(name="message", example=api_c.AUTH401_ERROR_MESSAGE)


AUTH401_RESPONSE = {
    HTTPStatus.UNAUTHORIZED.value: {
        "schema": UnAuth401Schema,
        "description": api_c.AUTH401_ERROR_MESSAGE,
    },
}


class FailedDependency424Schema(Schema):
    """Failed Dependency schema."""

    code = Int(name="code", example=424)
    message = Str(
        name="message", example=api_c.FAILED_DEPENDENCY_ERROR_MESSAGE
    )


FAILED_DEPENDENCY_424_RESPONSE = {
    HTTPStatus.FAILED_DEPENDENCY.value: {
        "schema": FailedDependency424Schema,
        "description": api_c.FAILED_DEPENDENCY_ERROR_MESSAGE,
    },
}


class EmptyResponseDependencySchema(Schema):
    """Empty Response Dependency schema."""

    code = Int(name="code", example=404)
    message = Str(
        name="message", example=api_c.EMPTY_RESPONSE_DEPENDENCY_ERROR_MESSAGE
    )


EMPTY_RESPONSE_DEPENDENCY_404_RESPONSE = {
    HTTPStatus.NOT_FOUND.value: {
        "schema": EmptyResponseDependencySchema,
        "description": api_c.FAILED_DEPENDENCY_ERROR_MESSAGE,
    },
}


def redact_fields(data: dict, redacted_fields: list) -> dict:
    """Function is meant to redact fields that a customer is not allowed to see

    Args:
        data (dict): original data with all fields
        redacted_fields (list): list of fields that need to be redacted

    Returns:
        dict: the original body with sensitive fields redacted

    """
    for field in redacted_fields:
        if field in data:
            data[field] = api_c.REDACTED

    return data


def get_next_schedule(
        cron_expression: str, start_date: datetime
) -> Union[datetime, None]:
    """Get the next schedule from the cron expression.

    Args:
        cron_expression (str): Cron Expression of the schedule.
        start_date (datetime): Start Datetime.

    Returns:
        next_schedule(datetime): Next Schedule datetime.
    """

    if isinstance(cron_expression, str) and isinstance(start_date, datetime):
        cron_expression=cron_expression.replace("?", "*")
        try:
            return croniter(cron_expression[:-2], start_date).get_next(datetime)
        except CroniterNotAlphaError:
            logger.error("Encountered cron expression error, returning None")
    return None


if __name__ == "__main__":
    pass
