"""
Paths for Orchestration API
"""
from http import HTTPStatus
from typing import Tuple
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError, INCLUDE

from huxunifylib.database import (
    delivery_platform_management as destination_management,
    orchestration_management,
)
from huxunify.api.schema.orchestration import (
    AudienceGetSchema,
    AudiencePutSchema,
    AudiencePostSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
import huxunify.api.constants as api_c
from huxunify.api.route.utils import add_view_to_blueprint, get_db_client


# setup the orchestration blueprint
orchestration_bp = Blueprint(
    api_c.ORCHESTRATION_ENDPOINT, import_name=__name__
)


def add_destinations(destination_ids) -> list:
    """Fetch destinations data using destination ids.

    ---

        Args:
            destination_ids (list): Destinations Ids.

        Returns:
            destinations (list): Destination objects.

    """

    if destination_ids is not None:
        object_ids = [ObjectId(x) for x in destination_ids]
        return destination_management.get_delivery_platforms_by_id(
            get_db_client(), object_ids
        )
    return None


@add_view_to_blueprint(
    orchestration_bp, api_c.AUDIENCE_ENDPOINT, "AudienceView"
)
class AudienceView(SwaggerView):
    """
    Audience view class
    """

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of all audiences",
            "schema": {"type": "array", "items": AudienceGetSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get all audience."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    def get(self) -> Tuple[list, int]:  # pylint: disable=no-self-use
        """Retrieves all audience.

        ---
        Returns:
            Tuple[list, int]: list of audience, HTTP status.

        """

        audiences = orchestration_management.get_all_audiences(get_db_client())
        for audience in audiences:
            audience[api_c.DESTINATIONS_TAG] = add_destinations(
                audience.get(api_c.DESTINATIONS_TAG)
            )
        # TODO - Fetch Engagements, Audience data (size,..) from CDM based on the filters
        return (
            jsonify(AudienceGetSchema().dump(audiences, many=True)),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    orchestration_bp,
    f"{api_c.AUDIENCE_ENDPOINT}/<audience_id>",
    "AudienceGetView",
)
class AudienceGetView(SwaggerView):
    """
    Single Audience Get view class
    """

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": AudienceGetSchema,
            "description": "Retrieved audience details.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve audience details.",
            "schema": {
                "example": {"message": "Destination cannot be validated"},
            },
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    def get(self, audience_id: str) -> Tuple[dict, int]:
        """Get an audience by ID.

        ---
        Args:
            audience_id (str): Audience ID.

        Returns:
            Tuple[dict, int]: Audience, HTTP status.

        """

        if not ObjectId.is_valid(audience_id):
            return {"message": api_c.INVALID_ID}, HTTPStatus.BAD_REQUEST

        audience = orchestration_management.get_audience(
            get_db_client(), ObjectId(audience_id)
        )

        audience[api_c.DESTINATIONS_TAG] = add_destinations(
            audience.get(api_c.DESTINATIONS_TAG)
        )
        # TODO - Fetch Engagements, Audience data (size,..) from CDM based on the filters
        # Add dummy insights objects for test purpose.
        audience[api_c.AUDIENCE_INSIGHTS] = api_c.DUMMY_INSIGHTS_RESPONSE
        return (
            AudienceGetSchema(unknown=INCLUDE).dump(audience),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    orchestration_bp,
    api_c.AUDIENCE_ENDPOINT,
    "AudiencePostView",
)
class AudiencePostView(SwaggerView):
    """
    Audience Post view class
    """

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Audience body.",
            "example": {
                api_c.AUDIENCE_NAME: "My Audience",
                api_c.DESTINATIONS_TAG: [
                    "71364317897acad4bac4373b",
                    "67589317897acad4bac4373b",
                ],
                api_c.AUDIENCE_ENGAGEMENTS: [
                    "84759317897acad4bac4373b",
                    "46826317897acad4bac4373b",
                ],
                api_c.AUDIENCE_FILTERS: [
                    {
                        api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                        api_c.AUDIENCE_SECTION_FILTERS: [
                            {
                                api_c.AUDIENCE_FILTER_FIELD: "filter_field",
                                api_c.AUDIENCE_FILTER_TYPE: "type",
                                api_c.AUDIENCE_FILTER_VALUE: "value",
                            }
                        ],
                    }
                ],
            },
        },
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": AudienceGetSchema,
            "description": "Audience created.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create audience.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    def post(self) -> Tuple[dict, int]:  # pylint: disable=no-self-use
        """Creates a new audience.

        ---
        Returns:
            Tuple[dict, int]: Created audience, HTTP status.

        """
        # TODO - implement after HUS-254 is done to grab user/okta_id
        user_id = ObjectId()

        try:
            body = AudiencePostSchema().load(request.get_json(), partial=True)
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        audience_doc = orchestration_management.create_audience(
            database=get_db_client(),
            name=body[api_c.AUDIENCE_NAME],
            audience_filters=body.get(api_c.AUDIENCE_FILTERS),
            destination_ids=body.get(api_c.DESTINATIONS_TAG),
            user_id=user_id,
        )

        return AudienceGetSchema().dump(audience_doc), HTTPStatus.CREATED


@add_view_to_blueprint(
    orchestration_bp,
    f"{api_c.AUDIENCE_ENDPOINT}/<audience_id>",
    "AudiencePutView",
)
class AudiencePutView(SwaggerView):
    """
    Audience Put view class
    """

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "description": "Audience Object.",
            "type": "object",
            "example": {
                api_c.AUDIENCE_NAME: "My Audience",
                api_c.DESTINATIONS_TAG: [
                    "71364317897acad4bac4373b",
                    "67589317897acad4bac4373b",
                ],
                api_c.AUDIENCE_ENGAGEMENTS: [
                    "76859317897acad4bac4373b",
                    "46826317897acad4bac4373b",
                ],
                api_c.AUDIENCE_FILTERS: [
                    {
                        api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                        api_c.AUDIENCE_SECTION_FILTERS: [
                            {
                                api_c.AUDIENCE_FILTER_FIELD: "filter_field",
                                api_c.AUDIENCE_FILTER_TYPE: "type",
                                api_c.AUDIENCE_FILTER_VALUE: "value",
                            }
                        ],
                    }
                ],
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "schema": AudienceGetSchema,
            "description": "Updated Audience.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update audience.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    def put(self, audience_id: str) -> Tuple[dict, int]:
        """Updates an existing audience.

        ---
        Args:
            audience_id (str): Audience ID.

        Returns:
            Tuple[dict, int]: Audience doc, HTTP status.

        """

        # TODO - implement after HUS-254 is done to grab user/okta_id
        user_id = ObjectId()
        # load into the schema object
        try:
            body = AudiencePutSchema().load(request.get_json(), partial=True)
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        audience_doc = orchestration_management.update_audience(
            database=get_db_client(),
            audience_id=ObjectId(audience_id),
            name=body.get(api_c.AUDIENCE_NAME),
            audience_filters=body.get(api_c.AUDIENCE_FILTERS),
            destination_ids=body.get(api_c.DESTINATIONS_TAG),
            user_id=user_id,
        )

        return AudienceGetSchema().dump(audience_doc), HTTPStatus.OK
