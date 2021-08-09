"""
Purpose of this file is for holding methods to query and pull data from CDP.
"""
import datetime
import logging
import time
import asyncio
from typing import Tuple, Optional

import requests
import aiohttp
import async_timeout
from bson import ObjectId
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
            f"{config.CDP_SERVICE}/healthcheck",
            timeout=5,
        )
        return response.status_code, "CDM available."

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        return False, getattr(exception, "message", repr(exception))


def get_customer_profiles(token: str, batch_size: int, offset: int) -> dict:
    """Retrieves customer profiles.

    Args:
        batch_size (int): number of customer profiles to be returned in a batch
        offset (int): Offset for customer profiles
        token (str): OKTA JWT Token.

    Returns:
        dict: dictionary containing the customer profile information

    """

    # get config
    config = get_config()

    response = requests.get(
        f"{config.CDP_SERVICE}/customer-profiles?limit={batch_size}&offset={offset}",
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        return {}

    response_data = response.json()[api_c.BODY]
    return {
        api_c.TOTAL_CUSTOMERS: len(response_data),
        api_c.CUSTOMERS_TAG: response_data,
    }


def get_customer_profile(token: str, hux_id: str) -> dict:
    """Retrieves a customer profile.

    Args:
        token (str): OKTA JWT Token.
        hux_id (str): hux id for a customer.

    Returns:
        dict: dictionary containing the customer profile information

    """

    # get config
    config = get_config()

    response = requests.get(
        f"{config.CDP_SERVICE}/customer-profiles/{hux_id}",
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        return {}

    return clean_cdm_fields(response.json()[api_c.BODY])


def get_customers_overview(
    token: str,
    filters: Optional[dict] = None,
) -> dict:
    """Fetch customers overview data.

    Args:
        token (str): OKTA JWT Token.
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
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        return {}

    return clean_cdm_fields(response.json()[api_c.BODY])


def get_customers_count_async(
    token: str, audiences: list, default_size: int = 0
) -> dict:
    """Retrieves audience size asynchronously

    Args:
        token (str): OKTA JWT Token.
        audiences (list): list of audience docs.
        default_size (int): default size if the audience post fails. default is zero.

    Returns:
        dict: Audience ObjectId to Size mapping dict.

    """

    # get the audience count URL.
    url = f"{get_config().CDP_SERVICE}/customer-profiles/audience/count"

    # generate arg list for the async query
    task_args = [
        (
            token,
            x[db_c.ID],
            x[api_c.AUDIENCE_FILTERS]
            if x.get(api_c.AUDIENCE_FILTERS)
            else api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER,
            url,
        )
        for x in audiences
    ]

    # set the event loop
    asyncio.set_event_loop(asyncio.SelectorEventLoop())

    # start timer
    timer = time.perf_counter()

    # send all responses at once and wait until they are all done.
    responses = asyncio.get_event_loop().run_until_complete(
        asyncio.gather(*(get_async_customers(*x) for x in task_args))
    )

    # log execution time summary
    total_ticks = time.perf_counter() - timer
    logging.info(
        "Executed %s requests to the customer API in %0.4f seconds. ~%0.4f requests per second.",
        len(audiences),
        total_ticks,
        len(audiences) / total_ticks,
    )

    # create a dict for audience_id to get size
    audience_size_dict = {}

    # iterate each response.
    for response in responses:

        # get audience id from the response
        audience_id = ObjectId(response[1])

        # get the response dict
        response = response[0]

        # validate response code
        if response["code"] != 200 or api_c.BODY not in response:
            # invalid response set default
            audience_size_dict[audience_id] = default_size
            continue

        # set the total count, otherwise set the default size if not found
        audience_size_dict[audience_id] = response[api_c.BODY].get(
            api_c.TOTAL_COUNT, default_size
        )

    return audience_size_dict


async def get_async_customers(
    token: str, audience_id: ObjectId, audience_filters, url
) -> dict:
    """asynchronously process getting audience size

    Args:
        token (str): OKTA JWT Token.
        audience_id (ObjectId): audience id.
        audience_filters (dict): audience filters
        url (str): url of the service to call.

    Returns:
       dict: audience id to size mapping dict.
    """

    # setup the aiohttp session so we can process the calls asynchronously
    async with aiohttp.ClientSession() as session, async_timeout.timeout(10):
        # run the async post request
        async with session.post(
            url,
            json=audience_filters,
            headers={
                api_c.CUSTOMERS_API_HEADER_KEY: token,
            },
        ) as response:
            # await the responses, and return them as they come in.
            try:
                return await response.json(), str(audience_id)
            except aiohttp.client.ContentTypeError:
                logging.error(
                    "CDM post request failed for audience id %s", audience_id
                )
                return {"code": 500}, str(audience_id)


def get_idr_data_feeds() -> list:
    """
    Fetch IDR data feeds
    """
    # TODO: Update after CDM API for IDR data feeds is available
    response = [
        {
            api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fc",
            api_c.DATAFEED_NAME: "Really_long_Feed_Name_106",
            api_c.DATAFEED_DATA_SOURCE: db_c.CDP_DATA_SOURCE_BLUECORE,
            api_c.DATAFEED_NEW_IDS_COUNT: 21,
            api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 2023532,
            api_c.MATCH_RATE: 0.98,
            api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow(),
        },
        {
            api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fd",
            api_c.DATAFEED_NAME: "Really_long_Feed_Name_105",
            api_c.DATAFEED_DATA_SOURCE: db_c.CDP_DATA_SOURCE_BLUECORE,
            api_c.DATAFEED_NEW_IDS_COUNT: 54,
            api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 3232,
            api_c.MATCH_RATE: 0.97,
            api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow()
            - datetime.timedelta(days=1),
        },
        {
            api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4fe",
            api_c.DATAFEED_NAME: "Really_long_Feed_Name_102",
            api_c.DATAFEED_DATA_SOURCE: db_c.CDP_DATA_SOURCE_BLUECORE,
            api_c.DATAFEED_NEW_IDS_COUNT: 300,
            api_c.DATAFEED_RECORDS_PROCESSED_COUNT: 3012,
            api_c.MATCH_RATE: 0.98,
            api_c.DATAFEED_LAST_RUN_DATE: datetime.datetime.utcnow()
            - datetime.timedelta(days=7),
        },
        {
            api_c.DATAFEED_ID: "60e87d6d70815aade4d6c4ff",
            api_c.DATAFEED_NAME: "Really_long_Feed_Name_100",
            api_c.DATAFEED_DATA_SOURCE: db_c.CDP_DATA_SOURCE_BLUECORE,
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
