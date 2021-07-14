"""
Purpose of this file is for holding methods to query and pull data from CDP.
"""
import datetime
from typing import Tuple, Optional

import requests
from dateutil.parser import parse, ParserError

from huxunifylib.database import constants as db_c

from huxunify.api.config import get_config
from huxunify.api import constants as api_c


# fields to convert to datetime from the responses
DEFAULT_DATETIME = datetime.datetime(1, 1, 1, 1, 00)
DATETIME_FIELDS = [
    "since",
    "last_click",
    "last_purchase",
    "last_email_open",
    "updated",
]


def check_cdm_api_connection() -> Tuple[bool, str]:
    """Validate the cdm api connection.
    Args:

    Returns:
        tuple[bool, str]: Returns if the connection is valid, and the message.
    """
    # get config
    config = get_config()

    # submit the post request to get documentation
    try:
        response = requests.get(
            f"{config.CDP_SERVICE}/docs",
            headers=config.CDP_HEADERS,
            timeout=5,
        )
        return response.status_code, "CDM available."

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        return False, getattr(exception, "message", repr(exception))


def get_customer_profiles() -> dict:
    """Retrieves customer profiles.

    Args:

    Returns:
        dict: dictionary containing the customer profile information

    """

    # get config
    config = get_config()

    response = requests.get(
        f"{config.CDP_SERVICE}/customer-profiles", headers=config.CDP_HEADERS
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        return {}

    response_data = response.json()[api_c.BODY]
    return {
        api_c.TOTAL_CUSTOMERS: len(response_data),
        api_c.CUSTOMERS_TAG: response_data,
    }


def get_customer_profile(hux_id: str) -> dict:
    """Retrieves a customer profile.

    Args:
        hux_id (str): hux id for a customer.

    Returns:
        dict: dictionary containing the customer profile information

    """

    # get config
    config = get_config()

    response = requests.get(
        f"{config.CDP_SERVICE}/customer-profiles/{hux_id}",
        headers=config.CDP_HEADERS,
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        return {}

    return clean_cdm_fields(response.json()[api_c.BODY])


def get_customers_overview(
    filters: Optional[dict] = None,
) -> dict:
    """Fetch customers overview data.

    Args:
        filters (Optional[dict]): filters to pass into
            customers_overview endpoint.

    Returns:
        dict: dictionary of overview data

    """

    # get config
    config = get_config()

    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights",
        json=filters if filters else api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER,
        headers=config.CDP_HEADERS,
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        return {}

    return clean_cdm_fields(response.json()[api_c.BODY])


def get_idr_data_feeds() -> list:
    """
    Fetch IDR data feeds
    """
    # TODO: Update after CDM API for IDR data feeds is available
    response = [
        {
            api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fc",
            api_c.DATAFEED_NAME: "Really_long_Feed_Name_106",
            api_c.DATAFEED_DATA_SOURCE: db_c.DELIVERY_PLATFORM_SFMC,
            api_c.DATAFEED_NEW_IDS_COUNT: 21,
            api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 2023532,
            api_c.MATCH_RATE: 0.98,
            api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow(),
        },
        {
            api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fd",
            api_c.DATAFEED_NAME: "Really_long_Feed_Name_105",
            api_c.DATAFEED_DATA_SOURCE: db_c.DELIVERY_PLATFORM_FACEBOOK,
            api_c.DATAFEED_NEW_IDS_COUNT: 54,
            api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 3232,
            api_c.MATCH_RATE: 0.97,
            api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow()
            - datetime.timedelta(days=1),
        },
        {
            api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fe",
            api_c.DATAFEED_NAME: "Really_long_Feed_Name_102",
            api_c.DATAFEED_DATA_SOURCE: db_c.DELIVERY_PLATFORM_FACEBOOK,
            api_c.DATAFEED_NEW_IDS_COUNT: 300,
            api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 3012,
            api_c.MATCH_RATE: 0.98,
            api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow()
            - datetime.timedelta(days=7),
        },
        {
            api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4ff",
            api_c.DATAFEED_NAME: "Really_long_Feed_Name_100",
            api_c.DATAFEED_DATA_SOURCE: db_c.DELIVERY_PLATFORM_SFMC,
            api_c.DATAFEED_NEW_IDS_COUNT: 612,
            api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 2045,
            api_c.MATCH_RATE: 0.98,
            api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow()
            - datetime.timedelta(days=30),
        },
    ]

    return response


def clean_cdm_fields(body: dict) -> dict:
    """Clean and map any CDM fields date types.

    Args:
        body (dict): cdm response body dict.

    Returns:
        dict: dictionary of cleaned cdm body.

    """
    for date_field in DATETIME_FIELDS:
        if date_field not in body:
            continue
        if isinstance(body[date_field], datetime.datetime):
            continue
        try:
            # ignoretz this to make it naive format for uniformity
            body[date_field] = parse(body[date_field], ignoretz=True)
        except (ParserError, TypeError):
            body[date_field] = DEFAULT_DATETIME
    return body
