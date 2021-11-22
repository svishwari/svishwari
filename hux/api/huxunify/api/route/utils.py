"""Purpose of this file is to house route utilities"""
from datetime import datetime
import re
import csv
from typing import Tuple, Union
from http import HTTPStatus
from bson import ObjectId
from pandas import DataFrame
from dateutil.relativedelta import relativedelta

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
from huxunifylib.database.user_management import (
    get_user,
    get_all_users,
    set_user,
)
from huxunifylib.database.client import DatabaseClient

from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.tecton import check_tecton_connection
from huxunify.api.data_connectors.aws import (
    check_aws_ssm,
    check_aws_batch,
)
from huxunify.api.data_connectors.okta import (
    check_okta_connection,
    get_user_info,
)
from huxunify.api.data_connectors.cdp import check_cdm_api_connection
from huxunify.api.data_connectors.cdp_connection import (
    check_cdp_connections_api_connection,
)
from huxunify.api.exceptions import (
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
        record_health_status_metric(api_c.MONGO_CONNECTION_HEALTH, True)
        return True, "Mongo available."
    # pylint: disable=broad-except
    # pylint: disable=unused-variable
    except Exception as exception:
        record_health_status_metric(api_c.MONGO_CONNECTION_HEALTH, False)
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

    if metric_type == api_c.DISPLAY_ADS:
        for name in api_c.DISPLAY_ADS_METRICS:
            metric[name] = sum(
                [
                    item[name]
                    for item in perf_metrics
                    if name in item.keys()
                    and item[name] is not None
                    and not isinstance(item[name], str)
                ]
            )
    elif metric_type == api_c.EMAIL:
        for name in api_c.EMAIL_METRICS:
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
        api_c.ID: str(target_id),
        api_c.NAME: name,
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
        api_c.NAME,
        api_c.EMAIL,
        api_c.PHONE,
        api_c.ADDRESS,
        api_c.COOKIE,
    ]:
        data[val][api_c.PROP] = val.title()
        data[val][api_c.ICON] = val
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
        api_c.GENDER_WOMEN: [
            {
                api_c.DATE: date_parser(
                    x[api_c.MONTH], x[api_c.YEAR]
                ),
                api_c.LTV: round(x[api_c.AVG_SPENT_WOMEN], 4)
                if x[api_c.AVG_SPENT_WOMEN]
                else 0,
            }
            for x in gender_spending
        ],
        api_c.GENDER_MEN: [
            {
                api_c.DATE: date_parser(
                    x[api_c.MONTH], x[api_c.YEAR]
                ),
                api_c.LTV: round(x[api_c.AVG_SPENT_MEN], 4)
                if x[api_c.AVG_SPENT_MEN]
                else 0,
            }
            for x in gender_spending
        ],
        api_c.GENDER_OTHER: [
            {
                api_c.DATE: date_parser(
                    x[api_c.MONTH], x[api_c.YEAR]
                ),
                api_c.LTV: round(x[api_c.AVG_SPENT_OTHER], 4)
                if x[api_c.AVG_SPENT_OTHER]
                else 0,
            }
            for x in gender_spending
        ],
    }


def do_not_transform_fields(
    dataframe: DataFrame,
) -> DataFrame:
    """Returns the csv file data without any transformation.

    Args:
        dataframe (DataFrame): input dataframe.

    Returns:
        dataframe (DataFrame): input dataframe.
    """

    return dataframe


class Validation:
    """Validation class for input parameters"""

    @staticmethod
    def validate_integer(value: str) -> int:
        """Validates that an integer is valid

        Args:
            value (str): String value from the caller.

        Returns:
            int: Result of the integer conversion.

        Raises:
            InputParamsValidationError: Error that is raised if input is invalid.
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
            InputParamsValidationError: Error that is raised if input is
                invalid.
        """

        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False

        raise ue.InputParamsValidationError(value, "boolean")

    @staticmethod
    def validate_date(
        date_string: str, date_format: str = api_c.DEFAULT_DATE_FORMAT
    ) -> datetime:
        """Validates is a single date is valid

        Args:
            date_string (str): Input date string.
            date_format (str): Date string format.

        Returns:
            datetime: datetime object for the string date passed in

        Raises:
            InputParamsValidationError: Error that is raised if input is
                invalid.
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
        date_format: str = api_c.DEFAULT_DATE_FORMAT,
    ) -> None:
        """Validates that a date range is valid

        Args:
            start_date (str): Input start date string.
            end_date (str): Input end date string.
            date_format (str): Date string format.

        Raises:
            InputParamsValidationError: Error that is raised if input is
                invalid.
        """

        start = Validation.validate_date(start_date, date_format)
        end = Validation.validate_date(end_date, date_format)

        if start > end:
            raise ue.InputParamsValidationError(
                message=f"The start date {start_date} cannot "
                f"be greater than the end date {end_date}."
            )

    # pylint: disable=anomalous-backslash-in-string
    @staticmethod
    def validate_hux_id(hux_id: str) -> None:
        """Validates the format of the HUX ID.

        Args:
            hux_id (str): Hux ID.

        Raises:
            InputParamsValidationError: Error that is raised if input ID is
                invalid.
        """

        if not re.match("^HUX\d{15}$", hux_id):
            raise ue.InputParamsValidationError(hux_id, "HUX ID")


def is_component_favorite(
    okta_user_id: str, component_name: str, component_id: str
) -> bool:
    """Checks if component is in favorites of a user.
    Args:
        okta_user_id (str): Okta User ID.
        component_name (str): Name of component in user favorite.
        component_id (str): ID of the favorite component.
    Returns:
        bool: If component is favorite or not.
    """
    user_favorites = get_user(get_db_client(), okta_user_id).get(
        api_c.FAVORITES
    )

    if (component_name in db_c.FAVORITE_COMPONENTS) and (
        ObjectId(component_id) in user_favorites.get(component_name)
    ):
        return True

    return False


def get_start_end_dates(request: dict, delta: int) -> (str, str):
    """Get date range.

    Args:
        request (dict) : Request object.
        delta (int) : Time in months.

    Returns:
        start_date, end_date (str, str): Date range.
    """

    start_date = (
        request.args.get(api_c.START_DATE)
        if request and request.args.get(api_c.START_DATE)
        else datetime.strftime(
            datetime.utcnow().date() - relativedelta(months=delta),
            api_c.DEFAULT_DATE_FORMAT,
        )
    )
    end_date = (
        request.args.get(api_c.END_DATE)
        if request and request.args.get(api_c.END_DATE)
        else datetime.strftime(
            datetime.utcnow().date(),
            api_c.DEFAULT_DATE_FORMAT,
        )
    )
    return start_date, end_date


def get_user_favorites(
    database: DatabaseClient, user_name: str, component_name: str
) -> list:
    """Get user favorites for a component

    Args:
        database (DatabaseClient): A database client.
        user_name (str): Name of the user.
        component_name (str): Name of component in user favorite.

    Returns:
        list: List of ids of favorite component
    """
    user = get_all_users(database, {db_c.USER_DISPLAY_NAME: user_name})
    if not user:
        return []

    # take the first one,
    return user[0].get(api_c.FAVORITES, {}).get(component_name, [])


def get_user_from_db(access_token: str) -> Union[dict, Tuple[dict, int]]:
    """Get the corresponding user matching the okta access token from the DB.
    Create/Set a new user in DB if an user matching the valid okta access token
    is not currently present in the DB.

    Args:
        access_token (str): OKTA JWT token.

    Returns:
        Union[dict, Tuple[dict, int]]: Either a valid user dict or a tuple of
            response message along with the corresponding HTTP status code.
    """

    # set of keys required from user_info
    required_keys = {
        api_c.OKTA_ID_SUB,
        api_c.EMAIL,
        api_c.NAME,
    }

    # get the user information
    logger.info("Getting user info from OKTA.")
    user_info = get_user_info(access_token)
    logger.info("Successfully got user info from OKTA.")

    # checking if required keys are present in user_info
    if not required_keys.issubset(user_info.keys()):
        logger.info("Failure. Required keys not present in user_info dict.")
        return {
            "message": api_c.AUTH401_ERROR_MESSAGE
        }, HTTPStatus.UNAUTHORIZED

    logger.info(
        "Successfully validated required_keys are present in user_info."
    )

    # check if the user is in the database
    database = get_db_client()
    user = get_user(database, user_info[api_c.OKTA_ID_SUB])

    if user is None:
        # since a valid okta_id is extracted from the okta issuer, use the user
        # info and create a new user if no corresponding user record matching
        # the okta_id is found in DB
        user = set_user(
            database=database,
            okta_id=user_info[api_c.OKTA_ID_SUB],
            email_address=user_info[api_c.EMAIL],
            display_name=user_info[api_c.NAME],
            role=user_info.get(api_c.ROLE, api_c.VIEWER_LEVEL)
        )

        # return NOT_FOUND if user is still none
        if user is None:
            logger.info(
                "User not found in DB even after trying to create one."
            )
            return {
                api_c.MESSAGE: api_c.USER_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

    return user


# pylint: disable=unspecified-encoding
def read_csv_shap_data(file_path: str, features: list = None) -> dict:
    """Read in Shap Models Data CSV into a dict

    Args:
        file_path (str): relative file path of the csv file
        features (list): string list of the features to be returned.
        If none is passed, all features are returned

    Returns:
        dict: data placed into a dict where the keys are the column names

    """

    data = {}
    index = {}

    # load in the necessary data
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        column_names = next(csv_reader)

        if not features:
            features = column_names

        for feature in features:
            index[feature] = column_names.index(feature)
            data[feature] = []

        for row in csv_reader:
            for feature in features:
                data[feature].append(row[index[feature]])

    return data


# pylint: disable=unspecified-encoding
def read_stub_city_zip_data(file_path: str) -> list:
    """Read in City & Zip Data CSV into a dict

    Args:
        file_path(str): relative file path of the csv file

    Returns:
        list: City & Zip data list
    """
    with open(file_path, "r") as csv_file:
        data = list(csv.reader(csv_file))

    return data[1:]
