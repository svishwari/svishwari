"""File for email deliverability metrics functions."""

from datetime import datetime
from collections import defaultdict
from typing import Optional

from dateutil.relativedelta import relativedelta
from pymongo import MongoClient

from huxunifylib.database import constants as db_c
from huxunifylib.database.deliverability_metrics_management import (
    get_domain_wise_inbox_percentage_data,
    get_deliverability_data_performance_metrics,
    get_campaign_aggregated_sent_count,
)

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.route.utils import clean_domain_name_string


def get_delivered_rate_data(
    database: MongoClient,
    domains: list,
    start_date: datetime,
    end_date: datetime,
    fill_empty: bool = True,
) -> list:
    """Get delivered rate data.
    Args:
        database (MongoClient): A database client.
        domains (list): List of domain names to fetch delivered rate data.
        start_date (datetime): Start date for data to be fetched.
        end_date (datetime): End time for data to be fetched.
        fill_empty (Optional, bool): Fills empty dates with zeroes if True.
    Returns:
        list: Domain_wise list of delivered rate.
    """
    delivered_data = []
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

            delivered_data.append(
                {
                    api_c.DATE: inbox_percentage_data.get(db_c.CREATE_TIME),
                    clean_domain_name_string(
                        domain_data.get(db_c.DOMAIN_NAME)
                    ): inbox_percentage_data.get(db_c.INBOX_PERCENTAGE),
                }
            )
        delivered_data = sorted(
            delivered_data, key=lambda data: data.get(api_c.DATE)
        )
        if fill_empty:
            delivered_data = fill_domain_daily_data(
                start_date=start_date,
                end_date=end_date,
                domain_data=delivered_data,
                domain_name=clean_domain_name_string(
                    domain_data.get(db_c.DOMAIN_NAME)
                ),
            )
    return delivered_data


# pylint: disable=too-many-locals
def get_performance_metrics_deliverability_data(
    database: MongoClient,
    domains: list,
    start_date: datetime,
    end_date: datetime,
    fill_empty: Optional[bool] = True,
) -> dict:
    """Get performance metrics email deliverability metrics.
    Args:
        database (MongoClient): A database client.
        domains (list): List of domain names to fetch delivered rate data.
        start_date (datetime): Start date for data to be fetched.
        end_date (datetime): End time for data to be fetched.
        fill_empty (Optional(bool)): Fills empty dates with zeroes if True.
    Returns:
        dict: Deliverability data dict.
    """

    sent_count_data = []
    delivered_data = []
    open_rate_data = []
    click_rate_data = []
    unsubscribe_rate_data = []
    complaints_rate_data = []

    # Combination of both delivered and open rate data.
    delivered_open_rate_data = []

    domain_campaign_sent = defaultdict(dict)
    aggregated_sent_data = get_campaign_aggregated_sent_count(
        database=database,
        domains=domains,
        start_date=start_date,
        end_date=end_date,
    )
    for sent_data in aggregated_sent_data:
        domain_campaign_sent[sent_data.get(api_c.DOMAIN_NAME)][
            sent_data.get(api_c.CAMPAIGN_ID)
        ] = sent_data.get(api_c.SENT)

    deliverability_data = get_deliverability_data_performance_metrics(
        database=database,
        domains=domains,
        start_date=start_date,
        end_date=end_date,
        mock=bool(get_config().FLASK_ENV == api_c.TEST_MODE),
    )
    prev_delivery = {}
    prev_sent = {}

    curr_delivery = {}
    curr_sent = {}

    for domain_data in deliverability_data:
        # For domain name from performance metrics we get complete address.
        domain_name = clean_domain_name_string(
            domain_data.get(api_c.DOMAIN_NAME)
        )
        domain_aggregated_sent = domain_campaign_sent.get(
            domain_data.get(api_c.DOMAIN_NAME), {}
        )

        for metrics in domain_data.get(api_c.DELIVERABILITY_METRICS, []):
            campaign_aggregated_sent = domain_aggregated_sent.get(
                metrics.get(api_c.CAMPAIGN_ID)
            )
            if not prev_sent.get(
                metrics.get(api_c.CAMPAIGN_ID)
            ) and not prev_delivery.get(metrics.get(api_c.CAMPAIGN_ID)):
                prev_delivery[
                    metrics.get(api_c.CAMPAIGN_ID)
                ] = campaign_aggregated_sent
                prev_sent[
                    metrics.get(api_c.CAMPAIGN_ID)
                ] = campaign_aggregated_sent
            # Sent is sent - hard bounces, unsubs, complaints.
            curr_sent[metrics.get(api_c.CAMPAIGN_ID)] = (
                prev_sent[metrics.get(api_c.CAMPAIGN_ID)]
                - metrics.get(api_c.HARD_BOUNCES)
                - metrics.get(api_c.UNSUBSCRIBES)
                - metrics.get(api_c.COMPLAINTS)
            )
            # Delivery is sent - soft bounces.
            curr_delivery[metrics.get(api_c.CAMPAIGN_ID)] = curr_sent[
                metrics.get(api_c.CAMPAIGN_ID)
            ] - metrics.get(api_c.SOFT_BOUNCES)

            sent_count_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: prev_sent[metrics.get(api_c.CAMPAIGN_ID)],
                }
            )

            delivered_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: prev_delivery[metrics.get(api_c.CAMPAIGN_ID)],
                }
            )

            open_rate_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: metrics.get(api_c.OPENS)
                    / prev_delivery[metrics.get(api_c.CAMPAIGN_ID)],
                }
            )

            click_rate_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: metrics.get(api_c.CLICKS)
                    / prev_delivery[metrics.get(api_c.CAMPAIGN_ID)],
                }
            )

            unsubscribe_rate_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: metrics.get(api_c.UNSUBSCRIBES)
                    / prev_delivery[metrics.get(api_c.CAMPAIGN_ID)],
                }
            )

            complaints_rate_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    domain_name: metrics.get(api_c.COMPLAINTS)
                    / prev_delivery[metrics.get(api_c.CAMPAIGN_ID)],
                }
            )

            delivered_open_rate_data.append(
                {
                    api_c.DATE: metrics.get(api_c.DATE),
                    api_c.DOMAIN_NAME: domain_name,
                    api_c.OPEN_RATE: metrics.get(api_c.OPENS)
                    / prev_delivery[metrics.get(api_c.CAMPAIGN_ID)],
                    api_c.DELIVERED_COUNT: prev_delivery[
                        metrics.get(api_c.CAMPAIGN_ID)
                    ],
                }
            )
            prev_sent[metrics.get(api_c.CAMPAIGN_ID)] = curr_sent[
                metrics.get(api_c.CAMPAIGN_ID)
            ]
            prev_delivery[metrics.get(api_c.CAMPAIGN_ID)] = curr_delivery[
                metrics.get(api_c.CAMPAIGN_ID)
            ]

        if fill_empty:
            sent_count_data = sorted(
                sent_count_data, key=lambda data: data.get(api_c.DATE)
            )
            sent_count_data = fill_domain_daily_data(
                start_date=start_date,
                end_date=end_date,
                domain_data=sent_count_data,
                domain_name=domain_name,
            )

            open_rate_data = sorted(
                open_rate_data, key=lambda data: data.get(api_c.DATE)
            )
            open_rate_data = fill_domain_daily_data(
                start_date=start_date,
                end_date=end_date,
                domain_data=open_rate_data,
                domain_name=domain_name,
            )

            click_rate_data = sorted(
                click_rate_data, key=lambda data: data.get(api_c.DATE)
            )
            click_rate_data = fill_domain_daily_data(
                start_date=start_date,
                end_date=end_date,
                domain_data=click_rate_data,
                domain_name=domain_name,
            )

            unsubscribe_rate_data = sorted(
                unsubscribe_rate_data, key=lambda data: data.get(api_c.DATE)
            )
            unsubscribe_rate_data = fill_domain_daily_data(
                start_date=start_date,
                end_date=end_date,
                domain_data=unsubscribe_rate_data,
                domain_name=domain_name,
            )

            complaints_rate_data = sorted(
                complaints_rate_data, key=lambda data: data.get(api_c.DATE)
            )
            complaints_rate_data = fill_domain_daily_data(
                start_date=start_date,
                end_date=end_date,
                domain_data=complaints_rate_data,
                domain_name=domain_name,
            )

            delivered_open_rate_data = sorted(
                delivered_open_rate_data, key=lambda data: data.get(api_c.DATE)
            )
    return {
        api_c.SENT: sorted(
            sent_count_data, key=lambda data: data.get(api_c.DATE)
        ),
        api_c.OPEN_RATE: sorted(
            open_rate_data, key=lambda data: data.get(api_c.DATE)
        ),
        api_c.CLICK_RATE: sorted(
            click_rate_data, key=lambda data: data.get(api_c.DATE)
        ),
        api_c.UNSUBSCRIBE_RATE: sorted(
            unsubscribe_rate_data, key=lambda data: data.get(api_c.DATE)
        ),
        api_c.COMPLAINTS_RATE: sorted(
            complaints_rate_data, key=lambda data: data.get(api_c.DATE)
        ),
        f"{api_c.DELIVERED}_{api_c.OPEN_RATE}": sorted(
            delivered_open_rate_data, key=lambda data: data.get(api_c.DATE)
        ),
    }


def fill_domain_daily_data(
    start_date: datetime,
    end_date: datetime,
    domain_name: str,
    domain_data: list,
) -> list:
    """Fills missing daily data with zeroes.
    Args:
        start_date (datetime): Start date for filled data.
        end_date (datetime): End date for filled data.
        domain_name (str): Name of domain which data is being filled.
        domain_data (list): Actual data of the domain.
    Returns:
        list: Missing dates filled with zeroes.
    """
    filled_data = []
    curr_date = start_date
    idx = 0

    while curr_date.date() < end_date.date():
        if idx < len(domain_data) and curr_date.strftime(
            "%Y-%m-%d"
        ) == domain_data[idx].get(api_c.DATE).strftime("%Y-%m-%d"):
            domain_data[idx][api_c.DATE] = datetime.fromisoformat(
                domain_data[idx][api_c.DATE].isoformat()
            )
            filled_data.append(domain_data[idx])
            idx += 1
        else:
            filled_data.append({domain_name: 0, api_c.DATE: curr_date})

        curr_date += relativedelta(days=1)

    return filled_data
