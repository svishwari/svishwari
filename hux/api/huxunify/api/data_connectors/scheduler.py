"""Purpose of this module is to park schedule modules for delivery schedule."""
import asyncio
from datetime import datetime
from pymongo import MongoClient
from huxunifylib.connectors.util.selector import (
    get_delivery_platform_connector,
)
from huxunifylib.util.general.logging import logger
from huxunifylib.database import constants as db_c, collection_management
from huxunifylib.database.cache_management import (
    create_cache_entry,
    get_cache_entry,
)
from huxunifylib.database.collection_management import get_documents
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database import (
    delivery_platform_management as destination_management,
)
from huxunifylib.database.delivery_platform_management import (
    get_delivery_platform,
    get_all_delivery_platforms,
)
from huxunifylib.database.orchestration_management import (
    get_audience,
    get_all_audiences,
)
from huxunifylib.database.survey_metrics_management import (
    get_all_distinct_segment_filters,
)
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.cdp import (
    get_customers_count_async,
    get_customers_overview,
)
from huxunify.api.data_connectors.courier import (
    get_destination_config,
    get_audience_destination_pairs,
)
from huxunify.api.data_connectors.jira import JiraConnection
from huxunify.api.data_connectors.okta import get_env_okta_user_bearer_token
from huxunify.api.data_connectors.trust_id import (
    get_trust_id_comparison_data_by_segment,
)
from huxunify.api.schema.utils import get_next_schedule

monthly_period_items_dict = {
    "first": "1",
    "second": "2",
    "third": "3",
    "fourth": "4",
    "last": "L",
}

day_of_week_name_dict = {
    "Monday": "1",
    "Tuesday": "2",
    "Wednesday": "3",
    "Thursday": "4",
    "Friday": "5",
    "Saturday": "6",
    "Sunday": "7",
}


# pylint: disable=too-many-branches
def _add_cron_for_monthly(schedule: dict, cron_exp: dict) -> str:
    """Adds monthly cron to existing cron expression.

    Args:
         schedule: Dictionary object of schedule.
         cron_exp: Cron exp dict to append monthly schedule.
     Returns:
         dict: Updated cron expression.
    """

    day_of_month_cron_str = ""
    day_of_week_cron_str = ""

    day_of_month_list = (
        schedule.get("day_of_month")
        if isinstance(schedule.get("day_of_month"), list)
        else [schedule.get("day_of_month")]
    )

    day_of_month_list = [str(item) for item in day_of_month_list]
    period_items = [
        item.lower() for item in schedule.get("monthly_period_items", [])
    ]

    if len(period_items) == 1:
        period_item_val = monthly_period_items_dict.get(period_items[0])

        if period_items[0] == "day":
            day_of_month_cron_str = ",".join(day_of_month_list) + ","

        elif period_items[0] == "last":

            for d_month in day_of_month_list:
                day_of_week_digit = day_of_week_name_dict.get(d_month)
                if day_of_week_digit:
                    day_of_week_cron_str = (
                        f"{day_of_week_cron_str}"
                        f"{period_item_val}"
                        f"{day_of_week_digit},"
                    )

                elif d_month == "Day":
                    day_of_month_cron_str = (
                        f"{day_of_month_cron_str}" f"{period_item_val},"
                    )

        elif period_item_val:
            for d_month in day_of_month_list:
                day_of_week_digit = day_of_week_name_dict.get(d_month)
                if day_of_week_digit:
                    day_of_week_cron_str = (
                        f"{day_of_week_cron_str}"
                        f"{day_of_week_digit}#"
                        f"{period_item_val},"
                    )

                elif d_month == "Day":
                    day_of_month_cron_str = (
                        f"{day_of_month_cron_str}" f"{period_item_val},"
                    )

    elif len(day_of_month_list) == 1:
        if day_of_month_list[0] == "Day":
            for period_item in period_items:
                period_item_val = monthly_period_items_dict.get(period_item)
                if period_item_val:
                    day_of_month_cron_str = (
                        f"{day_of_month_cron_str}" f"{period_item_val},"
                    )
        day_of_week_digit = day_of_week_name_dict.get(day_of_month_list[0])
        if day_of_week_digit:
            for period_item in period_items:
                period_item_val = monthly_period_items_dict.get(period_item)
                if period_item == "last":
                    day_of_week_cron_str = (
                        f"{day_of_week_cron_str}"
                        f"{period_item_val}"
                        f"{day_of_week_digit},"
                    )

                elif period_item_val:
                    day_of_week_cron_str = (
                        f"{day_of_week_cron_str}"
                        f"{day_of_week_digit}#"
                        f"{period_item_val},"
                    )

    if day_of_month_cron_str:
        cron_exp["day_of_month"] = day_of_month_cron_str[:-1]

    if day_of_week_cron_str:
        cron_exp["day_of_week"] = day_of_week_cron_str[:-1]

    if schedule["every"] > 1:
        cron_exp["month"] = f"{cron_exp['month']}/{schedule['every']}"

    return cron_exp


def generate_cron(schedule: dict) -> str:
    """To generate cron expression based on the schedule object
    Args:
        schedule: dictionary object of schedule

    Returns:
        str: cron expression
    """
    cron_exp = {
        "minute": "*",
        "hour": "*",
        "day_of_month": "*",
        "month": "*",
        "day_of_week": "?",
        "year": "*",
    }

    cron_exp["minute"] = schedule.get("minute", "*")
    if schedule.get("period") == "AM":
        cron_exp["hour"] = (
            0 if schedule.get("hour") == 12 else schedule.get("hour", "*")
        )
    else:
        if schedule.get("hour"):
            cron_exp["hour"] = schedule.get("hour") + 12

    cron_exp["month"] = schedule.get("month", "*")

    if schedule["periodicity"] == "Weekly":
        cron_exp["day_of_month"] = "?"

        cron_exp["day_of_week"] = ",".join(schedule.get("day_of_week"))
        if schedule["every"] > 1:
            cron_exp[
                "day_of_week"
            ] = f"{cron_exp['day_of_week']}#{schedule['every']}"

    if schedule["periodicity"] == "Daily":
        cron_exp["day_of_month"] = "*"
        if schedule["every"] > 1:
            cron_exp[
                "day_of_month"
            ] = f"{cron_exp['day_of_month']}/{schedule['every']}"

    if schedule["periodicity"] == "Monthly":
        cron_exp = _add_cron_for_monthly(schedule, cron_exp)

    return " ".join([str(val) for val in cron_exp.values()])


async def delivery_destination(
    database, engagement, audience_id, destination_id
):
    """Async function that couriers delivery jobs.

    Args:
        database (MongoClient): The mongo database client.
        engagement (dict): Engagement object.
        audience_id (ObjectId): Audience ID.
        destination_id (ObjectId): Destination ID.
    """

    # get audience object for delivering
    audience = get_audience(database, audience_id)
    if not audience:
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_CRITICAL,
            (
                f"Failed to delivered audience ID "
                f'"{audience_id}" from engagement '
                f'"{engagement[db_c.NAME]}" to destination ID '
                f'"{destination_id}" because the audience does not exist.'
            ),
            db_c.NOTIFICATION_CATEGORY_DELIVERY,
            engagement[db_c.UPDATED_BY],
        )
        return

    # get destination object for delivering
    destination = get_delivery_platform(database, destination_id)
    if not destination:
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_CRITICAL,
            (
                f"Failed to delivered audience ID "
                f'"{audience_id}" from engagement '
                f'"{engagement[db_c.NAME]}" to destination ID '
                f'"{destination_id}" because the destination does not exist.'
            ),
            db_c.NOTIFICATION_CATEGORY_DELIVERY,
            engagement[db_c.UPDATED_BY],
        )
        return

    delivery_job_ids = []
    for pair in get_audience_destination_pairs(engagement[api_c.AUDIENCES]):
        if [pair[0], pair[1][db_c.OBJECT_ID]] != [
            audience_id,
            destination_id,
        ]:
            continue
        batch_destination = get_destination_config(
            database,
            *pair,
            engagement[db_c.ID],
            username=engagement[db_c.UPDATED_BY],
        )
        batch_destination.register()
        batch_destination.submit()
        delivery_job_ids.append(
            str(batch_destination.audience_delivery_job_id)
        )

    logger.info(
        "Successfully created delivery jobs %s.",
        ",".join(delivery_job_ids),
    )
    # create notification
    create_notification(
        database,
        db_c.NOTIFICATION_TYPE_SUCCESS,
        (
            f"Successfully delivered audience "
            f'"{audience[db_c.NAME]}" from engagement '
            f'"{engagement[db_c.NAME]}" to destination '
            f'"{destination[db_c.NAME]}".'
        ),
        db_c.NOTIFICATION_CATEGORY_DELIVERY,
        engagement[db_c.UPDATED_BY],
    )


def run_scheduled_deliveries(database: MongoClient) -> None:
    """function to run all scheduled deliveries per CRON Expressions.

    Args:
        database (MongoClient): The mongo database client.

    """

    # get database
    current_time = datetime.utcnow()

    # set the event loop
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    loop = asyncio.get_event_loop()

    # get active engagements
    for engagement in get_documents(
        database=database,
        collection=db_c.ENGAGEMENTS_COLLECTION,
        query_filter={db_c.STATUS: {"$ne": db_c.STATUS_INACTIVE}},
    )[db_c.DOCUMENTS]:
        # process audiences
        for audience in engagement.get(api_c.AUDIENCES):
            # process each destination
            for destination in audience.get(api_c.DESTINATIONS):
                if not isinstance(destination, dict):
                    continue
                delivery_schedule = (
                    audience.get(api_c.DELIVERY_SCHEDULE)
                    if audience.get(api_c.DELIVERY_SCHEDULE)
                    else engagement.get(api_c.DELIVERY_SCHEDULE)
                )
                # if no delivery schedule exists, continue
                if not delivery_schedule:
                    continue

                if delivery_schedule.get(api_c.SCHEDULE_CRON):
                    schedule_cron = delivery_schedule[api_c.SCHEDULE_CRON]
                else:
                    schedule_cron = generate_cron(
                        delivery_schedule.get(api_c.SCHEDULE)
                    )
                # check if the schedule falls within the cron time frame.
                next_schedule = get_next_schedule(
                    schedule_cron,
                    current_time,
                )

                # check if next schedule is within one minute
                if (current_time - next_schedule).total_seconds() > 60:
                    # skip otherwise.
                    continue

                # fire and forget task.
                task = loop.create_task(
                    delivery_destination(
                        database,
                        engagement,
                        audience[db_c.OBJECT_ID],
                        destination[db_c.OBJECT_ID],
                    )
                )
                loop.run_until_complete(task)


def run_scheduled_destination_checks(database: MongoClient) -> None:
    """function to run scheduled destination validations.

    Args:
        database (MongoClient): The mongo database client.

    """

    # set the event loop
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    loop = asyncio.get_event_loop()
    error_count = 0
    for destination in get_all_delivery_platforms(database, enabled=True):
        connector = get_delivery_platform_connector(
            destination[api_c.DELIVERY_PLATFORM_TYPE],
            destination[api_c.AUTHENTICATION_DETAILS],
        )
        if connector is not None:
            try:
                # fire and forget task.
                task = loop.create_task(connector)
                loop.run_until_complete(task)
            # pylint: disable=broad-except
            except Exception as exception:
                error_count += 1
                logger.error(
                    "%s: %s while connecting to destination %s.",
                    exception.__class__,
                    str(exception),
                    destination[api_c.DELIVERY_PLATFORM_TYPE],
                )
                destination[db_c.DELIVERY_PLATFORM_STATUS] = db_c.STATUS_FAILED

                # create JIRA ticket for the request.
                JiraConnection().create_jira_issue(
                    api_c.TASK,
                    f"Removing Destination '{destination[api_c.NAME]}'.",
                    "\n".join(
                        f"{key.title()}: {value}"
                        for key, value in destination.items()
                    ),
                )

                # Sending Notification
                create_notification(
                    database,
                    db_c.NOTIFICATION_TYPE_CRITICAL,
                    (
                        f"Destination {destination[api_c.NAME]} connection got error"
                    ),
                    db_c.NOTIFICATION_CATEGORY_AUDIENCES,
                    api_c.UNIFIED_OKTA_TEST_USER_NAME,
                )

                destination_management.update_delivery_platform(
                    database=database,
                    delivery_platform_id=destination[db_c.ID],
                    name=destination[db_c.DELIVERY_PLATFORM_NAME],
                    delivery_platform_type=destination[
                        db_c.DELIVERY_PLATFORM_TYPE
                    ],
                    status=api_c.STATUS_ERROR,
                    deleted=True,
                )
                error_alert_doc = collection_management.get_document(
                    database=database,
                    collection=db_c.CONFIGURATIONS_COLLECTION,
                    query_filter={api_c.TYPE: api_c.ERROR_ALERTS},
                )

                collection_management.update_document(
                    database=database,
                    collection=db_c.CONFIGURATIONS_COLLECTION,
                    document_id=error_alert_doc[db_c.ID],
                    update_doc={
                        api_c.MODULES: {
                            api_c.DESTINATIONS: True,
                            api_c.MODELS: error_alert_doc[api_c.MODULES][
                                api_c.MODELS
                            ],
                            api_c.DATASOURCES: error_alert_doc[api_c.MODULES][
                                api_c.DATASOURCES
                            ],
                        }
                    },
                )

    if error_count == 0:
        error_alert_doc = collection_management.get_document(
            database=database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            query_filter={api_c.TYPE: api_c.ERROR_ALERTS},
        )

        collection_management.update_document(
            database=database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            document_id=error_alert_doc[db_c.ID],
            update_doc={
                api_c.MODULES: {
                    api_c.DESTINATIONS: False,
                    api_c.MODELS: error_alert_doc[api_c.MODULES][api_c.MODELS],
                    api_c.DATASOURCES: error_alert_doc[api_c.MODULES][
                        api_c.DATASOURCES
                    ],
                }
            },
        )


def run_scheduled_customer_profile_audience_count(
    database: MongoClient,
) -> None:
    """Function to run scheduled customer profile audience count refresh.

    Args:
        database (MongoClient): The mongo database client.
    """

    # get the current environment's okta user bearer token
    okta_access_token = get_env_okta_user_bearer_token()

    if okta_access_token:
        # get all audiences from audiences collection
        audiences = get_all_audiences(database=database)

        # get the cdp customers count for each of the audiences using async
        # method
        audience_size_dict = get_customers_count_async(
            okta_access_token, audiences
        )

        # iterate through each audience to update the size of the corresponding
        # audience in audiences collection
        for audience in audiences:
            collection_management.update_document(
                database=database,
                collection=db_c.AUDIENCES_COLLECTION,
                document_id=audience[db_c.ID],
                update_doc={
                    db_c.SIZE: audience_size_dict.get(audience[db_c.ID])
                },
                username=audience[db_c.UPDATED_BY],
            )
    else:
        logger.error(
            "Failed to run scheduled customer profile audience count for each "
            "audience since failed to obtain get env okta user access bearer "
            "token."
        )


async def cache_customer_overview_audience_insights(
    database: MongoClient, okta_access_token: str, audience_filters: dict
) -> None:
    """Fetch and cache customer overview audience insights for the audience
    filters.

    Args:
        database (MongoClient): The mongo database client.
        okta_access_token (str): OKTA JWT Token.
        audience_filters (dict): Audience filters of an audience.
    """

    data = get_customers_overview(
        token=okta_access_token,
        filters={api_c.AUDIENCE_FILTERS: audience_filters},
    )

    cache_key = {
        api_c.ENDPOINT: f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.OVERVIEW}",
        **{api_c.AUDIENCE_FILTERS: audience_filters},
    }

    create_cache_entry(
        database=database,
        cache_key=cache_key,
        cache_value=data,
    )


def run_scheduled_customer_overview_audience_insights(
    database: MongoClient,
) -> None:
    """Function to run scheduled customer overview audience insights cache
    refresh.

    Args:
        database (MongoClient): The mongo database client.
    """

    # get the current environment's okta user bearer token
    okta_access_token = get_env_okta_user_bearer_token()

    if okta_access_token:
        # set the event loop
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        loop = asyncio.get_event_loop()

        # get all audiences from audiences collection
        audiences = get_all_audiences(database=database)

        # iterate through the audiences to refresh the cache for customer
        # overview audience insights for each unique type of filters in each
        # audience document of audiences collection
        for audience in audiences:
            cache_key = {
                api_c.ENDPOINT: f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.OVERVIEW}",
                **{
                    api_c.AUDIENCE_FILTERS: audience.get(
                        api_c.AUDIENCE_FILTERS, None
                    )
                },
            }

            # check if cache data for matching key is not expired and present
            # in DB before proceeding further to cache new data
            cache_data = get_cache_entry(
                database=database, cache_key=cache_key
            )

            if not cache_data:
                # fire and forget task
                task = loop.create_task(
                    cache_customer_overview_audience_insights(
                        database,
                        okta_access_token,
                        audience.get(api_c.AUDIENCE_FILTERS, None),
                    )
                )
                loop.run_until_complete(task)
    else:
        logger.error(
            "Failed to run scheduled customer overview audience insights cache"
            " refresh for each since failed to obtain get env okta user access"
            " bearer token."
        )


async def cache_trust_id_comparison_insights(
    database: MongoClient, segment_filter: list
) -> None:
    """Fetch and cache trust id comparison insights for the segment
    filters.

    Args:
        database (MongoClient): The mongo database client.
        segment_filter (list): Segment Filters.
    """

    comparison_data = get_trust_id_comparison_data_by_segment(
        database, segment_filter
    )

    cache_key = {
        api_c.ENDPOINT: f"{api_c.TRUST_ID_TAG}.{api_c.COMPARISON}",
        **{api_c.TRUST_ID_SEGMENT_FILTERS: segment_filter},
    }

    create_cache_entry(
        database=database,
        cache_key=cache_key,
        cache_value=comparison_data,
    )


def run_scheduled_trust_id_comparison_insights(
    database: MongoClient,
) -> None:
    """Function to run scheduled trust id comparison insights.

    Args:
        database (MongoClient): The mongo database client.
    """

    # # get the current environment's okta user bearer token
    # okta_access_token = get_env_okta_user_bearer_token()

    # if okta_access_token:
    #     # set the event loop
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    loop = asyncio.get_event_loop()

    # get all distinct trust id segment filters
    segment_filters = get_all_distinct_segment_filters(database=database)

    # add default filter
    segment_filters.append([])

    # iterate through the segment filters to refresh the cache for trust id
    # comparison insights for each unique type of filters
    for segment_filter in segment_filters:
        cache_key = {
            api_c.ENDPOINT: f"{api_c.TRUST_ID_TAG}.{api_c.COMPARISON}",
            **{api_c.TRUST_ID_SEGMENT_FILTERS: segment_filter},
        }

        # check if cache data for matching key is not expired and present
        # in DB before proceeding further to cache new data
        cache_data = get_cache_entry(database=database, cache_key=cache_key)

        if not cache_data:
            # fire and forget task
            task = loop.create_task(
                cache_trust_id_comparison_insights(
                    database,
                    segment_filter,
                )
            )
            loop.run_until_complete(task)
