# pylint: disable=no-self-use
"""
Paths for engagement API
"""
import logging
from http import HTTPStatus
from typing import Tuple

from connexion.exceptions import ProblemException
from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView
from marshmallow import ValidationError

from huxunifylib.database import constants as db_c
from huxunifylib.database.engagement_management import (
    get_engagement,
    get_engagements,
    set_engagement,
    delete_engagement,
)
from huxunify.api.schema.engagement import EngagementGetSchema
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import add_view_to_blueprint, get_db_client
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c

engagement_bp = Blueprint(api_c.ENGAGEMENT_ENDPOINT, import_name=__name__)


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

    @marshal_with(EngagementGetSchema(many=True))
    def get(self) -> Tuple[dict, int]:
        """Retrieves all engagements.

        ---

        Returns:
            Tuple[dict, int]: dict of engagements and http code

        """

        try:
            return get_engagements(get_db_client()), HTTPStatus.OK.value

        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail="Unable to get engagements.",
            ) from exc


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

    @marshal_with(EngagementGetSchema)
    def get(self, engagement_id: str) -> Tuple[dict, int]:
        """Retrieves an engagement by ID

        Args:
            engagement_id (str): id of the engagement

        Returns:
            Tuple[dict, int]: dict of the engagement and http code

        """

        try:
            valid_id = (
                EngagementGetSchema()
                .load({db_c.USER_ID: engagement_id}, partial=True)
                .get(db_c.USER_ID)
            )
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        try:
            return (
                get_engagement(get_db_client(), engagement_id=valid_id),
                HTTPStatus.OK.value,
            )

        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail=f"Unable to get engagement with ID {engagement_id}.",
            ) from exc


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
                db_c.AUDIENCES: [],
                db_c.ENGAGEMENT_DELIVERY_SCHEDULE: {},
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

    def post(self) -> Tuple[dict, int]:
        """Creates a new engagement.

        ---
        Returns:
            Tuple[dict, int]: Engagement created, HTTP status.

        """

        try:
            body = EngagementGetSchema().load(request.get_json())
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        try:
            engagement_id = set_engagement(
                database=get_db_client(),
                name=body[db_c.ENGAGEMENT_NAME],
                description=body[db_c.ENGAGEMENT_DESCRIPTION],
                audiences=body[db_c.AUDIENCES],
                delivery_schedule=body[db_c.ENGAGEMENT_DELIVERY_SCHEDULE],
            )

            return (
                get_engagement(get_db_client(), engagement_id=engagement_id),
                HTTPStatus.OK.value,
            )

        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail="Unable to create a new engagement.",
            ) from exc


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

    def delete(self, engagement_id: str) -> Tuple[dict, int]:
        """Deletes an engagement.

        ---
        Args:
            engagement_id (str): Engagement id

        Returns:
            Tuple[dict, int]: message, HTTP status

        """

        try:
            valid_id = (
                EngagementGetSchema()
                .load({db_c.USER_ID: engagement_id}, partial=True)
                .get(db_c.USER_ID)
            )
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        try:
            success_flag = delete_engagement(
                get_db_client(), engagement_id=valid_id
            )
            if success_flag:
                return {
                    "message": api_c.OPERATION_SUCCESS
                }, HTTPStatus.OK.value

            return {
                "message": api_c.OPERATION_FAILED
            }, HTTPStatus.INTERNAL_SERVER_ERROR.value

        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail="Unable to create a new engagement.",
            ) from exc
