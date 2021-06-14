"""
Paths for Orchestration API
"""
import datetime
import random
from http import HTTPStatus
from random import randrange
from typing import Tuple
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError, INCLUDE

from huxunifylib.database import (
    delivery_platform_management as destination_management,
    user_management,
    orchestration_management,
    db_exceptions,
    data_management,
)
import huxunifylib.database.constants as db_c

from huxunify.api.schema.orchestration import (
    AudienceGetSchema,
    AudiencePutSchema,
    AudiencePostSchema,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
import huxunify.api.constants as api_c
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
    get_user_id,
)

# setup the orchestration blueprint
orchestration_bp = Blueprint(
    api_c.ORCHESTRATION_ENDPOINT, import_name=__name__
)


@orchestration_bp.before_request
@secured()
def before_request():
    """Protect all of the orchestration endpoints."""
    pass  # pylint: disable=unnecessary-pass


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
            "description": "List of all Audiences.",
            "schema": {"type": "array", "items": AudienceGetSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get all Audiences."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    def get(self) -> Tuple[list, int]:  # pylint: disable=no-self-use
        """Retrieves all audiences.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: list of audience, HTTP status.

        """

        audiences = orchestration_management.get_all_audiences(get_db_client())
        for audience in audiences:
            audience[api_c.DESTINATIONS_TAG] = add_destinations(
                audience.get(api_c.DESTINATIONS_TAG)
            )
            audience[api_c.CREATED_BY] = user_management.get_user(
                get_db_client(), audience.get(api_c.CREATED_BY)
            )
            audience[api_c.UPDATED_BY] = user_management.get_user(
                get_db_client(), audience.get(api_c.UPDATED_BY)
            )

            # TODO - Fetch Engagements, Audience data (size,..) from CDM based on the filters
            # Add stub size, last_delivered_on for test purposes.
            audience[api_c.SIZE] = randrange(10000000)
            audience[
                api_c.AUDIENCE_LAST_DELIVERED
            ] = datetime.datetime.utcnow() - random.random() * datetime.timedelta(
                days=1000
            )

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
            "description": "Retrieved Audience details.",
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
        """Retrieves an audience.

        ---
        security:
            - Bearer: ["Authorization"]

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
        audience[api_c.CREATED_BY] = user_management.get_user(
            get_db_client(), audience.get(api_c.CREATED_BY)
        )
        audience[api_c.UPDATED_BY] = user_management.get_user(
            get_db_client(), audience.get(api_c.UPDATED_BY)
        )

        # TODO - Fetch Engagements, Audience data (size,..) from CDM based on the filters
        # Add stub insights, size, last_delivered_on for test purposes.
        audience[api_c.AUDIENCE_INSIGHTS] = api_c.STUB_INSIGHTS_RESPONSE
        audience[api_c.SIZE] = randrange(10000000)
        audience[
            api_c.AUDIENCE_LAST_DELIVERED
        ] = datetime.datetime.utcnow() - random.random() * datetime.timedelta(
            days=1000
        )
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

    @get_user_id()
    def post(self, user_id) -> Tuple[dict, int]:  # pylint: disable=no-self-use
        """Creates a new audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user_id (ObjectId): user_id extracted from Okta.

        Returns:
            Tuple[dict, int]: Created audience, HTTP status.

        """

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
    @get_user_id()
    def put(self, audience_id: str, user_id: str) -> Tuple[dict, int]:
        """Updates an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user_id (ObjectId): user_id extracted from Okta.

        Returns:
            Tuple[dict, int]: Audience doc, HTTP status.

        """

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


@add_view_to_blueprint(
    orchestration_bp,
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

        # validate object id
        if not ObjectId.is_valid(audience_id):
            return {"message": "Invalid Object ID"}, HTTPStatus.BAD_REQUEST

        # convert to an ObjectId
        audience_id = ObjectId(audience_id)

        # check if audience exists
        audience = None
        try:
            audience = orchestration_management.get_audience(
                get_db_client(), audience_id
            )
        except db_exceptions.InvalidID:
            pass

        if not audience:
            return {
                "message": "Audience does not exist."
            }, HTTPStatus.BAD_REQUEST

        # validate delivery route
        # TODO - hook up to connectors for HUS-437 in Sprint 10
        return {
            "message": f"Successfully created delivery job(s) for audience ID {audience_id}"
        }, HTTPStatus.OK


@add_view_to_blueprint(
    orchestration_bp, f"{api_c.AUDIENCE_ENDPOINT}/rules", "AudienceRules"
)
class AudienceRules(SwaggerView):
    """
    Audience rules class
    """

    responses = {
        HTTPStatus.OK.value: {"description": "Get audience rules dictionary"},
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get all audience rules."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    def get(self) -> Tuple[dict, int]:  # pylint: disable=no-self-use
        """Retrieves all audience rules.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: dict of audience rules, HTTP status.

        """

        rules_constants = data_management.get_constant(
            get_db_client(), db_c.AUDIENCE_FILTER_CONSTANTS
        )

        # TODO HUS-356. Stubbed, this will come from CDM
        # Min/ max values will come from cdm, we will build this dynamically
        # list of genders will come from cdm
        # locations will come from cdm
        rules_from_cdm = {
            "rule_attributes": {
                "model_scores": {
                    "propensity_to_unsubscribe": {
                        "name": "Propensity to unsubscribe",
                        "type": "range",
                        "min": 0.0,
                        "max": 1.0,
                        "steps": 0.05,
                    },
                    "actual_lifetime_value": {
                        "name": "Actual lifetime value",
                        "type": "range",
                        "min": 0,
                        "max": 50000,
                        "steps": 1000,
                    },
                    "propensity_to_purchase": {
                        "name": "Propensity to purchase",
                        "type": "range",
                        "min": 0.0,
                        "max": 1.0,
                        "steps": 0.05,
                    },
                },
                "general": {
                    "age": {
                        "name": "Age",
                        "type": "range",
                        "min": 0,
                        "max": 100
                    },
                    "email": {"name": "Email", "type": "text"},
                    "gender": {
                        "name": "Gender",
                        "type": "text",  # text for 5.0, list for future
                        "options": [],
                    },
                    "location": {
                        "name": "Location",
                        "country": {
                            "name": "Country",
                            "type": "text",  # text for 5.0, list for future
                            "options": [],
                        },
                        "state": {
                            "name": "State",
                            "type": "text",  # text for 5.0, list for future
                            "options": [],
                        },
                        "city": {
                            "name": "City",
                            "type": "text",  # text for 5.0, list for future
                            "options": [],
                        },
                        "zip_code": {"name": "Zip code", "type": "text"},
                    },
                },
            }
        }

        rules_constants = rules_constants["value"]
        rules_constants.update(rules_from_cdm)

        return rules_constants, HTTPStatus.OK.value
