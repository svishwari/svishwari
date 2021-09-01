"""Purpose of this file is to house all methods to connect to CDP connections API"""
import requests
from dateutil.parser import parse

from huxunifylib.util.general.logging import logger

from huxunify.api import constants as api_c
from huxunify.api.config import get_config


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
        f"{config.CDP_CONNECTION_SERVICE}{api_c.CDM_IDENTITY_ENDPOINT}/"
        f"{api_c.CDM_DATAFEEDS}",
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

    datafeeds = response.json()[api_c.BODY]
    _ = [
        x.update({api_c.TIMESTAMP: parse(x.get(api_c.TIMESTAMP))})
        for x in datafeeds
    ]

    return datafeeds


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
        f"{config.CDP_CONNECTION_SERVICE}{api_c.CDM_IDENTITY_ENDPOINT}/"
        f"{api_c.CDM_DATAFEEDS}/{datafeed_id}",
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

    datafeed = response.json()[api_c.BODY]
    datafeed[api_c.PINNING][api_c.PINNING_TIMESTAMP] = (
        parse(datafeed[api_c.PINNING].get(api_c.PINNING_TIMESTAMP))
        if datafeed[api_c.PINNING].get(api_c.PINNING_TIMESTAMP)
        else None
    )
    datafeed[api_c.STITCHED][api_c.STITCHED_TIMESTAMP] = (
        parse(datafeed[api_c.STITCHED].get(api_c.STITCHED_TIMESTAMP))
        if datafeed[api_c.STITCHED].get(api_c.STITCHED_TIMESTAMP)
        else None
    )
    return datafeed
