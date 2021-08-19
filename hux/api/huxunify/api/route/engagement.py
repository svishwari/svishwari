# pylint: disable=no-self-use, C0302
"""
Paths for engagement API
"""
from pathlib import Path
import zipfile
from http import HTTPStatus
from random import uniform
from typing import Tuple
from itertools import groupby
from operator import itemgetter

from bson import ObjectId
from flask import Blueprint, request, jsonify, Response
from flasgger import SwaggerView

from huxunifylib.util.general.logging import logger
from huxunifylib.connectors import FacebookConnector
from huxunifylib.database import constants as db_c
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database.engagement_management import (
    get_engagement,
    get_engagements_summary,
    set_engagement,
    delete_engagement,
    update_engagement,
    remove_audiences_from_engagement,
    append_audiences_to_engagement,
    append_destination_to_engagement_audience,
    remove_destination_from_engagement_audience,
)
from huxunifylib.database.orchestration_management import get_audience
from huxunifylib.database import (
    delivery_platform_management,
)
from huxunifylib.database.delivery_platform_management import (
    get_delivery_platform,
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
    DestinationEngagedAudienceSchema,
    weighted_engagement_status,
    EngagementPutSchema,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
    api_error_handler,
    get_user_name,
    validate_destination,
    validate_destination_id,
)
from huxunify.api.data_connectors.courier import toggle_event_driven_routers
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.performance_metrics import (
    get_performance_metrics,
    generate_metrics_file,
)
from huxunify.api.data_connectors.aws import (
    get_auth_from_parameter_store,
)

engagement_bp = Blueprint(api_c.ENGAGEMENT_ENDPOINT, import_name=__name__)


# TODO Add updated_by fields to engagement_mgmt in set, update and delete methods
@engagement_bp.before_request
@secured()
def before_request():
    """Protect all of the engagement endpoints."""
    pass  # pylint: disable=unnecessary-pass


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
            logger.error("Invalid Object ID %s.", engagement_id)
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        # get the engagement summary
        engagements = get_engagements_summary(
            get_db_client(), [ObjectId(engagement_id)]
        )

        if not engagements:
            logger.error(
                "Engagements not found for engagement ID %s.", engagement_id
            )
            return {"message": "Not found"}, HTTPStatus.NOT_FOUND.value

        # TODO: HUS-837 Change once match_rate data can be fetched from CDM
        for engagement in engagements:
            for audience in engagement[db_c.AUDIENCES]:
                for destination in audience[db_c.DESTINATIONS]:
                    if db_c.LATEST_DELIVERY in destination:
                        destination[db_c.LATEST_DELIVERY][
                            api_c.MATCH_RATE
                        ] = round(uniform(0.2, 0.9), 2)

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

        database = get_db_client()
        engagement_id = set_engagement(
            database=database,
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
        engagement = get_engagement(database, engagement_id=engagement_id)
        logger.info(
            "Successfully created engagement %s.", engagement[db_c.NAME]
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f'New engagement named "{engagement[db_c.NAME]}" '
                f"created by {user_name}."
            ),
            api_c.ENGAGEMENT_TAG,
        )
        return (
            EngagementGetSchema().dump(engagement),
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
            logger.error("Invalid Object ID %s.", engagement_id)
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        body = EngagementPutSchema().load(request.get_json())

        database = get_db_client()

        engagement = update_engagement(
            database=database,
            engagement_id=ObjectId(engagement_id),
            user_name=user_name,
            name=body.get(db_c.ENGAGEMENT_NAME),
            description=body.get(db_c.ENGAGEMENT_DESCRIPTION),
            audiences=body.get(db_c.AUDIENCES),
            delivery_schedule=body[db_c.ENGAGEMENT_DELIVERY_SCHEDULE]
            if db_c.ENGAGEMENT_DELIVERY_SCHEDULE in body
            else {},
            status=body.get(db_c.STATUS),
        )
        logger.info(
            "Successfully updated engagement with ID %s.", engagement_id
        )

        # toggle routers since the engagement was updated.
        toggle_event_driven_routers(database)

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            f'Engagement "{engagement[db_c.NAME]}" updated by {user_name}.',
            api_c.ENGAGEMENT_TAG,
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

    @get_user_name()
    @api_error_handler()
    def delete(self, engagement_id: str, user_name: str) -> Tuple[dict, int]:
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
            logger.error("Invalid Object ID %s.", engagement_id)
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        engagement_id = ObjectId(engagement_id)
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        if delete_engagement(database, engagement_id):
            create_notification(
                database,
                db_c.NOTIFICATION_TYPE_INFORMATIONAL,
                (
                    f'Engagement "{engagement[db_c.NAME]}" '
                    f"deleted by {user_name}."
                ),
                api_c.ENGAGEMENT_TAG,
            )
            logger.info("Successfully deleted engagement %s.", engagement_id)

            # toggle routers since the engagement was deleted.
            toggle_event_driven_routers(database)

            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK.value

        logger.info("Could not delete engagement %s.", engagement_id)
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
            logger.error("Invalid Object ID %s.", engagement_id)
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        database = get_db_client()

        engagement = get_engagement(database, ObjectId(engagement_id))

        if engagement is None:
            return {
                "message": api_c.ENGAGEMENT_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        body = AudienceEngagementSchema().load(
            request.get_json(), partial=True
        )

        # validate audiences exist
        audience_names = []
        for audience in body[api_c.AUDIENCES]:
            audience_to_attach = get_audience(
                database, ObjectId(audience[api_c.ID])
            )
            if not audience_to_attach:
                logger.error(
                    "Audience does not exist: %s.", audience[api_c.ID]
                )
                return {
                    "message": f"Audience does not exist: {audience[api_c.ID]}"
                }, HTTPStatus.BAD_REQUEST
            audience_names.append(audience_to_attach[db_c.NAME])
        append_audiences_to_engagement(
            database,
            ObjectId(engagement_id),
            user_name,
            body[api_c.AUDIENCES],
        )

        logger.info(
            "Successfully added %s to engagement %s.",
            len(audience_names),
            engagement_id,
        )

        for audience_name in audience_names:
            create_notification(
                database,
                db_c.NOTIFICATION_TYPE_SUCCESS,
                (
                    f'Audience "{audience_name}" added to engagement '
                    f'"{engagement[db_c.NAME]}" by {user_name}.'
                ),
                api_c.ENGAGEMENT_TAG,
            )

        # toggle routers since the engagement was updated.
        toggle_event_driven_routers(database)

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
            logger.error("Invalid Object ID %s.", engagement_id)
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        database = get_db_client()

        engagement = get_engagement(database, ObjectId(engagement_id))

        if engagement is None:
            return {
                "message": api_c.ENGAGEMENT_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        audience_ids = []
        body = AudienceEngagementDeleteSchema().load(
            request.get_json(), partial=True
        )
        audience_names = []
        for audience_id in body[api_c.AUDIENCE_IDS]:
            if not ObjectId.is_valid(audience_id):
                logger.error("Invalid Object ID %s.", audience_id)
                return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST
            audience_ids.append(ObjectId(audience_id))
            audience = get_audience(database, ObjectId(audience_id))
            if audience is None:
                return {
                    "message": api_c.AUDIENCE_NOT_FOUND
                }, HTTPStatus.NOT_FOUND
            audience_names.append(audience[db_c.NAME])

        remove_audiences_from_engagement(
            database,
            ObjectId(engagement_id),
            user_name,
            audience_ids,
        )
        logger.info(
            "Successfully deleted %s from engagement %s.",
            len(audience_names),
            engagement_id,
        )

        for audience_name in audience_names:
            create_notification(
                database,
                db_c.NOTIFICATION_TYPE_INFORMATIONAL,
                (
                    f'Audience "{audience_name}" removed from engagement '
                    f'"{engagement[db_c.NAME]}" by {user_name}.'
                ),
                api_c.ENGAGEMENT_TAG,
            )

        # toggle routers since the engagement was updated.
        toggle_event_driven_routers(database)

        return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK.value


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/{api_c.AUDIENCE}/"
    f"<audience_id>/{api_c.DESTINATIONS}",
    "AddDestinationEngagedAudience",
)
class AddDestinationEngagedAudience(SwaggerView):
    """
    Class to add a destination to an engagement audience
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
            "name": db_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "60fff065b2075450922261cf",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Destinations body.",
            "example": {
                api_c.ID: "60ae035b6c5bf45da27f17e6",
                db_c.DELIVERY_PLATFORM_CONFIG: {
                    db_c.DATA_EXTENSION_NAME: "SFMC Test Audience"
                },
            },
        },
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": EngagementGetSchema,
            "description": "Destination added to Engagement Audience.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create the engagement.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    @get_user_name()
    def post(
        self, engagement_id: str, audience_id: str, user_name: str
    ) -> Tuple[dict, int]:
        """Adds a destination to an engagement audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement id
            audience_id (str): Audience id
            user_name (str): user_name extracted from Okta.

        Returns:
            Tuple[dict, int]: Destination Audience Engagement added, HTTP status.

        """

        if not (
            ObjectId.is_valid(engagement_id) and ObjectId.is_valid(audience_id)
        ):
            logger.error("Invalid Object ID.")
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        destination = DestinationEngagedAudienceSchema().load(
            request.get_json(), partial=True
        )
        destination[api_c.ID] = validate_destination_id(destination[api_c.ID])

        database = get_db_client()
        # get destinations
        destination_to_attach = get_delivery_platform(
            database, destination[api_c.ID]
        )
        append_destination_to_engagement_audience(
            database,
            ObjectId(engagement_id),
            ObjectId(audience_id),
            destination,
            user_name,
        )

        engagement = get_engagement(database, ObjectId(engagement_id))
        audience = get_audience(database, ObjectId(audience_id))
        logger.info(
            "Destination %s added to audience %s from engagement %s.",
            destination_to_attach[db_c.NAME],
            audience[db_c.NAME],
            engagement[db_c.NAME],
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f'Destination "{destination_to_attach[db_c.NAME]}" added to '
                f'audience "{audience[db_c.NAME]}" from engagement '
                f'"{engagement[db_c.NAME]}" by {user_name}'
            ),
            api_c.ENGAGEMENT_TAG,
        )

        # toggle routers since the engagement was updated.
        toggle_event_driven_routers(database)

        return EngagementGetSchema().dump(engagement), HTTPStatus.OK.value


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/{api_c.AUDIENCE}/"
    f"<audience_id>/{api_c.DESTINATIONS}",
    "RemoveDestinationEngagedAudience",
)
class RemoveDestinationEngagedAudience(SwaggerView):
    """
    Class to remove a destination from an engagement audience
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
            "name": db_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "60fff065b2075450922261cf",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Destinations body.",
            "example": {
                api_c.ID: "60ae035b6c5bf45da27f17e6",
            },
        },
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": EngagementGetSchema,
            "description": "Destination added to Engagement Audience.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create the engagement.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    @get_user_name()
    def delete(
        self, engagement_id: str, audience_id: str, user_name: str
    ) -> Tuple[dict, int]:
        """Removes a destination from an engagement audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement id
            audience_id (str): Audience id
            user_name (str): user_name extracted from Okta.

        Returns:
            Tuple[dict, int]: Destination Audience Engagement added, HTTP status.

        """

        if not (
            ObjectId.is_valid(engagement_id) and ObjectId.is_valid(audience_id)
        ):
            logger.error("Invalid Object ID.")
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        destination = DestinationEngagedAudienceSchema().load(
            request.get_json(), partial=True
        )
        destination_id = validate_destination_id(destination[api_c.ID])

        database = get_db_client()
        # get destination
        destination_to_remove = get_delivery_platform(database, destination_id)
        if not destination_to_remove:
            logger.error(
                "Destination %s does not exist.", destination[api_c.ID]
            )
            return {
                "message": f"Destination does not exist: {destination[api_c.ID]}"
            }, HTTPStatus.BAD_REQUEST

        remove_destination_from_engagement_audience(
            database,
            ObjectId(engagement_id),
            ObjectId(audience_id),
            destination_id,
            user_name,
        )

        engagement = get_engagement(database, ObjectId(engagement_id))
        audience = get_audience(database, ObjectId(audience_id))

        logger.info(
            "Destination %s successfully removed from audience %s from engagement %s by %s.",
            destination_to_remove[db_c.NAME],
            audience[db_c.NAME],
            engagement[db_c.NAME],
            user_name,
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f'Destination "{destination_to_remove[db_c.NAME]}" removed from audience '
                f'"{audience[db_c.NAME]}" from engagement '
                f'"{engagement[db_c.NAME]}" by {user_name}'
            ),
            api_c.ENGAGEMENT_TAG,
        )

        # toggle routers since the engagement was updated.
        toggle_event_driven_routers(database)

        return EngagementGetSchema().dump(engagement), HTTPStatus.OK.value


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
                        api_c.AD_SET_ID: "ad_set_id",
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
    @validate_destination()
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
        if not all(ObjectId.is_valid(x) for x in [audience_id, engagement_id]):
            logger.error("Invalid Object ID.")
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        # convert to ObjectIds
        engagement_id = ObjectId(engagement_id)
        audience_id = ObjectId(audience_id)

        # check if engagement exists
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        if not engagement:
            logger.error("Engagement %s not found.", engagement_id)
            return {
                "message": api_c.ENGAGEMENT_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        # validate that the engagement has audiences
        if db_c.AUDIENCES not in engagement:
            logger.error(
                "Engagement %s does not have audiences.", engagement_id
            )
            return {
                "message": "Engagement has no audiences."
            }, HTTPStatus.BAD_REQUEST

        # validate that the audience is attached
        audience_ids = [x[db_c.OBJECT_ID] for x in engagement[db_c.AUDIENCES]]
        if audience_id not in audience_ids:
            logger.error(
                "Engagement %s does not have audience %s attached.",
                engagement_id,
                audience_id,
            )
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
            logger.error("Destination not attached to engagement audience.")
            return {
                "message": "Destination is not attached to the "
                "engagement audience."
            }, HTTPStatus.BAD_REQUEST

        body = CampaignPutSchema().load(request.get_json())

        delivery_jobs = (
            delivery_platform_management.get_delivery_jobs_using_metadata(
                database, engagement_id, audience_id, destination_id
            )
        )
        if delivery_jobs is None:
            logger.error(
                "Could not attach campaigns for engagement %s audience %s.",
                engagement_id,
                audience_id,
            )
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
        delivery_jobs = []

        for delivery_job_id, value in groupby(
            campaigns, key=itemgetter(api_c.DELIVERY_JOB_ID)
        ):
            delivery_job = delivery_platform_management.get_delivery_job(
                database, ObjectId(delivery_job_id)
            )
            if delivery_job is None and (
                delivery_job[api_c.ENGAGEMENT_ID] != engagement_id
            ):
                logger.error(
                    "Invalid data cannot attach campaign to engagement %s audience %s.",
                    engagement_id,
                    audience_id,
                )
                return {
                    "message": "Invalid data, cannot attach campaign."
                }, HTTPStatus.BAD_REQUEST

            updated_campaigns = [
                {
                    k: v
                    for k, v in d.items()
                    if k
                    in [
                        api_c.NAME,
                        api_c.ID,
                        api_c.AD_SET_ID,
                        api_c.AD_SET_NAME,
                    ]
                }
                for d in value
            ]
            delivery_jobs.append(
                delivery_platform_management.create_delivery_job_generic_campaigns(
                    get_db_client(),
                    ObjectId(delivery_job_id),
                    updated_campaigns,
                )
            )

        # get return campaigns.
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
        logger.info(
            "Successfully attached campaigns to engagement %s audience %s.",
            engagement_id,
            audience_id,
        )

        # toggle routers since the engagement was updated.
        toggle_event_driven_routers(database)

        return (
            jsonify(CampaignSchema().dump(campaigns, many=True)),
            HTTPStatus.OK,
        )


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
    @validate_destination()
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
        if not all(ObjectId.is_valid(x) for x in [audience_id, engagement_id]):
            logger.error("Invalid Object ID.")
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        # convert to ObjectIds
        engagement_id = ObjectId(engagement_id)
        audience_id = ObjectId(audience_id)

        # check if engagement exists
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        if not engagement:
            logger.error(
                "Engagement with engagement ID %s not found.", engagement_id
            )
            return {
                "message": api_c.ENGAGEMENT_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        # validate that the engagement has audiences
        if db_c.AUDIENCES not in engagement:
            logger.error(
                "Engagement with ID %s has no audiences.", engagement_id
            )
            return {
                "message": "Engagement has no audiences."
            }, HTTPStatus.BAD_REQUEST

        # validate that the audience is attached
        audience_ids = [x[db_c.OBJECT_ID] for x in engagement[db_c.AUDIENCES]]
        if audience_id not in audience_ids:
            logger.error(
                "Audience with ID %s is not attached to engagement %s.",
                audience_id,
                engagement_id,
            )
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
            logger.error(
                "Destination is not attached to the engagement audience."
            )
            return {
                "message": "Destination is not attached to the "
                "engagement audience."
            }, HTTPStatus.BAD_REQUEST

        delivery_jobs = (
            delivery_platform_management.get_delivery_jobs_using_metadata(
                database, engagement_id, audience_id, destination_id
            )
        )
        if not delivery_jobs:
            logger.error(
                "No delivery jobs found for engagement ID %s, audience ID %s, destination_id %s.",
                engagement_id,
                audience_id,
                destination_id,
            )
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
                    campaign[api_c.NAME] = campaign[api_c.NAME]
                    campaign[api_c.AD_SET_ID] = campaign[api_c.AD_SET_ID]
                    campaign[api_c.AD_SET_NAME] = campaign[api_c.AD_SET_NAME]
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
    # pylint: disable=too-many-return-statements, too-many-locals
    @api_error_handler()
    @validate_destination()
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
        if not all(ObjectId.is_valid(x) for x in [audience_id, engagement_id]):
            logger.error("Invalid Object ID.")
            return {"message": api_c.INVALID_OBJECT_ID}, HTTPStatus.BAD_REQUEST

        # convert to ObjectIds
        engagement_id = ObjectId(engagement_id)
        audience_id = ObjectId(audience_id)

        # check if engagement exists
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        if not engagement:
            logger.error(
                "Engagement with engagement ID %s not found.", engagement_id
            )
            return {
                "message": api_c.ENGAGEMENT_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        # validate that the engagement has audiences
        if db_c.AUDIENCES not in engagement:
            logger.error(
                "Engagement with ID %s has no audiences.", engagement_id
            )
            return {
                "message": "Engagement has no audiences."
            }, HTTPStatus.BAD_REQUEST

        # validate that the audience is attached
        audience_ids = [x[db_c.OBJECT_ID] for x in engagement[db_c.AUDIENCES]]
        if audience_id not in audience_ids:
            logger.error(
                "Audience with ID %s is not attached to engagement %s.",
                audience_id,
                engagement_id,
            )
            return {
                "message": "Audience is not attached to the engagement."
            }, HTTPStatus.BAD_REQUEST

        # validate that the destination ID is attached to the audience
        valid_destination = False
        for audience in engagement[db_c.AUDIENCES]:
            for destination in audience[db_c.DESTINATIONS]:
                if (
                    isinstance(destination, dict)
                    and destination_id == destination[db_c.OBJECT_ID]
                ):
                    valid_destination = True

        if not valid_destination:
            logger.error(
                "Destination is not attached to the engagement audience."
            )
            return {
                "message": "Destination is not attached to the "
                "engagement audience."
            }, HTTPStatus.BAD_REQUEST

        destination = delivery_platform_management.get_delivery_platform(
            database, destination_id
        )

        # Get existing delivery jobs
        delivery_jobs = (
            delivery_platform_management.get_delivery_jobs_using_metadata(
                database, engagement_id, audience_id, destination_id
            )
        )
        if not delivery_jobs:
            logger.error(
                "No delivery jobs found for engagement ID %s, audience ID %s, destination_id %s.",
                engagement_id,
                audience_id,
                destination_id,
            )
            return {
                "message": "Could not find any delivery jobs to map."
            }, HTTPStatus.BAD_REQUEST

        logger.info("Getting existing campaigns from facebook.")
        # Get existing campaigns from facebook
        facebook_connector = FacebookConnector(
            auth_details=get_auth_from_parameter_store(
                destination[api_c.AUTHENTICATION_DETAILS],
                destination[api_c.DELIVERY_PLATFORM_TYPE],
            )
        )

        campaigns = facebook_connector.get_campaigns()

        if campaigns is None:
            logger.error("Could not find any campaigns in Facebook to map.")
            return {
                "message": "Could not find any Campaigns to map."
            }, HTTPStatus.BAD_REQUEST

        logger.info("Got existing campaigns from Facebook.")

        campaign_mappings = []
        for campaign in campaigns:
            ad_sets = facebook_connector.get_campaign_ad_sets(
                campaign.get(api_c.ID)
            )
            for ad_set in ad_sets:
                campaign_mapping = {
                    api_c.ID: campaign.get(api_c.ID),
                    api_c.AD_SET_ID: ad_set.get(api_c.ID),
                    api_c.NAME: campaign.get(api_c.NAME),
                    api_c.AD_SET_NAME: ad_set.get(api_c.NAME),
                }
                campaign_mappings.append(campaign_mapping)

        # Build response object
        campaign_schema = {
            "campaigns": list(campaign_mappings),
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

    parameters = api_c.ENGAGEMENT_ID_PARAMS

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
            logger.error("Invalid Object ID %s.", engagement_id)
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        # setup the database
        database = get_db_client()

        engagement = get_engagement(database, ObjectId(engagement_id))
        if not engagement:
            logger.error(
                "Engagement with engagement ID %s not found", engagement_id
            )
            return {"message": "Engagement not found."}, HTTPStatus.NOT_FOUND

        final_metric = get_performance_metrics(
            database, engagement, engagement_id, api_c.DISPLAY_ADS
        )

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

    parameters = api_c.ENGAGEMENT_ID_PARAMS

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
            logger.error("Invalid Object ID %s.", engagement_id)
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        # setup the database
        database = get_db_client()

        engagement = get_engagement(database, ObjectId(engagement_id))
        if not engagement:
            logger.error(
                "Engagement with engagement ID %s not found.", engagement_id
            )
            return {"message": "Engagement not found."}, HTTPStatus.NOT_FOUND

        final_metric = get_performance_metrics(
            database, engagement, engagement_id, api_c.EMAIL
        )
        return (
            AudiencePerformanceEmailSchema().dump(final_metric),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<{api_c.ENGAGEMENT_ID}>/"
    f"{api_c.AUDIENCE_PERFORMANCE}/download",
    "EngagementPerformanceDownloadView",
)
class EngagementPerformanceDownload(SwaggerView):
    """
    Class for downloading engagement performance metrics
    """

    parameters = api_c.ENGAGEMENT_ID_PARAMS

    responses = {
        HTTPStatus.OK.value: {
            "description": "Download Performance Metrics",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to download engagement metrics.",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    @api_error_handler()
    def get(self, engagement_id: str) -> Tuple[Response, int]:
        """Retrieves email performance metrics.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): ID of an engagement

        Returns:
            Tuple[Response, int]: Response of Performance Metrics
                HTTP Status Code

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        # setup the database
        database = get_db_client()

        engagement = get_engagement(database, ObjectId(engagement_id))
        if not engagement:
            return {"message": "Engagement not found."}, HTTPStatus.NOT_FOUND

        final_email_metric = get_performance_metrics(
            database, engagement, engagement_id, api_c.EMAIL
        )

        final_display_ads_metric = get_performance_metrics(
            database, engagement, engagement_id, api_c.DISPLAY_ADS
        )

        folder_name = "performancemetrics"

        # generate performance metrics csv performancemetrics
        generate_metrics_file(engagement_id, final_email_metric, api_c.EMAIL)

        generate_metrics_file(
            engagement_id, final_display_ads_metric, api_c.DISPLAY_ADS
        )

        zipfile_name = f"{engagement_id}_performance_metrics.zip"

        # zip all the performancemetrics which are inside in the folder
        with zipfile.ZipFile(
            zipfile_name, "w", compression=zipfile.ZIP_STORED
        ) as zipfolder:

            folder = Path(folder_name)
            for file in folder.glob("**/*.csv"):
                zipfolder.write(file)
                file.unlink()

        zip_file = Path(zipfile_name)
        data = zip_file.read_bytes()
        zip_file.unlink()

        return (
            Response(
                data,
                headers={
                    "Content-Type": "application/zip",
                    "Content-Disposition": "attachment; filename=%s;"
                    % zipfile_name,
                },
            ),
            HTTPStatus.OK,
        )
