"""Purpose of this file is to house route utilities."""
# pylint: disable=too-many-lines
import statistics
from collections import defaultdict, namedtuple
from datetime import datetime, timedelta
import re
from itertools import groupby
from pathlib import Path
from typing import Tuple, Union, Generator, Callable, List
from http import HTTPStatus

import pandas as pd
from bson import ObjectId

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from pandas import DataFrame

from healthcheck import HealthCheck
from decouple import config
from connexion.exceptions import ProblemException
from pymongo import MongoClient

from huxunifylib.util.general.logging import logger

from huxunifylib.database.audit_management import create_audience_audit
from huxunifylib.database.survey_metrics_management import get_survey_responses
from huxunifylib.database.util.client import db_client_factory
from huxunifylib.database import (
    constants as db_c,
)
from huxunifylib.database.collection_management import get_document
from huxunifylib.database.user_management import (
    get_user,
    get_all_users,
    set_user,
)
from huxunifylib.database.client import DatabaseClient

from huxunify.api.data_connectors.cloud.cloud_client import CloudClient
from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.okta import (
    check_okta_connection,
    get_user_info,
)
from huxunify.api.data_connectors.cdp import (
    check_cdm_api_connection,
)
from huxunify.api.data_connectors.cdp_connection import (
    check_cdp_connections_api_connection,
)
from huxunify.api.data_connectors.jira import JiraConnection
from huxunify.api.exceptions import (
    unified_exceptions as ue,
)
from huxunify.api.prometheus import record_health_status, Connections
from huxunify.api.stubbed_data.stub_shap_data import shap_data
from huxunify.api.schema.user import RequestedUserSchema


def handle_api_exception(exc: Exception, description: str = "") -> None:
    """Purpose of this function is to handle general api exceptions,
    and reduce code in the route.

    Args:
        exc (Exception): Exception object to handle.
        description (str): Exception description.

    Returns:
          None.
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


@record_health_status(Connections.DB)
def check_mongo_connection() -> Tuple[bool, str]:
    """Validate mongo DB connection.

    Returns:
        Tuple[bool, str]: Returns if the connection is valid, and the message.
    """

    try:
        # test finding documents, call directly to see errors.
        _ = list(
            get_db_client()[db_c.DATA_MANAGEMENT_DATABASE][
                db_c.CDP_DATA_SOURCES_COLLECTION
            ].find({})
        )
        logger.info("Mongo is available")
        return True, "Mongo available."
    # pylint: disable=broad-except
    except Exception:
        logger.exception("Mongo Health Check failed.")
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
    health.add_check(check_okta_connection)
    health.add_check(CloudClient().health_check_secret_storage)
    health.add_check(CloudClient().health_check_batch_service)
    health.add_check(CloudClient().health_check_storage_service)
    health.add_check(check_cdm_api_connection)
    health.add_check(check_cdp_connections_api_connection)
    health.add_check(JiraConnection.check_jira_connection)
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
                api_c.DATE: date_parser(x[api_c.MONTH], x[api_c.YEAR]),
                api_c.LTV: round(x[api_c.AVG_SPENT_WOMEN], 4)
                if x[api_c.AVG_SPENT_WOMEN]
                else 0,
            }
            for x in gender_spending
        ],
        api_c.GENDER_MEN: [
            {
                api_c.DATE: date_parser(x[api_c.MONTH], x[api_c.YEAR]),
                api_c.LTV: round(x[api_c.AVG_SPENT_MEN], 4)
                if x[api_c.AVG_SPENT_MEN]
                else 0,
            }
            for x in gender_spending
        ],
        api_c.GENDER_OTHER: [
            {
                api_c.DATE: date_parser(x[api_c.MONTH], x[api_c.YEAR]),
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
    def validate_integer(
        value: str, validate_zero_or_greater: bool = False
    ) -> int:
        """Validates that an integer is valid.

        Args:
            value (str): String value from the caller.
            validate_zero_or_greater(bool): Boolean value to validate if value
            is equal to or greater than zero.

        Returns:
            int: Result of the integer conversion.

        Raises:
            InputParamsValidationError: Error that is raised if input is
                invalid.
        """

        # max_value added to protect snowflake/and other apps that
        # are not able to handle 32int+
        max_value = 2147483647

        if value.isdigit():
            if validate_zero_or_greater and int(value) < 0:
                raise ue.InputParamsValidationError(
                    value, "zero or positive integer"
                )
            if not validate_zero_or_greater and int(value) <= 0:
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
        """Validates is a single date is valid.

        Args:
            date_string (str): Input date string.
            date_format (str): Date string format.

        Returns:
            datetime: datetime object for the string date passed in.

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
    user: dict, component_name: str, component_id: str
) -> bool:
    """Checks if component is in favorites of a user.

    Args:
        user (dict): User dict.
        component_name (str): Name of component in user favorite.
        component_id (str): ID of the favorite component.

    Returns:
        bool: If component is favorite or not.
    """

    user_favorites = user.get(api_c.FAVORITES, {})

    if (component_name in db_c.FAVORITE_COMPONENTS) and (
        ObjectId(component_id) in user_favorites.get(component_name, [])
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
    """Get user favorites for a component.

    Args:
        database (DatabaseClient): A database client.
        user_name (str): Name of the user.
        component_name (str): Name of component in user favorite.

    Returns:
        list: List of ids of favorite component.
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
        logger.warning("Failure. Required keys not present in user_info dict.")
        return {
            "message": api_c.AUTH401_ERROR_MESSAGE
        }, HTTPStatus.UNAUTHORIZED

    logger.info(
        "Successfully validated required_keys are present in user_info."
    )

    # check if the user is in the database
    logger.info("Getting database client.")
    database = get_db_client()
    logger.info("Successfully got database client.")

    user = get_user(database, user_info[api_c.OKTA_ID_SUB])

    if user is None:
        # since a valid okta_id is extracted from the okta issuer, use the user
        # info and create a new user if no corresponding user record matching
        # the okta_id is found in DB
        logger.info("Setting user in database.")
        user = set_user(
            database=database,
            okta_id=user_info[api_c.OKTA_ID_SUB],
            email_address=user_info[api_c.EMAIL],
            display_name=user_info[api_c.NAME],
            role=user_info.get(api_c.ROLE, db_c.USER_ROLE_VIEWER),
        )
        logger.info("Successfully set user in database.")

        # return NOT_FOUND if user is still none
        if user is None:
            logger.warning(
                "User not found in DB even after trying to create one."
            )
            return {api_c.MESSAGE: api_c.USER_NOT_FOUND}, HTTPStatus.NOT_FOUND

    return user


def get_required_shap_data(features: list = None) -> dict:
    """Read in Shap Models Data JSON into a dict.

    Args:
        features (list): string list of the features to be returned.
            If none is passed, all features are returned.

    Returns:
        dict: data placed into a dict where the keys are the column names.
    """

    # return required shap feature data
    return {
        feature: data
        for feature, data in shap_data.items()
        if feature in features
    }


def convert_unique_city_filter(request_json: dict) -> dict:
    """To convert request json to have unique city.

    Args:
        request_json (dict): Input audience filter json object.

    Returns:
        dict: Converted audience filter.
    """

    try:
        for filters in request_json[api_c.AUDIENCE_FILTERS]:
            for item in filters[api_c.AUDIENCE_SECTION_FILTERS]:
                if (
                    item[api_c.AUDIENCE_FILTER_FIELD]
                    == api_c.AUDIENCE_FILTER_CITY
                ):
                    city_value, state_value, _ = item.get(
                        api_c.AUDIENCE_FILTER_VALUE
                    ).split("|")
                    item[api_c.AUDIENCE_FILTER_VALUE] = city_value

                    filters[api_c.AUDIENCE_SECTION_FILTERS].append(
                        {
                            api_c.AUDIENCE_FILTER_FIELD: api_c.STATE.title(),
                            api_c.AUDIENCE_FILTER_TYPE: api_c.AUDIENCE_FILTERS_EQUALS,
                            api_c.AUDIENCE_FILTER_VALUE: state_value,
                        }
                    )
        return request_json
    except KeyError:
        logger.info("Incorrect Audience Filter Object")
        return request_json

    except ValueError:
        logger.info("Incorrect Audience Filter Object")
        return request_json


def match_rate_data_for_audience(delivery: dict, match_rate_data: dict = None):
    """To get digital platform data for engaged audience delivery.

    Args:
        delivery (dict): Audience delivery data.
        match_rate_data (dict): Match rate data as dictionary, destination
        will be the key.
    """

    if match_rate_data is None:
        match_rate_data = {}
    if delivery.get(api_c.STATUS, "").lower() == api_c.DELIVERED:
        # Digital platform data will be populated based
        # on last successful delivery to an ad_platform.
        if match_rate_data.get(delivery.get(api_c.DELIVERY_PLATFORM_TYPE)):
            # Always ensure the latest successful
            # delivery is considered.
            prev_update_time = match_rate_data[
                delivery.get(api_c.DELIVERY_PLATFORM_TYPE)
            ].get(api_c.AUDIENCE_LAST_DELIVERY)

            prev_update_time = (
                prev_update_time
                if isinstance(prev_update_time, datetime)
                else datetime.min
            )
            if delivery.get(db_c.UPDATE_TIME) > prev_update_time:
                match_rate_data[delivery.get(api_c.DELIVERY_PLATFORM_TYPE)] = {
                    api_c.AUDIENCE_LAST_DELIVERY: delivery.get(
                        db_c.UPDATE_TIME
                    ),
                    api_c.MATCH_RATE: 0,
                }
        else:
            match_rate_data[delivery.get(api_c.DELIVERY_PLATFORM_TYPE)] = {
                api_c.AUDIENCE_LAST_DELIVERY: delivery.get(db_c.UPDATE_TIME),
                api_c.MATCH_RATE: 0,
            }

    else:
        # Delivery jobs on ad_platforms undelivered.
        if not match_rate_data.get(delivery.get(api_c.DELIVERY_PLATFORM_TYPE)):
            match_rate_data[delivery.get(api_c.DELIVERY_PLATFORM_TYPE)] = {
                api_c.AUDIENCE_LAST_DELIVERY: None,
                api_c.MATCH_RATE: None,
            }


# pylint: disable=too-many-nested-blocks
def set_destination_category_in_engagement(engagement: dict):
    """Set destination_category in engagement dictionary.

    Args:
        engagement (dict): engagement dict to be set with destination_category.
    """

    # build destination_category object that groups audiences by destinations
    destinations_categories = []
    for aud in engagement[db_c.AUDIENCES]:
        # build the audience dict with necessary fields for grouped destination
        audience = {
            api_c.ID: aud[api_c.ID],
            api_c.NAME: aud.get(api_c.NAME, None),
            api_c.IS_LOOKALIKE: aud[api_c.IS_LOOKALIKE],
            api_c.SIZE: aud.get(api_c.SIZE, 0),
        }

        for dest in aud[db_c.DESTINATIONS]:
            destinations = []

            # build the destination dict nested with corresponding audience
            # and latest delivery data
            audience[api_c.LATEST_DELIVERY] = dest[api_c.LATEST_DELIVERY]
            audience[db_c.REPLACE_AUDIENCE] = dest.get(
                db_c.REPLACE_AUDIENCE, False
            )
            destination = {
                api_c.ID: dest[api_c.ID],
                api_c.NAME: dest[api_c.NAME],
                api_c.DESTINATION_AUDIENCES: [],
                api_c.DESTINATION_TYPE: dest[api_c.DELIVERY_PLATFORM_TYPE],
                db_c.LINK: dest.get(db_c.LINK),
            }

            destination[api_c.DESTINATION_AUDIENCES].append(audience)
            destinations.append(destination)

            # if destinations_categories is not populated yet, then append a
            # destination_category dict as required by the response schema
            if destinations_categories:
                for destination_category in destinations_categories:
                    # check if the destination category is already present to
                    # update the existing dict data
                    if (
                        destination_category[api_c.CATEGORY]
                        == dest[api_c.CATEGORY]
                    ):
                        for destination_type in destination_category[
                            api_c.DESTINATIONS
                        ]:
                            # check if the destination_type is already present
                            # to update just the nested audiences object within
                            if (
                                destination_type[api_c.NAME]
                                == destination[api_c.NAME]
                            ):
                                destination_type[
                                    api_c.DESTINATION_AUDIENCES
                                ].extend(
                                    destination[api_c.DESTINATION_AUDIENCES]
                                )
                                break
                        # if the current destination is still not grouped,
                        # then this is the first time this particular
                        # destination_type is encountered
                        else:
                            destination_category[api_c.DESTINATIONS].extend(
                                destinations
                            )
                        break
                # if the current destination is still not grouped, then this
                # is the first time this particular destination_category is
                # encountered
                else:
                    destinations_categories.append(
                        {
                            api_c.CATEGORY: dest[api_c.CATEGORY],
                            api_c.DESTINATIONS: destinations,
                        }
                    )
            else:
                destinations_categories.append(
                    {
                        api_c.CATEGORY: dest[api_c.CATEGORY],
                        api_c.DESTINATIONS: destinations,
                    }
                )

    engagement[api_c.DESTINATION_CATEGORIES] = destinations_categories


def create_description_for_user_request(
    first_name: str,
    last_name: str,
    email: str,
    access_level: str,
    pii_access: bool,
    reason_for_request: str,
    requested_by: str,
    project_name: str = get_config().DEFAULT_NEW_USER_PROJECT_NAME,
    okta_group_name: str = get_config().DEFAULT_OKTA_GROUP_NAME,
    okta_app: str = get_config().DEFAULT_OKTA_APP,
) -> str:
    """Create HUS issue description using new user request data.

    Args:
        first_name (str): First name of the user requested.
        last_name (str): Last name of the user requested.
        email (str): Email of the user requested.
        access_level (str): Access level of the user requested.
        pii_access (bool): If allowed PII access.
        reason_for_request (str): Description of why access request.
        requested_by (str): User Name of the person requesting.
        project_name (str, Optional): Project name which user needs to
            be granted access.
        okta_group_name (str, Optional): Okta group name to which user
            must be added.
        okta_app (str, Optional): Okta app name to which user needs
            permission.

    Returns:
        str: Description for HUS issue.
    """

    return (
        f"*Project Name:* {project_name} \n"
        f"*Required Info:* Please add {first_name} {last_name} to the"
        f" {okta_group_name} group. \n"
        f"*Reason for Request:* {reason_for_request} \n"
        f"*User:* {first_name}, {last_name} \n"
        f"*Email:* {email} \n"
        f"*Access Level:* {access_level} \n"
        f"*PII Access:* {pii_access} \n"
        f"*Okta Group Name:* {okta_group_name} \n"
        f"*Okta App:* {okta_app} \n"
        f"*Requested by:* {requested_by}"
    )


def validate_if_resource_owner(
    resource_name: str, resource_id: str, user_name: str
) -> bool:
    """Validates if the user given is the resource owner.

    Args:
         resource_name (str): Name of the resource.
         resource_id (str): ID of the resource.
         user_name (str): User name of the user.

     Returns:
         bool: True if the name of user is the same as created_by.
    """

    resource_collection_mapping = {
        api_c.AUDIENCE: db_c.AUDIENCES_COLLECTION,
        api_c.ENGAGEMENT: db_c.ENGAGEMENTS_COLLECTION,
    }
    # Get the collection from the mapping.
    collection = resource_collection_mapping.get(resource_name)
    if collection:
        resource = get_document(
            database=get_db_client(),
            collection=collection,
            query_filter={db_c.ID: ObjectId(resource_id)},
        )
        # Add check if resource name is audience, considering lookalikes.
        if not resource and resource_name == api_c.AUDIENCE:
            resource = get_document(
                database=get_db_client(),
                collection=db_c.LOOKALIKE_AUDIENCE_COLLECTION,
                query_filter={db_c.ID: ObjectId(resource_id)},
            )

        if resource and resource.get(db_c.CREATED_BY, "") == user_name:
            return True

    return False


def filter_team_member_requests(team_member_request_issues: list) -> list:
    """Filters Jira team member requests.

    Args:
        team_member_request_issues (list): List of Jira issues.

    Returns:
        list: Filtered and reformatted user requests.
    """

    status_score_mapping = {
        api_c.STATE_TO_DO: 0,
        api_c.STATE_IN_PROGRESS: 1,
        api_c.STATE_IN_REVIEW: 2,
        api_c.STATE_DONE: 3,
    }
    filtered_user_requests = []

    if team_member_request_issues:
        user_info = defaultdict(list)
        for issue in team_member_request_issues:
            request_details = extract_user_request_details_from_issue(issue)

            if RequestedUserSchema().validate(data=request_details):
                user_info[request_details.get(api_c.EMAIL)].append(
                    request_details
                )
        # pylint: disable=unused-variable
        for user_email, info in user_info.items():
            info.sort(
                key=lambda x: status_score_mapping.get(x.get(api_c.STATUS)),
                reverse=True,
            )
            filtered_user_requests.append(info[0])

    return filtered_user_requests


# pylint: disable=anomalous-backslash-in-string
def extract_user_request_details_from_issue(
    team_member_request_issue: dict,
) -> dict:
    """Extracts user request details from Jira issue.

    Args:
        team_member_request_issue (dict): Jira issue for team member request.

    Returns:
        dict: Team member request issue details.
    """

    description = team_member_request_issue.get(api_c.FIELDS, {}).get(
        api_c.DESCRIPTION, None
    )

    if not description:
        logger.info("No description found while parsing user request")
        return {}

    email = re.search("Email:\*(.*?)\\n", description)
    pii_access = re.search("PII Access:\*(.*?)\\n", description)
    display_name = re.search("User:\*(.*?)\\n", description)
    access_level = re.search("Access Level:\*(.*?)\\n", description)

    return {
        api_c.EMAIL: email.groups()[0].strip() if email else None,
        api_c.USER_PII_ACCESS: Validation.validate_bool(
            pii_access.groups()[0].strip()
        )
        if pii_access
        else False,
        api_c.DISPLAY_NAME: display_name.groups()[0].strip()
        if display_name
        else None,
        api_c.USER_ACCESS_LEVEL: access_level.groups()[0].strip()
        if access_level
        else None,
        api_c.STATUS: team_member_request_issue.get(api_c.FIELDS, {})
        .get(api_c.STATUS, {})
        .get(api_c.NAME),
        api_c.UPDATED: parse(
            team_member_request_issue.get(api_c.FIELDS, {}).get(api_c.UPDATED)
        ),
        api_c.CREATED: parse(
            team_member_request_issue.get(api_c.FIELDS, {}).get(api_c.CREATED)
        ),
        api_c.KEY: team_member_request_issue.get(api_c.KEY),
    }


def group_and_aggregate_datafeed_details_by_date(
    datafeed_details: list,
) -> list:
    """Group and aggregate data feed details by date.

    Args:
        datafeed_details (list): list of data feed details to group.

    Returns:
        list: List of aggregated and grouped data feed details.
    """

    grouped_datafeed_details = []

    grouped_by_date = groupby(
        datafeed_details, lambda x: x[api_c.PROCESSED_START_DATE]
    )

    stdev_sample_list = []
    for df_date, df_details in grouped_by_date:
        data_feed_by_date = {
            api_c.NAME: df_date,
            api_c.DATA_FILES: [],
        }
        total_records_received = 0
        total_records_processed = 0

        status = api_c.STATUS_COMPLETE
        for df_detail in df_details:
            # set last processed start for datafeeds aggregated by date
            # i.e. Minimum of last processed start for all grouped datafeeds
            if (
                not data_feed_by_date.get(api_c.PROCESSED_START_DATE)
                or data_feed_by_date[api_c.PROCESSED_START_DATE]
                >= df_detail[api_c.PROCESSED_START_DATE]
            ):
                data_feed_by_date[api_c.PROCESSED_START_DATE] = df_detail[
                    api_c.PROCESSED_START_DATE
                ]
            # set last processed end for datafeeds aggregated by date
            # i.e. Maximum of last processed end for all grouped datafeeds
            if (
                not data_feed_by_date.get(api_c.PROCESSED_END_DATE)
                or data_feed_by_date[api_c.PROCESSED_END_DATE]
                <= df_detail[api_c.PROCESSED_END_DATE]
            ):
                data_feed_by_date[api_c.PROCESSED_END_DATE] = df_detail[
                    api_c.PROCESSED_END_DATE
                ]
            total_records_received += df_detail.get(api_c.RECORDS_RECEIVED, 0)
            total_records_processed += df_detail.get(
                api_c.RECORDS_PROCESSED, 0
            )
            data_feed_by_date[api_c.DATA_FILES].append(df_detail)

            if (
                status == api_c.STATUS_COMPLETE
                and df_detail[api_c.STATUS] == api_c.STATUS_RUNNING
            ):
                status = api_c.STATUS_INCOMPLETE

            elif (
                status in [api_c.STATUS_COMPLETE, api_c.STATUS_INCOMPLETE]
                and df_detail[api_c.STATUS] == api_c.STATUS_FAILED
            ):
                status = api_c.STATUS_FAILED

        if status in [api_c.STATUS_COMPLETE] and data_feed_by_date.get(
            api_c.PROCESSED_END_DATE
        ):
            data_feed_by_date[
                api_c.RUN_DURATION
            ] = parse_seconds_to_duration_string(
                int(
                    (
                        data_feed_by_date[api_c.PROCESSED_END_DATE]
                        - data_feed_by_date[api_c.PROCESSED_START_DATE]
                    ).total_seconds()
                )
            )

        records_processed_percentage = (
            round(total_records_processed / total_records_received, 3)
            if total_records_received
            else 0
        )

        _ = data_feed_by_date.update(
            {
                api_c.RECORDS_PROCESSED: total_records_processed,
                api_c.RECORDS_RECEIVED: total_records_received,
                api_c.RECORDS_PROCESSED_PERCENTAGE: {
                    api_c.VALUE: records_processed_percentage,
                    api_c.FLAG_INDICATOR: (
                        statistics.stdev(stdev_sample_list)
                        if len(stdev_sample_list) > 1
                        else 0
                    )
                    > 0.1,
                },
                api_c.STATUS: status,
            }
        )

        grouped_datafeed_details.append(data_feed_by_date)

    return grouped_datafeed_details


def clean_and_aggregate_datafeed_details(
    datafeed_details: list, do_aggregate: bool = False
) -> list:
    """Clean and aggregate datafeed details.

    Args:
        datafeed_details (list): List of data feed file details.
        do_aggregate (bool): Flag specifying if aggregation needed.

    Returns:
        list: list of data feed details.
    """

    stdev_sample_list = []
    for df_detail in datafeed_details:
        records_processed_percentage = (
            (
                df_detail[api_c.RECORDS_PROCESSED]
                / df_detail[api_c.RECORDS_RECEIVED]
            )
            if df_detail.get(api_c.RECORDS_RECEIVED)
            else 0
        )
        # TODO: Refactor computing standard deviation once we have clarity
        stdev_sample_list.append(records_processed_percentage)
        _ = df_detail.update(
            {
                api_c.PROCESSED_START_DATE: parse(
                    df_detail[api_c.PROCESSED_START_DATE]
                ),
                api_c.PROCESSED_END_DATE: parse(
                    df_detail[api_c.PROCESSED_END_DATE]
                ),
                api_c.STATUS: df_detail[api_c.STATUS].title(),
                api_c.SUB_STATUS: df_detail[api_c.SUB_STATUS].title(),
                api_c.RECORDS_PROCESSED_PERCENTAGE: {
                    api_c.VALUE: records_processed_percentage,
                    api_c.FLAG_INDICATOR: (
                        statistics.stdev(stdev_sample_list)
                        if len(stdev_sample_list) > 1
                        else 0
                    )
                    > 0.1,
                },
            }
        )
        # compute run duration if success or running and end_dt available

        if df_detail[api_c.STATUS] in [
            api_c.STATUS_SUCCESS,
            api_c.STATUS_RUNNING,
        ] and df_detail.get(api_c.PROCESSED_END_DATE):
            df_detail[api_c.RUN_DURATION] = parse_seconds_to_duration_string(
                int(
                    (
                        df_detail[api_c.PROCESSED_END_DATE]
                        - df_detail[api_c.PROCESSED_START_DATE]
                    ).total_seconds()
                )
            )

    return (
        group_and_aggregate_datafeed_details_by_date(datafeed_details)
        if do_aggregate
        else datafeed_details
    )


def clean_domain_name_string(domain_name: str) -> str:
    """Cleans strings like abc.com for Marshmallow attribute field.

    Args:
        domain_name (str): Name of the domain.

    Returns:
        str: Cleaned domain name.
    """

    # This is to handle @ present in sfmc data.
    if "@" in domain_name:
        domain_name = domain_name.split("@")[1]

    return domain_name.replace(".", "-")


def parse_seconds_to_duration_string(duration: int):
    """Convert duration timedelta to HH:MM:SS format.

    Args:
        duration (int): Duration in seconds.

    Returns:
        str: duration string.
    """

    seconds = duration % 60
    minutes = (duration // 60) % 60
    hours = duration // (60 * 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def generate_cache_key_string(data: Union[dict, list]) -> Generator:
    """Generates cache key strings for dicts and lists.

    Args:
        data (Union[dict,list]): Input data to get cache key.

    Yields:
        Generator: String Generator.
    """

    for item in data:
        if isinstance(item, list):
            generate_cache_key_string(item)
        elif isinstance(item, dict):
            yield " ".join(
                [x for key, value in item.items() for x in [key, str(value)]]
            )
        else:
            yield item


def set_destination_authentication_secrets(
    authentication_details: dict,
    destination_id: str,
    destination_type: str,
) -> dict:
    """Save authentication details in cloud provider secret storage

    Args:
        authentication_details (dict): The key/secret pair to store away.
        destination_id (str): destinations ID.
        destination_type (str): destination type (i.e. facebook, sfmc)

    Returns:
        ssm_params (dict): The key to where the parameters are stored.

    Raises:
        KeyError: Exception when the key is missing in the object.
        ProblemException: Any exception raised during endpoint execution.
    """

    ssm_params = {}

    if destination_type not in api_c.DESTINATION_SECRETS:
        raise KeyError(
            f"{destination_type} does not have a secret store mapping."
        )

    for (
        parameter_name,
        secret,
    ) in authentication_details.items():

        # only store secrets in ssm, otherwise store in object.
        if (
            parameter_name
            in api_c.DESTINATION_SECRETS[destination_type][api_c.MONGO]
        ):
            ssm_params[parameter_name] = secret
            continue

        param_name = f"{api_c.PARAM_STORE_PREFIX}-{parameter_name}"
        ssm_params[parameter_name] = param_name
        try:
            CloudClient().set_secret(secret_name=param_name, value=secret)
        except Exception as exc:
            logger.error("Failed to connect to secret store.")
            logger.error(exc)
            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail=f"{api_c.SECRET_STORAGE_ERROR_MSG}"
                f" destination_id: {destination_id}.",
            ) from exc

    return ssm_params


def generate_audience_file(
    data_batches: pd.DataFrame,
    transform_function: Callable,
    audience_id: ObjectId,
    download_type: str,
    user_name: str,
    database: DatabaseClient,
) -> None:
    """Generates Audience File

    Args:
        database(DatabaseClient): MongoDB Client
        user_name(str): User name
        download_type(str): Download Type selected
        audience_id(ObjectId): Audience Id
        data_batches(pd.Dataframe): Data batches retrieved from cdp
        transform_function(Callable): Transform Function

    Returns:

    """
    folder_name = "downloadaudiences"
    audience_file_name = (
        f"{datetime.now().strftime('%m%d%Y%H%M%S')}"
        f"_{audience_id}_{download_type}.csv"
    )
    with open(
        Path(__file__).parent.parent.joinpath(folder_name)
        / audience_file_name,
        "w",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        for dataframe_batch in data_batches:
            transform_function(dataframe_batch).to_csv(
                csvfile,
                mode="a",
                index=False,
            )

    logger.info(
        "Uploading generated %s audience file to %s S3 bucket",
        audience_file_name,
        get_config().S3_DATASET_BUCKET,
    )
    filename = (
        Path(__file__).parent.parent.joinpath(folder_name)
        / audience_file_name,
    )
    if CloudClient().upload_file(
        file_name=str(filename[0]),
        bucket=get_config().S3_DATASET_BUCKET,
        object_name=audience_file_name,
        user_name=user_name,
        file_type=api_c.AUDIENCE,
    ):
        create_audience_audit(
            database=database,
            audience_id=audience_id,
            download_type=download_type,
            file_name=audience_file_name,
            user_name=user_name,
        )
        logger.info(
            "Created an audit log for %s audience file creation",
            audience_file_name,
        )


def convert_filters_for_events(filters: dict, event_types: List[dict]) -> None:
    """Method to Convert for Events

    Args:
        filters (dict): An audience filter
        event_types(List[dict]): List of event_types

    Returns:

    """
    for section in filters[api_c.AUDIENCE_FILTERS]:
        for section_filter in section[api_c.AUDIENCE_SECTION_FILTERS]:
            if section_filter.get(api_c.AUDIENCE_FILTER_FIELD) in [
                x[api_c.TYPE] for x in event_types
            ]:
                event_name = section_filter.get(api_c.AUDIENCE_FILTER_FIELD)
                if section_filter.get(api_c.TYPE) == "within_the_last":
                    is_range = True
                elif section_filter.get(api_c.TYPE) == "not_within_the_last":
                    is_range = False
                elif section_filter.get(api_c.TYPE) == "between":
                    is_range = True
                else:
                    break
                if section_filter.get(api_c.TYPE) == "between":
                    start_date = section_filter.get(
                        api_c.AUDIENCE_FILTER_VALUE
                    )[0]
                    end_date = section_filter.get(api_c.AUDIENCE_FILTER_VALUE)[
                        1
                    ]
                else:
                    start_date = (
                        datetime.utcnow()
                        - timedelta(
                            days=int(
                                section_filter.get(
                                    api_c.AUDIENCE_FILTER_VALUE
                                )[0]
                            )
                        )
                    ).strftime("%Y-%m-%d")
                    end_date = datetime.utcnow().strftime("%Y-%m-%d")
                section_filter.update({api_c.AUDIENCE_FILTER_FIELD: "event"})
                section_filter.update({api_c.TYPE: "event"})
                section_filter.update(
                    {
                        api_c.VALUE: [
                            {
                                api_c.AUDIENCE_FILTER_FIELD: "event_name",
                                api_c.TYPE: "equals",
                                api_c.VALUE: event_name,
                            },
                            {
                                api_c.AUDIENCE_FILTER_FIELD: "created",
                                api_c.TYPE: api_c.AUDIENCE_FILTER_RANGE
                                if is_range
                                else api_c.AUDIENCE_FILTER_NOT_RANGE,
                                api_c.VALUE: [start_date, end_date],
                            },
                        ]
                    }
                )


# pylint: disable=unused-variable
async def build_notification_recipients_and_send_email(
    database: DatabaseClient, notifications: list, req_env_url_root: str
):
    """Get user alert configuration and prepare notifications to send user
    email.

    Args:
        database (DatabaseClient): A database client.
        notifications (list): list of notifications to be prepared for email.
        req_env_url_root (str): Environment base URL that needs to be passed in
            to send email function.
    """

    if not notifications:
        return

    # get all users with alerts configured
    users = get_all_users(
        database=database,
        filter_dict={db_c.USER_ALERTS: {"$exists": True, "$ne": []}},
        project_dict={
            db_c.USER_DISPLAY_NAME: 1,
            api_c.USER_EMAIL_ADDRESS: 1,
            db_c.USER_ALERTS: 1,
        },
    )

    if not users:
        return

    # process each notification from the list of fetched notifications
    for notification in notifications:
        notification_category = notification[db_c.NOTIFICATION_FIELD_CATEGORY]
        notification_type = notification[db_c.NOTIFICATION_FIELD_TYPE]
        notification_description = notification[
            db_c.NOTIFICATION_FIELD_DESCRIPTION
        ]

        if (notification_category not in db_c.NOTIFICATION_CATEGORIES) or (
            notification_type not in db_c.NOTIFICATION_TYPES
        ):
            continue

        recipients_list = []

        # process each user document to compare the user's alert configuration
        # against the notification category and type
        for user_doc in users:
            for user_alert_category in user_doc.get(db_c.USER_ALERTS).values():
                for (
                    alert_category_key,
                    alert_category_value,
                ) in user_alert_category.items():
                    # break out of the loop to move to next user if category
                    # of notification matches the user alert category type
                    if notification_category == alert_category_key:
                        if alert_category_value.get(notification_type, False):
                            recipients_list.append(
                                (
                                    user_doc.get(api_c.USER_EMAIL_ADDRESS),
                                    user_doc.get(api_c.DISPLAY_NAME),
                                )
                            )
                        break
                else:
                    continue
                break
            else:
                continue

        if not recipients_list:
            continue

        send_email_dict = {
            api_c.NOTIFICATION_EMAIL_RECIPIENTS: recipients_list,
            api_c.NOTIFICATION_EMAIL_ALERT_CATEGORY: notification_category,
            api_c.NOTIFICATION_EMAIL_ALERT_TYPE: notification_type,
            api_c.NOTIFICATION_EMAIL_ALERT_DESCRIPTION: notification_description,
            api_c.URL: req_env_url_root,
        }

        # TODO: call send email function to actually send an email
        # send_email(**send_email_dict)


def populate_trust_id_segments(
    database: DatabaseClient, custom_segments: list, add_default: bool = True
) -> list:
    """Function to populate Trust ID Segment data.
    Args:
        database (DatabaseClient): A database client.
        custom_segments(list): List of user specific segments data.
        add_default (Optional, bool): Flag to add All Customers.
    Returns:
        list: Filled segments data with survey responses.
    """

    segments_data = []
    # Set default segment without any filters
    if add_default:
        segments_data.append(
            {
                api_c.SEGMENT_NAME: "All Customers",
                api_c.SEGMENT_FILTERS: [],
                api_c.SURVEY_RESPONSES: get_survey_responses(
                    database=database
                ),
            }
        )

    for seg in custom_segments:
        survey_response = get_survey_responses(
            database=database,
            filters=seg[api_c.SEGMENT_FILTERS],
        )
        segments_data.append(
            {
                api_c.SEGMENT_NAME: seg[api_c.SEGMENT_NAME],
                api_c.SEGMENT_FILTERS: seg[api_c.SEGMENT_FILTERS],
                api_c.SURVEY_RESPONSES: survey_response
                if survey_response
                else [],
            }
        )
    return segments_data


def get_engaged_audience_last_delivery(audience: dict) -> None:
    """Method for getting last delivery at engagement and engaged audience level

    Args:
        audience(dict): Engagement Object

    Returns:
    """

    delivery_times = []

    delivery_times.extend(
        [
            destination[api_c.LATEST_DELIVERY][db_c.UPDATE_TIME]
            for destination in audience[api_c.DESTINATIONS]
            if destination[api_c.LATEST_DELIVERY].get(api_c.STATUS).lower()
            == api_c.DELIVERED
        ]
    )
    audience[api_c.AUDIENCE_LAST_DELIVERED] = (
        max(delivery_times) if delivery_times else None
    )


def convert_cdp_buckets_to_histogram(
    bucket_data: list, field: str = None
) -> namedtuple:
    """Method to convert data from CDP response to histogram format.

    Args:
         bucket_data (list): Body of CDP count-by response.
         field (str): Name of field.
    Returns:
        Tuple[Union[int, float], Union[int, float], list]: Max, min and
            converted values list.
    """
    CDPHistogramData = namedtuple("CDPHistogramData", "max_val min_val values")

    if field == api_c.AGE:
        value = api_c.AGE
        max_val = bucket_data[-1].get(api_c.AGE)
        min_val = bucket_data[0].get(api_c.AGE)

    else:
        value = api_c.VALUE_FROM
        max_val = bucket_data[-1].get(api_c.VALUE_TO)
        min_val = bucket_data[0].get(api_c.VALUE_FROM)

    return CDPHistogramData(
        max_val,
        min_val,
        [
            (data.get(value), data.get(api_c.CUSTOMER_COUNT))
            for data in bucket_data
        ],
    )
