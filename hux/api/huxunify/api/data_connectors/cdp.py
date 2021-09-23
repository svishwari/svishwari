"""Purpose of this file is for holding methods to query and pull data from CDP."""
import random
import time
import asyncio
from collections import defaultdict
from typing import Tuple, Optional, List
from datetime import datetime, timedelta

import requests
import aiohttp
import async_timeout
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
        dict: dictionary of overview data

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
    # TODO : Get date range from CDP
    return {
        "overview": clean_cdm_fields(response.json()[api_c.BODY]),
        "date_range": {
            api_c.START_DATE: datetime.now()
            - timedelta(days=random.randint(1000, 5000)),
            api_c.END_DATE: datetime.now(),
        },
    }


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


def fill_empty_customer_events(
    start_date: datetime, end_date: datetime
) -> list:
    """Fill empty events for dates between start_date and end_date.

    Args:
        start_date (datetime): Start date between which dates, events need to be filled.
        end_date (datetime): End date between which dates, events need to be filled.
    Returns:
        list: Customer events with zero.
    """
    return [
        {
            api_c.DATE: start_date + timedelta(days=i),
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


def fill_customer_events_missing_dates(
    customer_events: list, start_date: datetime, end_date: datetime
) -> list:
    """Get events for a customer grouped by date.

    Args:
        customer_events (list): Customer events in CDM API body.
        start_date (datetime): Start date in filter.
        end_date (datetime): End date in filter.
    Returns:
        list: Customer events including zeros for missing dates.
    """
    prev_date = start_date
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
                        prev_date - timedelta(1),
                        prev_date + timedelta(1),
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

    if end_date > prev_date and (end_date - prev_date).days >= 1:
        customer_events_dates_filled = (
            customer_events_dates_filled
            + fill_empty_customer_events(prev_date, end_date + timedelta(1))
        )

    customer_events_dates_filled.sort(
        key=lambda customer_event_: customer_event_.get("date")
    )
    return customer_events_dates_filled


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
        list: Customer events with respective counts
    """

    config = get_config()
    current_time = datetime.utcnow()

    # YTD by default
    default_filter = {
        api_c.START_DATE: current_time.strftime("%Y-01-01"),
        api_c.END_DATE: current_time.strftime("%Y-%m-%d"),
    }

    filters = filters if filters else default_filter

    # set missing start or end date
    filters[api_c.START_DATE] = filters.get(
        api_c.START_DATE,
        current_time.strftime("%Y-01-01"),
    )
    filters[api_c.END_DATE] = filters.get(
        api_c.END_DATE,
        current_time.strftime("%Y-%m-%d"),
    )

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
        parse(filters.get(api_c.START_DATE) + "T00:00:00Z"),
        parse(filters.get(api_c.END_DATE) + "T00:00:00Z"),
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
    """Get spending details of customer by cities

    Args:
        token (str): OKTA JWT Token.
        filters (Optional[dict]): filters to pass into
            customers_overview endpoint.

    Returns:
        list: list of income details of customers by cities

    """
    return [
        {api_c.NAME: x[api_c.CITY], api_c.LTV: round(x["avg_ltv"], 4)}
        for x in get_city_ltvs(token, filters=filters)
    ]


def get_customer_count_by_state(
    token: str, filters: Optional[dict] = None
) -> list:
    """
    Get demographic details of customers by state

    Args:
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into
            count_by_state endpoint, default None

    Returns:
        list: list of state demographic data

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
    body = clean_cdm_fields(response.json()[api_c.BODY])

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
        list: list of demographic details by state

    """
    filters = (
        {api_c.AUDIENCE_FILTERS: filters}
        if filters
        else api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER
    )
    customer_count_by_state = get_customer_count_by_state(token, filters)

    geographic_response = [
        {
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
            api_c.LTV: round(x.get(api_c.AVG_LTV, 0), 4),
        }
        for x in customer_count_by_state
    ]
    return geographic_response


def get_demographic_by_country(
    token: str, filters: Optional[dict] = None
) -> list:
    """
    Get demographic details of customers by country

    Args:
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into
            count_by_state endpoint, default None

    Returns:
        list: list of demographic details by country

    """
    customer_count_by_state = get_customer_count_by_state(token=token)
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
            {"name": country, "avg_ltv": avg_ltv, "size": total_customer_count}
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
        date_filters (dict): filters to pass into
            customer insights count by day endpoint.

    Returns:
        dict: dictionary of customer count data.
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
    """
    Get spending details of customers by city

    Args:
        token (str): OKTA JWT Token.
        filters (dict):  filters to pass into
            city_ltvs endpoint
        offset (int): offset
        limit (int): limit

    Returns:
        list: list of spending details by cities

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

    return [clean_cdm_fields(data) for data in response.json()[api_c.BODY]]


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


def get_spending_by_gender(
    token: str,
    start_date: str,
    end_date: str,
    filters: Optional[dict] = None,
) -> List[Optional[dict]]:
    """

    Args:
        token (str): OKTA JWT Token.
        start_date (str): String value of start date
        end_date (str): String value of end date
        filters (dict):  filters to pass into
            spending-by-month endpoint

    Returns:
        list: list of spending details by gender
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


def add_missing_customer_count_by_day(
    response_body: list, date_filters: dict
) -> list:
    """
    Add customer data for missing dates

    Args:
        response_body (list): list of customer count data
        date_filters (dict): start_date and end_date for which customer
            data is being fetched

    Returns:
        customer_data_by_day (list): customer count data
            for all days within start_date and end_date

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

    return customer_data_by_day
