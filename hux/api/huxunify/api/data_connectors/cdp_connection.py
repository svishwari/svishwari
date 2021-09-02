"""Purpose of this file is to house all methods to connect to CDP connections API"""
from typing import Tuple, Union
import requests

from huxunifylib.util.general.logging import logger

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.data_connectors.cdp import clean_cdm_fields


def check_cdp_connections_api_connection() -> Tuple[Union[int, bool], str]:
    """Validate the cdp connections api connection.
    Args:

    Returns:
        tuple[Union[int,bool], str]: Returns if the connection is valid, and the message.
    """
    # get config
    config = get_config()

    # submit the post request to get documentation
    try:
        response = requests.get(
            f"{config.CDP_CONNECTION_SERVICE}healthcheck",
            timeout=5,
        )
        return response.status_code, "CDP connections available."

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        logger.error(
            "CDP Connections Health Check failed with %s.", repr(exception)
        )
        return False, getattr(
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

    return {
        k: clean_cdm_fields(v) for k, v in response.json()[api_c.BODY].items()
    }
