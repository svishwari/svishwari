# pylint: disable=no-self-use, C0302
"""
Paths for engagement API
"""
import logging
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from connexion.exceptions import ProblemException
from flask import Blueprint, request, jsonify
from flasgger import SwaggerView
from marshmallow import ValidationError

from huxunifylib.database import constants as db_c
import huxunifylib.database.db_exceptions as de
from huxunifylib.database.engagement_management import (
    get_engagement,
    get_engagements,
    set_engagement,
    delete_engagement,
    update_engagement,
    remove_audiences_from_engagement,
    append_audiences_to_engagement,
)
from huxunifylib.database import (
    orchestration_management,
    delivery_platform_management,
)
from huxunify.api.schema.engagement import (
    EngagementPostSchema,
    EngagementGetSchema,
    AudienceEngagementSchema,
    AudienceEngagementDeleteSchema,
    AudiencePerformanceDisplayAdsSchema,
    AudiencePerformanceEmailSchema,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
    api_error_handler,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.courier import (
    get_destination_config,
    get_audience_destination_pairs,
)

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
            return (
                jsonify(
                    EngagementGetSchema().dump(
                        get_engagements(get_db_client()), many=True
                    )
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
            eng = get_engagement(
                get_db_client(), engagement_id=ObjectId(engagement_id)
            )

            if not eng:
                return {"message": "Not found"}, HTTPStatus.NOT_FOUND.value

            return (
                EngagementGetSchema().dump(eng),
                HTTPStatus.OK,
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
                db_c.AUDIENCES: [
                    {
                        api_c.ID: "60ae035b6c5bf45da27f17d6",
                        api_c.DESTINATIONS: [
                            {
                                api_c.ID: "60ae035b6c5bf45da27f17e5",
                                "contact_list": "sfmc_extension_name",
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
            body = EngagementPostSchema().load(
                request.get_json(), partial=("delivery_schedule",)
            )
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
                user_id=ObjectId(),
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

    def put(self, engagement_id: str) -> Tuple[dict, int]:
        """Updates an engagement.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement id

        Returns:
            Tuple[dict, int]: Engagement updated, HTTP status.

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        user_id = ObjectId()

        try:
            body = EngagementPostSchema().load(request.get_json())
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        try:
            engagement = update_engagement(
                database=get_db_client(),
                engagement_id=ObjectId(engagement_id),
                user_id=user_id,
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
                EngagementGetSchema().dump(engagement),
                HTTPStatus.OK,
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
                detail="Unable to delete a new engagement.",
            ) from exc


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

    def post(self, engagement_id: str) -> Tuple[dict, int]:
        """Adds audience to engagement.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement id

        Returns:
            Tuple[dict, int]: Audience Engagement added, HTTP status.

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        user_id = ObjectId()

        try:
            body = AudienceEngagementSchema().load(
                request.get_json(), partial=True
            )
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        try:
            append_audiences_to_engagement(
                get_db_client(),
                ObjectId(engagement_id),
                user_id,
                body[api_c.AUDIENCES],
            )
            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK.value
        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail="Unable to add audience to engagement.",
            ) from exc


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

    def delete(self, engagement_id: str) -> Tuple[dict, int]:
        """Deletes audience from engagement.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            engagement_id (str): Engagement id

        Returns:
            Tuple[dict, int]: Audience deleted from engagement, HTTP status

        """

        if not ObjectId.is_valid(engagement_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        user_id = ObjectId()
        audience_ids = []
        try:
            body = AudienceEngagementDeleteSchema().load(
                request.get_json(), partial=True
            )
            for audience_id in body[api_c.AUDIENCE_IDS]:
                if not ObjectId.is_valid(audience_id):
                    return HTTPStatus.BAD_REQUEST
                audience_ids.append(ObjectId(audience_id))
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        try:
            remove_audiences_from_engagement(
                get_db_client(),
                ObjectId(engagement_id),
                user_id,
                audience_ids,
            )
            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK.value
        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail="Unable to delete audience from engagement.",
            ) from exc


@add_view_to_blueprint(
    engagement_bp,
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
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DELIVERY_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
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

        # convert the engagement ID
        engagement_id = ObjectId(engagement_id)

        # check if engagement exists
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
        if not engagement:
            return {
                "message": "Engagement does not exist."
            }, HTTPStatus.BAD_REQUEST

        # submit jobs for all the audience/destination pairs
        delivery_job_ids = []

        for pair in get_audience_destination_pairs(
            engagement[api_c.AUDIENCES]
        ):
            batch_destination = get_destination_config(database, *pair)
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
    engagement_bp,
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
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.DELIVERY_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
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
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
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
        audience_ids = [x[db_c.ID] for x in engagement[db_c.AUDIENCES]]
        if audience_id not in audience_ids:
            return {
                "message": "Audience is not attached to the engagement."
            }, HTTPStatus.BAD_REQUEST

        # validate the audience exists
        if not orchestration_management.get_audience(database, audience_id):
            return {
                "message": "Audience does not exist."
            }, HTTPStatus.BAD_REQUEST

        # submit jobs for the audience/destination pairs
        delivery_job_ids = []
        for pair in get_audience_destination_pairs(
            engagement[api_c.AUDIENCES]
        ):
            if pair[0] != audience_id:
                continue
            batch_destination = get_destination_config(database, *pair)
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
    engagement_bp,
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

        # convert to ObjectIds
        engagement_id = ObjectId(engagement_id)
        audience_id = ObjectId(audience_id)
        destination_id = ObjectId(destination_id)

        # check if engagement exists
        database = get_db_client()
        engagement = get_engagement(database, engagement_id)
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
        audience_ids = [x[db_c.ID] for x in engagement[db_c.AUDIENCES]]
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

        # validate the audience exists
        audience = orchestration_management.get_audience(database, audience_id)
        if not audience:
            return {
                "message": "Audience does not exist."
            }, HTTPStatus.BAD_REQUEST

        # submit jobs for the audience/destination pairs
        delivery_job_ids = []
        for pair in get_audience_destination_pairs(
            engagement[api_c.AUDIENCES]
        ):
            if pair != [audience_id, destination_id]:
                continue
            batch_destination = get_destination_config(database, *pair)
            batch_destination.register()
            batch_destination.submit()
            delivery_job_ids.append(
                str(batch_destination.audience_delivery_job_id)
            )

        # validate delivery route
        return {
            "message": f"Successfully created delivery job(s) "
            f"{','.join(delivery_job_ids)}"
        }, HTTPStatus.OK


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
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ENGAGEMENT_TAG]

    # pylint: disable=unused-argument
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

        display_ads = {
            "summary": {
                api_c.SPEND: 2000000,
                api_c.REACH: 500000,
                api_c.IMPRESSIONS: 456850,
                api_c.CONVERSIONS: 521006,
                api_c.CLICKS: 498587,
                api_c.FREQUENCY: 500,
                api_c.CPM: 850,
                api_c.CTR: 0.5201,
                api_c.CPA: 652,
                api_c.CPC: 485,
                api_c.ENGAGEMENT_RATE: 0.5601,
            },
            "audience_performance": [
                {
                    api_c.AUDIENCE_NAME: "audience_1",
                    api_c.SPEND: 2000000,
                    api_c.REACH: 500000,
                    api_c.IMPRESSIONS: 456850,
                    api_c.CONVERSIONS: 521006,
                    api_c.CLICKS: 498587,
                    api_c.FREQUENCY: 500,
                    api_c.CPM: 850,
                    api_c.CTR: 0.5201,
                    api_c.CPA: 652,
                    api_c.CPC: 485,
                    api_c.ENGAGEMENT_RATE: 0.5601,
                    "campaigns": [
                        {
                            api_c.DESTINATION_NAME: "Facebook",
                            api_c.IS_MAPPED: True,
                            api_c.SPEND: 2000000,
                            api_c.REACH: 500000,
                            api_c.IMPRESSIONS: 456850,
                            api_c.CONVERSIONS: 521006,
                            api_c.CLICKS: 498587,
                            api_c.FREQUENCY: 500,
                            api_c.CPM: 850,
                            api_c.CTR: 0.5201,
                            api_c.CPA: 652,
                            api_c.CPC: 485,
                            api_c.ENGAGEMENT_RATE: 0.5601,
                        },
                        {
                            api_c.DESTINATION_NAME: "Salesforce Marketing Cloud",
                            api_c.IS_MAPPED: True,
                            api_c.SPEND: 2000000,
                            api_c.REACH: 500000,
                            api_c.IMPRESSIONS: 456850,
                            api_c.CONVERSIONS: 521006,
                            api_c.CLICKS: 498587,
                            api_c.FREQUENCY: 500,
                            api_c.CPM: 850,
                            api_c.CTR: 0.5201,
                            api_c.CPA: 652,
                            api_c.CPC: 485,
                            api_c.ENGAGEMENT_RATE: 0.5601,
                        },
                    ],
                },
            ],
        }
        return (
            AudiencePerformanceDisplayAdsSchema().dump(display_ads),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    engagement_bp,
    f"{api_c.ENGAGEMENT_ENDPOINT}/<engagement_id>/"
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

    # pylint: disable=unused-argument
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

        email = {
            "summary": {
                api_c.EMAIL: 1200000,
                api_c.SENT: 125,
                api_c.HARD_BOUNCES: 0.1,
                api_c.DELIVERED: 125,
                api_c.DELIVERED_RATE: 0.1,
                api_c.OPEN: 365200,
                api_c.OPEN_RATE: 0.1,
                api_c.CLICKS: 365200,
                api_c.CTR: 0.7208,
                api_c.COTR: 0.7208,
                api_c.UNIQUE_CLICKS: 365200,
                api_c.UNIQUE_OPENS: 225100,
                api_c.UNSUBSCRIBE: 365200,
                api_c.UNSUBSCRIBE_RATE: 0.7208,
            },
            "audience_performance": [
                {
                    api_c.AUDIENCE_NAME: "audience_1",
                    api_c.EMAIL: 1200000,
                    api_c.SENT: 125,
                    api_c.HARD_BOUNCES: 0.1,
                    api_c.DELIVERED: 125,
                    api_c.DELIVERED_RATE: 0.1,
                    api_c.OPEN: 365200,
                    api_c.OPEN_RATE: 0.1,
                    api_c.CLICKS: 365200,
                    api_c.CTR: 0.7208,
                    api_c.COTR: 0.7208,
                    api_c.UNIQUE_CLICKS: 365200,
                    api_c.UNIQUE_OPENS: 225100,
                    api_c.UNSUBSCRIBE: 365200,
                    api_c.UNSUBSCRIBE_RATE: 0.7208,
                    "campaigns": [
                        {
                            api_c.DESTINATION_NAME: "Facebook",
                            api_c.IS_MAPPED: True,
                            api_c.EMAIL: 1200000,
                            api_c.SENT: 125,
                            api_c.HARD_BOUNCES: 0.1,
                            api_c.DELIVERED: 125,
                            api_c.DELIVERED_RATE: 0.1,
                            api_c.OPEN: 365200,
                            api_c.OPEN_RATE: 0.1,
                            api_c.CLICKS: 365200,
                            api_c.CTR: 0.7208,
                            api_c.COTR: 0.7208,
                            api_c.UNIQUE_CLICKS: 365200,
                            api_c.UNIQUE_OPENS: 225100,
                            api_c.UNSUBSCRIBE: 365200,
                            api_c.UNSUBSCRIBE_RATE: 0.7208,
                        },
                        {
                            api_c.DESTINATION_NAME: "Salesforce Marketing Cloud",
                            api_c.IS_MAPPED: True,
                            api_c.EMAIL: 1200000,
                            api_c.SENT: 125,
                            api_c.HARD_BOUNCES: 0.1,
                            api_c.DELIVERED: 125,
                            api_c.DELIVERED_RATE: 0.1,
                            api_c.OPEN: 365200,
                            api_c.OPEN_RATE: 0.1,
                            api_c.CLICKS: 365200,
                            api_c.CTR: 0.7208,
                            api_c.COTR: 0.7208,
                            api_c.UNIQUE_CLICKS: 365200,
                            api_c.UNIQUE_OPENS: 225100,
                            api_c.UNSUBSCRIBE: 365200,
                            api_c.UNSUBSCRIBE_RATE: 0.7208,
                        },
                    ],
                },
            ],
        }
        return (
            AudiencePerformanceEmailSchema().dump(email),
            HTTPStatus.OK,
        )
