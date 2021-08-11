"""
Paths for Orchestration API
"""
from http import HTTPStatus
from typing import Tuple, Union
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, request, jsonify
from marshmallow import INCLUDE
from pymongo import MongoClient

from huxunifylib.util.general.logging import logger
from huxunifylib.connectors import FacebookConnector
from huxunifylib.database.notification_management import create_notification
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
    LookalikeAudiencePostSchema,
    LookalikeAudienceGetSchema,
    is_audience_lookalikeable,
)
from huxunify.api.schema.engagement import (
    weight_delivery_status,
)
from huxunify.api.data_connectors.cdp import (
    get_customers_overview,
    get_customers_count_async,
)
from huxunify.api.data_connectors.aws import get_auth_from_parameter_store
from huxunify.api.schema.utils import AUTH401_RESPONSE
import huxunify.api.constants as api_c
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
    get_user_name,
    api_error_handler,
    validate_destination_id,
    get_token_from_request,
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

    parameters = [
        {
            "name": api_c.LOOKALIKEABLE,
            "description": "Only return audiences that are lookalikeable",
            "in": "query",
            "type": "string",
            "required": False,
            "default": False,
        },
        {
            "name": api_c.DELIVERIES,
            "description": "Number of delivery objects to return per audience",
            "in": "query",
            "type": "int",
            "required": False,
            "default": api_c.DEFAULT_AUDIENCE_DELIVERY_COUNT,
        },
    ]

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

        # get all audiences and deliveries
        database = get_db_client()
        audiences = orchestration_management.get_all_audiences_and_deliveries(
            database
        )

        # get all audiences because document DB does not allow for replaceRoot
        audience_dict = {
            x[db_c.ID]: x
            for x in orchestration_management.get_all_audiences(database)
        }

        # get customer sizes
        token_response = get_token_from_request(request)
        customer_size_dict = get_customers_count_async(
            token_response[0], audiences
        )

        # get the x number of last deliveries to provide per audience
        delivery_limit = int(
            request.args.get(
                api_c.DELIVERIES, api_c.DEFAULT_AUDIENCE_DELIVERY_COUNT
            )
        )

        # process each audience object
        for audience in audiences:
            # workaround because DocumentDB does not allow $replaceRoot
            # do replace root by bringing the nested engagement up a level.
            audience.update(audience_dict[audience[db_c.ID]])

            # take the last X number of deliveries
            # remove any empty ones, and only show the delivered/succeeded
            audience[api_c.DELIVERIES] = [
                x
                for x in audience[api_c.DELIVERIES]
                if x
                and x.get(db_c.STATUS)
                in [db_c.AUDIENCE_STATUS_DELIVERED, db_c.STATUS_SUCCEEDED]
            ][:delivery_limit]

            # set the destinations
            audience[api_c.DESTINATIONS_TAG] = add_destinations(
                database, audience.get(api_c.DESTINATIONS_TAG)
            )

            audience[api_c.SIZE] = customer_size_dict.get(audience[db_c.ID])
            audience[api_c.LOOKALIKEABLE] = is_audience_lookalikeable(audience)

        # get all lookalikes and append to the audience list
        lookalikes = destination_management.get_all_delivery_platform_lookalike_audiences(
            database
        )

        # set the is_lookalike property to True so UI knows it is a lookalike.
        for lookalike in lookalikes:
            lookalike[api_c.LOOKALIKEABLE] = False
            lookalike[api_c.IS_LOOKALIKE] = True

        # combine the two lists and serve.
        audiences += lookalikes

        # if lookalikeable flag was passed, filter out the audiences
        # that are not lookalikeable.
        if request.args.get(api_c.LOOKALIKEABLE, False):
            audiences = [
                x
                for x in audiences
                if x[api_c.LOOKALIKEABLE] == api_c.STATUS_ACTIVE
            ]

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

        token_response = get_token_from_request(request)

        database = get_db_client()

        # get the audience
        audience_id = ObjectId(audience_id)
        audience = orchestration_management.get_audience(database, audience_id)

        if not audience:
            # check if lookalike
            lookalike = destination_management.get_delivery_platform_lookalike_audience(
                database, audience_id
            )
            if not lookalike:
                logger.error("Audience with id %s not found.", audience_id)
                return {
                    "message": api_c.AUDIENCE_NOT_FOUND
                }, HTTPStatus.NOT_FOUND

            # grab the source audience ID of the lookalike
            audience = orchestration_management.get_audience(
                database, lookalike[db_c.LOOKALIKE_SOURCE_AUD_ID]
            )
            # set the filters from the audience object
            lookalike[db_c.AUDIENCE_FILTERS] = audience[db_c.AUDIENCE_FILTERS]
            lookalike[api_c.IS_LOOKALIKE] = True

            # set audience to lookalike
            audience = lookalike

        # get the audience insights
        engagement_deliveries = orchestration_management.get_audience_insights(
            database,
            audience[db_c.ID],
        )

        # process each engagement
        logger.info("Processing each engagement.")
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
            if {api_c.STATUS: api_c.STATUS_NOT_DELIVERED} in engagement[
                api_c.DELIVERIES
            ]:
                engagement[api_c.DELIVERIES].remove(
                    {api_c.STATUS: api_c.STATUS_NOT_DELIVERED}
                )

            # set the weighted status for the engagement based on deliveries
            engagement[api_c.STATUS] = weight_delivery_status(engagement)
            engagements.append(engagement)

        logger.info("Successfully processed each engagement.")
        # set the list of engagements for an audience
        audience[api_c.AUDIENCE_ENGAGEMENTS] = engagements

        # get the max last delivered date for all destinations in an audience
        delivery_times = [
            x[api_c.AUDIENCE_LAST_DELIVERED]
            for x in engagements
            if x.get(api_c.AUDIENCE_LAST_DELIVERED)
        ]
        audience[api_c.AUDIENCE_LAST_DELIVERED] = (
            max(delivery_times) if delivery_times else None
        )

        # set the destinations
        audience[api_c.DESTINATIONS_TAG] = add_destinations(
            database, audience.get(api_c.DESTINATIONS_TAG)
        )

        # get live audience size
        customers = get_customers_overview(
            token_response[0],
            {api_c.AUDIENCE_FILTERS: audience[api_c.AUDIENCE_FILTERS]},
        )

        # Add insights, size.
        audience[api_c.AUDIENCE_INSIGHTS] = customers
        audience[api_c.SIZE] = customers.get(api_c.TOTAL_CUSTOMERS)
        audience[
            api_c.LOOKALIKE_AUDIENCES
        ] = destination_management.get_all_delivery_platform_lookalike_audiences(
            database, {db_c.LOOKALIKE_SOURCE_AUD_ID: audience_id}
        )
        audience[api_c.LOOKALIKEABLE] = is_audience_lookalikeable(audience)

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

        token_response = get_token_from_request(request)

        # validate destinations
        database = get_db_client()
        if db_c.DESTINATIONS in body:
            # validate list of dict objects
            for destination in body[db_c.DESTINATIONS]:
                # check if dict instance
                if not isinstance(destination, dict):
                    logger.error("Destination must be objects.")
                    return {
                        "message": "destinations must be objects"
                    }, HTTPStatus.BAD_REQUEST

                # check if destination id assigned
                if db_c.OBJECT_ID not in destination:
                    logger.error(
                        "Destination object missing the %s field.",
                        db_c.OBJECT_ID,
                    )
                    return {
                        "message": f"{destination} missing the "
                        f"{db_c.OBJECT_ID} field."
                    }, HTTPStatus.BAD_REQUEST

                # validate object id
                # map to an object ID field
                # validate the destination object exists.
                destination[db_c.OBJECT_ID] = validate_destination_id(
                    destination[db_c.OBJECT_ID]
                )

        engagement_ids = []
        if api_c.AUDIENCE_ENGAGEMENTS in body:
            # validate list of dict objects
            for engagement_id in body[api_c.AUDIENCE_ENGAGEMENTS]:

                # map to an object ID field
                engagement_id = ObjectId(engagement_id)

                # validate the engagement object exists.
                if not engagement_management.get_engagement(
                    database, engagement_id
                ):
                    logger.error(
                        "Engagement with ID %s does not exist.", engagement_id
                    )
                    return {
                        "message": f"Engagement with ID {engagement_id} "
                        f"does not exist."
                    }
                engagement_ids.append(engagement_id)

        try:
            # get live audience size
            customers = get_customers_overview(
                token_response[0],
                {api_c.AUDIENCE_FILTERS: body.get(api_c.AUDIENCE_FILTERS)},
            )

            # create the audience
            audience_doc = orchestration_management.create_audience(
                database=database,
                name=body[api_c.AUDIENCE_NAME],
                audience_filters=body.get(api_c.AUDIENCE_FILTERS),
                destination_ids=body.get(api_c.DESTINATIONS),
                user_name=user_name,
                size=customers.get(api_c.TOTAL_CUSTOMERS, 0),
            )

            # add notification
            create_notification(
                database,
                db_c.NOTIFICATION_TYPE_SUCCESS,
                (
                    f'New audience named "{audience_doc[db_c.NAME]}" '
                    f"added by {user_name}."
                ),
                api_c.ORCHESTRATION_TAG,
            )

            # attach the audience to each of the engagements
            for engagement_id in engagement_ids:
                engagement = (
                    engagement_management.append_audiences_to_engagement(
                        database,
                        engagement_id,
                        user_name,
                        [
                            {
                                db_c.OBJECT_ID: audience_doc[db_c.ID],
                                db_c.DESTINATIONS: body.get(
                                    api_c.DESTINATIONS
                                ),
                            }
                        ],
                    )
                )
                # add audience attached notification
                create_notification(
                    database,
                    db_c.NOTIFICATION_TYPE_SUCCESS,
                    (
                        f'Audience "{audience_doc[db_c.NAME]}" '
                        f'added to engagement "{engagement[db_c.NAME]}" '
                        f"by {user_name}."
                    ),
                    api_c.ORCHESTRATION_TAG,
                )

        except db_exceptions.DuplicateName:
            logger.error(
                "Duplicate Audience name %s.", body[api_c.AUDIENCE_NAME]
            )
            return {
                "message": f"Duplicate name '{body[api_c.AUDIENCE_NAME]}'"
            }, HTTPStatus.BAD_REQUEST

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

        database = get_db_client()
        audience_doc = orchestration_management.update_audience(
            database=database,
            audience_id=ObjectId(audience_id),
            name=body.get(api_c.AUDIENCE_NAME),
            audience_filters=body.get(api_c.AUDIENCE_FILTERS),
            destination_ids=body.get(api_c.DESTINATIONS_TAG),
            user_name=user_name,
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            f'Audience "{audience_doc[db_c.NAME]}" updated by {user_name}.',
            api_c.ORCHESTRATION_TAG,
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
                    "ltv_predicted": {
                        "name": "Predicted lifetime value",
                        "type": "range",
                        "min": 0,
                        "max": 1100,
                        "steps": 20,
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


@add_view_to_blueprint(
    orchestration_bp,
    f"{api_c.LOOKALIKE_AUDIENCES_ENDPOINT}",
    "SetLookalikeAudience",
)
class SetLookalikeAudience(SwaggerView):
    """
    Set Lookalike Audience Class
    """

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Lookalike Audience Parameters.",
            "example": {
                api_c.NAME: "New Lookalike Audience",
                api_c.AUDIENCE_ID: str(ObjectId()),
                api_c.AUDIENCE_SIZE_PERCENTAGE: 1.5,
                api_c.ENGAGEMENT_IDS: [
                    str(ObjectId()),
                    str(ObjectId()),
                    str(ObjectId()),
                ],
            },
        }
    ]

    responses = {
        HTTPStatus.CREATED.value: {
            "schema": LookalikeAudienceGetSchema,
            "description": "Successfully created lookalike audience.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create a lookalike audience"
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use, unsubscriptable-object
    @api_error_handler()
    @get_user_name()
    def post(self, user_name: str) -> Tuple[dict, int]:
        """Sets lookalike audience

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user_name (str): user_name extracted from Okta

        Returns:
            Tuple[dict, int]: lookalike audience configuration, HTTP status.

        """

        body = LookalikeAudiencePostSchema().load(
            request.get_json(), partial=True
        )
        source_audience_id = body[api_c.AUDIENCE_ID]
        engagement_ids = body[api_c.ENGAGEMENT_IDS]

        database = get_db_client()
        source_audience = orchestration_management.get_audience(
            database, ObjectId(source_audience_id)
        )

        if not source_audience:
            logger.error("Audience %s not found.", body[api_c.AUDIENCE_ID])
            return {"message": api_c.AUDIENCE_NOT_FOUND}, HTTPStatus.NOT_FOUND

        destination = destination_management.get_delivery_platform_by_type(
            database, db_c.DELIVERY_PLATFORM_FACEBOOK
        )

        destination_connector = FacebookConnector(
            auth_details=get_auth_from_parameter_store(
                destination[api_c.AUTHENTICATION_DETAILS],
                destination[api_c.DELIVERY_PLATFORM_TYPE],
            )
        )

        if not destination_connector.check_connection():
            logger.error("Facebook authentication failed.")
            return {
                "message": api_c.DESTINATION_AUTHENTICATION_FAILED
            }, HTTPStatus.BAD_REQUEST

        most_recent_job = destination_management.get_all_delivery_jobs(
            database,
            {
                db_c.DELIVERY_PLATFORM_ID: destination[db_c.ID],
                db_c.AUDIENCE_ID: ObjectId(source_audience_id),
                db_c.ENGAGEMENT_ID: {
                    "$in": [ObjectId(x) for x in engagement_ids]
                },
                db_c.STATUS: {
                    "$in": [
                        db_c.STATUS_SUCCEEDED,
                        db_c.AUDIENCE_STATUS_DELIVERED,
                    ]
                },
            },
            limit=1,
        )

        # cursor returns a list, lets take the first one if data exist.
        most_recent_job = most_recent_job[0] if most_recent_job else None
        if most_recent_job is None:
            logger.error("%s.", api_c.SUCCESSFUL_DELIVERY_JOB_NOT_FOUND)
            return {
                "message": api_c.SUCCESSFUL_DELIVERY_JOB_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        timestamp = most_recent_job[db_c.JOB_START_TIME].strftime(
            db_c.AUDIENCE_NAME_DATE_FORMAT
        )

        destination_connector.get_new_lookalike_audience(
            f"{source_audience[db_c.NAME]} - {timestamp}",
            body[api_c.NAME],
            body[api_c.AUDIENCE_SIZE_PERCENTAGE],
            "US",
        )

        logger.info("Creating delivery platform lookalike audience.")
        lookalike_audience = (
            destination_management.create_delivery_platform_lookalike_audience(
                database,
                destination[db_c.ID],
                ObjectId(body[api_c.AUDIENCE_ID]),
                body[api_c.NAME],
                body[api_c.AUDIENCE_SIZE_PERCENTAGE],
                "US",
                user_name,
                0,  # TODO HUS-801 - set lookalike SIZE correctly.
            )
        )

        for engagement_id in body[api_c.ENGAGEMENT_IDS]:
            engagement_management.append_audiences_to_engagement(
                database,
                ObjectId(engagement_id),
                user_name,
                [
                    {
                        api_c.ID: lookalike_audience[db_c.ID],
                        db_c.LOOKALIKE: True,
                        api_c.DESTINATIONS: {api_c.ID: destination[db_c.ID]},
                    }
                ],
            )
        logger.info(
            "Successfully created delivery platform lookalike audience."
        )
        return (
            LookalikeAudienceGetSchema().dump(lookalike_audience),
            HTTPStatus.CREATED,
        )
