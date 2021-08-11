# pylint: disable=no-self-use, C0302
"""
Paths for delivery API
"""
from http import HTTPStatus
from random import uniform
from typing import Tuple
from bson import ObjectId
from flask import Blueprint, jsonify
from flasgger import SwaggerView
from huxunifylib.util.general.logging import logger
from huxunifylib.database import (
    constants as db_c,
    delivery_platform_management,
)
from huxunifylib.database.delivery_platform_management import (
    get_delivery_platform,
)
from huxunifylib.database.engagement_management import (
    get_engagement,
    get_engagements_by_audience,
)
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database.orchestration_management import (
    get_audience,
    get_all_audiences,
)

from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    api_error_handler,
    secured,
    validate_delivery_params,
    validate_destination,
)
from huxunify.api.schema.orchestration import (
    EngagementDeliveryHistorySchema,
    AudienceDeliveryHistorySchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.courier import (
    get_destination_config,
    get_audience_destination_pairs,
)


delivery_bp = Blueprint("/", import_name=__name__)


@delivery_bp.before_request
@secured()
def before_request():
    """Protect all of the engagement endpoints."""
    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    delivery_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/"
    f"{api_c.AUDIENCE}/<audience_id>/{api_c.DESTINATION}/<destination_id>/{api_c.DELIVER}",
    "EngagementDeliverDestinationView",
)
class EngagementDeliverDestinationView(SwaggerView):
    """
    Engagement audience destination delivery class
    """

    parameters = [
        {
            "name": api_c.ENGAGEMENT_ID,
            "description": "Engagement ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Result.",
            "schema": {
                "example": {"message": "Delivery job created."},
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to deliver engagement.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DELIVERY_TAG]

    # pylint: disable=no-self-use
    # pylint: disable=too-many-return-statements
    @api_error_handler()
    @validate_destination()
    @validate_delivery_params
    def post(
        self, engagement_id: str, audience_id: str, destination_id: str
    ) -> Tuple[dict, int]:
        """Delivers one destination for an engagement audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement ID.
            audience_id (str): Audience ID.
            destination_id (str): Destination ID.

        Returns:
            Tuple[dict, int]: Message indicating connection
                success/failure, HTTP Status.

        """
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        target_audience = get_audience(database, audience_id)
        target_destination = get_delivery_platform(database, destination_id)

        # validate that the destination ID is attached to the audience
        valid_destination = False
        for audience in engagement[db_c.AUDIENCES]:
            for destination in audience[db_c.DESTINATIONS]:
                if isinstance(
                    destination, dict
                ) and destination_id == destination.get(db_c.OBJECT_ID):
                    valid_destination = True

        if not valid_destination:
            logger.error(
                "Destination is not attached to the engagement %s  audience %s.",
                engagement_id,
                audience_id,
            )
            return {
                "message": "Destination is not attached to the "
                "engagement audience."
            }, HTTPStatus.BAD_REQUEST

        database = get_db_client()
        delivery_job_ids = []
        for pair in get_audience_destination_pairs(
            engagement[api_c.AUDIENCES]
        ):
            if [pair[0], pair[1][db_c.OBJECT_ID]] != [
                audience_id,
                destination_id,
            ]:
                continue
            batch_destination = get_destination_config(
                database, engagement_id, *pair
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
                f"Successfully scheduled a delivery of audience "
                f'"{target_audience[db_c.NAME]}" from engagement '
                f'"{engagement[db_c.NAME]}" to destination '
                f'"{target_destination[db_c.NAME]}".'
            ),
            api_c.DELIVERY_TAG,
        )
        return {
            "message": f"Successfully created delivery job(s) "
            f"{','.join(delivery_job_ids)}"
        }, HTTPStatus.OK


@add_view_to_blueprint(
    delivery_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/{api_c.AUDIENCE}/<audience_id>/{api_c.DELIVER}",
    "EngagementDeliverAudienceView",
)
class EngagementDeliverAudienceView(SwaggerView):
    """
    Engagement audience delivery class
    """

    parameters = [
        {
            "name": api_c.ENGAGEMENT_ID,
            "description": "Engagement ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Result.",
            "schema": {
                "example": {"message": "Delivery job created."},
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to deliver engagement.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": api_c.ENGAGEMENT_NOT_FOUND
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DELIVERY_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @validate_delivery_params
    def post(self, engagement_id: str, audience_id: str) -> Tuple[dict, int]:
        """Delivers one audience for an engagement.
        ---
        security:
            - Bearer: ["Authorization"]
        Args:
            engagement_id (str): Engagement ID.
            audience_id (str): Audience ID.
        Returns:
            Tuple[dict, int]: Message indicating connection
                success/failure, HTTP Status.
        """
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        audience = get_audience(database, audience_id)

        # submit jobs for the audience/destination pairs
        delivery_job_ids = []
        for pair in get_audience_destination_pairs(
            engagement[api_c.AUDIENCES]
        ):
            if pair[0] != audience_id:
                continue
            batch_destination = get_destination_config(
                database, engagement_id, *pair
            )
            batch_destination.register(engagement)
            batch_destination.submit()
            delivery_job_ids.append(
                str(batch_destination.audience_delivery_job_id)
            )
        # create notification
        logger.info(
            "Successfully created delivery jobs %s.",
            ",".join(delivery_job_ids),
        )
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f"Successfully scheduled a delivery of "
                f'audience "{audience[db_c.NAME]}" from engagement '
                f'"{engagement[db_c.NAME]}" across platforms.'
            ),
            api_c.DELIVERY_TAG,
        )
        return {
            "message": f"Successfully created delivery job(s) "
            f"{','.join(delivery_job_ids)}"
        }, HTTPStatus.OK


@add_view_to_blueprint(
    delivery_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/{api_c.DELIVER}",
    "EngagementDeliverView",
)
class EngagementDeliverView(SwaggerView):
    """
    Engagement delivery class
    """

    parameters = [
        {
            "name": api_c.ENGAGEMENT_ID,
            "description": "Engagement ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "60bfeaa3fa9ba04689906f7a",
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Delivery job created.",
            "schema": {
                "example": {"message": "Delivery job created."},
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to deliver engagement.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": api_c.ENGAGEMENT_NOT_FOUND
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DELIVERY_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @validate_delivery_params
    def post(self, engagement_id: str) -> Tuple[dict, int]:
        """Delivers all audiences for an engagement.
        ---
        security:
            - Bearer: ["Authorization"]
        Args:
            engagement_id (str): Engagement ID.
        Returns:
            Tuple[dict, int]: Message indicating connection
                success/failure, HTTP Status.
        """

        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        # submit jobs for all the audience/destination pairs
        delivery_job_ids = []

        for pair in get_audience_destination_pairs(
            engagement[api_c.AUDIENCES]
        ):
            batch_destination = get_destination_config(
                database, engagement_id, *pair
            )
            batch_destination.register(engagement)
            batch_destination.submit()
            delivery_job_ids.append(
                str(batch_destination.audience_delivery_job_id)
            )
        # create notification
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f"Successfully scheduled a delivery of all audiences "
                f'from engagement "{engagement[db_c.NAME]}".'
            ),
            api_c.DELIVERY_TAG,
        )
        logger.info(
            "Successfully created delivery jobs %s.",
            ",".join(delivery_job_ids),
        )
        return {
            "message": f"Successfully created delivery job(s) "
            f"{','.join(delivery_job_ids)}"
        }, HTTPStatus.OK


@add_view_to_blueprint(
    delivery_bp,
    f"{api_c.AUDIENCE_ENDPOINT}/<audience_id>/deliver",
    "AudienceDeliverView",
)
class AudienceDeliverView(SwaggerView):
    """
    Audience delivery class
    """

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Result.",
            "schema": {
                "example": {"message": "Delivery job created."},
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to deliver audience.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DELIVERY_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @validate_delivery_params
    def post(self, audience_id: str) -> Tuple[dict, int]:
        """Delivers an audience for all of the engagements it is apart of.
        ---
        security:
            - Bearer: ["Authorization"]
        Args:
            audience_id (str): Audience ID.
        Returns:
            Tuple[dict, int]: Message indicating connection
                success/failure, HTTP Status.
        """

        database = get_db_client()
        # get audience
        audience = get_audience(database, audience_id)
        # get engagements
        engagements = get_engagements_by_audience(database, audience_id)
        # submit jobs for the audience/destination pairs
        delivery_job_ids = []
        for engagement in engagements:
            for pair in get_audience_destination_pairs(
                engagement[api_c.AUDIENCES]
            ):
                if pair[0] != audience_id:
                    continue
                batch_destination = get_destination_config(
                    database, engagement[db_c.ID], *pair
                )
                batch_destination.register(engagement)
                batch_destination.submit()
                delivery_job_ids.append(
                    str(batch_destination.audience_delivery_job_id)
                )
        # create notification
        logger.info(
            "Successfully created delivery jobs %s.",
            ",".join(delivery_job_ids),
        )
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f"Successfully scheduled a delivery of audience "
                f'"{audience[db_c.NAME]}".'
            ),
            api_c.DELIVERY_TAG,
        )
        return {
            "message": f"Successfully created delivery job(s) for audience ID {audience_id}"
        }, HTTPStatus.OK


@add_view_to_blueprint(
    delivery_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/{api_c.DELIVERY_HISTORY}",
    "EngagementDeliverHistoryView",
)
class EngagementDeliverHistoryView(SwaggerView):
    """
    Engagement delivery history class
    """

    parameters = [
        {
            "name": api_c.ENGAGEMENT_ID,
            "description": "Engagement ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "60bfeaa3fa9ba04689906f7a",
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Successfully fetched delivery history.",
            "schema": {
                "type": "array",
                "items": EngagementDeliveryHistorySchema,
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to show deliver history.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": api_c.ENGAGEMENT_NOT_FOUND
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DELIVERY_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self, engagement_id: str) -> Tuple[dict, int]:
        """Delivery history of all audiences for an engagement.
        ---
        security:
            - Bearer: ["Authorization"]
        Args:
            engagement_id (str): Engagement ID.
        Returns:
            Tuple[dict, int]: Delivery history, HTTP Status.
        """

        # validate object id
        if not ObjectId.is_valid(engagement_id):
            logger.error("Invalid Object ID %s.", engagement_id)
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        # convert the engagement ID
        engagement_id = ObjectId(engagement_id)

        # check if engagement exists
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        if not engagement:
            logger.error("Engagement with ID %s not found.", engagement_id)
            return {
                "message": api_c.ENGAGEMENT_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        delivery_jobs = (
            delivery_platform_management.get_delivery_jobs_using_metadata(
                database, engagement_id=engagement_id
            )
        )

        # extract delivery platform ids from the engaged audiences
        destination_ids = [
            z.get(api_c.ID)
            for x in engagement[api_c.AUDIENCES]
            for z in x[api_c.DESTINATIONS]
            if isinstance(z, dict)
        ]

        # get destinations at once to lookup name for each delivery job
        destination_dict = {
            x[db_c.ID]: x
            for x in delivery_platform_management.get_delivery_platforms_by_id(
                database, destination_ids
            )
        }

        # get audiences at once to lookup name for each delivery job
        audience_dict = {x[db_c.ID]: x for x in get_all_audiences(database)}

        delivery_history = []
        for job in delivery_jobs:
            if (
                job.get(db_c.STATUS) == db_c.AUDIENCE_STATUS_DELIVERED
                and job.get(api_c.AUDIENCE_ID)
                and job.get(db_c.DELIVERY_PLATFORM_ID)
            ):
                # append the necessary schema to the response list.
                delivery_history.append(
                    {
                        api_c.AUDIENCE: audience_dict.get(
                            job.get(db_c.AUDIENCE_ID)
                        ),
                        api_c.DESTINATION: destination_dict.get(
                            job.get(db_c.DELIVERY_PLATFORM_ID)
                        ),
                        api_c.SIZE: job.get(
                            db_c.DELIVERY_PLATFORM_AUD_SIZE, 0
                        ),
                        # TODO: HUS-837 Change once match_rate data can be fetched from CDM
                        api_c.MATCH_RATE: round(uniform(0.2, 0.9), 2),
                        api_c.DELIVERED: job.get(db_c.UPDATE_TIME),
                    }
                )

        return (
            jsonify(
                EngagementDeliveryHistorySchema().dump(
                    delivery_history, many=True
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    delivery_bp,
    f"{api_c.AUDIENCE_ENDPOINT}/<audience_id>/{api_c.DELIVERY_HISTORY}",
    "AudienceDeliverHistoryView",
)
class AudienceDeliverHistoryView(SwaggerView):
    """
    Audience delivery history class
    """

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "60bfeaa3fa9ba04689906f7a",
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Successfully fetched delivery history.",
            "schema": {
                "type": "array",
                "items": AudienceDeliveryHistorySchema,
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to show deliver history.",
        },
        HTTPStatus.NOT_FOUND.value: {"description": api_c.AUDIENCE_NOT_FOUND},
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DELIVERY_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self, audience_id: str) -> Tuple[dict, int]:
        """Retrieves delivery history of an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.

        Returns:
            Tuple[dict, int]: Delivery history, HTTP Status.

        """

        # validate object id
        if not ObjectId.is_valid(audience_id):
            logger.error("Invalid Object ID %s.", audience_id)
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        # convert the audience ID
        audience_id = ObjectId(audience_id)

        # check if audience exists
        database = get_db_client()
        audience = get_audience(database, audience_id)
        if not audience:
            logger.error("Audience with ID %s not found.", audience_id)
            return {"message": api_c.AUDIENCE_NOT_FOUND}, HTTPStatus.NOT_FOUND

        delivery_jobs = (
            delivery_platform_management.get_delivery_jobs_using_metadata(
                database, audience_id=audience_id
            )
        )

        # get destinations at once to lookup name for each delivery job
        destination_dict = {
            x[db_c.ID]: x
            for x in delivery_platform_management.get_all_delivery_platforms(
                database
            )
        }

        # get engagements ahead of time by the audience
        engagement_dict = {
            x[db_c.ID]: x
            for x in get_engagements_by_audience(database, audience_id)
        }

        delivery_history = []
        for job in delivery_jobs:
            if (
                job.get(db_c.STATUS) == db_c.AUDIENCE_STATUS_DELIVERED
                and job.get(api_c.ENGAGEMENT_ID)
                and job.get(db_c.DELIVERY_PLATFORM_ID)
            ):

                delivery_history.append(
                    {
                        api_c.ENGAGEMENT: engagement_dict.get(
                            job.get(db_c.ENGAGEMENT_ID)
                        ),
                        api_c.DESTINATION: destination_dict.get(
                            job.get(db_c.DELIVERY_PLATFORM_ID)
                        ),
                        api_c.SIZE: job.get(
                            db_c.DELIVERY_PLATFORM_AUD_SIZE, 0
                        ),
                        # TODO: HUS-837 Change once match_rate data can be fetched from CDM
                        api_c.MATCH_RATE: round(uniform(0.2, 0.9), 2),
                        api_c.DELIVERED: job.get(db_c.UPDATE_TIME),
                    }
                )

        return (
            jsonify(
                AudienceDeliveryHistorySchema().dump(
                    delivery_history, many=True
                )
            ),
            HTTPStatus.OK,
        )
