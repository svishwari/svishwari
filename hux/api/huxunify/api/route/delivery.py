# pylint: disable=no-self-use, C0302
"""
Paths for delivery API
"""
from http import HTTPStatus
from random import randrange
from typing import Tuple
from bson import ObjectId
from flask import Blueprint, jsonify
from flasgger import SwaggerView
from huxunifylib.database import constants as db_c, engagement_management
from huxunifylib.database import (
    orchestration_management,
    delivery_platform_management,
)
from huxunifylib.database.engagement_management import get_engagement
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    api_error_handler,
    secured,
    validate_delivery_params,
    validate_destination_wrapper,
)
from huxunify.api.schema.orchestration import DeliveryHistorySchema
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
    @validate_destination_wrapper()
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

        # validate that the destination ID is attached to the audience
        valid_destination = False
        for audience in engagement[db_c.AUDIENCES]:
            for destination in audience[db_c.DESTINATIONS]:
                if destination_id == destination[db_c.OBJECT_ID]:
                    valid_destination = True

        if not valid_destination:
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
            batch_destination.register()
            batch_destination.submit()
            delivery_job_ids.append(
                str(batch_destination.audience_delivery_job_id)
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
            batch_destination.register()
            batch_destination.submit()
            delivery_job_ids.append(
                str(batch_destination.audience_delivery_job_id)
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
            batch_destination.register()
            batch_destination.submit()
            delivery_job_ids.append(
                str(batch_destination.audience_delivery_job_id)
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
        # get engagements
        engagements = engagement_management.get_engagements_by_audience(
            database, audience_id
        )
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
                batch_destination.register()
                batch_destination.submit()
                delivery_job_ids.append(
                    str(batch_destination.audience_delivery_job_id)
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
            "schema": {"type": "array", "items": DeliveryHistorySchema},
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
    @validate_delivery_params
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
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        # convert the engagement ID
        engagement_id = ObjectId(engagement_id)

        # check if engagement exists
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        if not engagement:
            return {
                "message": api_c.ENGAGEMENT_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        delivery_jobs = (
            delivery_platform_management.get_delivery_jobs_using_metadata(
                database, engagement_id=engagement_id
            )
        )
        delivery_history = []
        for job in delivery_jobs:
            if (
                job.get(db_c.STATUS) == db_c.STATUS_SUCCEEDED
                and job.get(api_c.AUDIENCE_ID)
                and job.get(db_c.DELIVERY_PLATFORM_ID)
            ):
                delivery_history.append(
                    {
                        api_c.AUDIENCE: orchestration_management.get_audience(
                            database, job.get(api_c.AUDIENCE_ID)
                        ),
                        api_c.DESTINATION: delivery_platform_management.get_delivery_platform(
                            database, job.get(db_c.DELIVERY_PLATFORM_ID)
                        ),
                        # TODO : Get audience size from CDM
                        api_c.SIZE: randrange(10000000),
                        api_c.DELIVERED: job.get(db_c.JOB_END_TIME),
                    }
                )

        return (
            jsonify(DeliveryHistorySchema().dump(delivery_history, many=True)),
            HTTPStatus.OK,
        )
