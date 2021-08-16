"""
Purpose of this file is for holding methods to query and pull data from CDP.
"""
import datetime
import time
import asyncio
import math
from typing import Tuple, Optional
from random import randint

import requests
import aiohttp
import async_timeout
from bson import ObjectId
from dateutil.parser import parse, ParserError

from huxunifylib.database import constants as db_c
from huxunifylib.util.general.logging import logger

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
        logger.error("CDM Health Check failed with %s.", repr(exception))
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
    logger.info("Getting Customer Profiles info from CDP API.")
    response = requests.get(
        f"{config.CDP_SERVICE}/customer-profiles?limit={batch_size}&offset={offset}",
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Unable to get Customer Profiles from CDP API got %s.",
            response.status_code,
        )
        return {}

    response_data = response.json()[api_c.BODY]
    logger.info("Successfully retrieved Customer Profiles info from CDP API.")
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
    logger.info("Getting Customer Profile info for %s from CDP API.", hux_id)
    response = requests.get(
        f"{config.CDP_SERVICE}/customer-profiles/{hux_id}",
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Unable to get Customer Profile info for %s from CDP API got %s.",
            hux_id,
            response.status_code,
        )
        return {}

    logger.info(
        "Successfully retrieved Customer Profile info for %s from CDP API.",
        hux_id,
    )
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
    logger.info("Getting Customer Profile Insights from CDP API.")
    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights",
        json=filters if filters else api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER,
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Could not get customer profile insights from CDP API got %s %s.",
            response.status_code,
            response.text,
        )
        return {}
    logger.info(
        "Successfully retrieved Customer Profile Insights from CDP API."
    )
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
    logger.info(
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
                logger.error(
                    "CDM post request failed for audience id %s.", audience_id
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


def generate_idr_matching_trends_distribution(
    number_of_points: int,
    min_point: int = 5,
    max_point: int = 9,
    lambda_: float = 0.5,
    multiplier: int = 1,
):
    """Generates normalized exponential data with randomness
    Args:
        number_of_points (int): Number of points to generate
        min_point (int): Maximum value in data.
        max_point (int): Minimum value in data.
        lambda_ (float): Value to control rise of exponent
        multiplier (int): 1 represent increasing exponential data, -1 for decreasing
    Returns:
        list: Generated exponential data

    """
    # TODO: Remove after CDM API for IDR matching trends is available

    data = [
        multiplier * math.e ** (x * lambda_ / number_of_points)
        for x in range(0, number_of_points)
    ]
    return add_randomness(
        normalize_values(
            data, max_range_val=max_point, min_range_val=min_point
        )
    )


def normalize_values(
    values: list, max_range_val: int = 1, min_range_val: int = 0
):
    """Normalizes values in a list to be in the given range
    Args:
        values (list): Values to be normalized.
        max_range_val (int): Maximum value in range.
        min_range_val (int): Minimum value in range.

    Returns:
        list: Normalized values.
    """
    # TODO: Remove after CDM API for IDR matching trends is available

    min_val = min(values)
    max_val = max(values)
    return [
        int(
            ((x - min_val) / (max_val - min_val))
            * (max_range_val - min_range_val)
        )
        + min_range_val
        for x in values
    ]


def add_randomness(values: list, variation_percentage: float = 0.005):
    """Adds random numbers to a list of values
    Args:
        values (list): List of values which needs randomness
        variation_percentage (float): Variation percentage which is added or subtracted from a value
    Returns:
        list: Values with randomness
    """
    # TODO: Remove after CDM API for IDR matching trends is available

    return [
        val
        + randint(
            -int(variation_percentage * val), int(variation_percentage * val)
        )
        for val in values
    ]


def get_idr_matching_trends(token: str) -> list:
    """Retrieves IDR matching trends data YTD
    Args:
        token (str): OKTA JWT Token.
    Returns:
       list: count of known, anonymous, unique ids on a day.
    """
    # TODO: Update after CDM API for IDR matching trends is available
    year_for_date = datetime.datetime.now().year
    start_date = datetime.datetime.fromisoformat(f"{year_for_date}-01-01")
    end_date = datetime.datetime.utcnow()
    diff_date = end_date - start_date
    num_points = diff_date.days

    days = [start_date + datetime.timedelta(days=i) for i in range(num_points)]

    # call customer-profile insights to get id counts
    customer_profile_info = get_customers_overview(token)
    known_ids_count = customer_profile_info.get(
        api_c.TOTAL_KNOWN_IDS, api_c.KNOWN_IDS_MAX_COUNT
    )

    unique_ids_count = customer_profile_info.get(
        api_c.TOTAL_UNIQUE_IDS, api_c.UNIQUE_HUX_IDS_MAX_COUNT
    )

    unknown_ids_count = customer_profile_info.get(
        api_c.TOTAL_UNKNOWN_IDS, api_c.ANONYMOUS_IDS_MIN_COUNT
    )

    known_ids = generate_idr_matching_trends_distribution(
        num_points,
        min_point=known_ids_count - (0.35 * known_ids_count),
        max_point=known_ids_count,
        lambda_=api_c.KNOWN_IDS_LAMBDA,
    )

    unique_hux_ids = generate_idr_matching_trends_distribution(
        num_points,
        min_point=unique_ids_count - (0.35 * known_ids_count),
        max_point=unique_ids_count,
        lambda_=api_c.UNIQUE_HUX_IDS_LAMBDA,
    )
    # setting multiplier to -1 to get exponentially decreasing values
    anonymous_ids = generate_idr_matching_trends_distribution(
        num_points,
        min_point=unknown_ids_count,
        max_point=unknown_ids_count + (0.35 * unknown_ids_count),
        lambda_=api_c.ANONYMOUS_IDS_LAMBDA,
        multiplier=-1,
    )

    return [
        {
            api_c.DATE: day,
            api_c.KNOWN_IDS: known_ids_count,
            api_c.UNIQUE_HUX_IDS: unique_hux_ids_count,
            api_c.ANONYMOUS_IDS: anonymous_ids_count,
        }
        for day, known_ids_count, unique_hux_ids_count, anonymous_ids_count in zip(
            days, known_ids, unique_hux_ids, anonymous_ids
        )
    ]


def get_customer_events_data(hux_id: str) -> list:
    """Get events for a customer grouped by date.

    Args:
        hux_id (str): hux id for a customer.
    Returns:
        list: customer events with respective counts
    """

    # pylint: disable=unused-argument
    # TODO: Remove pylint unused-argument and update after CDM API for customer events is available
    response = [
        {
            api_c.DATE: datetime.datetime.utcnow()
            - datetime.timedelta(days=x),
            api_c.CUSTOMER_TOTAL_DAILY_EVENT_COUNT: api_c.CUSTOMER_EVENTS_SAMPLE_COUNTS[
                api_c.CUSTOMER_TOTAL_DAILY_EVENT_COUNT
            ][
                x
            ],
            api_c.CUSTOMER_DAILY_EVENT_WISE_COUNT: {
                api_c.ABANDONED_CART_EVENT: api_c.CUSTOMER_EVENTS_SAMPLE_COUNTS[
                    api_c.ABANDONED_CART_EVENT
                ][
                    x
                ],
                api_c.CUSTOMER_LOGIN_EVENT: api_c.CUSTOMER_EVENTS_SAMPLE_COUNTS[
                    api_c.CUSTOMER_LOGIN_EVENT
                ][
                    x
                ],
                api_c.VIEWED_CART_EVENT: api_c.CUSTOMER_EVENTS_SAMPLE_COUNTS[
                    api_c.VIEWED_CART_EVENT
                ][x],
                api_c.VIEWED_CHECKOUT_EVENT: api_c.CUSTOMER_EVENTS_SAMPLE_COUNTS[
                    api_c.VIEWED_CHECKOUT_EVENT
                ][
                    x
                ],
                api_c.VIEWED_SALE_ITEM_EVENT: api_c.CUSTOMER_EVENTS_SAMPLE_COUNTS[
                    api_c.VIEWED_SALE_ITEM_EVENT
                ][
                    x
                ],
            },
        }
        for x in reversed(range(8))
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
            body[date_field] = None

    return body


def get_demographic_by_state(
    token: str, filters: Optional[dict] = None
) -> list:
    """
    Get demographic details of customers by state

    Args:
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into
            count_by_state endpoint, default None

    Returns:
        list of demographic details by state

    """
    # get config
    config = get_config()
    logger.info("Retrieving demographic insights by state.")
    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights/count-by-state",
        json=filters if filters else api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER,
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Failed to retrieve state demographic insights %s %s.",
            response.status_code,
            response.text,
        )
        return {}
    logger.info("Successfully retrieved state demographic insights.")
    body = clean_cdm_fields(response.json()[api_c.BODY])

    total_customers = sum([x[api_c.SIZE] for x in body])
    geographic_response = [
        {
            api_c.NAME: api_c.STATE_NAMES.get(x[api_c.STATE], x[api_c.STATE]),
            api_c.POPULATION_PERCENTAGE: round(
                x[api_c.SIZE] / total_customers, 4
            ),
            api_c.SIZE: x[api_c.SIZE],
            api_c.GENDER_WOMEN: round(
                x[api_c.GENDER_WOMEN] / x[api_c.SIZE], 4
            ),
            api_c.GENDER_MEN: round(x[api_c.GENDER_MEN] / x[api_c.SIZE], 4),
            api_c.GENDER_OTHER: round(
                x[api_c.GENDER_OTHER] / x[api_c.SIZE], 4
            ),
            api_c.LTV: x.get(api_c.LTV, 0),
        }
        for x in body
    ]
    return geographic_response
