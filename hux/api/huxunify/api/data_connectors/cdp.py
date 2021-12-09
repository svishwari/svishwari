"""Purpose of this file is for holding methods to query and pull data from CDP.
"""
# pylint:disable=too-many-lines
import time
import asyncio
import random
from collections import defaultdict
from typing import Tuple, Optional, List
from datetime import datetime

import requests
import aiohttp
import async_timeout
from aiohttp import ClientSession
from bson import ObjectId
from dateutil.parser import parse, ParserError
from dateutil.relativedelta import relativedelta

from huxunifylib.database import constants as db_c
from huxunifylib.util.general.logging import logger

from huxunify.api.config import get_config
from huxunify.api.exceptions import integration_api_exceptions as iae
from huxunify.api import constants as api_c
from huxunify.api.prometheus import record_health_status_metric

# fields to convert to datetime from the responses
DEFAULT_DATETIME = datetime(1, 1, 1, 1, 00)
DATETIME_FIELDS = [
    "since",
    "last_click",
    "last_purchase",
    "last_email_open",
    "updated",
    api_c.DAY,
    api_c.PINNING_TIMESTAMP,
    api_c.STITCHED_TIMESTAMP,
    api_c.TIMESTAMP,
]


def check_cdm_api_connection() -> Tuple[bool, str]:
    """Validate the cdm api connection.

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
        record_health_status_metric(api_c.CDM_API_CONNECTION_HEALTH, True)
        return response.status_code, "CDM available."

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        logger.error("CDM Health Check failed with %s.", repr(exception))
        record_health_status_metric(api_c.CDM_API_CONNECTION_HEALTH, False)
        return False, getattr(exception, "message", repr(exception))


def get_customer_profiles(token: str, batch_size: int, offset: int) -> dict:
    """Retrieves customer profiles.

    Args:
        batch_size (int): number of customer profiles to be returned in a
            batch.
        offset (int): Offset for customer profiles.
        token (str): OKTA JWT Token.

    Returns:
        dict: dictionary containing the customer profile information.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
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
            "Unable to retrieve Customer Profiles, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_SERVICE}/customer-profiles?limit={batch_size}&offset={offset}",
            response.status_code,
        )

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
        dict: dictionary containing the customer profile information.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
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
            "Unable to retrieve Customer Profile info for %s, %s %s.",
            hux_id,
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_SERVICE}/customer-profiles/{hux_id}",
            response.status_code,
        )

    logger.info(
        "Successfully retrieved Customer Profile info for %s from CDP API.",
        hux_id,
    )
    return clean_cdm_fields(response.json()[api_c.BODY])


# pylint: disable=unused-argument
def get_idr_overview(
    token: str, start_date: str = None, end_date: str = None
) -> dict:
    """Fetch IDR overview data.

    Args:
        token (str): OKTA JWT Token.
        start_date (str): Start date.
        end_date (str): End date.

    Returns:
        dict: dictionary of overview data.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # TODO : Update to use idr insights api, with start/end date as query params.
    # get config
    config = get_config()
    logger.info("Getting IDR Insights from CDP API.")
    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights",
        json=api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER,
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Unable to retrieve customer profile insights, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_SERVICE}/customer-profiles/insights",
            response.status_code,
        )

    logger.info(
        "Successfully retrieved Customer Profile Insights from CDP API."
    )

    return clean_cdm_fields(response.json()[api_c.BODY])


def get_customers_overview(
    token: str,
    filters: Optional[dict] = None,
) -> dict:
    """Fetch customers overview data.

    Args:
        token (str): OKTA JWT Token.
        filters (Optional[dict]): filters to pass into customers_overview
            endpoint, default None.

    Returns:
        dict: dictionary of overview data.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
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
            "Unable to retrieve profile insights, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_SERVICE}/customer-profiles/insights",
            response.status_code,
        )

    logger.info(
        "Successfully retrieved Customer Profile Insights from CDP API."
    )

    # clean up cdm date fields in the response
    response_body = clean_cdm_fields(response.json()[api_c.BODY])

    # clean up the cdm gender fields in the response
    return clean_cdm_gender_fields(response_body)


def get_customers_count_async(
    token: str, audiences: list, default_size: int = 0
) -> dict:
    """Retrieves audience size asynchronously.

    Args:
        token (str): OKTA JWT Token.
        audiences (list): list of audience docs.
        default_size (int): default size if the audience post fails, default
            is zero.

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
    """Asynchronously process getting audience size.

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


def fill_empty_customer_events(
    start_date: datetime, end_date: datetime, time_diff: dict
) -> list:
    """Fill empty events for dates between start_date and end_date.

    Args:
        start_date (datetime): Start date between which dates, events need to
            be filled.
        end_date (datetime): End date between which dates, events need to
            be filled.
        time_diff (dict): Time difference on which data needs to be added

    Returns:
        list: Customer events with zero.
    """

    missing_data = []
    skip = {k: 1 for k in time_diff.keys()}
    curr_date = start_date + relativedelta(**skip)

    while curr_date.date() < end_date.date():
        missing_data.append(
            {
                api_c.DATE: curr_date,
                api_c.CUSTOMER_TOTAL_DAILY_EVENT_COUNT: 0,
                api_c.CUSTOMER_DAILY_EVENT_WISE_COUNT: {
                    api_c.VIEWED_CHECKOUT_EVENT: 0,
                    api_c.ABANDONED_CARTS: 0,
                    api_c.TRAITS_ANALYZED: 0,
                    api_c.SALES_MADE: 0,
                    api_c.CONTENT_VIEWED: 0,
                    api_c.PRODUCTS_SEARCHED: 0,
                    api_c.PURCHASES_MADE: 0,
                },
            }
        )
        curr_date += relativedelta(**skip)

    return missing_data


def fill_customer_events_missing_dates(
    customer_events: list,
    start_date: datetime,
    end_date: datetime,
    interval: str = "day",
) -> list:
    """Get events for a customer grouped by date.

    Args:
        customer_events (list): Customer events in CDM API body.
        start_date (datetime): Start date in filter.
        end_date (datetime): End date in filter.
        interval (str): Interval which the event data will be aggregated,
            default to "day"

    Returns:
        list: Customer events including zeros for missing dates.
    """

    # if interval == "day":
    prev_date = start_date
    time_diff = {"days": 1}

    if interval == "week":
        prev_date = start_date - relativedelta(
            days=(start_date.isoweekday() - 1)
        )
        time_diff = {"weeks": 1}
    elif interval == "month":
        prev_date = start_date - relativedelta(days=(start_date.day - 1))
        time_diff = {"months": 1}

    customer_events_dates_filled = []
    # fill empty events so that no date(day) is missing
    for idx, customer_event in enumerate(customer_events):
        curr_date = parse(customer_event.get(api_c.DATE))
        # fill for 1 day previous
        if idx == 0:
            if (
                curr_date.date() > prev_date.date()
            ):  # curr_date > prev_date and (curr_date - prev_date).days >= 1:
                customer_events_dates_filled = (
                    customer_events_dates_filled
                    + fill_empty_customer_events(
                        prev_date - relativedelta(**time_diff),
                        prev_date + relativedelta(**time_diff),
                        time_diff,
                    )
                )

        customer_event[api_c.DATE] = curr_date
        customer_events_dates_filled.append(customer_event)

        if (
            curr_date.date() > prev_date.date()
        ):  # and (curr_date - prev_date).days > 1:
            data_to_fill = fill_empty_customer_events(
                prev_date, curr_date, time_diff
            )
            customer_events_dates_filled = (
                customer_events_dates_filled + data_to_fill
            )
        prev_date = curr_date

    if (
        end_date.date() > prev_date.date()
    ):  # and (end_date - prev_date).days >= 1:
        customer_events_dates_filled = (
            customer_events_dates_filled
            + fill_empty_customer_events(
                prev_date, end_date + relativedelta(**time_diff), time_diff
            )
        )

    customer_events_dates_filled.sort(
        key=lambda customer_event_: customer_event_.get("date")
    )
    return customer_events_dates_filled


def get_customer_events_data(
    token: str,
    hux_id: str,
    start_date_str: str,
    end_date_str: str,
    interval: str,
) -> list:
    """Get events for a customer grouped by date.

    Args:
        token (str): OKTA JWT Token.
        hux_id (str): hux id for a customer.
        start_date_str (str): Start date string for sql query.
        end_date_str (str): End date string for sql query.
        interval (str): Interval i.e. day/week/month

    Returns:
        list: Customer events with respective counts.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    config = get_config()

    logger.info("Getting customer events info from CDP API.")
    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/{hux_id}/events",
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
        json={
            api_c.START_DATE: start_date_str,
            api_c.END_DATE: end_date_str,
            api_c.INTERVAL: interval,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Unable to retrieve Customer Profiles, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_SERVICE}/customer-profiles/{hux_id}/events",
            response.status_code,
        )

    customer_events = response.json().get(api_c.BODY)

    # no customer events found in the date range, return empty
    if not customer_events:
        return []

    return fill_customer_events_missing_dates(
        customer_events,
        parse(start_date_str + "T00:00:00Z"),
        parse(end_date_str + "T00:00:00Z"),
        interval,
    )


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
        if isinstance(body[date_field], datetime):
            continue
        try:
            # ignoretz this to make it naive format for uniformity
            body[date_field] = parse(body[date_field], ignoretz=True)
        except (ParserError, TypeError):
            body[date_field] = None

    return body


def get_spending_by_cities(token: str, filters: Optional[dict] = None) -> list:
    """Get spending details of customer by cities.

    Args:
        token (str): OKTA JWT Token.
        filters (Optional[dict]): filters to pass into customers_overview
            endpoint.

    Returns:
        list: list of income details of customers by cities.
    """

    return [
        {api_c.NAME: x[api_c.CITY], api_c.LTV: round(x["avg_ltv"], 4)}
        for x in get_city_ltvs(token, filters=filters)
    ]


def get_customer_count_by_state(
    token: str, filters: Optional[dict] = None
) -> list:
    """Get demographic details of customers by state.

    Args:
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into count_by_state endpoint,
            default None.

    Returns:
        list: list of state demographic data.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()
    logger.info("Retrieving demographic insights by state.")
    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights/count-by-state",
        json=filters if filters else {},
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
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_SERVICE}/customer-profiles/insights/count-by-state",
            response.status_code,
        )

    logger.info("Successfully retrieved state demographic insights.")

    return response.json()[api_c.BODY]


def get_demographic_by_state(
    token: str, filters: Optional[dict] = None
) -> list:
    """Get demographic details of customers by state.

    Args:
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into count_by_state endpoint,
            default None.

    Returns:
        list: list of demographic details by state.
    """

    filters = (
        {api_c.AUDIENCE_FILTERS: filters}
        if filters
        else api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER
    )

    return get_geographic_customers_data(
        get_customer_count_by_state(token, filters)
    )


# pylint: disable=unused-argument
def get_demographic_by_country(
    token: str, filters: Optional[dict] = None
) -> list:
    """Get demographic details of customers by country.

    Args:
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into count_by_state endpoint,
            default None.

    Returns:
        list: list of demographic details by country.
    """

    customer_count_by_state = get_customer_count_by_state(
        token=token,
        filters=filters if filters else api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER,
    )
    # start timer
    timer = time.perf_counter()
    # group customer count data by country
    data_by_country = defaultdict(list)
    customer_insights_by_country = []
    for item in customer_count_by_state:
        data_by_country[item["country"]].append(item)

    for country, country_items in data_by_country.items():
        total_customer_count = sum(map(lambda x: x["size"], country_items))
        avg_ltv = (
            sum(map(lambda x: x["avg_ltv"] * x["size"], country_items))
            / total_customer_count
            if country_items
            else None
        )
        customer_insights_by_country.append(
            {
                "name": country,
                "avg_ltv": avg_ltv,
                "size": total_customer_count,
                "country_label": api_c.COUNTRIES_LIST.get(country, " "),
            }
        )
    # log execution time summary
    total_ticks = time.perf_counter() - timer
    logger.info(
        "Grouped customer count data by country in %0.4f seconds.", total_ticks
    )

    return customer_insights_by_country


def get_customers_insights_count_by_day(
    token: str, date_filters: dict
) -> dict:
    """Fetch customer insights count by day data.

    Args:
        token (str): OKTA JWT Token.
        date_filters (dict): filters to pass into customer insights count by
            day endpoint.

    Returns:
        dict: dictionary of customer count data.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()

    logger.info("Attempting to get customer insights count by day from CDP.")

    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights/count-by-day",
        json=date_filters,
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Unable to retrieve customer insights count by day data, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_SERVICE}/customer-profiles/insights/count-by-day",
            response.status_code,
        )

    logger.info(
        "Successfully retrieved customer insights count by day data from "
        "CDP API."
    )

    response_body = response.json()[api_c.BODY]

    for record in response_body:
        try:
            record[api_c.RECORDED] = parse(record[api_c.RECORDED])
        except (ParserError, TypeError):
            record[api_c.RECORDED] = None

    return add_missing_customer_count_by_day(response_body, date_filters)


def get_city_ltvs(
    token: str,
    filters: Optional[dict] = None,
    offset: int = 0,
    limit: int = api_c.DEFAULT_BATCH_SIZE,
) -> list:
    """Get spending details of customers by city.

    Args:
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into city_ltvs endpoint.
        offset (int): offset.
        limit (int): limit.

    Returns:
        list: list of spending details by cities.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()
    logger.info("Retrieving spending insights by city.")
    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights/city-ltvs",
        json=filters if filters else {},
        params=dict(offset=offset, limit=limit),
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Failed to retrieve city-level spending insights, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_SERVICE}/customer-profiles/insights/city-ltvs",
            response.status_code,
        )

    logger.info("Successfully retrieved city-level demographic insights.")

    return get_customer_insights_by_cities(
        [clean_cdm_fields(data) for data in response.json()[api_c.BODY]]
    )


def get_customer_insights_by_cities(customer_insights_by_cities: list) -> list:
    """Get customer insights by cities

    Args:
        customer_insights_by_cities (list): List of customer insights

    Returns:
        list: Formatted List of customer insights

    """
    return [
        {
            api_c.CITY: x[api_c.CITY],
            api_c.STATE: x[api_c.STATE],
            api_c.STATE_LABEL: api_c.STATE_NAMES.get(x[api_c.STATE]),
            api_c.COUNTRY: x[api_c.COUNTRY],
            api_c.COUNTRY_LABEL: api_c.COUNTRIES_LIST.get(x[api_c.COUNTRY]),
            api_c.AVG_LTV: x[api_c.AVG_LTV],
            api_c.CUSTOMER_COUNT: x[api_c.CUSTOMER_COUNT],
        }
        for x in customer_insights_by_cities
    ]


def clean_cdm_gender_fields(response_body: dict) -> dict:
    """Clean and map CDM gender count and average fields appropriately.

    Args:
        response_body (dict): cdm response body dict.

    Returns:
        dict: dictionary of cleaned cdm response body.
    """

    gender_fields = [
        (api_c.GENDER_MEN, api_c.GENDER_MEN_COUNT),
        (api_c.GENDER_WOMEN, api_c.GENDER_WOMEN_COUNT),
        (api_c.GENDER_OTHER, api_c.GENDER_OTHER_COUNT),
    ]

    # add each individual gender count from the response body into total_count
    total_count = sum(
        [response_body.get(gender[0]) or 0 for gender in gender_fields]
    )

    # set the count values and the calculated individual gender average against
    # appropriate fields in the response body for each individual gender
    for gender_type, gender_type_count in gender_fields:
        response_body[gender_type_count] = response_body[gender_type]
        response_body[gender_type] = (
            round(response_body[gender_type_count] / total_count, 4)
            if total_count > 0
            else 0
        )

    return response_body


def get_geographic_customers_data(customer_count_by_state: list) -> list:
    """Aggregate customers data by states

    Args:
        customer_count_by_state (list): List of customer count data by state

    Returns:
        list: list of geographically aggregated data
    """
    return [
        {
            api_c.COUNTRY: x[api_c.COUNTRY],
            api_c.COUNTRY_LABEL: api_c.COUNTRIES_LIST.get(x[api_c.COUNTRY]),
            api_c.STATE: x[api_c.STATE],
            api_c.NAME: api_c.STATE_NAMES.get(x[api_c.STATE], x[api_c.STATE]),
            api_c.POPULATION_PERCENTAGE: round(
                x[api_c.SIZE]
                / sum([x[api_c.SIZE] for x in customer_count_by_state]),
                4,
            )
            if sum([x[api_c.SIZE] for x in customer_count_by_state]) != 0
            else 0,
            api_c.SIZE: x[api_c.SIZE],
            api_c.GENDER_WOMEN: round(x[api_c.GENDER_WOMEN] / x[api_c.SIZE], 4)
            if x[api_c.SIZE] != 0
            else 0,
            api_c.GENDER_MEN: round(x[api_c.GENDER_MEN] / x[api_c.SIZE], 4)
            if x[api_c.SIZE] != 0
            else 0,
            api_c.GENDER_OTHER: round(x[api_c.GENDER_OTHER] / x[api_c.SIZE], 4)
            if x[api_c.SIZE] != 0
            else 0,
            api_c.AVG_LTV: round(x.get(api_c.AVG_LTV, 0), 4),
            api_c.MIN_LTV: round(x.get(api_c.MIN_LTV, 0), 4),
            api_c.MAX_LTV: round(x.get(api_c.MAX_LTV, 0), 4),
            api_c.MIN_AGE: x.get(api_c.MIN_AGE, 0),
            api_c.MAX_AGE: x.get(api_c.MAX_AGE, 0),
        }
        for x in customer_count_by_state
    ]


def get_spending_by_gender(
    token: str,
    start_date: str,
    end_date: str,
    filters: Optional[dict] = None,
) -> List[Optional[dict]]:
    """Get spending details of customer by gender.

    Args:
        token (str): OKTA JWT Token.
        start_date (str): String value of start date.
        end_date (str): String value of end date.
        filters (dict):  filters to pass into spending-by-month endpoint.

    Returns:
        list: list of spending details by gender.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    request_payload = (
        filters if filters else api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER
    )
    request_payload[api_c.START_DATE] = start_date
    request_payload[api_c.END_DATE] = end_date

    # get config
    config = get_config()
    logger.info("Retrieving spending insights by gender.")
    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
        json=request_payload,
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )

    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Failed to retrieve state demographic insights, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
            response.status_code,
        )

    logger.info("Successfully retrieved state demographic insights.")
    return sorted(
        clean_cdm_fields(response.json()[api_c.BODY]),
        key=lambda x: (x[api_c.YEAR], x[api_c.MONTH]),
    )


def get_revenue_by_day(
    token: str,
    start_date: str,
    end_date: str,
    filters: Optional[dict] = None,
) -> List[Optional[dict]]:
    """Get revenue details of customer.

    Args:
        token (str): OKTA JWT Token.
        start_date (str): String value of start date.
        end_date (str): String value of end date.
        filters (dict):  filters to pass into spending-by-month endpoint.

    Returns:
        list: list of spending details by gender.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    request_payload = (
        filters if filters else api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER
    )
    request_payload[api_c.START_DATE] = start_date
    request_payload[api_c.END_DATE] = end_date

    # get config
    config = get_config()
    logger.info("Retrieving spending by month.")

    # TODO: Update the API call to CDM with correct endpoint when available
    response = requests.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
        json=request_payload,
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    )
    if response.status_code != 200 or api_c.BODY not in response.json():
        logger.error(
            "Failed to retrieve spending insights by month, %s %s.",
            response.status_code,
            response.text,
        )
        raise iae.FailedAPIDependencyError(
            f"{config.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
            response.status_code,
        )

    logger.info("Successfully retrieved spending insights by month.")
    spending_by_month = sorted(
        clean_cdm_fields(response.json()[api_c.BODY]),
        key=lambda x: (x[api_c.YEAR], x[api_c.MONTH]),
    )

    spending_by_day = []

    for i, month_data in enumerate(spending_by_month):
        spending_by_day.append(
            {
                api_c.DATE: datetime(
                    year=month_data[api_c.YEAR],
                    month=month_data[api_c.MONTH],
                    day=int(
                        datetime.strptime(
                            start_date, api_c.DEFAULT_DATE_FORMAT
                        ).day
                    )
                    if i == 0
                    else 1,
                ),
                api_c.LTV: (
                    (
                        month_data[api_c.AVG_SPENT_MEN]
                        * month_data[api_c.GENDER_MEN]
                    )
                    + (
                        month_data[api_c.AVG_SPENT_WOMEN]
                        * month_data[api_c.GENDER_WOMEN]
                    )
                    + (
                        month_data[api_c.AVG_SPENT_OTHER]
                        * month_data[api_c.GENDER_OTHER]
                    )
                )
                / (
                    month_data[api_c.GENDER_MEN]
                    + month_data[api_c.GENDER_WOMEN]
                    + month_data[api_c.GENDER_OTHER]
                ),
            }
        )
        spending_by_day[-1][api_c.REVENUE] = round(
            (spending_by_day[-1][api_c.LTV] * random.choice([0.8, 1.0, 1.2])),
            2,
        )

    return add_missing_revenue_data_by_day(
        spending_by_day, start_date, end_date
    )


def add_missing_revenue_data_by_day(
    spending_by_day: list, start_date: str, end_date: str
) -> list:
    """Add revenue data for missing dates.

    Args:
        spending_by_day (list): list of revenue data.
        start_date (dict): start_date from which revenue data is being fetched
        end_date (dict): end_date to which revenue data is being fetched

    Returns:
        list: list of revenue data for all days from start_date to end_date
    """
    revenue_data_by_day = []

    start_date = datetime.strptime(start_date, api_c.DEFAULT_DATE_FORMAT)
    end_date = datetime.strptime(end_date, api_c.DEFAULT_DATE_FORMAT)
    # TODO remove stub when data is returned from CDP.
    sample_ltv = sample_revenue = 27

    for num_day in range(int((end_date - start_date).days) + 1):
        current_date = start_date + relativedelta(days=num_day)

        if spending_by_day and current_date == spending_by_day[0].get(
            api_c.DATE
        ):
            revenue_data_by_day.append(spending_by_day.pop(0))
        else:
            revenue_data_by_day.append(
                {
                    api_c.DATE: current_date,
                    api_c.LTV: sample_ltv
                    + (sample_ltv * random.uniform(-0.2, 0.3)),
                    api_c.REVENUE: sample_revenue
                    + (sample_revenue * random.uniform(-0.2, 0.3)),
                }
            )
    return revenue_data_by_day


def add_missing_customer_count_by_day(
    response_body: list, date_filters: dict
) -> list:
    """Add customer data for missing dates.

    Args:
        response_body (list): list of customer count data.
        date_filters (dict): start_date and end_date for which customer data
            is being fetched.

    Returns:
        customer_data_by_day (list): customer count data for all days within
            start_date and end_date.
    """

    customer_data_by_day = []

    start_date = datetime.strptime(
        date_filters[api_c.START_DATE], api_c.DEFAULT_DATE_FORMAT
    )
    end_date = datetime.strptime(
        date_filters[api_c.END_DATE], api_c.DEFAULT_DATE_FORMAT
    )

    for num_day in range(int((end_date - start_date).days) + 1):
        current_date = start_date + relativedelta(days=num_day)

        if response_body and current_date == response_body[0].get(
            api_c.RECORDED
        ):
            customer_data_by_day.append(response_body.pop(0))
        else:
            customer_data_by_day.append(
                {
                    api_c.RECORDED: current_date,
                    api_c.TOTAL_COUNT: response_body[0].get(api_c.TOTAL_COUNT)
                    - response_body[0].get(api_c.DIFFERENCE_COUNT)
                    if response_body
                    else customer_data_by_day[-1][api_c.TOTAL_COUNT],
                }
            )
        # TODO: Fetch this data from CDP once it is ready
        customer_data_by_day[-1][api_c.CUSTOMERS_LEFT] = random.randint(
            -57000, 0
        )
    return customer_data_by_day


async def get_customer_count_by_state_async(
    session: ClientSession, token: str, filters: Optional[dict] = None
) -> list:
    """Get demographic details of customers by state.

    Args:
        session (ClientSession): Async IO http client session.
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into count_by_state endpoint,
            default None.

    Returns:
        list: list of state demographic data.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()
    logger.info("Retrieving demographic insights by state.")
    # run the async post request
    async with session.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights/count-by-state",
        json=filters if filters else {},
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    ) as response:
        response_body = await response.json()
        if response.status != 200 or api_c.BODY not in response_body:
            logger.error(
                "Failed to retrieve state demographic insights %s %s.",
                response.status,
                response.text,
            )
            raise iae.FailedAPIDependencyError(
                f"{config.CDP_SERVICE}/customer-profiles/insights/count-by-state",
                response.status,
            )

        logger.info("Successfully retrieved state demographic insights.")

        return response_body[api_c.BODY]


async def get_demographic_by_state_async(
    session: ClientSession, token: str, filters: dict
) -> list:
    """Get demographic details of customers by state.

    Args:
        session (ClientSession): Async IO http client session.
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into count_by_state endpoint.

    Returns:
        list: list of demographic details by state.
    """
    return get_geographic_customers_data(
        await get_customer_count_by_state_async(session, token, filters)
    )


async def get_city_ltvs_async(
    session: ClientSession,
    token: str,
    filters: dict,
    offset: int = 0,
    limit: int = api_c.DEFAULT_BATCH_SIZE,
) -> list:
    """Get spending details of customers by city.

    Args:
        session (ClientSession): Async IO http client session.
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into city_ltvs endpoint.
        offset (int): offset.
        limit (int): limit.

    Returns:
        list: list of spending details by cities.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()
    logger.info("Retrieving spending insights by city.")
    # run the async post request
    async with session.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights/city-ltvs",
        json=filters,
        params=dict(offset=offset, limit=limit),
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    ) as response:
        response_body = await response.json()
        if response.status != 200 or api_c.BODY not in response_body:
            logger.error(
                "Failed to retrieve city-level spending insights, %s %s.",
                response.status,
                response.text,
            )
            raise iae.FailedAPIDependencyError(
                f"{config.CDP_SERVICE}/customer-profiles/insights/city-ltvs",
                response.status,
            )

        logger.info("Successfully retrieved city-level demographic insights.")

        return [clean_cdm_fields(data) for data in response_body[api_c.BODY]]


async def get_spending_by_gender_async(
    session: ClientSession,
    token: str,
    start_date: str,
    end_date: str,
    filters: dict,
) -> List[Optional[dict]]:
    """Get spending details of customer by gender.

    Args:
        session (ClientSession): Async IO http client session.
        token (str): OKTA JWT Token.
        start_date (str): String value of start date.
        end_date (str): String value of end date.
        filters (dict):  filters to pass into spending-by-month endpoint.

    Returns:
        list: list of spending details by gender.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    request_payload = filters
    request_payload[api_c.START_DATE] = start_date
    request_payload[api_c.END_DATE] = end_date

    # get config
    config = get_config()
    logger.info("Retrieving spending insights by gender.")
    # run the async post request
    async with session.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
        json=request_payload,
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    ) as response:
        response_body = await response.json()
        if response.status != 200 or api_c.BODY not in response_body:
            logger.error(
                "Failed to retrieve state demographic insights, %s %s.",
                response.status,
                response.text,
            )
            raise iae.FailedAPIDependencyError(
                f"{config.CDP_SERVICE}/customer-profiles/insights/spending-by-month",
                response.status,
            )

        logger.info("Successfully retrieved state demographic insights.")
        return sorted(
            clean_cdm_fields(response_body[api_c.BODY]),
            key=lambda x: (x[api_c.YEAR], x[api_c.MONTH]),
        )


async def get_customers_overview_async(
    session: ClientSession,
    token: str,
    filters: dict,
) -> dict:
    """Fetch customers overview data asynchronously.

    Args:
        session (ClientSession): Async IO http client session.
        token (str): OKTA JWT Token.
        filters (dict): filters to pass into customers_overview endpoint.

    Returns:
        dict: dictionary of overview data.

    Raises:
        FailedAPIDependencyError: Integrated dependent API failure error.
    """

    # get config
    config = get_config()
    logger.info("Getting Customer Profile Insights from CDP API.")
    # run the async post request
    async with session.post(
        f"{config.CDP_SERVICE}/customer-profiles/insights",
        json=filters,
        headers={
            api_c.CUSTOMERS_API_HEADER_KEY: token,
        },
    ) as response:
        response_body = await response.json()
        if response.status != 200 or api_c.BODY not in response_body:
            logger.error(
                "Unable to retrieve profile insights, %s %s.",
                response.status,
                response.text,
            )
            raise iae.FailedAPIDependencyError(
                f"{config.CDP_SERVICE}/customer-profiles/insights",
                response.status,
            )

        logger.info(
            "Successfully retrieved Customer Profile Insights from CDP API."
        )

        # clean up cdm date and gender fields in the response
        return clean_cdm_gender_fields(
            clean_cdm_fields(response_body[api_c.BODY])
        )
