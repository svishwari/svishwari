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
            {api_c.AUDIENCE_FILTERS: x[api_c.AUDIENCE_FILTERS]}
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


def fill_empty_customer_events(
    start_date: datetime, end_date: datetime
) -> list:
    """Fill empty events for dates between start_date and end_date

    Args:
        start_date(datetime): start date between which dates, events need to be filled
        end_date (datetime): end date between which dates, events need to be filled
    Returns:
        list: customer events with zero
    """
    return [
        {
            api_c.DATE: start_date + datetime.timedelta(days=i),
            api_c.CUSTOMER_TOTAL_DAILY_EVENT_COUNT: 0,
            api_c.CUSTOMER_DAILY_EVENT_WISE_COUNT: {
                api_c.ABANDONED_CART_EVENT: 0,
                api_c.CUSTOMER_LOGIN_EVENT: 0,
                api_c.VIEWED_CART_EVENT: 0,
                api_c.VIEWED_CHECKOUT_EVENT: 0,
                api_c.VIEWED_SALE_ITEM_EVENT: 0,
                api_c.ITEM_PURCHASED_EVENT: 0,
                api_c.TRAIT_COMPUTED_EVENT: 0,
            },
        }
        for i in range(1, (end_date - start_date).days)
    ]


def get_customer_events_data(
    token: str, hux_id: str, filters: Optional[dict] = None
) -> list:
    """Get events for a customer grouped by date.

    Args:
        token (str): OKTA JWT Token.
        hux_id (str): hux id for a customer.
        filters (Optional[dict]): filters to pass into
            customer events endpoint.
    Returns:
        list: customer events with respective counts
    """

    config = get_config()

    # YTD by default
    default_filter = {
        api_c.START_DATE: "%s-01-01T00:00:00Z"
        % datetime.datetime.utcnow().year,
        api_c.END_DATE: datetime.datetime.utcnow().strftime("%Y-%m-%d")
        + "T00:00:00Z",
    }

    filters = filters if filters else default_filter

    logger.info("Getting customer events info from CDP API.")
    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/{hux_id}/events",
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
        json=filters,
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Unable to get Customer Profiles from CDP API got %s.",
            response.status_code,
        )
        return {}

    customer_events = response.json().get(api_c.BODY)

    prev_date = parse(filters.get(api_c.START_DATE))
    end_date = parse(filters.get(api_c.END_DATE))

    # no customer events found in the date range, return empty
    if not customer_events:
        return []

    customer_events_dates_filled = []

    # fill empty events so that no date(day) is missing
    for idx, customer_event in enumerate(customer_events):
        curr_date = parse(customer_event.get(api_c.DATE))
        # fill for 1 day previous
        if idx == 0:
            if curr_date > prev_date and (curr_date - prev_date).days >= 1:
                customer_events_dates_filled = (
                    customer_events_dates_filled
                    + fill_empty_customer_events(
                        prev_date - datetime.timedelta(1),
                        prev_date + datetime.timedelta(1),
                    )
                )

        customer_event[api_c.DATE] = curr_date
        customer_events_dates_filled.append(customer_event)

        if curr_date > prev_date and (curr_date - prev_date).days > 1:
            customer_events_dates_filled = (
                customer_events_dates_filled
                + fill_empty_customer_events(prev_date, curr_date)
            )
        prev_date = curr_date

    if end_date > prev_date and (end_date - prev_date).days > 1:
        customer_events_dates_filled = (
            customer_events_dates_filled
            + fill_empty_customer_events(prev_date, end_date)
        )

    customer_events_dates_filled.sort(
        key=lambda customer_event_: customer_event_.get("date")
    )

    return customer_events_dates_filled


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


def get_spending_by_cities(token: str, filters: Optional[dict] = None) -> dict:
    """Get spending details of customer by cities

    Args:
        token (str): OKTA JWT Token.
        filters (Optional[dict]): filters to pass into
            customers_overview endpoint.

    Returns:
        dict of income details of customers by cities

    """
    city_income_default_filter = api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER
    city_income_default_filter[api_c.COUNT] = 5

    # get config
    config = get_config()
    logger.info("Retrieving customer income details by cities from CDP API.")
    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights/city-ltvs",
        json=filters if filters else city_income_default_filter,
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Could not get customer income details by state from CDP API got %s %s.",
            response.status_code,
            response.text,
        )
        return {}
    logger.info(
        "Successfully retrieved customer income details by state from CDP API."
    )

    return [
        {api_c.NAME: x[api_c.CITY], api_c.LTV: round(x["avg_ltv"], 4)}
        for x in clean_cdm_fields(response.json()[api_c.BODY])
    ]
