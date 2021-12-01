"""Purpose of this module is to park schedule modules for delivery schedule"""
import asyncio
from datetime import datetime
from pymongo import MongoClient
from huxunifylib.database import constants as db_c
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database.engagement_management import get_engagements
from huxunifylib.database.delivery_platform_management import (
    get_delivery_platform,
)
from huxunifylib.database.orchestration_management import get_audience
from huxunifylib.util.general.logging import logger
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import get_next_schedule
from huxunify.api.data_connectors.courier import (
    get_destination_config,
    get_audience_destination_pairs,
)


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
        cron_exp["day_of_month"] = ",".join(schedule.get("day_of_month"))
        if schedule["every"] > 1:
            cron_exp["month"] = f"{cron_exp['month']}/{schedule['every']}"
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
            api_c.DELIVERY_TAG,
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
            api_c.DELIVERY_TAG,
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
            database, engagement[db_c.ID], *pair
        )
        batch_destination.register(engagement)
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
        api_c.DELIVERY_TAG,
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

    # get engagements
    for engagement in get_engagements(database):

        # process audiences
        for audience in engagement.get(api_c.AUDIENCES):

            # process each destination
            for destination in audience.get(api_c.DESTINATIONS):
                if not isinstance(destination, dict) or not destination.get(
                    api_c.DELIVERY_SCHEDULE
                ):
                    continue

                # check if the schedule falls within the cron time frame.
                next_schedule = get_next_schedule(
                    generate_cron(destination.get(api_c.DELIVERY_SCHEDULE)),
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
