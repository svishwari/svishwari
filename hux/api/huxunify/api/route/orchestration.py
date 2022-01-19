# pylint: disable=too-many-lines,unused-argument
"""Paths for Orchestration API."""
import asyncio
import re
from http import HTTPStatus
from threading import Thread
from typing import Tuple, Union
from datetime import datetime, timedelta
import aiohttp
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, request, jsonify
from marshmallow import INCLUDE
from pymongo import MongoClient

from huxunifylib.util.general.logging import logger
from huxunifylib.connectors import (
    CustomAudienceDeliveryStatusError,
    FacebookConnector,
)

from huxunifylib.database.delete_util import delete_lookalike_audience
from huxunifylib.database.delivery_platform_management import (
    update_pending_delivery_jobs,
)
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database import (
    delivery_platform_management as destination_management,
    orchestration_management,
    engagement_management,
    engagement_audience_management as eam,
    collection_management as cm,
)
import huxunifylib.database.constants as db_c

from huxunify.api.exceptions import integration_api_exceptions as iae
from huxunify.api.schema.orchestration import (
    AudienceGetSchema,
    AudienceInsightsGetSchema,
    AudiencePutSchema,
    AudiencePostSchema,
    LookalikeAudiencePostSchema,
    LookalikeAudienceGetSchema,
    is_audience_lookalikeable,
    LookalikeAudiencePutSchema,
)
from huxunify.api.schema.engagement import (
    weight_delivery_status,
)
from huxunify.api.data_connectors.cdp import (
    get_customers_overview,
    get_demographic_by_state_async,
    get_city_ltvs_async,
    get_spending_by_gender_async,
    get_customers_overview_async,
)
from huxunify.api.data_connectors.aws import get_auth_from_parameter_store
from huxunify.api.data_connectors.okta import (
    get_token_from_request,
)
from huxunify.api.data_connectors.courier import (
    get_destination_config,
    get_audience_destination_pairs,
)
from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
    FAILED_DEPENDENCY_424_RESPONSE,
    get_next_schedule,
)
import huxunify.api.constants as api_c
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.route.utils import (
    get_db_client,
    group_gender_spending,
    Validation as validation,
    is_component_favorite,
    get_user_favorites,
    convert_unique_city_filter,
    match_rate_data_for_audience,
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


async def get_audience_insights_async(token: str, audience_filters: dict):
    """Fetch audience insights from CDM

    Args:
        token (str): OKTA JWT token.
        audience_filters (dict): Audience filters.

    Returns:
        dict: Audience insights object.
    """
    audience_insights = {}
    filters = (
        {api_c.AUDIENCE_FILTERS: audience_filters}
        if audience_filters
        else api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER
    )
    async with aiohttp.ClientSession() as session:
        responses = await asyncio.gather(
            get_demographic_by_state_async(
                session,
                token,
                filters,
            ),
            get_city_ltvs_async(
                session,
                token,
                filters,
            ),
            get_spending_by_gender_async(
                session,
                token,
                filters=filters,
                start_date=str(datetime.utcnow().date() - timedelta(days=180)),
                end_date=str(datetime.utcnow().date()),
            ),
            get_customers_overview_async(
                session,
                token,
                filters,
            ),
        )
    audience_insights[api_c.DEMOGRAPHIC] = responses[0]
    audience_insights[api_c.INCOME] = responses[1]
    audience_insights[api_c.SPEND] = group_gender_spending(responses[2])
    customers_overview = responses[3]
    audience_insights[api_c.GENDER] = {
        gender: {
            api_c.POPULATION_PERCENTAGE: customers_overview.get(gender, 0),
            api_c.SIZE: customers_overview.get(f"{gender}_{api_c.COUNT}", 0),
        }
        for gender in api_c.GENDERS
    }
    return audience_insights


def get_audience_standalone_deliveries(audience: dict) -> list:
    """Get standalone deliveries list of an audience built for GET audience
    by ID response.

     Args:
        audience (dict): audience dictionary.

    Returns:
        list: List of standalone audience deliveries.
    """
    if not audience.get(api_c.DESTINATIONS):
        return []
    database = get_db_client()

    standalone_deliveries = []
    standalone_delivery_jobs = destination_management.get_delivery_jobs(
        database,
        audience_id=audience[db_c.ID],
        engagement_id=db_c.ZERO_OBJECT_ID,
    )
    # extract delivery platform ids from the audience
    destination_ids = [
        x.get(api_c.ID)
        for x in audience[api_c.DESTINATIONS]
        if isinstance(x, dict)
    ]

    # get destinations at once to lookup name for each delivery job
    destination_dict = {
        x[db_c.ID]: x
        for x in destination_management.get_delivery_platforms_by_id(
            database, destination_ids
        )
    }
    if standalone_delivery_jobs:

        for job in standalone_delivery_jobs:
            # ignore deliveries to destinations no longer attached to the
            # audience
            if (
                job.get(db_c.DELIVERY_PLATFORM_ID)
                not in destination_dict.keys()
            ):
                continue

            # append the necessary schema to standalone_deliveries list
            standalone_deliveries.append(
                {
                    db_c.METRICS_DELIVERY_PLATFORM_NAME: destination_dict.get(
                        job.get(db_c.DELIVERY_PLATFORM_ID)
                    ).get(api_c.NAME),
                    api_c.DELIVERY_PLATFORM_TYPE: destination_dict.get(
                        job.get(db_c.DELIVERY_PLATFORM_ID)
                    ).get(api_c.DELIVERY_PLATFORM_TYPE),
                    api_c.STATUS: job.get(api_c.STATUS),
                    api_c.SIZE: job.get(db_c.DELIVERY_PLATFORM_AUD_SIZE, 0),
                    db_c.UPDATE_TIME: job.get(db_c.UPDATE_TIME),
                    db_c.DELIVERY_PLATFORM_ID: job.get(
                        db_c.DELIVERY_PLATFORM_ID
                    ),
                    db_c.IS_AD_PLATFORM: destination_dict.get(
                        job.get(db_c.DELIVERY_PLATFORM_ID)
                    ).get(db_c.IS_AD_PLATFORM),
                    db_c.LINK: destination_dict.get(
                        job.get(db_c.DELIVERY_PLATFORM_ID)
                    ).get(db_c.LINK),
                }
            )

    _ = [
        standalone_deliveries.append(
            {
                db_c.METRICS_DELIVERY_PLATFORM_NAME: destination_dict.get(
                    x
                ).get(api_c.NAME),
                api_c.DELIVERY_PLATFORM_TYPE: destination_dict.get(x).get(
                    api_c.DELIVERY_PLATFORM_TYPE
                ),
                api_c.STATUS: api_c.STATUS_NOT_DELIVERED,
                api_c.SIZE: 0,
                db_c.UPDATE_TIME: None,
                db_c.DELIVERY_PLATFORM_ID: x,
                db_c.LINK: destination_dict.get(x).get(db_c.LINK),
            }
        )
        for x in destination_ids
        if x
        not in [
            y.get(db_c.DELIVERY_PLATFORM_ID) for y in standalone_deliveries
        ]
    ]

    return standalone_deliveries


@add_view_to_blueprint(
    orchestration_bp, api_c.AUDIENCE_ENDPOINT, "AudienceView"
)
class AudienceView(SwaggerView):
    """Audience view class."""

    parameters = [
        {
            "name": api_c.LOOKALIKEABLE,
            "description": "Only return audiences that are lookalikeable",
            "in": "query",
            "type": "boolean",
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
        {
            "name": api_c.FAVORITES,
            "description": "Only return audiences favorited by the user",
            "in": "query",
            "type": "boolean",
            "required": False,
            "default": False,
            "example": "False",
        },
        {
            "name": api_c.WORKED_BY,
            "description": "Only return audiences worked on by the user",
            "in": "query",
            "type": "boolean",
            "required": False,
            "default": False,
            "example": "False",
        },
        {
            "name": api_c.ATTRIBUTE,
            "description": "Only return audiences matching the attributes",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "required": False,
            "example": "age",
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    # TODO: HUS-1791 - refactor.
    # pylint: disable=no-self-use,too-many-locals,too-many-statements,too-many-branches
    def get(self, user: dict) -> Tuple[list, int]:
        """Retrieves all audiences.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[list, int]: list of audience, HTTP status code.
        """

        database = get_db_client()
        # read the optional request args and set the required filter_dict to
        # query the DB.
        filter_dict = {}
        favorite_audiences = None
        favorite_lookalike_audiences = get_user_favorites(
            database, user[api_c.USER_NAME], api_c.LOOKALIKE
        )

        if request.args.get(api_c.FAVORITES) and validation.validate_bool(
            request.args.get(api_c.FAVORITES)
        ):
            favorite_audiences = get_user_favorites(
                database, user[api_c.USER_NAME], api_c.AUDIENCES
            )

        if request.args.get(api_c.WORKED_BY) and validation.validate_bool(
            request.args.get(api_c.WORKED_BY)
        ):
            filter_dict[api_c.WORKED_BY] = user[api_c.USER_NAME]

        attribute_list = request.args.getlist(api_c.ATTRIBUTE)
        # set the attribute_list to filter_dict only if it is populated and
        # validation is successful
        if attribute_list:
            filter_dict[api_c.ATTRIBUTE] = attribute_list

        # Update delivery status.
        logger.info("Updating delivery jobs")
        Thread(
            target=update_pending_delivery_jobs,
            args=[
                database,
            ],
        ).start()

        # get all audiences
        audiences = orchestration_management.get_all_audiences(
            database=database,
            filters=filter_dict,
            audience_ids=favorite_audiences,
        )

        # TODO - ENABLE AFTER WE HAVE A CACHING STRATEGY IN PLACE
        # # get customer sizes
        # customer_size_dict = get_customers_count_async(
        #     token_response[0], audiences
        # )

        # get the x number of last deliveries to provide per audience
        delivery_limit = (
            validation.validate_integer(request.args.get(api_c.DELIVERIES))
            if request.args.get(api_c.DELIVERIES)
            else api_c.DEFAULT_AUDIENCE_DELIVERY_COUNT
        )
        lookalikeable = (
            validation.validate_bool(request.args.get(api_c.LOOKALIKEABLE))
            if request.args.get(api_c.LOOKALIKEABLE)
            else False
        )

        # get unique destinations per audience across engagements
        audience_destinations = eam.get_all_engagement_audience_destinations(
            database
        )

        # Check if favourite audiences is not set
        if favorite_audiences is None:
            favorite_audiences = get_user_favorites(
                database, user[api_c.USER_NAME], api_c.AUDIENCES
            )

        # get list of deliveries and last_delivered for engagement, audience
        # pair by aggregating from engagements collection because document DB
        # does not allow for $replaceRoot
        audience_deliveries_dict = {
            x[db_c.AUDIENCE_ID]: {
                api_c.DELIVERIES: x.get(api_c.DELIVERIES, []),
                api_c.AUDIENCE_LAST_DELIVERED: x.get(
                    api_c.AUDIENCE_LAST_DELIVERED
                ),
            }
            for x in eam.get_all_engagement_audience_deliveries(
                database, audience_ids=list(x.get(db_c.ID) for x in audiences)
            )
        }

        # process each audience object
        for audience in audiences:

            # update the audience object with deliveries and last_delivery
            # fields from audience_deliveries_dict
            deliveries_dict = audience_deliveries_dict.get(audience[db_c.ID])
            if deliveries_dict:
                audience.update(deliveries_dict)
            else:
                audience[api_c.DELIVERIES] = []
                audience[api_c.AUDIENCE_LAST_DELIVERED] = None

            # find the matched audience destinations
            matched_destinations = [
                x
                for x in audience_destinations
                if x[db_c.ID] == audience[db_c.ID]
            ]

            # set the unique destinations
            audience[db_c.DESTINATIONS] = (
                matched_destinations[0].get(db_c.DESTINATIONS, [])
                if matched_destinations
                else []
            )

            # remove any empty ones, and only preserve that are delivered or
            # succeeded and if the delivery_platform_id is for a destination
            # that is part of audience destinations
            audience[api_c.DELIVERIES] = (
                [
                    aud_delivery
                    for aud_delivery in audience[api_c.DELIVERIES]
                    if aud_delivery
                    and (
                        aud_delivery.get(db_c.STATUS)
                        in [
                            db_c.AUDIENCE_STATUS_DELIVERED,
                            db_c.STATUS_SUCCEEDED,
                            db_c.AUDIENCE_STATUS_DELIVERING,
                        ]
                    )
                    and (
                        aud_delivery[db_c.DELIVERY_PLATFORM_ID]
                        == aud_destination[db_c.ID]
                        for aud_destination in audience[db_c.DESTINATIONS]
                    )
                ]
                if audience[db_c.DESTINATIONS]
                else []
            )

            # sort audience deliveries based on delivery_job's update_time in
            # descending order since document DB does not preserve soft order
            # if sort is done before group stage until version 4.0 as per
            # documentation
            audience[api_c.DELIVERIES].sort(
                key=lambda delivery: delivery[db_c.UPDATE_TIME], reverse=True
            )

            # set the lookalikeable field in audience before limiting the
            # number of deliveries in it based on delivery_limit
            audience[api_c.LOOKALIKEABLE] = is_audience_lookalikeable(audience)

            # set the weighted status for the audience based on deliveries
            # Calculate status before filtering deliveries by delivery_limit
            audience[api_c.STATUS] = weight_delivery_status(audience)

            # take the last X number of deliveries
            audience[api_c.DELIVERIES] = audience[api_c.DELIVERIES][
                :delivery_limit
            ]

            # if not a part of any engagements and not delivered.
            # set last delivery date to None.
            if audience[api_c.STATUS] == api_c.STATUS_NOT_DELIVERED:
                audience[api_c.AUDIENCE_LAST_DELIVERED] = None

            audience[api_c.FAVORITE] = bool(
                audience[db_c.ID] in favorite_audiences
            )

        # fetch lookalike audiences if lookalikeable is set to false
        # as lookalike audiences can not be lookalikeable
        if not lookalikeable:
            # get all lookalikes and append to the audience list
            query_filter = {db_c.DELETED: False}
            if request.args.get(api_c.FAVORITES) and validation.validate_bool(
                request.args.get(api_c.FAVORITES)
            ):
                query_filter[db_c.ID] = {"$in": favorite_lookalike_audiences}

            if request.args.get(api_c.WORKED_BY) and validation.validate_bool(
                request.args.get(api_c.WORKED_BY)
            ):
                query_filter.update(
                    {
                        "$or": [
                            {db_c.CREATED_BY: user[api_c.USER_NAME]},
                            {db_c.UPDATED_BY: user[api_c.USER_NAME]},
                        ]
                    }
                )

            if attribute_list:
                query_filter["$and"] = [
                    {
                        db_c.LOOKALIKE_ATTRIBUTE_FILTER_FIELD: {
                            "$regex": re.compile(rf"^{attribute}$(?i)")
                        }
                    }
                    for attribute in attribute_list
                ]

            lookalikes = cm.get_documents(
                database,
                db_c.LOOKALIKE_AUDIENCE_COLLECTION,
                query_filter,
                {db_c.DELETED: 0},
            )
            lookalikes = (
                []
                if lookalikes is None
                else lookalikes.get(db_c.DOCUMENTS, [])
            )

            # get the facebook delivery platform for lookalikes
            facebook_destination = (
                destination_management.get_delivery_platform_by_type(
                    database, db_c.DELIVERY_PLATFORM_FACEBOOK
                )
            )

            # set the is_lookalike property to True so UI knows it is a lookalike.
            for lookalike in lookalikes:
                lookalike[api_c.LOOKALIKEABLE] = False
                lookalike[api_c.IS_LOOKALIKE] = True

                lookalike[db_c.STATUS] = lookalike.get(
                    db_c.STATUS, db_c.AUDIENCE_STATUS_ERROR
                )
                lookalike[db_c.AUDIENCE_LAST_DELIVERED] = lookalike[
                    db_c.CREATE_TIME
                ]
                lookalike[db_c.DESTINATIONS] = (
                    [facebook_destination] if facebook_destination else []
                )
                lookalike[api_c.FAVORITE] = bool(
                    lookalike[db_c.ID] in favorite_lookalike_audiences
                )
                if db_c.LOOKALIKE_SOURCE_AUD_FILTERS in lookalike:
                    # rename the key
                    lookalike[db_c.AUDIENCE_FILTERS] = lookalike.pop(
                        db_c.LOOKALIKE_SOURCE_AUD_FILTERS
                    )

            # combine the two lists and serve.
            audiences += lookalikes

        else:
            # if lookalikeable is set to true, filter out the audiences
            # that are not lookalikeable.
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
    """Single Audience Get view class."""

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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use, too-many-locals, too-many-branches
    # pylint: disable=too-many-statements
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, audience_id: str, user: dict) -> Tuple[dict, int]:
        """Retrieves an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Audience, HTTP status code.
        """

        token_response = get_token_from_request(request)

        database = get_db_client()

        # Update delivery status.
        logger.info("Updating delivery jobs")
        Thread(
            target=update_pending_delivery_jobs,
            args=[
                database,
            ],
        ).start()

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

            lookalike[api_c.IS_LOOKALIKE] = True
            # set source audience attribute filters for the lookalike
            lookalike[db_c.AUDIENCE_FILTERS] = lookalike[
                db_c.LOOKALIKE_SOURCE_AUD_FILTERS
            ]
            # TODO: HUS-837 change once we can generate real lookalikes from FB.
            lookalike[api_c.MATCH_RATE] = 0
            # check and set if source/seed audience this lookalike audience is
            # created from exists in DB
            lookalike[api_c.LOOKALIKE_SOURCE_EXISTS] = bool(
                orchestration_management.get_audience(
                    database, lookalike[db_c.LOOKALIKE_SOURCE_AUD_ID]
                )
            )

            # set audience to lookalike
            audience = lookalike

        # get the audience insights
        engagement_deliveries = orchestration_management.get_audience_insights(
            database,
            audience[db_c.ID],
        )

        match_rate_data = {}
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

            # TODO: HUS-837 Change once match_rate data can be fetched from CDM
            # validate if engagement contain deliveries since there are checks
            # above to remove empty and not-delivered deliveries
            if api_c.DELIVERIES in engagement:
                for delivery in engagement[api_c.DELIVERIES]:

                    if delivery.get(api_c.IS_AD_PLATFORM) and not audience.get(
                        api_c.IS_LOOKALIKE, False
                    ):
                        # Todo remove when actual match rates are
                        #  populated.
                        delivery[api_c.MATCH_RATE] = 0
                        match_rate_data_for_audience(delivery, match_rate_data)

                    # Update time field can be missing if no deliveries.
                    if not delivery.get(db_c.UPDATE_TIME):
                        delivery[db_c.UPDATE_TIME] = None
                    if engagement.get(db_c.ENGAGEMENT_DELIVERY_SCHEDULE):
                        delivery[
                            db_c.ENGAGEMENT_DELIVERY_SCHEDULE
                        ] = engagement[db_c.ENGAGEMENT_DELIVERY_SCHEDULE][
                            api_c.SCHEDULE
                        ][
                            api_c.PERIODICIY
                        ]
                        delivery[api_c.NEXT_DELIVERY] = get_next_schedule(
                            engagement[db_c.ENGAGEMENT_DELIVERY_SCHEDULE][
                                api_c.SCHEDULE_CRON
                            ],
                            engagement[db_c.ENGAGEMENT_DELIVERY_SCHEDULE][
                                api_c.START_DATE
                            ],
                        )

            # set the weighted status for the engagement based on deliveries
            engagement[api_c.STATUS] = weight_delivery_status(engagement)
            engagements.append(engagement)

        logger.info("Successfully processed each engagement.")
        # set the list of engagements for an audience
        audience[api_c.AUDIENCE_ENGAGEMENTS] = engagements
        # set the list of standalone_deliveries for an audience
        standalone_deliveries = get_audience_standalone_deliveries(audience)

        # get the max last delivered date for all destinations in an audience
        delivery_times = [
            x[api_c.AUDIENCE_LAST_DELIVERED]
            for x in engagements
            if x.get(api_c.AUDIENCE_LAST_DELIVERED)
        ]
        audience[api_c.AUDIENCE_LAST_DELIVERED] = (
            max(delivery_times) if delivery_times else None
        )

        # get unique destinations per audience across engagements
        audience_destinations = eam.get_all_engagement_audience_destinations(
            database, [audience[db_c.ID]]
        )

        # check if any audiences returned, if so, set the destinations.
        audience[db_c.DESTINATIONS] = (
            audience_destinations[0].get(db_c.DESTINATIONS, [])
            if audience_destinations
            else []
        )

        # Add insights, size.
        audience[api_c.AUDIENCE_INSIGHTS] = get_customers_overview(
            token_response[0],
            {api_c.AUDIENCE_FILTERS: audience[api_c.AUDIENCE_FILTERS]},
        )
        audience[api_c.SIZE] = audience[api_c.AUDIENCE_INSIGHTS].get(
            api_c.TOTAL_CUSTOMERS, 0
        )

        # query DB and populate lookalike audiences in audience dict only if
        # the audience is not a lookalike audience since lookalike audience
        # cannot have lookalike audiences of its own

        audience[api_c.LOOKALIKE_AUDIENCES] = (
            destination_management.get_all_delivery_platform_lookalike_audiences(
                database, {db_c.LOOKALIKE_SOURCE_AUD_ID: audience_id}
            )
            if not audience.get(api_c.IS_LOOKALIKE, False)
            else []
        )

        if audience[api_c.LOOKALIKE_AUDIENCES]:
            for lookalike_audience in audience[api_c.LOOKALIKE_AUDIENCES]:
                lookalike_audience[
                    api_c.DELIVERY_PLATFORM_LINK
                ] = destination_management.get_delivery_platform(
                    database, lookalike_audience.get(db_c.DELIVERY_PLATFORM_ID)
                ).get(
                    db_c.LINK
                )

        for delivery in standalone_deliveries:
            if delivery.get(api_c.IS_AD_PLATFORM) and not audience.get(
                api_c.IS_LOOKALIKE, False
            ):
                match_rate_data_for_audience(delivery, match_rate_data)

        if engagements:
            # TODO: HUS-1992 - below code needs to be revised to set
            #  audience["lookalikeable"] by passing in the audience object that
            #  has deliveries populated within
            # set lookalikeable value in audience as per history of deliveries made
            # against all engagements the audience is attached to to keep it
            # consistent with GET all audiences response
            audience_deliveries = eam.get_all_engagement_audience_deliveries(
                database, audience_ids=[audience_id]
            )
            audience_deliveries = audience_deliveries + standalone_deliveries
        else:
            audience_deliveries = standalone_deliveries
        if audience_deliveries:
            audience_deliveries[0][api_c.DELIVERIES] = (
                [
                    aud_delivery
                    for aud_delivery in audience_deliveries[0].get(
                        api_c.DELIVERIES, []
                    )
                    if aud_delivery
                    and (
                        aud_delivery.get(db_c.STATUS)
                        in [
                            db_c.AUDIENCE_STATUS_DELIVERED,
                            db_c.STATUS_SUCCEEDED,
                        ]
                    )
                    and (
                        aud_delivery[db_c.DELIVERY_PLATFORM_ID]
                        == aud_destination[db_c.ID]
                        for aud_destination in audience[db_c.DESTINATIONS]
                    )
                ]
                if audience[db_c.DESTINATIONS]
                else []
            )
            audience[api_c.LOOKALIKEABLE] = is_audience_lookalikeable(
                audience_deliveries[0]
            )
        else:
            audience[api_c.LOOKALIKEABLE] = api_c.STATUS_DISABLED

        audience.update(
            {
                api_c.DIGITAL_ADVERTISING: {
                    api_c.MATCH_RATES: [
                        {
                            api_c.DESTINATION: delivery_platform_data[0],
                            api_c.MATCH_RATE: delivery_platform_data[1].get(
                                api_c.MATCH_RATE
                            ),
                            api_c.AUDIENCE_LAST_DELIVERY: delivery_platform_data[
                                1
                            ].get(
                                api_c.AUDIENCE_LAST_DELIVERY
                            ),
                        }
                        for delivery_platform_data in match_rate_data.items()
                    ]
                }
                if match_rate_data
                else None,
                api_c.AUDIENCE_STANDALONE_DELIVERIES: standalone_deliveries,
                api_c.FAVORITE: is_component_favorite(
                    user[db_c.OKTA_ID], api_c.AUDIENCES, str(audience_id)
                ),
            }
        )
        return (
            AudienceGetSchema(unknown=INCLUDE).dump(audience),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    orchestration_bp,
    f"{api_c.AUDIENCE_ENDPOINT}/<audience_id>/{api_c.AUDIENCE_INSIGHTS}",
    "AudienceInsightsGetView",
)
class AudienceInsightsGetView(SwaggerView):
    """Single Audience Insights Get view class."""

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
            "schema": AudienceInsightsGetSchema,
            "description": "Retrieved Audience insights.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve audience insights.",
            "schema": {
                "example": {"message": "Failed to retrieve audience insights"},
            },
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, audience_id: str, user: dict) -> Tuple[dict, int]:
        """Retrieves audience insights for an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: AudienceInsights, HTTP status code.
        """

        token_response = get_token_from_request(request)

        database = get_db_client()

        # get the audience
        audience_id = ObjectId(audience_id)

        audience = orchestration_management.get_audience(database, audience_id)
        lookalike = (
            destination_management.get_delivery_platform_lookalike_audience(
                database, audience_id
            )
        )

        if not audience and not lookalike:
            logger.error("Audience with id %s not found.", audience_id)
            return {"message": api_c.AUDIENCE_NOT_FOUND}, HTTPStatus.NOT_FOUND

        if not audience and lookalike:
            # grab the source audience ID of the lookalike
            audience = orchestration_management.get_audience(
                database, lookalike[db_c.LOOKALIKE_SOURCE_AUD_ID]
            )

        audience_insights = {}

        # check if the source audience exists.
        if audience:
            audience_insights = asyncio.run(
                get_audience_insights_async(
                    token_response[0],
                    audience[api_c.AUDIENCE_FILTERS],
                )
            )

        return (
            AudienceInsightsGetSchema(unknown=INCLUDE).dump(audience_insights),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    orchestration_bp,
    api_c.AUDIENCE_ENDPOINT,
    "AudiencePostView",
)
class AudiencePostView(SwaggerView):
    """Audience Post view class."""

    parameters = [
        {
            "name": api_c.DELIVER,
            "description": "Create and Deliver",
            "in": "query",
            "type": "boolean",
            "required": "false",
            "default": "false",
        },
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
                            db_c.DATA_EXTENSION_NAME: "Deloitte SFMC Ext"
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
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def post(self, user: dict) -> Tuple[dict, int]:
        """Creates a new audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Created audience, HTTP status code.
        """

        body = AudiencePostSchema().load(request.get_json(), partial=True)

        token_response = get_token_from_request(request)

        # validate destinations
        database = get_db_client()
        if db_c.DESTINATIONS in body:
            # validate list of dict objects
            for destination in body[api_c.DESTINATIONS]:
                # validate object id
                # map to an object ID field
                # validate the destination object exists.
                destination[db_c.OBJECT_ID] = ObjectId(
                    destination[db_c.OBJECT_ID]
                )
                destination[db_c.DATA_ADDED] = datetime.utcnow()

                if not destination_management.get_delivery_platform(
                    get_db_client(), destination[db_c.OBJECT_ID]
                ):
                    logger.error(
                        "Could not find destination with id %s.",
                        destination[db_c.OBJECT_ID],
                    )
                    return {
                        "message": api_c.DESTINATION_NOT_FOUND
                    }, HTTPStatus.NOT_FOUND

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
                    }, HTTPStatus.NOT_FOUND
                engagement_ids.append(engagement_id)
        audience_filters = convert_unique_city_filter(
            {api_c.AUDIENCE_FILTERS: body.get(api_c.AUDIENCE_FILTERS)}
        )
        # get live audience size
        customers = get_customers_overview(
            token_response[0],
            audience_filters,
        )

        # create the audience
        audience_doc = orchestration_management.create_audience(
            database=database,
            name=body[api_c.AUDIENCE_NAME],
            audience_filters=audience_filters.get(api_c.AUDIENCE_FILTERS),
            destination_ids=body.get(api_c.DESTINATIONS),
            user_name=user[api_c.USER_NAME],
            size=customers.get(api_c.TOTAL_CUSTOMERS, 0),
        )

        # add notification
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f'New audience named "{audience_doc[db_c.NAME]}" '
                f"added by {user[api_c.USER_NAME]}."
            ),
            api_c.ORCHESTRATION_TAG,
            user[api_c.USER_NAME],
        )

        # attach the audience to each of the engagements
        for engagement_id in engagement_ids:
            engagement = engagement_management.append_audiences_to_engagement(
                database,
                engagement_id,
                user[api_c.USER_NAME],
                [
                    {
                        db_c.OBJECT_ID: audience_doc[db_c.ID],
                        db_c.DESTINATIONS: body.get(api_c.DESTINATIONS),
                    }
                ],
            )
            # add audience attached notification
            create_notification(
                database,
                db_c.NOTIFICATION_TYPE_SUCCESS,
                (
                    f'Audience "{audience_doc[db_c.NAME]}" '
                    f'added to engagement "{engagement[db_c.NAME]}" '
                    f"by {user[api_c.USER_NAME]}."
                ),
                api_c.ORCHESTRATION_TAG,
                user[api_c.USER_NAME],
            )

        # deliver audience
        if request.args.get(api_c.DELIVER):
            # TODO: make this OOP between routes.

            # get engagements
            engagements = engagement_management.get_engagements_by_audience(
                database, audience_doc[db_c.ID]
            )

            # submit jobs for the audience/destination pairs
            for engagement in engagements:
                for pair in get_audience_destination_pairs(
                    engagement[api_c.AUDIENCES]
                ):
                    if pair[0] != audience_doc[db_c.ID]:
                        continue
                    batch_destination = get_destination_config(
                        database, engagement[db_c.ID], *pair
                    )
                    batch_destination.register()
                    batch_destination.submit()

        return AudienceGetSchema().dump(audience_doc), HTTPStatus.CREATED


@add_view_to_blueprint(
    orchestration_bp,
    f"{api_c.AUDIENCE_ENDPOINT}/<audience_id>",
    "AudiencePutView",
)
class AudiencePutView(SwaggerView):
    """Audience Put view class."""

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
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def put(self, audience_id: str, user: dict) -> Tuple[dict, int]:
        """Updates an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: Audience doc, HTTP status code.
        """

        # load into the schema object
        body = AudiencePutSchema().load(request.get_json(), partial=True)
        database = get_db_client()

        if not orchestration_management.get_audience(
            database, ObjectId(audience_id)
        ):
            return {
                api_c.MESSAGE: api_c.AUDIENCE_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        # validate destinations
        if db_c.DESTINATIONS in body:
            # validate list of dict objects
            for destination in body[api_c.DESTINATIONS]:
                # map to an object ID field
                # validate the destination object exists.
                destination[db_c.OBJECT_ID] = ObjectId(
                    destination[db_c.OBJECT_ID]
                )

                if not destination_management.get_delivery_platform(
                    database, destination[db_c.OBJECT_ID]
                ):
                    logger.error(
                        "Could not find destination with id %s.",
                        destination[db_c.OBJECT_ID],
                    )
                    return {
                        "message": api_c.DESTINATION_NOT_FOUND
                    }, HTTPStatus.NOT_FOUND

        audience_doc = orchestration_management.update_audience(
            database=database,
            audience_id=ObjectId(audience_id),
            name=body.get(api_c.AUDIENCE_NAME),
            audience_filters=convert_unique_city_filter(
                {api_c.AUDIENCE_FILTERS: body.get(api_c.AUDIENCE_FILTERS)}
            ).get(api_c.AUDIENCE_FILTERS)
            if body.get(api_c.AUDIENCE_FILTERS)
            else body.get(api_c.AUDIENCE_FILTERS),
            destination_ids=body.get(api_c.DESTINATIONS),
            user_name=user[api_c.USER_NAME],
        )

        # check if any engagements to add, otherwise return.
        if not body.get(api_c.ENGAGEMENT_IDS):
            return AudienceGetSchema().dump(audience_doc), HTTPStatus.OK

        # audience put engagement ids
        put_engagement_ids = [
            ObjectId(x) for x in body.get(api_c.ENGAGEMENT_IDS)
        ]

        # loop each engagement
        removed = []
        for engagement in engagement_management.get_engagements(database):
            # check if audience is in the engagement doc
            audience_in_engagement = audience_doc[db_c.ID] in [
                x[db_c.OBJECT_ID] for x in engagement[db_c.AUDIENCES]
            ]

            # evaluate engagement
            if (
                engagement[db_c.ID] in put_engagement_ids
                and audience_in_engagement
            ):
                # audience is in engagement and engagement is in PUT ids.
                # no update is needed for this scenario.
                pass
            elif engagement[db_c.ID] in put_engagement_ids:
                # engagement is in the PUT ids, but the audience is not.
                # append audience to the engagement.
                engagement_management.append_audiences_to_engagement(
                    database,
                    engagement.get(db_c.ID),
                    user[api_c.USER_NAME],
                    [
                        {
                            db_c.OBJECT_ID: audience_doc[db_c.ID],
                            db_c.DESTINATIONS: audience_doc[db_c.DESTINATIONS],
                        }
                    ],
                )
            elif audience_in_engagement:
                # audience is in engagement, but the engagement is not in the PUT ids.
                # remove the audience from engagement.
                engagement_management.remove_audiences_from_engagement(
                    database,
                    engagement[db_c.ID],
                    user[api_c.USER_NAME],
                    [audience_doc[db_c.ID]],
                )
                removed.append(engagement[db_c.ID])

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            f'Audience "{audience_doc[db_c.NAME]}" updated by {user[api_c.USER_NAME]}.',
            api_c.ORCHESTRATION_TAG,
            user[api_c.USER_NAME],
        )

        return AudienceGetSchema().dump(audience_doc), HTTPStatus.OK


@add_view_to_blueprint(
    orchestration_bp, f"{api_c.AUDIENCE_ENDPOINT}/rules", "AudienceRules"
)
class AudienceRules(SwaggerView):
    """Audience rules class."""

    responses = {
        HTTPStatus.OK.value: {"description": "Get audience rules dictionary"},
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get all audience rules."
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[dict, int]:
        """Retrieves all audience rules.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: dict of audience rules, HTTP status code.
        """

        rules_constants = {
            "text_operators": {
                "contains": "Contains",
                "not_contains": "Does not contain",
                "equals": "Equals",
                "not_equals": "Does not equal",
            }
        }

        # TODO HUS-356. Stubbed, this will come from CDM
        # Min/ max values will come from cdm, we will build this dynamically
        # list of genders will come from cdm
        # locations will come from cdm
        rules_from_cdm = {
            "rule_attributes": {
                "model_scores": {
                    "age_density": {
                        "name": "Propensity to unsubscribe",
                        "type": "range",
                        "min": 0,
                        "max": 99,
                        "steps": 5,
                        "values": [
                            (46, 3631),
                            (51, 2807),
                            (55, 2131),
                            (54, 2261),
                            (25, 3284),
                            (69, 421),
                            (43, 4012),
                            (26, 3386),
                            (63, 955),
                            (24, 3099),
                            (59, 1485),
                            (70, 350),
                            (77, 107),
                            (18, 8804),
                            (64, 867),
                            (31, 4097),
                            (56, 1916),
                            (34, 4392),
                            (21, 2623),
                            (44, 3878),
                            (48, 3394),
                            (19, 2207),
                            (52, 2703),
                            (78, 86),
                            (61, 1125),
                            (73, 218),
                            (36, 4417),
                            (57, 1835),
                            (60, 1265),
                            (49, 3188),
                            (39, 4407),
                            (20, 2453),
                            (45, 3883),
                            (30, 3997),
                            (28, 3855),
                            (65, 760),
                            (32, 4348),
                            (40, 4370),
                            (22, 2797),
                            (27, 3612),
                            (50, 2944),
                            (72, 265),
                            (67, 571),
                            (29, 3914),
                            (33, 4233),
                            (42, 4111),
                            (58, 1597),
                            (23, 2989),
                            (38, 4394),
                            (53, 2381),
                            (68, 443),
                            (47, 3531),
                            (71, 303),
                            (37, 4298),
                            (75, 202),
                            (66, 658),
                            (41, 4261),
                            (62, 1063),
                            (79, 65),
                            (35, 4500),
                            (74, 208),
                            (76, 128),
                        ],
                    },
                    "propensity_to_unsubscribe": {
                        "name": "Propensity to unsubscribe",
                        "type": "range",
                        "min": 0.0,
                        "max": 1.0,
                        "steps": 0.05,
                        "values": [
                            (0.024946739301654024, 11427),
                            (0.07496427927927932, 11322),
                            (0.12516851755300673, 11508),
                            (0.17490722222222196, 11340),
                            (0.22475237305041784, 11028),
                            (0.27479887395267527, 10861),
                            (0.32463341819221986, 10488),
                            (0.3748012142488386, 9685),
                            (0.424857603462838, 9472),
                            (0.4748600344076149, 8719),
                            (0.5247584942372063, 8069),
                            (0.5748950945245762, 7141),
                            (0.6248180486698927, 6616),
                            (0.6742800016897607, 5918),
                            (0.7240552640642912, 5226),
                            (0.7748771045863732, 4666),
                            (0.8245333194000475, 4067),
                            (0.8741182097701148, 3480),
                            (0.9238849161073824, 2980),
                            (0.9741102931596075, 2456),
                        ],
                    },
                    "ltv_predicted": {
                        "name": "Predicted lifetime value",
                        "type": "range",
                        "min": 0,
                        "max": 998.80,
                        "steps": 20,
                        "values": [
                            (25.01266121420892, 20466),
                            (74.90030921605447, 19708),
                            (124.93400516206559, 18727),
                            (174.636775834374, 17618),
                            (224.50257155855883, 15540),
                            (274.4192853530467, 14035),
                            (324.5557537562226, 11650),
                            (374.0836229319332, 9608),
                            (424.08129865033845, 7676),
                            (474.0542931632165, 6035),
                            (523.573803219089, 4610),
                            (573.6697460367739, 3535),
                            (623.295952316871, 2430),
                            (674.0507447610822, 1737),
                            (722.9281163886425, 1127),
                            (773.0364963285016, 828),
                            (823.8157326407769, 515),
                            (872.0919142507652, 327),
                            (922.9545223902437, 205),
                            (975.5857619444447, 108),
                        ],
                    },
                    "propensity_to_purchase": {
                        "name": "Propensity to purchase",
                        "type": "range",
                        "min": 0.0,
                        "max": 1.0,
                        "steps": 0.05,
                        "values": [
                            (0.02537854973094943, 11522),
                            (0.07478697708351197, 11651),
                            (0.1248279331496129, 11249),
                            (0.1747714344852409, 11112),
                            (0.2249300773782431, 10985),
                            (0.2748524565641576, 10763),
                            (0.32492868003913766, 10220),
                            (0.3745931779533858, 9997),
                            (0.42461185061435747, 9278),
                            (0.4747488547963946, 8767),
                            (0.5245381213163091, 8144),
                            (0.5748252185124849, 7368),
                            (0.6245615267403664, 6694),
                            (0.6745955099966098, 5902),
                            (0.7241630427350405, 5265),
                            (0.7744812744022826, 4559),
                            (0.824692568267536, 3977),
                            (0.8744300917431203, 3379),
                            (0.9241139159001297, 3044),
                            (0.9740590406189552, 2585),
                        ],
                    },
                },
                "general": {
                    "age": {
                        "name": "Age",
                        "type": "range",
                        "min": 18,
                        "max": 79,
                    },
                    "email": {
                        "name": "Email",
                        "type": "list",
                        "options": [{"fake.com": "fake.com"}],
                    },
                    "gender": {
                        "name": "Gender",
                        "type": "list",  # text for 5.0, list for future
                        "options": [
                            {
                                "female": "Female",
                            },
                            {
                                "male": "Male",
                            },
                            {
                                "other": "Other",
                            },
                        ],
                    },
                    "location": {
                        "name": "Location",
                        "country": {
                            "name": "Country",
                            "type": "list",
                            "options": [{"US": "USA"}],
                        },
                        "state": {
                            "name": "State",
                            "type": "list",
                            "options": [
                                {key: value}
                                for key, value in api_c.STATE_NAMES.items()
                            ],
                        },
                        "city": {
                            "name": "City",
                            "type": "list",
                            "options": [],
                        },
                        "zip_code": {
                            "name": "Zip",
                            "type": "list",
                            "options": [],
                        },
                    },
                },
            }
        }

        rules_constants.update(rules_from_cdm)

        return rules_constants, HTTPStatus.OK.value


@add_view_to_blueprint(
    orchestration_bp,
    f"{api_c.LOOKALIKE_AUDIENCES_ENDPOINT}",
    "SetLookalikeAudience",
)
class SetLookalikeAudience(SwaggerView):
    """Set Lookalike Audience Class."""

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
        HTTPStatus.ACCEPTED.value: {
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
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def post(self, user: dict) -> Tuple[dict, int]:
        """Create lookalike audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[dict, int]: lookalike audience configuration,
                HTTP status code.

        Raises:
            FailedDestinationDependencyError: Destination Dependency
                error.
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
            raise iae.FailedDestinationDependencyError(
                destination[api_c.NAME], HTTPStatus.FAILED_DEPENDENCY
            )

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

        try:
            # set status to error for now.
            status = api_c.STATUS_ERROR
            # Commented as creating lookalike audience is restricted in facebook
            # as we are using fake customer data
            # timestamp = most_recent_job[db_c.JOB_START_TIME].strftime(
            #     db_c.AUDIENCE_NAME_DATE_FORMAT
            # )
            #
            # destination_connector.get_new_lookalike_audience(
            #     f"{source_audience[db_c.NAME]} - {timestamp}",
            #     body[api_c.NAME],
            #     body[api_c.AUDIENCE_SIZE_PERCENTAGE],
            #     "US",
            # )

            logger.info("Creating delivery platform lookalike audience.")
            lookalike_audience = destination_management.create_delivery_platform_lookalike_audience(
                database,
                destination[db_c.ID],
                source_audience,
                body[api_c.NAME],
                body[api_c.AUDIENCE_SIZE_PERCENTAGE],
                "US",
                user[api_c.USER_NAME],
                0,  # TODO HUS-801 - set lookalike SIZE correctly.
                status,
            )

        except CustomAudienceDeliveryStatusError:
            return {
                "message": (
                    f"Failed to create a lookalike audience, "
                    f"{body[api_c.NAME]}: the selected audience "
                    f"to create a lookalike from is inactive or unusable.",
                ),
            }, HTTPStatus.NOT_FOUND

        for engagement_id in body[api_c.ENGAGEMENT_IDS]:
            engagement_management.append_audiences_to_engagement(
                database,
                ObjectId(engagement_id),
                user[api_c.USER_NAME],
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

        # add notification
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f"New lookalike audience named "
                f'"{lookalike_audience[db_c.NAME]}" added by {user[api_c.USER_NAME]}.'
            ),
            api_c.ORCHESTRATION_TAG,
            user[api_c.USER_NAME],
        )
        return (
            LookalikeAudienceGetSchema().dump(lookalike_audience),
            HTTPStatus.ACCEPTED,
        )


@add_view_to_blueprint(
    orchestration_bp,
    f"{api_c.LOOKALIKE_AUDIENCES_ENDPOINT}/<audience_id>",
    "EditLookalikeAudience",
)
class PutLookalikeAudience(SwaggerView):
    """Set Lookalike Audience Class."""

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Lookalike Audience Parameters.",
            "example": {
                api_c.NAME: "New Lookalike Audience Name",
            },
        },
    ]

    responses = {
        HTTPStatus.ACCEPTED.value: {
            "schema": LookalikeAudienceGetSchema,
            "description": "Successfully edited lookalike audience.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to edit the lookalike audience"
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use, unsubscriptable-object
    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def put(self, audience_id: str, user: dict) -> Tuple[dict, int]:
        """Edits lookalike audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): ID of the audience to be deleted.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: lookalike audience configuration,
                HTTP status code.

        Raises:
            FailedDestinationDependencyError: Destination Dependency
                error.
        """

        body = LookalikeAudiencePutSchema().load(
            request.get_json(), partial=True
        )

        database = get_db_client()

        update_doc = orchestration_management.update_lookalike_audience(
            database,
            ObjectId(audience_id),
            body[api_c.NAME],
            user[api_c.USER_NAME],
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f'Lookalike audience "{update_doc[db_c.NAME]}" '
                f"edited by {user[api_c.USER_NAME]}."
            ),
            api_c.ORCHESTRATION_TAG,
            user[api_c.USER_NAME],
        )

        return (
            LookalikeAudienceGetSchema().dump(update_doc),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    orchestration_bp,
    f"{api_c.AUDIENCE_ENDPOINT}/<audience_id>",
    "DeleteAudienceView",
)
class DeleteAudienceView(SwaggerView):
    """Hard deletes an audience."""

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
        HTTPStatus.NO_CONTENT.value: {
            "description": "Successfully deleted the audience from the database.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to delete the audience.",
            "schema": {
                "example": {"message": "Destination cannot be validated"},
            },
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def delete(self, audience_id: str, user: dict) -> Tuple[dict, int]:
        """Deletes an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): ID of the audience to be deleted.
            user (dict): user object.

        Returns:
            Tuple[dict, int]: response dict, HTTP status code.
        """

        database = get_db_client()

        # get the audience first
        # The code exists like this to cover scenario of two users
        # deleting the same resource at almost the same time
        audience = cm.get_document(
            database,
            db_c.AUDIENCES_COLLECTION,
            {db_c.ID: ObjectId(audience_id)},
        )

        # attempt to delete the audience from audiences collection first
        if audience:
            deleted_audience = orchestration_management.delete_audience(
                database, ObjectId(audience_id)
            )

            if deleted_audience:
                return {api_c.MESSAGE: {}}, HTTPStatus.NO_CONTENT
            logger.info(
                "Failed to delete audience %s by user %s.",
                audience_id,
                user[api_c.USER_NAME],
            )
            return {
                api_c.MESSAGE: api_c.OPERATION_FAILED
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        # attempt to delete the audience from lookalike_audiences collection
        # if audience not found in audiences collection
        audience = cm.get_document(
            database,
            db_c.LOOKALIKE_AUDIENCE_COLLECTION,
            {db_c.ID: ObjectId(audience_id)},
        )

        if not audience:
            return {api_c.MESSAGE: {}}, HTTPStatus.NO_CONTENT

        deleted_audience = delete_lookalike_audience(
            database, ObjectId(audience_id), soft_delete=False
        )

        # return failure if no document is deleted from either audiences
        # or lookalike_audiences collection
        if not deleted_audience:
            logger.info(
                "Failed to delete audience %s by user %s.",
                audience_id,
                user[api_c.USER_NAME],
            )
            return {
                api_c.MESSAGE: api_c.OPERATION_FAILED
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        delete_audience_from_engagements = (
            engagement_management.remove_audience_from_all_engagements(
                database, ObjectId(audience_id), user[api_c.USER_NAME]
            )
        )

        if not delete_audience_from_engagements:
            logger.info(
                "Failed to delete audience %s from engagements by user %s.",
                audience_id,
                user[api_c.USER_NAME],
            )
            return {
                api_c.MESSAGE: api_c.OPERATION_FAILED
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        logger.info(
            "Successfully deleted audience %s by user %s.",
            audience_id,
            user[api_c.USER_NAME],
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            f'Audience "{audience[db_c.NAME]}" successfully deleted by {user[api_c.USER_NAME]}.',
            api_c.ORCHESTRATION_TAG,
            user[api_c.USER_NAME],
        )

        return {api_c.MESSAGE: {}}, HTTPStatus.NO_CONTENT
