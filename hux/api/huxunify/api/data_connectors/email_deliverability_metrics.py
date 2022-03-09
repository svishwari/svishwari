"""File for email deliverability metrics functions."""

from datetime import datetime, timedelta
from collections import defaultdict
from random import uniform

from pymongo import MongoClient

from huxunifylib.database import constants as db_c
from huxunifylib.database.deliverability_metrics_management import (
    get_domain_wise_inbox_percentage_data,
    get_deliverability_data_performance_metrics,
)

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.route.utils import clean_domain_name_string


def get_delivered_rate_data(
    database: MongoClient,
    domains: list,
    start_date: datetime,
    end_date: datetime,
) -> list:
    """Get delivered rate data.
    Args:
        database (MongoClient): A database client.
        domains (list): List of domain names to fetch delivered rate data.
        start_date (datetime): Start date for data to be fetched.
        end_date (datetime): End time for data to be fetched.

    Returns:
        list: Domain_wise list of delivered rate.
    """
    delivered_rate_data = defaultdict(list)
    domain_inbox_percentage_data = get_domain_wise_inbox_percentage_data(
        database=database,
        domain_name=domains,
        start_date=start_date,
        end_date=end_date,
    )

    for domain_data in domain_inbox_percentage_data:
        for inbox_percentage_data in domain_data.get(
            db_c.INBOX_PERCENTAGE_DATA
        ):
            delivered_rate_data[
                inbox_percentage_data.get(db_c.CREATE_TIME)
            ].append(
                {
                    db_c.DOMAIN_NAME: domain_data.get(db_c.DOMAIN_NAME),
                    db_c.INBOX_PERCENTAGE: inbox_percentage_data.get(
                        db_c.INBOX_PERCENTAGE
                    ),
                }
            )

    dates_data_available = list(delivered_rate_data.keys())
    dates_data_available.sort()

    curr_date = start_date
    delivered_data_with_stub = []
    idx = 0
    while curr_date <= end_date:
        if (
            dates_data_available
            and curr_date.date() == dates_data_available[idx]
        ):

            data = {
                clean_domain_name_string(daily_data[db_c.DOMAIN_NAME]): round(
                    daily_data[db_c.INBOX_PERCENTAGE], 2
                )
                for daily_data in delivered_rate_data[
                    dates_data_available[idx]
                ]
            }
        else:
            # TODO - remove after, Fill with stub.
            data = {
                clean_domain_name_string(domain): round(uniform(0.6, 0.9), 2)
                for domain in domains
            }

        data[api_c.DATE] = curr_date
        delivered_data_with_stub.append(data)

        if (
            dates_data_available
            and curr_date.date() < dates_data_available[idx]
            and idx < len(dates_data_available) - 1
        ):
            idx += 1

        curr_date = curr_date + timedelta(days=1)

    return delivered_data_with_stub


def get_performance_metrics_deliverability_data(
    database: MongoClient,
    domains: list,
    start_date: datetime,
    end_date: datetime,
) -> dict:
    """Get performance metrics email deliverability metrics.
    Args:
        database (MongoClient): A database client.
        domains (list): List of domain names to fetch delivered rate data.
        start_date (datetime): Start date for data to be fetched.
        end_date (datetime): End time for data to be fetched.

    Returns:
        dict: Deliverability data dict.
    """

    sent_data = []
    delivered_data = []
    open_rate_data = []
    click_rate_data = []
    unsubscribe_rate_data = []
    complaints_rate_data = []

    deliverability_data = get_deliverability_data_performance_metrics(
        database=database,
        domains=domains,
        start_date=start_date,
        end_date=end_date,
        mock=bool(get_config().FLASK_ENV == api_c.TEST_MODE),
    )
    for domain_data in deliverability_data:
        # For domain name from performance metrics we get complete address.
        domain_name = clean_domain_name_string(
            domain_data.get(api_c.DOMAIN_NAME)
        )

        for metrics in domain_data.get(api_c.DELIVERABILITY_METRICS, []):

            sent_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: metrics.get(api_c.SENT),
                }
            )

            delivered_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: metrics.get(api_c.DELIVERED),
                }
            )

            open_rate_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: metrics.get(api_c.OPEN_RATE),
                }
            )

            click_rate_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: metrics.get(api_c.CLICK_RATE),
                }
            )

            unsubscribe_rate_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: metrics.get(api_c.UNSUBSCRIBE_RATE),
                }
            )

            complaints_rate_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: metrics.get(api_c.COMPLAINTS_RATE),
                }
            )

    return {
        api_c.SENT: sent_data,
        api_c.OPEN_RATE: open_rate_data,
        api_c.CLICK_RATE: click_rate_data,
        api_c.UNSUBSCRIBE_RATE: unsubscribe_rate_data,
        api_c.COMPLAINTS_RATE: complaints_rate_data,
    }
