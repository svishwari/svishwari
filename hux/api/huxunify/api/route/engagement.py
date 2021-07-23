# pylint: disable=no-self-use, C0302
"""
Paths for engagement API
"""
import logging
from http import HTTPStatus
from typing import Tuple
from itertools import groupby
from operator import itemgetter

from bson import ObjectId
from flask import Blueprint, request, jsonify
from flasgger import SwaggerView

from huxunifylib.connectors import FacebookConnector
from huxunifylib.database import constants as db_c
from huxunifylib.database.engagement_management import (
    get_engagement,
    get_engagements_summary,
    set_engagement,
    delete_engagement,
    update_engagement,
    remove_audiences_from_engagement,
    append_audiences_to_engagement,
)
from huxunifylib.database.orchestration_management import get_audience
from huxunifylib.database import (
    orchestration_management,
    delivery_platform_management,
)
from huxunifylib.database.delivery_platform_management import (
    get_performance_metrics_by_engagement_details,
    get_delivery_jobs_using_metadata,
)
from huxunify.api.schema.engagement import (
    EngagementPostSchema,
    EngagementGetSchema,
    AudienceEngagementSchema,
    AudienceEngagementDeleteSchema,
    AudiencePerformanceDisplayAdsSchema,
    AudiencePerformanceEmailSchema,
    CampaignSchema,
    CampaignMappingSchema,
    CampaignPutSchema,
    weighted_engagement_status,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
    api_error_handler,
    get_user_name,
    group_perf_metric,
    update_metrics,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.aws import get_auth_from_parameter_store

engagement_bp = Blueprint(api_c.ENGAGEMENT_ENDPOINT, import_name=__name__)


# TODO Add updated_by fields to engagement_mgmt in set, update and delete methods
@engagement_bp.before_request
@secured()
def before_request():
    """Protect all of the engagement endpoints."""
    pass  # pylint: disable=unnecessary-pass


# pylint: disable=too-many-locals
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
            logging.warning(
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
                logging.warning(
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
            #  Group performance metrics for the destination
            destination_metrics = update_metrics(
                destination_id,
                delivery_platform_management.get_delivery_platform(
                    database, destination_id
                )[api_c.NAME],
                audience_destination_jobs,
                performance_metrics,
                metrics_type,
            )
            audience_destination_metrics_list.append(destination_metrics)
            # TODO : HUS-796 - Group performance metrics by campaigns
        audience_metrics[
            api_c.DESTINATIONS
        ] = audience_destination_metrics_list
        audience_metrics_list.append(audience_metrics)

    return audience_metrics_list


@add_view_to_blueprint(
    engagement_bp, f"{api_c.ENGAGEMENT_ENDPOINT}", "EngagementSearch"
)
class EngagementSearch(SwaggerView):
    """
    Engagement Search Class
    """

    parameters = []
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of engagements.",
            "schema": {"type": "array", "items": EngagementGetSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    def get(self) -> Tuple[dict, int]:
        """Retrieves all engagements.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:

        Returns:
            Tuple[dict, int]: dict of engagements and http code

        """

        # get the engagement summary
        engagements = get_engagements_summary(get_db_client())

        # weight the engagement status
        engagements = weighted_engagement_status(engagements)

        return (
            jsonify(EngagementGetSchema().dump(engagements, many=True)),
            HTTPStatus.OK.value,
        )


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>",
    "IndividualEngagementSearch",
)
class IndividualEngagementSearch(SwaggerView):
    """
    Individual Engagement Search Class
    """

    parameters = [
        {
            "name": db_c.ENGAGEMENT_ID,
            "description": "Engagement ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve Individual Engagement",
            "schema": EngagementGetSchema,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    def get(self, engagement_id: str) -> Tuple[dict, int]:
        """Retrieves an engagement.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): id of the engagement

        Returns:
            Tuple[dict, int]: dict of the engagement and http code

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        # get the engagement summary
        engagements = get_engagements_summary(
            get_db_client(), [ObjectId(engagement_id)]
        )

        if not engagements:
            return {"message": "Not found"}, HTTPStatus.NOT_FOUND.value

        # weight the engagement status
        engagements = weighted_engagement_status(engagements)[0]

        return (
            EngagementGetSchema().dump(engagements),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    engagement_bp, f"{api_c.ENGAGEMENT_ENDPOINT}", "SetEngagement"
)
class SetEngagement(SwaggerView):
    """
    Class to create a new engagement
    """

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input engagement body.",
            "example": {
                db_c.ENGAGEMENT_NAME: "My Engagement",
                db_c.ENGAGEMENT_DESCRIPTION: "Engagement Description",
                db_c.AUDIENCES: [
                    {
                        api_c.ID: "60ae035b6c5bf45da27f17d6",
                        api_c.DESTINATIONS: [
                            {
                                api_c.ID: "60ae035b6c5bf45da27f17e5",
                                db_c.DELIVERY_PLATFORM_CONFIG: {
                                    db_c.DATA_EXTENSION_NAME: "SFMC Test Audience"
                                },
                            },
                            {
                                api_c.ID: "60ae035b6c5bf45da27f17e6",
                            },
                        ],
                    }
                ],
            },
        }
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": EngagementGetSchema,
            "description": "Engagement created.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create the engagement.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    @get_user_name()
    def post(self, user_name: str) -> Tuple[dict, int]:
        """Creates a new engagement.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user_name (str): user_name extracted from Okta.

        Returns:
            Tuple[dict, int]: Engagement created, HTTP status.

        """

        body = EngagementPostSchema().load(
            request.get_json(), partial=("delivery_schedule",)
        )

        engagement_id = set_engagement(
            database=get_db_client(),
            name=body[db_c.ENGAGEMENT_NAME],
            description=body[db_c.ENGAGEMENT_DESCRIPTION]
            if db_c.ENGAGEMENT_DESCRIPTION in body
            else None,
            audiences=body[db_c.AUDIENCES] if db_c.AUDIENCES in body else None,
            delivery_schedule=body[db_c.ENGAGEMENT_DELIVERY_SCHEDULE]
            if db_c.ENGAGEMENT_DELIVERY_SCHEDULE in body
            else None,
            user_name=user_name,
        )

        return (
            EngagementGetSchema().dump(
                get_engagement(get_db_client(), engagement_id=engagement_id)
            ),
            HTTPStatus.CREATED,
        )


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>",
    "UpdateEngagement",
)
class UpdateEngagement(SwaggerView):
    """
    Class to update an engagement
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
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input engagement body.",
            "example": {
                db_c.ENGAGEMENT_NAME: "My Engagement",
                db_c.ENGAGEMENT_DESCRIPTION: "Engagement Description",
                db_c.AUDIENCES: [
                    {
                        api_c.ID: "60ae035b6c5bf45da27f17d6",
                        api_c.DESTINATIONS: [
                            {
                                api_c.ID: "60ae035b6c5bf45da27f17e5",
                            },
                            {
                                api_c.ID: "60ae035b6c5bf45da27f17e6",
                            },
                        ],
                    }
                ],
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": EngagementGetSchema,
            "description": "Engagement updated.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update the engagement.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    @get_user_name()
    def put(self, engagement_id: str, user_name: str) -> Tuple[dict, int]:
        """Updates an engagement.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement id
            user_name (str): user_name extracted from Okta.

        Returns:
            Tuple[dict, int]: Engagement updated, HTTP status.

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        body = EngagementPostSchema().load(request.get_json())

        engagement = update_engagement(
            database=get_db_client(),
            engagement_id=ObjectId(engagement_id),
            user_name=user_name,
            name=body[db_c.ENGAGEMENT_NAME],
            description=body[db_c.ENGAGEMENT_DESCRIPTION]
            if db_c.ENGAGEMENT_DESCRIPTION in body
            else None,
            audiences=body[db_c.AUDIENCES] if db_c.AUDIENCES in body else None,
            delivery_schedule=body[db_c.ENGAGEMENT_DELIVERY_SCHEDULE]
            if db_c.ENGAGEMENT_DELIVERY_SCHEDULE in body
            else {},
        )

        return (
            EngagementGetSchema().dump(engagement),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>",
    "DeleteEngagement",
)
class DeleteEngagement(SwaggerView):
    """
    Delete Engagement Class
    """

    parameters = [
        {
            "name": db_c.ENGAGEMENT_ID,
            "description": "Engagement ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Delete Individual Engagement",
            "schema": EngagementGetSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "schema": NotFoundError,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    def delete(self, engagement_id: str) -> Tuple[dict, int]:
        """Deletes an engagement.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement id

        Returns:
            Tuple[dict, int]: message, HTTP status

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        if delete_engagement(
            get_db_client(), engagement_id=ObjectId(engagement_id)
        ):
            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK.value

        return {
            "message": api_c.OPERATION_FAILED
        }, HTTPStatus.INTERNAL_SERVER_ERROR.value


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/{api_c.AUDIENCES}",
    "AddAudienceEngagement",
)
class AddAudienceEngagement(SwaggerView):
    """
    Class to add audience to an engagement
    """

    parameters = [
        {
            "name": db_c.ENGAGEMENT_ID,
            "description": "Engagement ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Audience body.",
            "example": {
                api_c.AUDIENCES: [
                    {
                        api_c.ID: "60ae035b6c5bf45da27f17d6",
                        api_c.DESTINATIONS: [
                            {
                                api_c.ID: "60ae035b6c5bf45da27f17e5",
                            },
                            {
                                api_c.ID: "60ae035b6c5bf45da27f17e6",
                                db_c.DELIVERY_PLATFORM_CONFIG: {
                                    db_c.DATA_EXTENSION_NAME: "SFMC Test Audience"
                                },
                            },
                        ],
                    }
                ]
            },
        },
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": EngagementGetSchema,
            "description": "Audience added to Engagement.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create the engagement.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    @get_user_name()
    def post(self, engagement_id: str, user_name: str) -> Tuple[dict, int]:
        """Adds audience to engagement.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement id
            user_name (str): user_name extracted from Okta.

        Returns:
            Tuple[dict, int]: Audience Engagement added, HTTP status.

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        body = AudienceEngagementSchema().load(
            request.get_json(), partial=True
        )

        # validate audiences exist
        database = get_db_client()
        for audience in body[api_c.AUDIENCES]:
            if not get_audience(database, ObjectId(audience[api_c.ID])):
                return {
                    "message": f"Audience does not exist: {audience[api_c.ID]}"
                }, HTTPStatus.BAD_REQUEST

        append_audiences_to_engagement(
            database,
            ObjectId(engagement_id),
            user_name,
            body[api_c.AUDIENCES],
        )
        return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK.value


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/{api_c.AUDIENCES}",
    "DeleteAudienceEngagement",
)
class DeleteAudienceEngagement(SwaggerView):
    """
    Delete AudienceEngagement Class
    """

    parameters = [
        {
            "name": db_c.ENGAGEMENT_ID,
            "description": "Engagement ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input engagement body.",
            "example": {
                api_c.AUDIENCE_IDS: [
                    "60ae035b6c5bf45da27f17e5",
                    "60ae035b6c5bf45da27f17e6",
                ]
            },
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Delete Audience from Engagement.",
            "schema": EngagementGetSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "schema": NotFoundError,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    @get_user_name()
    def delete(self, engagement_id: str, user_name: str) -> Tuple[dict, int]:
        """Deletes audience from engagement.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement id
            user_name (str): user_name extracted from Okta.

        Returns:
            Tuple[dict, int]: Audience deleted from engagement, HTTP status

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        audience_ids = []
        body = AudienceEngagementDeleteSchema().load(
            request.get_json(), partial=True
        )
        for audience_id in body[api_c.AUDIENCE_IDS]:
            if not ObjectId.is_valid(audience_id):
                return HTTPStatus.BAD_REQUEST
            audience_ids.append(ObjectId(audience_id))

        remove_audiences_from_engagement(
            get_db_client(),
            ObjectId(engagement_id),
            user_name,
            audience_ids,
        )
        return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK.value


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/"
    f"{api_c.AUDIENCE}/<audience_id>/{api_c.DESTINATION}/<destination_id>/{api_c.CAMPAIGNS}",
    "UpdateCampaignsForAudience",
)
class UpdateCampaignsForAudience(SwaggerView):
    """
    Update campaigns for audience class
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
            "example": "8a8f7262997acad4bac4373b",
        },
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "77cf7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input engagement body.",
            "example": {
                api_c.CAMPAIGNS: [
                    {
                        api_c.NAME: "Test Campaign",
                        api_c.ID: "campaign_id",
                        api_c.DELIVERY_JOB_ID: "delivery_job_id",
                    },
                ]
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Result.",
            "schema": {
                "example": {"message": "Campaigns updated successfully."},
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update campaigns.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": api_c.ENGAGEMENT_NOT_FOUND
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CAMPAIGNS]

    # pylint: disable=no-self-use
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-locals
    # pylint: disable=# pylint: disable=too-many-branches
    @api_error_handler()
    def put(
        self, engagement_id: str, audience_id: str, destination_id: str
    ) -> Tuple[dict, int]:
        """Updates campaigns for an engagement audience.

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

        # validate object id
        if not all(
            ObjectId.is_valid(x)
            for x in [audience_id, engagement_id, destination_id]
        ):
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        # convert to ObjectIds
        engagement_id = ObjectId(engagement_id)
        audience_id = ObjectId(audience_id)
        destination_id = ObjectId(destination_id)

        # check if engagement exists
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        if not engagement:
            return {
                "message": api_c.ENGAGEMENT_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        # validate that the engagement has audiences
        if db_c.AUDIENCES not in engagement:
            return {
                "message": "Engagement has no audiences."
            }, HTTPStatus.BAD_REQUEST

        # validate that the audience is attached
        audience_ids = [x[db_c.OBJECT_ID] for x in engagement[db_c.AUDIENCES]]
        if audience_id not in audience_ids:
            return {
                "message": "Audience is not attached to the engagement."
            }, HTTPStatus.BAD_REQUEST

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

        # validate destination exists
        destination = delivery_platform_management.get_delivery_platform(
            database, destination_id
        )
        if not destination:
            return {
                "message": "Destination does not exist."
            }, HTTPStatus.BAD_REQUEST

        body = CampaignPutSchema().load(request.get_json())

        delivery_jobs = (
            delivery_platform_management.get_delivery_jobs_using_metadata(
                database, engagement_id, audience_id, destination_id
            )
        )
        if delivery_jobs is None:
            return {
                "message": "Could not attach campaigns."
            }, HTTPStatus.BAD_REQUEST

        # Delete all the existing campaigns from associated delivery jobs
        delivery_platform_management.delete_delivery_job_generic_campaigns(
            get_db_client(), [x[db_c.ID] for x in delivery_jobs]
        )

        # Group campaigns by Delivery job and update the list of campaigns for the delivery job
        campaigns = sorted(
            body[api_c.CAMPAIGNS], key=itemgetter(api_c.DELIVERY_JOB_ID)
        )
        for delivery_job_id, value in groupby(
            campaigns, key=itemgetter(api_c.DELIVERY_JOB_ID)
        ):
            delivery_job = delivery_platform_management.get_delivery_job(
                database, ObjectId(delivery_job_id)
            )
            if delivery_job is None and (
                delivery_job[api_c.ENGAGEMENT_ID] != engagement_id
            ):
                return {
                    "message": "Invalid data, cannot attach campaign."
                }, HTTPStatus.BAD_REQUEST

            updated_campaigns = [
                {k: v for k, v in d.items() if k in [api_c.NAME, api_c.ID]}
                for d in value
            ]
            delivery_platform_management.create_delivery_job_generic_campaigns(
                get_db_client(), ObjectId(delivery_job_id), updated_campaigns
            )

        return {"message": "Successfully attached campaigns."}, HTTPStatus.OK


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/"
    f"{api_c.AUDIENCE}/<audience_id>/{api_c.DESTINATION}/<destination_id>/{api_c.CAMPAIGNS}",
    "AudienceCampaignsGetView",
)
class AudienceCampaignsGetView(SwaggerView):
    """
    Audience campaigns GET class
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
            "example": "6f5f7262997acad4bac4373b",
        },
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "7f5f7262997acad4bac4373b",
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieved campaign details.",
            "schema": {"type": "array", "items": CampaignSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve campaigns.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": api_c.ENGAGEMENT_NOT_FOUND
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CAMPAIGNS]

    # pylint: disable=no-self-use
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    @api_error_handler()
    def get(
        self, engagement_id: str, audience_id: str, destination_id: str
    ) -> Tuple[dict, int]:
        """Get the campaign mappings from mongo.

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

        # validate object id
        if not all(
            ObjectId.is_valid(x)
            for x in [audience_id, engagement_id, destination_id]
        ):
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        # convert to ObjectIds
        engagement_id = ObjectId(engagement_id)
        audience_id = ObjectId(audience_id)
        destination_id = ObjectId(destination_id)

        # check if engagement exists
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        if not engagement:
            return {
                "message": api_c.ENGAGEMENT_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        # validate that the engagement has audiences
        if db_c.AUDIENCES not in engagement:
            return {
                "message": "Engagement has no audiences."
            }, HTTPStatus.BAD_REQUEST

        # validate that the audience is attached
        audience_ids = [x[db_c.OBJECT_ID] for x in engagement[db_c.AUDIENCES]]
        if audience_id not in audience_ids:
            return {
                "message": "Audience is not attached to the engagement."
            }, HTTPStatus.BAD_REQUEST

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

        # validate destination exists
        destination = delivery_platform_management.get_delivery_platform(
            database, destination_id
        )
        if not destination:
            return {
                "message": "Destination does not exist."
            }, HTTPStatus.BAD_REQUEST

        delivery_jobs = (
            delivery_platform_management.get_delivery_jobs_using_metadata(
                database, engagement_id, audience_id, destination_id
            )
        )
        if not delivery_jobs:
            return {
                "message": "Could not find any campaigns."
            }, HTTPStatus.BAD_REQUEST

        # Build response object
        campaigns = []
        for delivery_job in delivery_jobs:
            if delivery_job[db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS]:
                delivery_campaigns = delivery_job[
                    db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS
                ]
                for campaign in delivery_campaigns:
                    campaign[api_c.ID] = campaign[api_c.ID]
                    campaign[api_c.DELIVERY_JOB_ID] = delivery_job[db_c.ID]
                    campaign[db_c.CREATE_TIME] = delivery_job[db_c.CREATE_TIME]
                campaigns.extend(delivery_campaigns)

        return (
            jsonify(CampaignSchema().dump(campaigns, many=True)),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/"
    f"{api_c.AUDIENCE}/<audience_id>/{api_c.DESTINATION}/<destination_id>/campaign-mappings",
    "AudienceCampaignMappingsGetView",
)
class AudienceCampaignMappingsGetView(SwaggerView):
    """
    Audience campaign mappings class
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
            "example": "6f5f7262997acad4bac4373b",
        },
        {
            "name": api_c.DESTINATION_ID,
            "description": "Destination ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "7f5f7262997acad4bac4373b",
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieved campaign mappings.",
            "schema": {"type": "array", "items": CampaignMappingSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve campaign mappings.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": api_c.ENGAGEMENT_NOT_FOUND
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CAMPAIGNS]

    # pylint: disable=no-self-use
    # pylint: disable=too-many-return-statements
    @api_error_handler()
    def get(
        self, engagement_id: str, audience_id: str, destination_id: str
    ) -> Tuple[dict, int]:
        """Get the list of possible campaign mappings to attach to audience.

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

        # validate object id
        if not all(
            ObjectId.is_valid(x)
            for x in [audience_id, engagement_id, destination_id]
        ):
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        # convert to ObjectIds
        engagement_id = ObjectId(engagement_id)
        audience_id = ObjectId(audience_id)
        destination_id = ObjectId(destination_id)

        # check if engagement exists
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        if not engagement:
            return {
                "message": api_c.ENGAGEMENT_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        # validate that the engagement has audiences
        if db_c.AUDIENCES not in engagement:
            return {
                "message": "Engagement has no audiences."
            }, HTTPStatus.BAD_REQUEST

        # validate that the audience is attached
        audience_ids = [x[db_c.OBJECT_ID] for x in engagement[db_c.AUDIENCES]]
        if audience_id not in audience_ids:
            return {
                "message": "Audience is not attached to the engagement."
            }, HTTPStatus.BAD_REQUEST

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

        # validate destination exists
        destination = delivery_platform_management.get_delivery_platform(
            database, destination_id
        )
        if not destination:
            return {
                "message": "Destination does not exist."
            }, HTTPStatus.BAD_REQUEST

        # Get existing delivery jobs
        delivery_jobs = (
            delivery_platform_management.get_delivery_jobs_using_metadata(
                database, engagement_id, audience_id, destination_id
            )
        )
        if not delivery_jobs:
            return {
                "message": "Could not find any delivery jobs to map."
            }, HTTPStatus.BAD_REQUEST

        # Get existing campaigns from facebook
        facebook_connector = FacebookConnector(
            auth_details=get_auth_from_parameter_store(
                destination[api_c.AUTHENTICATION_DETAILS],
                destination[api_c.DELIVERY_PLATFORM_TYPE],
            )
        )

        campaigns = facebook_connector.get_campaigns()

        if campaigns is None:
            return {
                "message": "Could not find any Campaigns to map."
            }, HTTPStatus.BAD_REQUEST

        # Build response object
        campaign_schema = {
            "campaigns": list(campaigns),
            "delivery_jobs": delivery_jobs,
        }

        return CampaignMappingSchema().dump(campaign_schema), HTTPStatus.OK


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/"
    f"{api_c.AUDIENCE_PERFORMANCE}/"
    f"{api_c.DISPLAY_ADS}",
    "AudiencePerformanceDisplayAdsSchema",
)
class EngagementMetricsDisplayAds(SwaggerView):
    """
    Display Ads Engagement Metrics
    """

    parameters = [
        {
            "name": api_c.ENGAGEMENT_ID,
            "description": "Engagement ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "60b8d6d7d3cf80b4edcd890b",
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Display Ads Performance Metrics",
            "schema": {
                "example": {
                    "display_ads_summary": "Audience Metrics Display Ad"
                },
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve engagement metrics.",
        },
        HTTPStatus.NOT_FOUND.value: {
            "description": "Failed to find engagement or audience.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    def get(self, engagement_id: str) -> Tuple[dict, int]:
        """Retrieves display ad performance metrics.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): ID of an engagement

        Returns:
            Tuple[dict, int]: Response of Display Ads Performance Metrics,
                HTTP Status Code

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        # setup the database
        database = get_db_client()

        engagement = get_engagement(database, ObjectId(engagement_id))
        if not engagement:
            return {"message": "Engagement not found."}, HTTPStatus.NOT_FOUND

        # Get all destinations that are related to Display Ad metrics
        ads_destination = (
            delivery_platform_management.get_delivery_platform_by_type(
                database, db_c.DELIVERY_PLATFORM_FACEBOOK
            )
        )

        if not ads_destination:
            return {
                "message": "No performance metrics found for engagement."
            }, HTTPStatus.OK

        # Get Performance metrics by engagement and destination
        performance_metrics = get_performance_metrics_by_engagement_details(
            database,
            ObjectId(engagement_id),
            [ads_destination.get(db_c.ID)],
        )

        if not performance_metrics:
            return {
                "message": "No performance metrics found for engagement."
            }, HTTPStatus.OK

        # Get all the delivery jobs for the given engagement and destination
        delivery_jobs = get_delivery_jobs_using_metadata(
            database, engagement_id=ObjectId(engagement_id)
        )

        delivery_jobs = [
            x
            for x in delivery_jobs
            if x[db_c.DELIVERY_PLATFORM_ID] == ads_destination.get(db_c.ID)
        ]

        if not delivery_jobs:
            return {
                "message": "No performance metrics found for engagement."
            }, HTTPStatus.OK

        # Group all the performance metrics for the engagement
        final_metric = {
            api_c.SUMMARY: group_perf_metric(
                [x[db_c.PERFORMANCE_METRICS] for x in performance_metrics],
                api_c.DISPLAY_ADS,
            )
        }
        audience_metrics_list = group_engagement_performance_metrics(
            engagement,
            delivery_jobs,
            performance_metrics,
            [ads_destination.get(db_c.ID)],
            api_c.DISPLAY_ADS,
        )
        final_metric[api_c.AUDIENCE_PERFORMANCE_LABEL] = audience_metrics_list

        return (
            AudiencePerformanceDisplayAdsSchema().dump(final_metric),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<{api_c.ENGAGEMENT_ID}>/"
    f"{api_c.AUDIENCE_PERFORMANCE}/"
    f"{api_c.EMAIL}",
    "AudiencePerformanceEmailSchema",
)
class EngagementMetricsEmail(SwaggerView):
    """
    Email Engagement Metrics
    """

    parameters = [
        {
            "name": api_c.ENGAGEMENT_ID,
            "description": "Engagement ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "60b8d6d7d3cf80b4edcd890b",
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Email Audience Performance Metrics",
            "schema": {
                "example": {"email_summary": "Audience Metrics Email"},
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve email engagement metrics.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    def get(self, engagement_id: str) -> Tuple[dict, int]:
        """Retrieves email performance metrics.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): ID of an engagement

        Returns:
            Tuple[dict, int]: Response of Email Performance Metrics,
                HTTP Status Code

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        # setup the database
        database = get_db_client()

        engagement = get_engagement(database, ObjectId(engagement_id))
        if not engagement:
            return {"message": "Engagement not found."}, HTTPStatus.NOT_FOUND

        # Get all destinations that are related to Email metrics
        email_destination = (
            delivery_platform_management.get_delivery_platform_by_type(
                database, db_c.DELIVERY_PLATFORM_SFMC
            )
        )

        if not email_destination:
            return {
                "message": "No performance metrics found for engagement."
            }, HTTPStatus.OK

        # Get Performance metrics by engagement and destination
        performance_metrics = get_performance_metrics_by_engagement_details(
            database,
            ObjectId(engagement_id),
            [email_destination.get(db_c.ID)],
        )

        if not performance_metrics:
            return {
                "message": "No performance metrics found for engagement."
            }, HTTPStatus.OK

        # Get all the delivery jobs for the given engagement and destination
        delivery_jobs = get_delivery_jobs_using_metadata(
            database, engagement_id=ObjectId(engagement_id)
        )

        delivery_jobs = [
            x
            for x in delivery_jobs
            if x[db_c.DELIVERY_PLATFORM_ID] == email_destination.get(db_c.ID)
        ]

        if not delivery_jobs:
            return {
                "message": "No performance metrics found for engagement."
            }, HTTPStatus.OK

        # Group all the performance metrics for the engagement
        final_metric = {
            api_c.SUMMARY: group_perf_metric(
                [x[db_c.PERFORMANCE_METRICS] for x in performance_metrics],
                api_c.EMAIL,
            )
        }
        audience_metrics_list = group_engagement_performance_metrics(
            engagement,
            delivery_jobs,
            performance_metrics,
            [email_destination.get(db_c.ID)],
            api_c.EMAIL,
        )
        final_metric[api_c.AUDIENCE_PERFORMANCE_LABEL] = audience_metrics_list
        return (
            AudiencePerformanceEmailSchema().dump(final_metric),
            HTTPStatus.OK,
        )
