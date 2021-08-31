"""Module to park all performance metrics components"""
import csv
from datetime import datetime
from pathlib import Path

from bson import ObjectId
from pymongo import MongoClient
from huxunifylib.database import (
    constants as db_c,
    delivery_platform_management,
    orchestration_management,
)
from huxunifylib.database.delivery_platform_management import (
    get_performance_metrics_by_engagement_details,
    get_delivery_jobs_using_metadata,
)
from huxunifylib.util.general.logging import logger
from huxunify.api import constants as api_c
from huxunify.api.route.utils import (
    group_perf_metric,
    update_metrics,
    get_db_client,
)


def get_display_ads_campaign_metrics(
    delivery_jobs: list,
    performance_metrics: list,
    metrics_type: str,
) -> list:
    """Group performance metrics for campaigns

    Args:
        delivery_jobs (list) : Delivery jobs.
        performance_metrics (list): List of performance metrics.
        metrics_type (str): Type of performance metrics.

    Returns:
        list: Grouped performance metrics.
    """
    campaign_metrics_list = []
    delivery_campaigns = []
    for job in delivery_jobs:
        if job[db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS]:
            delivery_campaigns.extend(
                job[db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS]
            )

    for campaign in delivery_campaigns:
        job_list = []
        for job in delivery_jobs:
            if (
                job[db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS]
                and campaign in job[db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS]
            ):
                job_list.append(job)
        campaign_metrics_list.append(
            update_metrics(
                campaign[api_c.ID],
                campaign[api_c.NAME],
                job_list,
                performance_metrics,
                metrics_type,
            )
        )
    return campaign_metrics_list


# pylint: disable=too-many-locals, too-many-nested-blocks
def group_engagement_performance_metrics(
    engagement: object,
    delivery_jobs: list,
    performance_metrics: list,
    target_destinations: list,
    metrics_type: str,
) -> dict:
    """Group performance metrics for engagement

    Args:
        engagement (object) : Engagement object.
        delivery_jobs (list): List of delivery jobs.
        performance_metrics (list): List of performance metrics.
        target_destinations (list): List of target destinations.
        metrics_type (str): Type of performance metrics.

    Returns:
        dict: Grouped performance metrics.
    """

    database = get_db_client()
    audience_metrics_list = []
    # For each audience in engagement.audience
    for eng_audience in engagement.get(api_c.AUDIENCES):
        audience = orchestration_management.get_audience(
            database, eng_audience.get(api_c.ID)
        )
        if audience is None:
            logger.warning(
                "Audience not found, ignoring performance metrics for it. "
                "audience_id=%s, engagement_id=%s",
                eng_audience.get(api_c.ID),
                engagement.get(db_c.ID),
            )
            continue

        # Group all delivery jobs by audience id
        audience_delivery_jobs = [
            x
            for x in delivery_jobs
            if x[db_c.AUDIENCE_ID] == audience.get(db_c.ID)
        ]
        #  Group performance metrics for the audience
        audience_metrics = update_metrics(
            audience.get(db_c.ID),
            audience[api_c.NAME],
            audience_delivery_jobs,
            performance_metrics,
            metrics_type,
        )

        # Get metrics grouped by audience.destination
        audience_destination_metrics_list = []
        for audience_destination in eng_audience.get(api_c.DESTINATIONS):
            destination_id = audience_destination.get(api_c.ID)
            if (
                destination_id is None
                or destination_id not in target_destinations
            ):
                logger.warning(
                    "Invalid destination encountered, ignoring performance metrics for it. "
                    "destination_id=%s, audience_id=%s, engagement_id=%s",
                    destination_id,
                    eng_audience.get(api_c.ID),
                    engagement.get(db_c.ID),
                )
                continue
            # Group all delivery jobs by audience.destination
            audience_destination_jobs = [
                x
                for x in audience_delivery_jobs
                if x[db_c.DELIVERY_PLATFORM_ID] == destination_id
            ]

            # get delivery platform
            delivery_platform = (
                delivery_platform_management.get_delivery_platform(
                    database, destination_id
                )
            )

            #  Group performance metrics for the destination
            destination_metrics = update_metrics(
                destination_id,
                delivery_platform[api_c.NAME],
                audience_destination_jobs,
                performance_metrics,
                metrics_type,
            )
            destination_metrics[
                api_c.DELIVERY_PLATFORM_TYPE
            ] = delivery_platform[db_c.DELIVERY_PLATFORM_TYPE]

            if metrics_type == api_c.DISPLAY_ADS:
                destination_metrics[
                    api_c.CAMPAIGNS
                ] = get_display_ads_campaign_metrics(
                    audience_destination_jobs,
                    performance_metrics,
                    metrics_type,
                )
            audience_destination_metrics_list.append(destination_metrics)
        audience_metrics[
            api_c.DESTINATIONS
        ] = audience_destination_metrics_list
        audience_metrics_list.append(audience_metrics)

    return audience_metrics_list


def get_performance_metrics(
    database: MongoClient,
    engagement: object,
    engagement_id: str,
    ad_type: str,
) -> dict:
    """

    Args:
        database (MongoClient): Mongoclient instance
        engagement (object): Engagement object
        engagement_id (str): Id of engagement
        ad_type (str): Advertisement type

    Returns:
        dict: Email Performance metrics of an engagement
    """

    if ad_type == api_c.DISPLAY_ADS:
        destination_type = db_c.DELIVERY_PLATFORM_FACEBOOK
    else:
        destination_type = db_c.DELIVERY_PLATFORM_SFMC

    # Get all destinations that are related to Email metrics
    destination = delivery_platform_management.get_delivery_platform_by_type(
        database, destination_type
    )

    delivery_jobs = []
    performance_metrics = []
    if destination:
        # Get Performance metrics by engagement and destination
        performance_metrics = get_performance_metrics_by_engagement_details(
            database,
            ObjectId(engagement_id),
            [destination.get(db_c.ID)],
        )

        if performance_metrics:
            # Get all the delivery jobs for the given engagement and destination
            delivery_jobs = get_delivery_jobs_using_metadata(
                database, engagement_id=ObjectId(engagement_id)
            )

            delivery_jobs = [
                x
                for x in delivery_jobs
                if x[db_c.DELIVERY_PLATFORM_ID] == destination.get(db_c.ID)
            ]

    # Group all the performance metrics for the engagement
    final_metric = {
        api_c.SUMMARY: group_perf_metric(
            [x[db_c.PERFORMANCE_METRICS] for x in performance_metrics],
            ad_type,
        )
    }
    audience_metrics_list = group_engagement_performance_metrics(
        engagement,
        delivery_jobs,
        performance_metrics,
        [destination.get(db_c.ID)],
        ad_type,
    )
    final_metric[api_c.AUDIENCE_PERFORMANCE_LABEL] = audience_metrics_list

    return final_metric


def generate_metrics_file(
    engagement_id: str, final_metric: dict, metrics_type: str
) -> None:
    """

    Args:
        engagement_id (str): Id of engagement
        final_metric (dict): Performance metrics for an engagement
        metrics_type (str): Type of performance metrics

    Returns:

    """
    file_path = "performancemetrics"
    file_name = (
        f"{datetime.now().strftime('%m%d%Y%H%M%S')}"
        f"_{engagement_id}_{metrics_type}_metrics.csv"
    )
    logger.info("Writing File into %s", Path(file_path).resolve())

    with open(
        Path(__file__).parent.parent.parent.joinpath(file_path) / file_name,
        "w",
        newline="",
    ) as csv_file:
        field_names = [api_c.NAME] + list(final_metric[api_c.SUMMARY].keys())
        dict_writer = csv.DictWriter(csv_file, fieldnames=field_names)
        dict_writer.writeheader()

        final_metric[api_c.SUMMARY][api_c.NAME] = api_c.SUMMARY
        dict_writer.writerow(final_metric[api_c.SUMMARY])

        for audience in final_metric[api_c.AUDIENCE_PERFORMANCE_LABEL]:
            del audience[api_c.ID]
            del audience[api_c.DESTINATIONS]
            dict_writer.writerow(audience)
    return file_name
