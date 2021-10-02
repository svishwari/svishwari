"""Purpose of this file is to house route utilities"""
from datetime import datetime
from typing import Tuple
from http import HTTPStatus
from bson import ObjectId
from croniter import croniter
from marshmallow import ValidationError
from pandas import DataFrame

from healthcheck import HealthCheck
from decouple import config
from connexion.exceptions import ProblemException
from pymongo import MongoClient

from huxunifylib.util.general.logging import logger
from huxunifylib.connectors.util.client import db_client_factory

from huxunifylib.database.cdp_data_source_management import (
    get_all_data_sources,
)
from huxunifylib.database import (
    constants as db_c,
)

from huxunify.api.config import get_config
from huxunify.api import constants
from huxunify.api.data_connectors.tecton import check_tecton_connection
from huxunify.api.data_connectors.aws import check_aws_ssm, check_aws_batch
from huxunify.api.data_connectors.okta import (
    check_okta_connection,
)
from huxunify.api.data_connectors.cdp import check_cdm_api_connection
from huxunify.api.data_connectors.cdp_connection import (
    check_cdp_connections_api_connection,
)
from huxunify.api.exceptions import (
    integration_api_exceptions as iae,
    unified_exceptions as ue,
)
from huxunify.api.prometheus import record_health_status_metric


def handle_api_exception(exc: Exception, description: str = "") -> None:
    """Purpose of this function is to handle general api exceptions,
    and reduce code in the route.

    Args:
        exc (Exception): Exception object to handle.
        description (str): Exception description.

    Returns:
          None
    """

    logger.error(
        "%s: %s.",
        exc.__class__,
        exc,
    )

    return ProblemException(
        status=int(HTTPStatus.BAD_REQUEST.value),
        title=HTTPStatus.BAD_REQUEST.description,
        detail=description,
    )


def get_db_client() -> MongoClient:
    """Get DB client.

    Returns:
        MongoClient: MongoDB client.
    """

    return db_client_factory.get_resource(**get_config().MONGO_DB_CONFIG)


def check_mongo_connection() -> Tuple[bool, str]:
    """Validate mongo DB connection.

    Returns:
        Tuple[bool, str]: Returns if the connection is valid, and the message.
    """

    try:
        # test finding documents
        get_all_data_sources(get_db_client())
        record_health_status_metric(constants.MONGO_CONNECTION_HEALTH, True)
        return True, "Mongo available."
    # pylint: disable=broad-except
    # pylint: disable=unused-variable
    except Exception as exception:
        record_health_status_metric(constants.MONGO_CONNECTION_HEALTH, False)
        return False, "Mongo not available."


def get_health_check() -> HealthCheck:
    """Build and return the health check object.

    Returns:
        HealthCheck: HealthCheck object that processes checks when called.
    """

    health = HealthCheck()

    # check variable
    health.add_section("flask_env", config("FLASK_ENV", default="UNKNOWN"))

    # add health checks
    health.add_check(check_mongo_connection)
    health.add_check(check_tecton_connection)
    health.add_check(check_okta_connection)
    health.add_check(check_aws_ssm)
    health.add_check(check_aws_batch)
    # TODO HUS-1200
    # health.add_check(check_aws_s3)
    # health.add_check(check_aws_events)
    health.add_check(check_cdm_api_connection)
    health.add_check(check_cdp_connections_api_connection)
    return health


def group_perf_metric(perf_metrics: list, metric_type: str) -> dict:
    """Group performance metrics.

    Args:
        perf_metrics (list): List of performance metrics.
        metric_type (list): Type of performance metrics.

    Returns:
        perf_metric (dict): Grouped performance metric.
    """

    metric = {}

    if metric_type == constants.DISPLAY_ADS:
        for name in constants.DISPLAY_ADS_METRICS:
            metric[name] = sum(
                [
                    item[name]
                    for item in perf_metrics
                    if name in item.keys()
                    and item[name] is not None
                    and not isinstance(item[name], str)
                ]
            )
    elif metric_type == constants.EMAIL:
        for name in constants.EMAIL_METRICS:
            metric[name] = sum(
                [
                    item[name]
                    for item in perf_metrics
                    if name in item.keys()
                    and item[name] is not None
                    and not isinstance(item[name], str)
                ]
            )

    return metric


def get_friendly_delivered_time(delivered_time: datetime) -> str:
    """Group performance metrics.

    Args:
        delivered_time (datetime): Delivery time.

    Returns:
        time_difference (str): Time difference as days / hours / mins.
    """

    delivered = (datetime.utcnow() - delivered_time).total_seconds()

    # pylint: disable=no-else-return
    if delivered / (60 * 60 * 24) >= 1:
        return str(int(delivered / (60 * 60 * 24))) + " days ago"
    elif delivered / (60 * 60) >= 1:
        return str(int(delivered / (60 * 60))) + " hours ago"
    elif delivered / 60 >= 1:
        return str(int(delivered / 60)) + " minutes ago"
    else:
        return str(int(delivered)) + " seconds ago"


def get_next_schedule(cron_expression: str, start_date: datetime) -> datetime:
    """

    Args:
        cron_expression(str): Cron Expression of the schedule
        start_date(datetime): Start Datetime

    Returns:
        next_schedule(datetime): Next Schedule datetime
    """
    cron_iterator = croniter(cron_expression, start_date)
    return cron_iterator.get_next(datetime)


def update_metrics(
    target_id: ObjectId,
    name: str,
    jobs: list,
    perf_metrics: list,
    metric_type: str,
) -> dict:
    """Update performance metrics.

    Args:
        target_id (ObjectId) : Group Id.
        name (str): Name of group object.
        jobs (list): List of delivery jobs.
        perf_metrics (list): List of performance metrics.
        metric_type (str): Type of performance metrics.

    Returns:
        metric (dict): Grouped performance metrics.
    """

    delivery_jobs = [x[db_c.ID] for x in jobs]
    metric = {
        constants.ID: str(target_id),
        constants.NAME: name,
    }
    metric.update(
        group_perf_metric(
            [
                x[db_c.PERFORMANCE_METRICS]
                for x in perf_metrics
                if x[db_c.DELIVERY_JOB_ID] in delivery_jobs
            ],
            metric_type,
        )
    )
    return metric


def add_chart_legend(data: dict) -> dict:
    """Add chart legend data.

    Args:
        data (dict) : Chart data.

    Returns:
        response(dict): Chart data with legend details.
    """

    for val in [
        constants.NAME,
        constants.EMAIL,
        constants.PHONE,
        constants.ADDRESS,
        constants.COOKIE,
    ]:
        data[val][constants.PROP] = val.title()
        data[val][constants.ICON] = val
    return data


def group_gender_spending(gender_spending: list) -> dict:
    """Groups gender spending by gender/month.

    Args:
        gender_spending (list) : list of spending details by gender.

    Returns:
        response(dict): Gender spending grouped by gender / month.
    """

    date_parser = lambda x, y: datetime.strptime(
        f"1-{str(x)}-{str(y)}", "%d-%m-%Y"
    )
    return {
        constants.GENDER_WOMEN: [
            {
                constants.DATE: date_parser(
                    x[constants.MONTH], x[constants.YEAR]
                ),
                constants.LTV: round(x[constants.AVG_SPENT_WOMEN], 4)
                if x[constants.AVG_SPENT_WOMEN]
                else 0,
            }
            for x in gender_spending
        ],
        constants.GENDER_MEN: [
            {
                constants.DATE: date_parser(
                    x[constants.MONTH], x[constants.YEAR]
                ),
                constants.LTV: round(x[constants.AVG_SPENT_MEN], 4)
                if x[constants.AVG_SPENT_MEN]
                else 0,
            }
            for x in gender_spending
        ],
        constants.GENDER_OTHER: [
            {
                constants.DATE: date_parser(
                    x[constants.MONTH], x[constants.YEAR]
                ),
                constants.LTV: round(x[constants.AVG_SPENT_OTHER], 4)
                if x[constants.AVG_SPENT_OTHER]
                else 0,
            }
            for x in gender_spending
        ],
    }


def transform_fields_generic_file(
    dataframe: DataFrame,
) -> DataFrame:
    """Returns the csv file data without any transformation.

    Args:
        dataframe (DataFrame): input dataframe.

    Returns:
        dataframe (DataFrame): input dataframe.
    """

    return dataframe


def check_end_date_greater_than_start_date(
    start_date: str,
    end_date: str,
):
    """Raises error if start date is greater than end date.

    Args:
        start_date (str): start date.
        end_date (str): end date.

    Raises:
        FailedDateFilterIssue: Exception if start date is greater than
            end date.
    """

    start_date_format = ""
    end_date_format = ""

    if start_date:
        start_date_format = datetime.strptime(
            start_date, constants.DEFAULT_DATE_FORMAT
        )

    if end_date:
        end_date_format = datetime.strptime(
            end_date, constants.DEFAULT_DATE_FORMAT
        )

    if (
        start_date_format
        and end_date_format
        and start_date_format > end_date_format
    ):
        raise iae.FailedDateFilterIssue()


class Validation:
    """Validation class for input parameters"""

    def __init__(self):
        pass

    @staticmethod
    def validate_integer(value: str) -> int:
        """Validates that an integer is valid

        Args:
            value (str): String value from the caller.

        Returns:
            int: Result of the integer conversion.

        Raises:
            ValidationError: Error that is raised if input is invalid.

        """
        # max_value added to protect snowflake/and other apps that
        # are not able to handle 32int+
        max_value = 2147483647

        if value.isdigit():
            if int(value) <= 0:
                raise ue.InputParamsValidationError(value, "positive integer")
            if int(value) > max_value:
                raise ue.InputParamsValidationError(value, "integer")
            return int(value)

        raise ue.InputParamsValidationError(value, "integer")

    @staticmethod
    def validate_bool(value: str) -> bool:
        """Validates input boolean value for the user

        Args:
            value (str): String value from the caller.

        Returns:
            bool: Result of the boolean conversion.

        Raises:
            ValidationError: Error that is raised if input is invalid.

        """

        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False

        raise ue.InputParamsValidationError(value, "boolean")

    @staticmethod
    def validate_date(
        date_string: str, date_format: str = constants.DEFAULT_DATE_FORMAT
    ) -> datetime:
        """Validates is a single date is valid

        Args:
            date_string (str): Input date string.
            date_format (str): Date string format.

        Returns:
            datetime: datetime object for the string date passed in

        Raises:
            ValidationError: Error that is raised if input is invalid.

        """

        try:
            return datetime.strptime(date_string, date_format)
        except ValueError:
            raise ue.InputParamsValidationError(
                date_string, date_format
            ) from ValueError

    @staticmethod
    def validate_date_range(
        start_date: str,
        end_date: str,
        date_format: str = constants.DEFAULT_DATE_FORMAT,
    ):
        """Validates that a date range is valid

        Args:
            start_date (str): Input start date string.
            end_date (str): Input end date string.
            date_format (str): Date string format.

        Raises:
            ValidationError: Error that is raised if input is invalid.

        """

        start = Validation.validate_date(start_date, date_format)
        end = Validation.validate_date(end_date, date_format)

        if start > end:
            raise iae.FailedDateFilterIssue
