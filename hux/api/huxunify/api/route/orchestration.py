"""
Paths for Orchestration API
"""
import datetime
import random
from http import HTTPStatus
from random import randrange
from typing import Tuple, Union
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, request, jsonify
from marshmallow import INCLUDE
from pymongo import MongoClient

from huxunifylib.database import (
    delivery_platform_management as destination_management,
    orchestration_management,
    db_exceptions,
    engagement_management,
    data_management,
)
import huxunifylib.database.constants as db_c

from huxunify.api.schema.orchestration import (
    AudienceGetSchema,
    AudiencePutSchema,
    AudiencePostSchema,
)
from huxunify.api.schema.engagement import (
    weight_delivery_status,
)
from huxunify.api.data_connectors.cdp import get_customers_overview
from huxunify.api.schema.utils import AUTH401_RESPONSE
import huxunify.api.constants as api_c
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
    get_user_name,
)
from huxunify.api.route.utils import api_error_handler

# setup the orchestration blueprint
orchestration_bp = Blueprint(
    api_c.ORCHESTRATION_ENDPOINT, import_name=__name__
)


@orchestration_bp.before_request
@secured()
def before_request():
    """Protect all of the orchestration endpoints."""
    pass  # pylint: disable=unnecessary-pass


def add_destinations(
    database: MongoClient, destinations: list
) -> Union[list, None]:
    """Add destinations data using destination ids.
    ---
        Args:
            database (MongoClient): Mongo database.
            destinations (list): Destinations list.

        Returns:
            destinations (Union[list, None]): Destination objects.
    """

    if destinations is not None:
        object_ids = [ObjectId(x.get(api_c.ID)) for x in destinations]
        return destination_management.get_delivery_platforms_by_id(
            database, object_ids
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

    @api_error_handler()
    def get(self) -> Tuple[list, int]:  # pylint: disable=no-self-use
        """Retrieves all audiences.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: list of audience, HTTP status.

        """

        database = get_db_client()
        audiences = orchestration_management.get_all_audiences(database)
        for audience in audiences:
            audience[api_c.DESTINATIONS_TAG] = add_destinations(
                database, audience.get(api_c.DESTINATIONS_TAG)
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
    @api_error_handler()
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

        database = get_db_client()

        # get the audience
        audience_id = ObjectId(audience_id)
        audience = orchestration_management.get_audience(database, audience_id)

        if not audience:
            return {"message": api_c.AUDIENCE_NOT_FOUND}, HTTPStatus.NOT_FOUND

        # get the audience insights
        engagement_deliveries = orchestration_management.get_audience_insights(
            database, audience_id
        )

        # process each engagement
        engagements = []
        for engagement in engagement_deliveries:
            # workaround because DocumentDB does not allow $replaceRoot
            # do replace root by bringing the nested engagement up a level.
            engagement.update(engagement[api_c.ENGAGEMENT])

            # remove the nested engagement
            del engagement[api_c.ENGAGEMENT]

            # remove any empty delivery objects from DocumentDB Pipeline
            engagement[api_c.DELIVERIES] = [
                x for x in engagement[api_c.DELIVERIES] if x
            ]

            # set the weighted status for the engagement based on deliveries
            engagement[api_c.STATUS] = weight_delivery_status(engagement)
            engagements.append(engagement)

        # set the list of engagements for an audience
        audience[api_c.AUDIENCE_ENGAGEMENTS] = engagements

        # get the max last delivered date for all destinations in an audience
        audience[api_c.AUDIENCE_LAST_DELIVERED] = max(
            [x[api_c.AUDIENCE_LAST_DELIVERED] for x in engagements]
        )

        # set the destinations
        audience[api_c.DESTINATIONS_TAG] = add_destinations(
            database, audience.get(api_c.DESTINATIONS_TAG)
        )

        # get live audience size
        customers = get_customers_overview(audience[api_c.AUDIENCE_FILTERS])

        # Add insights, size.
        audience[api_c.AUDIENCE_INSIGHTS] = customers
        audience[api_c.SIZE] = customers.get(api_c.TOTAL_RECORDS)

        # TODO - HUS-436
        audience[db_c.LOOKALIKE_AUDIENCE_COLLECTION] = []

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
                api_c.DESTINATIONS: [
                    {
                        api_c.ID: "60b9601a6021710aa146df2f",
                        db_c.DELIVERY_PLATFORM_CONFIG: {
                            db_c.DATA_EXTENSION_NAME: "SFMC Test Audience"
                        },
                    }
                ],
                api_c.AUDIENCE_ENGAGEMENTS: [
                    "60d0dc9bfa9ba04689906f7b",
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

    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    # pylint: disable=no-self-use
    @api_error_handler()
    @get_user_name()
    def post(self, user_name: str) -> Tuple[dict, int]:
        """Creates a new audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user_name (str): user_name extracted from Okta.

        Returns:
            Tuple[dict, int]: Created audience, HTTP status.

        """

        body = AudiencePostSchema().load(request.get_json(), partial=True)

        # validate destinations
        database = get_db_client()
        if db_c.DESTINATIONS in body:
            # validate list of dict objects
            for destination in body[db_c.DESTINATIONS]:
                # check if dict instance
                if not isinstance(destination, dict):
                    return {
                        "message": "destinations must be objects"
                    }, HTTPStatus.BAD_REQUEST

                # check if destination id assigned
                if db_c.OBJECT_ID not in destination:
                    return {
                        "message": f"{destination} missing the "
                        f"{db_c.OBJECT_ID} field."
                    }, HTTPStatus.BAD_REQUEST

                # validate object id
                if not ObjectId.is_valid(destination[db_c.OBJECT_ID]):
                    return {
                        "message": f"{destination} has an invalid "
                        f"{db_c.OBJECT_ID} field."
                    }, HTTPStatus.BAD_REQUEST

                # map to an object ID field
                destination[db_c.OBJECT_ID] = ObjectId(
                    destination[db_c.OBJECT_ID]
                )

                # validate the destination object exists.
                if not destination_management.get_delivery_platform(
                    database, destination[db_c.OBJECT_ID]
                ):
                    return {
                        "message": f"Destination with ID "
                        f"{destination[db_c.OBJECT_ID]} does not exist."
                    }

        engagement_ids = []
        if api_c.AUDIENCE_ENGAGEMENTS in body:
            # validate list of dict objects
            for engagement_id in body[api_c.AUDIENCE_ENGAGEMENTS]:
                # validate object id
                if not ObjectId.is_valid(engagement_id):
                    return {
                        "message": f"{engagement_id} has an invalid "
                        f"{db_c.OBJECT_ID} field."
                    }, HTTPStatus.BAD_REQUEST

                # map to an object ID field
                engagement_id = ObjectId(engagement_id)

                # validate the engagement object exists.
                if not engagement_management.get_engagement(
                    database, engagement_id
                ):
                    return {
                        "message": f"Engagement with ID {engagement_id} "
                        f"does not exist."
                    }
                engagement_ids.append(engagement_id)

        try:
            # create the audience
            audience_doc = orchestration_management.create_audience(
                database=database,
                name=body[api_c.AUDIENCE_NAME],
                audience_filters=body.get(api_c.AUDIENCE_FILTERS),
                destination_ids=body.get(api_c.DESTINATIONS),
                user_name=user_name,
            )

            # attach the audience to each of the engagements
            for engagement_id in engagement_ids:
                engagement_management.append_audiences_to_engagement(
                    database,
                    engagement_id,
                    user_name,
                    [
                        {
                            db_c.OBJECT_ID: audience_doc[db_c.ID],
                            db_c.DESTINATIONS: body.get(api_c.DESTINATIONS),
                        }
                    ],
                )
        except db_exceptions.DuplicateName:
            return {
                "message": f"Duplicate name '{body[api_c.AUDIENCE_NAME]}'"
            }, HTTPStatus.BAD_REQUEST
        audience_doc[api_c.SIZE] = randrange(10000000)
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
                    {
                        api_c.ID: "60b9601a6021710aa146df2f",
                        db_c.DELIVERY_PLATFORM_CONFIG: {
                            db_c.DATA_EXTENSION_NAME: "SFMC Test Audience"
                        },
                    }
                ],
                api_c.ENGAGEMENT_IDS: [
                    "60d0dc9bfa9ba04689906f7b",
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
    @api_error_handler()
    @get_user_name()
    def put(self, audience_id: str, user_name: str) -> Tuple[dict, int]:
        """Updates an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user_name (str): user_name extracted from Okta.

        Returns:
            Tuple[dict, int]: Audience doc, HTTP status.

        """

        # load into the schema object
        body = AudiencePutSchema().load(request.get_json(), partial=True)

        audience_doc = orchestration_management.update_audience(
            database=get_db_client(),
            audience_id=ObjectId(audience_id),
            name=body.get(api_c.AUDIENCE_NAME),
            audience_filters=body.get(api_c.AUDIENCE_FILTERS),
            destination_ids=body.get(api_c.DESTINATIONS_TAG),
            user_name=user_name,
        )

        # TODO : attach the audience to each of the engagements
        return AudienceGetSchema().dump(audience_doc), HTTPStatus.OK


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

    @api_error_handler()
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
                },
                "general": {
                    "age": {
                        "name": "Age",
                        "type": "range",
                        "min": 0,
                        "max": 100,
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
