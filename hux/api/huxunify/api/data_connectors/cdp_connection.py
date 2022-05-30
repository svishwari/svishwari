"""Purpose of this file is to house all methods to connect to CDP connections
API.
"""
import random
import statistics
from typing import Tuple, Optional
from datetime import datetime, timedelta

import requests
from dateutil.parser import parse

from huxunifylib.util.general.logging import logger
from huxunify.api.prometheus import record_health_status, Connections

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.data_connectors.cdp import clean_cdm_fields, DEFAULT_DATETIME
from huxunify.api.exceptions import integration_api_exceptions as iae


@record_health_status(Connections.CDM_CONNECTION_SERVICE)
def check_cdp_connections_api_connection() -> Tuple[int, str]:
    """Validate the cdp connections api connection.

    Returns:
        tuple[int, str]: Returns if the connection is valid, and the message.
    """

    # get config
    config = get_config()

    # submit the post request to get documentation
    try:
        response = requests.get(
            f"{config.CDP_CONNECTION_SERVICE}/healthcheck",
            timeout=5,
        )
        if response.status_code == 200:
            logger.info("CDP is available.")
            return True, "CDP connections available."
        logger.error(
            "CDP is unavailable, returned a %s response.", response.status_code
        )
        return (
            False,
            f"Received status code: {response.status_code}, "
            f"Received message: {response.json()}",
        )

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        logger.exception("CDP Connections Health Check failed.")
        return getattr(exception, "code", repr(exception)), getattr(
            exception, "message", repr(exception)
        )


def get_identity_overview(
    token: str,
    filters: Optional[dict] = None,
) -> dict:
    """Get identity overview data

    Args:
        token (str): OKTA JWT token
        filters (dict): filters to pass into identity overview
            endpoint, default None.
    Returns:
        dict: dictionary of overview data.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()
    logger.info("Getting Identity Insights from CDP API.")
    response = requests.post(
        f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_IDENTITY_ENDPOINT}/"
        f"{api_c.INSIGHTS}",
        json=filters if filters else {},
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Unable to retrieve identity insights, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_IDENTITY_ENDPOINT}/"
            f"{api_c.INSIGHTS}",
            response.status_code,
        )

    logger.info(
        "Successfully retrieved Identity Insights from Connections API."
    )

    return clean_cdm_fields(response.json()[api_c.BODY])


def get_idr_data_feeds(token: str, start_date: str, end_date: str) -> list:
    """Fetch IDR data feeds.

    Args:
        token (str): OKTA JWT Token.
        start_date (str): Start date.
        end_date (str): End date.

    Returns:
       list: datafeeds processed within the given dates.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()
    logger.info(
        "Retrieving data-feeds for within %s and %s.", start_date, end_date
    )

    response = requests.post(
        f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_IDENTITY_ENDPOINT}/"
        f"{api_c.DATAFEEDS}",
        json={api_c.START_DATE: start_date, api_c.END_DATE: end_date},
        headers={api_c.CUSTOMERS_API_HEADER_KEY: token},
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Failed to retrieve identity data feeds, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_IDENTITY_ENDPOINT}/"
            f"{api_c.DATAFEEDS}",
            response.status_code,
        )

    logger.info("Successfully retrieved identity data feeds.")

    return [clean_cdm_fields(d) for d in response.json()[api_c.BODY]]


def get_idr_data_feed_details(token: str, datafeed_id: int) -> dict:
    """Fetch details of IDR datafeed by ID.

    Args:
        token (str): OKTA JWT Token.
        datafeed_id (int): Data feed ID.

    Returns:
        dict: Datafeed details object.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()
    logger.info(
        "Retrieving identity data-feed details with data feed id %s.",
        datafeed_id,
    )

    response = requests.get(
        f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_IDENTITY_ENDPOINT}/"
        f"{api_c.DATAFEEDS}/{datafeed_id}",
        headers={api_c.CUSTOMERS_API_HEADER_KEY: token},
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Failed to retrieve identity data feed details, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_IDENTITY_ENDPOINT}/"
            f"{api_c.DATAFEEDS}/{datafeed_id}",
            response.status_code,
        )

    logger.info("Successfully retrieved identity data feed details.")

    return {
        k: clean_cdm_fields(v) for k, v in response.json()[api_c.BODY].items()
    }


def get_data_sources(token: str) -> list:
    """Fetch data sources.

    Args:
        token (str): OKTA JWT token

    Returns:
        (list): List of data sources

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()
    logger.info("Retrieving data-sources.")

    response = requests.get(
        f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_CONNECTIONS_ENDPOINT}/"
        f"{api_c.DATASOURCES}",
        headers={api_c.CUSTOMERS_API_HEADER_KEY: token},
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Failed to retrieve data sources, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_CONNECTIONS_ENDPOINT}/"
            f"{api_c.DATASOURCES}",
            response.status_code,
        )

    logger.info("Successfully retrieved data sources.")

    return response.json()[api_c.BODY]


def get_data_source_data_feeds(token: str, data_source_type: str) -> list:
    """Retrieve data source data feeds.

    Args:
        token (str): OKTA JWT Token.
        data_source_type (str): type of data source.

    Returns:
        list: list of connection data-feeds.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    config = get_config()

    logger.info(
        "Retrieving data-feeds for data source with type %s.", data_source_type
    )

    response = requests.get(
        f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_CONNECTIONS_ENDPOINT}/"
        f"{data_source_type}/{api_c.DATA_FEEDS}",
        headers={api_c.CUSTOMERS_API_HEADER_KEY: token},
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Failed to retrieve %s connections data feeds, %s %s.",
            data_source_type,
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_CONNECTIONS_ENDPOINT}/"
            f"{data_source_type}/{api_c.DATA_FEEDS}",
            response.status_code,
        )

    logger.info(
        "Successfully retrieved %s data feed details.", data_source_type
    )

    data_feeds = response.json()[api_c.BODY]

    for data_feed in data_feeds:
        data_feed[api_c.PROCESSED_AT] = parse(
            data_feed.get(api_c.PROCESSED_AT)
        )

        # handle nulls and division by zero
        records_received = data_feed.get(api_c.RECORDS_RECEIVED, 1)
        if records_received is None or records_received == 0:
            data_feed[api_c.RECORDS_RECEIVED] = 1

        # handle nulls and division by zero
        records_processed = data_feed.get(api_c.RECORDS_PROCESSED, 0)
        if records_processed is None:
            data_feed[api_c.RECORDS_PROCESSED] = 1

        # handle nulls and division by zero
        thirty_days_avg = data_feed.get(api_c.THIRTY_DAYS_AVG, 0)
        if thirty_days_avg is None:
            data_feed[api_c.THIRTY_DAYS_AVG] = 1

        # clean this up after HUS-2172
        data_feed[api_c.RECORDS_PROCESSED_PERCENTAGE] = (
            data_feed[api_c.RECORDS_PROCESSED]
            / data_feed[api_c.RECORDS_RECEIVED]
        )
        data_feed[api_c.THIRTY_DAYS_AVG] = round(
            data_feed[api_c.THIRTY_DAYS_AVG] / 100, 1
        )

    # calculate standard deviation on records_processed_percentage to set
    # appropriate flag indicator
    stdev_sample_list = []
    # sort the data_feeds list from greater to smaller records processed
    # percentage value
    data_feeds.sort(
        key=lambda data_feed: data_feed[api_c.RECORDS_PROCESSED_PERCENTAGE],
        reverse=True,
    )
    for i, data_feed in enumerate(data_feeds):
        current_value = data_feed[api_c.RECORDS_PROCESSED_PERCENTAGE]

        # build up the sample list of processed percentage to calculate SD
        stdev_sample_list.append(current_value)

        # need at least 2 elements in the sample list to calculate SD for
        # current processed_percentage value
        current_stdev = statistics.stdev(stdev_sample_list) if i > 0 else 0

        # set records_processed_percentage for hte corresponding data feed with
        # the dict populated with value and flag_indicator if the current
        # calculated SD is greater than initial SD
        data_feed[api_c.RECORDS_PROCESSED_PERCENTAGE] = {
            api_c.VALUE: current_value,
            api_c.FLAG_INDICATOR: (current_stdev > 0.1),
        }

    # calculate standard deviation on thirty_days_avg to set appropriate flag
    # indicator
    stdev_sample_list = []
    # sort the data_feeds list from greater to smaller thirty days average
    # value
    data_feeds.sort(
        key=lambda data_feed: data_feed[api_c.THIRTY_DAYS_AVG],
        reverse=True,
    )
    for i, data_feed in enumerate(data_feeds):
        current_value = data_feed[api_c.THIRTY_DAYS_AVG]

        # build up the sample list of thirty days average to calculate SD
        stdev_sample_list.append(current_value)

        # need at least 2 elements in the sample list to calculate SD for
        # current thirty_days_avg value
        current_stdev = statistics.stdev(stdev_sample_list) if i > 0 else 0

        # set thirty_days_avg for the corresponding data feed with the dict
        # populated with value and flag_indicator if the current calculated SD
        # is greater than 0.1
        data_feed[api_c.THIRTY_DAYS_AVG] = {
            api_c.VALUE: current_value,
            api_c.FLAG_INDICATOR: (current_stdev > 0.1),
        }

    # sort the data_feeds list back to order based on processed_at time
    data_feeds.sort(key=lambda data_feed: data_feed[api_c.PROCESSED_AT])

    return data_feeds


def get_idr_matching_trends(
    token: str, start_date: str, end_date: str
) -> list:
    """Retrieves IDR matching trends data YTD.

    Args:
        token (str): OKTA JWT Token.
        start_date (str): Start date.
        end_date (str): End date.

    Returns:
       list: count of known, anonymous, unique ids on a day.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # TODO : Fetch date range from CDP
    start_date = (
        parse(start_date)
        if start_date
        else datetime.today() - timedelta(days=random.randint(100, 1000))
    ).strftime("%Y-%m-%d")

    end_date = (parse(end_date) if end_date else datetime.today()).strftime(
        "%Y-%m-%d"
    )

    filters = {api_c.START_DATE: start_date, api_c.END_DATE: end_date}

    config = get_config()
    logger.info("Getting IDR matching trends from CDP API.")
    response = requests.post(
        f"{config.CDP_CONNECTION_SERVICE}/identity/id-count-by-day",
        json=filters,
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Unable to retrieve IDR matching trends, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_CONNECTION_SERVICE}/identity/id-count-by-day",
            response.status_code,
        )

    logger.info("Successfully retrieved IDR matching trends from CDP API.")
    return sorted(
        [clean_cdm_fields(data) for data in response.json()[api_c.BODY]],
        key=lambda data: data.get(api_c.DAY, DEFAULT_DATETIME),
    )


def get_data_source_data_feed_details(
    token: str, data_source_type: str, datafeed_name: str, query_json: dict
) -> list:
    """Retrieve data source data feed details.

    Args:
        token (str): OKTA JWT Token.
        data_source_type (str): type of data source.
        datafeed_name (str): data feed name.
        query_json (dict): Filter dict

    Returns:
        list: list of connection data-feed details.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    config = get_config()

    logger.info(
        "Retrieving data-feed file details for data source with type %s and data feed name %s.",
        data_source_type,
        datafeed_name,
    )

    response = requests.post(
        f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_CONNECTIONS_ENDPOINT}/"
        f"{api_c.DATASOURCES}/{data_source_type}/feeds/{datafeed_name}/files",
        json=query_json,
        headers={api_c.CUSTOMERS_API_HEADER_KEY: token},
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Failed to retrieve file details of data feed %s for data source %s, %s %s.",
            datafeed_name,
            data_source_type,
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_CONNECTION_SERVICE}/{api_c.CDM_CONNECTIONS_ENDPOINT}/"
            f"{api_c.DATASOURCES}/{data_source_type}/feeds/{datafeed_name}/files",
            response.status_code,
        )

    logger.info(
        "Successfully retrieved file details for data feed %s and data source %s.",
        datafeed_name,
        data_source_type,
    )

    return response.json()[api_c.BODY]
