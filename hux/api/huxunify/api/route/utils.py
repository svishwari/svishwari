"""
purpose of this file is to house route utilities
"""
from datetime import datetime
from typing import Tuple, Union, Dict
from http import HTTPStatus
from bson import ObjectId

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
    delivery_platform_management as destination_management,
    constants as db_c,
)

from huxunify.api.config import get_config
from huxunify.api import constants
from huxunify.api.data_connectors.tecton import check_tecton_connection
from huxunify.api.data_connectors.aws import (
    check_aws_ssm,
    check_aws_batch,
)
from huxunify.api.data_connectors.okta import (
    check_okta_connection,
)
from huxunify.api.data_connectors.cdp import check_cdm_api_connection
from huxunify.api.data_connectors.cdp_connection import (
    check_cdp_connections_api_connection,
)


def handle_api_exception(exc: Exception, description: str = "") -> None:
    """
    Purpose of this function is to handle general api exceptions,
    and reduce code in the route
    Args:
        exc (Exception): Exception object to handle
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
    Args:

    Returns:
        tuple[bool, str]: Returns if the connection is valid, and the message.
    """
    try:
        # test finding documents
        get_all_data_sources(get_db_client())
        return True, "Mongo available."
    # pylint: disable=broad-except
    # pylint: disable=unused-variable
    except Exception as exception:
        return False, "Mongo not available."


def get_health_check() -> HealthCheck:
    """build and return the health check object

    Args:

    Returns:
        HealthCheck: HealthCheck object that processes checks when called

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
    health.add_check(check_cdm_api_connection)
    health.add_check(check_cdp_connections_api_connection)
    return health


def group_perf_metric(perf_metrics: list, metric_type: str) -> dict:
    """Group performance metrics
    ---

        Args:
            perf_metrics (list): List of performance metrics.
            metric_type (list): Type of performance metrics.

        Returns:
            perf_metric (dict): Grouped performance metric .

    """

    metric = {}

    if metric_type == constants.DISPLAY_ADS:
        for name in constants.DISPLAY_ADS_METRICS:
            metric[name] = sum(
                [
                    int(item[name])
                    for item in perf_metrics
                    if name in item.keys()
                ]
            )
    elif metric_type == constants.EMAIL:
        for name in constants.EMAIL_METRICS:
            metric[name] = sum(
                [
                    int(item[name])
                    for item in perf_metrics
                    if name in item.keys()
                ]
            )

    return metric


def get_friendly_delivered_time(delivered_time: datetime) -> str:
    """Group performance metrics
    ---

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
    """Update performance metrics

    Args:
        target_id (ObjectId) : Group Id.
        name (str): Name of group object.
        jobs (list): List of delivery jobs.
        perf_metrics (list): List of performance metrics.
        metric_type (str): Type of performance metrics.

    Returns:
        metric (dict): Grouped performance metrics .
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


def validate_destination_id(
    destination_id: str, check_if_destination_in_db: bool = True
) -> Union[ObjectId, Tuple[Dict[str, str], int]]:
    """Checks on destination_id

    Check if destination id is valid converts it to object_id.
    Also can check if destination_id is in db

    Args:
        destination_id (str) : Destination id.
        check_if_destination_in_db (bool): Optional; flag to check if destination in db

    Returns:
        response(dict): Message and HTTP status to be returned in response in
            case of failing checks,
        destination_id (ObjectId): Destination id as object id if
            all checks are successful.
    """
    destination_id = ObjectId(destination_id)

    if check_if_destination_in_db:
        if not destination_management.get_delivery_platform(
            get_db_client(), destination_id
        ):
            logger.error(
                "Could not find destination with id %s.", destination_id
            )
            return {
                "message": constants.DESTINATION_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

    return destination_id


def add_chart_legend(data: dict) -> dict:
    """Add chart legend data.

    Args:
        data (str) : Chart data.

    Returns:
        response(dict): Chart data with legend details.
    """

    for key in data:
        if key == constants.NAME:
            data[constants.NAME][constants.PROP] = "Name"
            data[constants.NAME][constants.ICON] = constants.NAME
        if key == constants.EMAIL:
            data[constants.EMAIL][constants.PROP] = "Email"
            data[constants.EMAIL][constants.ICON] = constants.EMAIL
        if key == constants.PHONE:
            data[constants.PHONE][constants.PROP] = "Phone"
            data[constants.PHONE][constants.ICON] = constants.PHONE
        if key == constants.ADDRESS:
            data[constants.ADDRESS][constants.PROP] = "Address"
            data[constants.ADDRESS][constants.ICON] = constants.ADDRESS
        if key == constants.COOKIE:
            data[constants.COOKIE][constants.PROP] = "Cookie"
            data[constants.COOKIE][constants.ICON] = constants.COOKIE
    return data
