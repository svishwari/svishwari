# pylint: disable=no-self-use
"""
Paths for engagement API
"""
import logging
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from connexion.exceptions import ProblemException
from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView
from marshmallow import ValidationError

from huxunifylib.database import constants as db_c
import huxunifylib.database.db_exceptions as de
from huxunifylib.database.engagement_management import (
    get_engagement,
    get_engagements,
    set_engagement,
    delete_engagement,
)
from huxunifylib.database import (
    orchestration_management,
    delivery_platform_management,
)
from huxunify.api.schema.engagement import (
    EngagementPostSchema,
    EngagementGetSchema,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c

engagement_bp = Blueprint(api_c.ENGAGEMENT_ENDPOINT, import_name=__name__)

# TODO - implement after HUS-443 is done to grab user/okta_id
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

    @marshal_with(EngagementGetSchema(many=True))
    def get(self) -> Tuple[dict, int]:
        """Retrieves all engagements.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:

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

        try:
            return (
                get_engagement(
                    get_db_client(), engagement_id=ObjectId(engagement_id)
                ),
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
                db_c.ENGAGEMENT_DELIVERY_SCHEDULE: None,
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
        security:
            - Bearer: ["Authorization"]

        Args:

        Returns:
            Tuple[dict, int]: Engagement created, HTTP status.

        """

        try:
            body = EngagementPostSchema().load(request.get_json())
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        try:
            engagement_id = set_engagement(
                database=get_db_client(),
                name=body[db_c.ENGAGEMENT_NAME],
                description=body[db_c.ENGAGEMENT_DESCRIPTION]
                if db_c.ENGAGEMENT_DESCRIPTION in body
                else None,
                audiences=body[db_c.AUDIENCES]
                if db_c.AUDIENCES in body
                else None,
                delivery_schedule=body[db_c.ENGAGEMENT_DELIVERY_SCHEDULE]
                if db_c.ENGAGEMENT_DELIVERY_SCHEDULE in body
                else None,
            )

            return (
                EngagementGetSchema().dump(
                    get_engagement(
                        get_db_client(), engagement_id=engagement_id
                    )
                ),
                HTTPStatus.CREATED,
            )

        except de.DuplicateName:
            return {
                "message": api_c.DUPLICATE_NAME
            }, HTTPStatus.BAD_REQUEST.value

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
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement id

        Returns:
            Tuple[dict, int]: message, HTTP status

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        try:
            if delete_engagement(
                get_db_client(), engagement_id=ObjectId(engagement_id)
            ):
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


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/deliver",
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
            "description": "Failed to deliver engagement.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DELIVERY_TAG]

    # pylint: disable=no-self-use
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

        # TODO - implement after HUS-479 is done
        # pylint: disable=unused-variable
        user_id = ObjectId()

        # validate object id
        if not ObjectId.is_valid(engagement_id):
            return {"message": "Invalid Object ID"}, HTTPStatus.BAD_REQUEST

        # validate engagement exists
        engagement_id = ObjectId(engagement_id)

        # check if engagement exists
        engagement = get_engagement(get_db_client(), engagement_id)
        if not engagement:
            return {
                "message": "Engagement does not exist."
            }, HTTPStatus.BAD_REQUEST

        # validate delivery route
        # TODO - hook up to connectors for HUS-437 in Sprint 10
        return {
            "message": f"Successfully created delivery job(s) for engagement ID {engagement_id}"
        }, HTTPStatus.OK


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/audience/<audience_id>/deliver",
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
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DELIVERY_TAG]

    # pylint: disable=no-self-use
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

        # TODO - implement after HUS-479 is done
        # pylint: disable=unused-variable
        user_id = ObjectId()

        # validate object id
        if not all(ObjectId.is_valid(x) for x in [audience_id, engagement_id]):
            return {"message": "Invalid Object ID"}, HTTPStatus.BAD_REQUEST

        # convert to ObjectIds
        engagement_id = ObjectId(engagement_id)
        audience_id = ObjectId(audience_id)

        # check if engagement exists
        engagement = get_engagement(get_db_client(), engagement_id)
        if not engagement:
            return {
                "message": "Engagement does not exist."
            }, HTTPStatus.BAD_REQUEST

        # validate that the engagement has audiences
        if db_c.AUDIENCES not in engagement:
            return {
                "message": "Engagement has no audiences."
            }, HTTPStatus.BAD_REQUEST

        # validate that the audience is attached
        audience_ids = [
            x[db_c.AUDIENCE_ID] for x in engagement[db_c.AUDIENCES]
        ]
        if audience_id not in audience_ids:
            return {
                "message": "Audience is not attached to the engagement."
            }, HTTPStatus.BAD_REQUEST

        # validate the audience exists
        if not orchestration_management.get_audience(
            get_db_client(), audience_id
        ):
            return {
                "message": "Audience does not exist."
            }, HTTPStatus.BAD_REQUEST

        # validate delivery route
        # TODO - hook up to connectors for HUS-437 in Sprint 10
        return {
            "message": f"Successfully created delivery job(s) for {engagement_id} and {audience_id}"
        }, HTTPStatus.OK


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/"
    f"audience/<audience_id>/destination/<destination_id>/deliver",
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

        # TODO - implement after HUS-479 is done
        # pylint: disable=unused-variable
        user_id = ObjectId()

        # validate object id
        if not all(
            ObjectId.is_valid(x)
            for x in [audience_id, engagement_id, destination_id]
        ):
            return {"message": "Invalid Object ID"}, HTTPStatus.BAD_REQUEST

        # validate engagement exists
        engagement_id = ObjectId(engagement_id)
        audience_id = ObjectId(audience_id)
        destination_id = ObjectId(destination_id)

        # check if engagement exists
        engagement = get_engagement(get_db_client(), engagement_id)
        if not engagement:
            return {
                "message": "Engagement does not exist."
            }, HTTPStatus.BAD_REQUEST

        # validate that the audience belongs to the engagement
        if db_c.AUDIENCES not in engagement:
            return {
                "message": "Engagement has no audiences."
            }, HTTPStatus.BAD_REQUEST

        # validate that the audience is attached
        audience_ids = [
            x[db_c.AUDIENCE_ID] for x in engagement[db_c.AUDIENCES]
        ]
        if audience_id not in audience_ids:
            return {
                "message": "Audience is not attached to the engagement."
            }, HTTPStatus.BAD_REQUEST

        # validate that the destination ID is attached to the audience
        valid_destination = False
        for audience in engagement[db_c.AUDIENCES]:
            for destination in audience[db_c.DESTINATIONS]:
                if destination_id == destination[db_c.DELIVERY_PLATFORM_ID]:
                    valid_destination = True

        if not valid_destination:
            return {
                "message": "Destination is not attached to the engagement audience."
            }, HTTPStatus.BAD_REQUEST

        # validate destination exists
        destination = delivery_platform_management.get_delivery_platform(
            get_db_client(), destination_id
        )
        if not destination:
            return {
                "message": "Destination does not exist."
            }, HTTPStatus.BAD_REQUEST

        # validate the audience exists
        audience = orchestration_management.get_audience(
            get_db_client(), audience_id
        )
        if not audience:
            return {
                "message": "Audience does not exist."
            }, HTTPStatus.BAD_REQUEST

        # validate the destination exists
        # TODO - hook up to connectors for HUS-437 in Sprint 10

        # validate delivery route
        return {
            "message": f"Successfully created delivery job(s) for {engagement_id} and {audience_id}"
        }, HTTPStatus.OK
