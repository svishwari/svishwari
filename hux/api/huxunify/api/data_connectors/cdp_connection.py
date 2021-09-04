"""Purpose of this file is to house all methods to connect to CDP connections API"""
import random
from typing import Tuple
from datetime import datetime, timedelta

import requests
from dateutil.parser import parse

from huxunifylib.util.general.logging import logger

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.data_connectors.cdp import clean_cdm_fields, DEFAULT_DATETIME


def check_cdp_connections_api_connection() -> Tuple[int, str]:
    """Validate the cdp connections api connection.
    Args:

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
        return response.status_code, "CDP connections available."

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        logger.error(
            "CDP Connections Health Check failed with %s.", repr(exception)
        )
        return getattr(exception, "code", repr(exception)), getattr(
            exception, "message", repr(exception)
        )


def get_idr_data_feeds(token: str, start_date: str, end_date: str) -> list:
    """
    Fetch IDR data feeds

    Args:
        token (str): OKTA JWT Token.
        start_date (str): Start date.
        end_date (str): End date.
    Returns:
       list: datafeeds processed within the given dates.
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
            "Failed to retrieve identity data feeds %s %s.",
            response.status_code,
            response.text,
        )
        return []

    logger.info("Successfully retrieved identity data feeds.")

    return [clean_cdm_fields(d) for d in response.json()[api_c.BODY]]


def get_idr_data_feed_details(token: str, datafeed_id: int) -> dict:
    """
    Fetch details of IDR datafeed by ID

    Args:
        token (str): OKTA JWT Token
        datafeed_id (int): Data feed ID

    Returns:
        dict: Datafeed details object
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
            "Failed to retrieve identity data feed details %s %s.",
            response.status_code,
            response.text,
        )
        return []

    logger.info("Successfully retrieved identity data feed details.")

    return {
        k: clean_cdm_fields(v) for k, v in response.json()[api_c.BODY].items()
    }


def get_connections_data_feeds(token: str, data_source_type: str) -> list:
    """
    Retrieve data source data feeds

    Args:
        token (str): OKTA JWT Token
        data_source_type (str): type of data source

    Returns:
        list: list of connection data-feeds

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
            "Failed to retrieve %s connections data feeds %s %s.",
            data_source_type,
            response.status_code,
            response.text,
        )
        return []

    logger.info(
        "Successfully retrieved %s data feed details.", data_source_type
    )

    data_feeds = response.json()[api_c.BODY]

    for data_feed in data_feeds:
        data_feed[api_c.PROCESSED_AT] = parse(
            data_feed.get(api_c.PROCESSED_AT)
        )
        data_feed["records_processed_percentage"] = data_feed.get(
            "records_processed", 0
        ) / data_feed.get("records_received", 1)
        data_feed["thirty_days_avg"] = (
            data_feed.get("thirty_days_avg", 0) / 100
        )
    return data_feeds


def get_idr_matching_trends(
    token: str, start_date: str, end_date: str
) -> list:
    """Retrieves IDR matching trends data YTD
    Args:
        token (str): OKTA JWT Token.
        start_date (str): Start date.
        end_date (str): End date.
    Returns:
       list: count of known, anonymous, unique ids on a day.
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
            "Could not get IDR matching trends from CDP API got %s %s.",
            response.status_code,
            response.text,
        )
        return []
    logger.info("Successfully retrieved IDR matching trends from CDP API.")
    return sorted(
        [clean_cdm_fields(data) for data in response.json()[api_c.BODY]],
        key=lambda data: data.get(api_c.DAY, DEFAULT_DATETIME),
    )
