"""Purpose of this file is to house schema utilities"""
from typing import AnyStr, Union
from http import HTTPStatus
from datetime import datetime
from bson import ObjectId
from flask_marshmallow import Schema
from marshmallow import ValidationError
from marshmallow.fields import Int, Str
from croniter import croniter, CroniterNotAlphaError, CroniterBadCronError
from huxunifylib.util.general.logging import logger
from huxunify.api import constants as api_c


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
        cron_expression = cron_expression.replace("?", "*")
        try:
            return croniter(cron_expression[:-2], start_date).get_next(
                datetime
            )
        except CroniterNotAlphaError:
            logger.error("Encountered cron expression error, returning None")

        except CroniterBadCronError:
            logger.error("Bad Cron Expression error, returning None")
    return None
