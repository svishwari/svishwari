# pylint: disable=too-many-lines,unused-argument,too-many-locals,
# too-many-function-args
"""Paths for Orchestration API."""
import asyncio
import re
import time
from http import HTTPStatus
from typing import Tuple, Union
from datetime import datetime, timedelta
import aiohttp
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, request, Response
from marshmallow import INCLUDE
from pymongo import MongoClient

from huxunifylib.util.general.logging import logger
from huxunifylib.connectors import (
    CustomAudienceDeliveryStatusError,
    FacebookConnector,
)

from huxunifylib.database.user_management import (
    delete_favorite_from_all_users,
)
import huxunifylib.database.constants as db_c
from huxunifylib.database.delete_util import delete_lookalike_audience
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database import (
    delivery_platform_management as destination_management,
    orchestration_management,
    engagement_management,
    engagement_audience_management as eam,
    collection_management as cm,
)

from huxunify.api.data_connectors.cloud.cloud_client import CloudClient
from huxunify.api.config import get_config
from huxunify.api.route.return_util import HuxResponse
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
    AudiencesBatchGetSchema,
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
    get_customer_event_types,
    get_customer_count_by_country,
)
from huxunify.api.data_connectors.aws import get_auth_from_parameter_store
from huxunify.api.data_connectors.cache import Caching
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
    convert_filters_for_events,
    convert_filters_for_contact_preference,
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
                    db_c.UPDATE_TIME: job.get(
                        db_c.UPDATE_TIME, job[db_c.CREATE_TIME]
                    ),
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
                db_c.DELIVERY_PLATFORM_ID: x,
                db_c.LINK: destination_dict.get(x).get(db_c.LINK),
                db_c.IS_AD_PLATFORM: destination_dict.get(x).get(
                    db_c.IS_AD_PLATFORM
                ),
            }
        )
        for x in destination_ids
        if x
        not in [
            y.get(db_c.DELIVERY_PLATFORM_ID) for y in standalone_deliveries
        ]
    ]

    return list(
        {
            value[db_c.DELIVERY_PLATFORM_ID]: value
            for value in sorted(
                standalone_deliveries,
                key=lambda x: x.get(db_c.UPDATE_TIME, datetime.utcnow()),
            )
        }.values()
    )


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
        {
            "name": api_c.EVENTS,
            "description": "Only return audiences matching the selected filters",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "required": False,
            "example": "created",
        },
        {
            "name": api_c.INDUSTRY_TAG,
            "description": "Only return audiences matching the industry tag",
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "required": False,
            "example": api_c.HEALTHCARE,
        },
        {
            "name": api_c.QUERY_PARAMETER_BATCH_SIZE,
            "in": "query",
            "type": "string",
            "description": "Max number of audiences to be returned. 0 returns all audiences",
            "example": api_c.AUDIENCES_DEFAULT_BATCH_SIZE,
            "required": False,
            "default": api_c.AUDIENCES_DEFAULT_BATCH_SIZE,
        },
        {
            "name": api_c.QUERY_PARAMETER_BATCH_NUMBER,
            "in": "query",
            "type": "string",
            "description": "Number of audiences per batch to be returned.",
            "example": api_c.DEFAULT_BATCH_NUMBER,
            "required": False,
            "default": api_c.DEFAULT_BATCH_NUMBER,
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of Audiences with total number of audiences.",
            "schema": AudiencesBatchGetSchema,
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

        events_list = request.args.getlist(api_c.EVENTS)
        # set the attribute_list to filter_dict only if it is populated and
        # validation is successful
        if events_list:
            filter_dict[db_c.EVENT] = events_list

        attribute_list = request.args.getlist(api_c.ATTRIBUTE)
        if attribute_list:
            # if the attribute filter list from the request contains contact_
            # preference, then update the filter dict with the CDM specific
            # filters the audiences collection is set
            if api_c.AUDIENCE_FILTER_CONTACT_PREFERENCE in attribute_list:
                filter_dict[
                    api_c.CONTACT_PREFERENCE_ATTRIBUTE
                ] = api_c.AUDIENCE_FILTER_CONTACT_PREFERENCES_CDM
                # remove the contact_preference filter from the attribute_list
                attribute_list.remove(api_c.AUDIENCE_FILTER_CONTACT_PREFERENCE)

            # update the filter_dict
            filter_dict[api_c.ATTRIBUTE] = attribute_list

        industry_tag_list = request.args.getlist(api_c.INDUSTRY_TAG)
        # set the industry_tag_list to filter_dict only if it is populated and
        # validation is successful
        if industry_tag_list:
            filter_dict[api_c.INDUSTRY_TAG] = industry_tag_list

        batch_size = validation.validate_integer(
            value=request.args.get(
                api_c.QUERY_PARAMETER_BATCH_SIZE,
                str(api_c.AUDIENCES_DEFAULT_BATCH_SIZE),
            ),
            validate_zero_or_greater=True,
        )

        batch_number = validation.validate_integer(
            request.args.get(
                api_c.QUERY_PARAMETER_BATCH_NUMBER,
                str(api_c.DEFAULT_BATCH_NUMBER),
            )
        )

        # get all audiences
        audiences = orchestration_management.get_all_audiences(
            database=database,
            filters=filter_dict,
            audience_ids=favorite_audiences,
            batch_size=batch_size,
            batch_number=batch_number,
        )

        # get total audiences count to add it to response for pagination
        # request
        audiences_count = orchestration_management.get_audiences_count(
            database=database,
            filters=filter_dict,
            audience_ids=favorite_audiences,
        )

        # query and fetch the lookalike audiences only if the batch size in the
        # request payload is greater than the audiences fetched, in which case
        # we can query the lookalike_audiences collection as well and append it
        # to the list of audiences to be returned in response
        fetch_lookalike_audiences = batch_size == 0 or (
            batch_size > 0 and len(audiences) < batch_size
        )

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

        audience_delivery_query_time = time.time()
        audience_deliveries_dict = eam.get_all_engagement_audience_deliveries(
            database, audience_ids=list(x.get(db_c.ID) for x in audiences)
        )

        logger.info(
            "Generated the audience deliveries in %.4f seconds.",
            time.time() - audience_delivery_query_time,
        )

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
            if audience.get(api_c.TAGS):
                audience[api_c.TAGS][api_c.INDUSTRY].sort()

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

            # convert contact preference in audience filters back to be
            # compatible for Unified UI
            convert_filters_for_contact_preference(
                filters={
                    api_c.AUDIENCE_FILTERS: audience.get(
                        api_c.AUDIENCE_FILTERS, None
                    )
                }
            )

        lookalikes_count = 0

        # fetch lookalike audiences if lookalikeable is set to false as
        # lookalike audiences can not be lookalikeable
        if not lookalikeable:
            # get all lookalikes and append to the audience list
            query_filter = {"$and": [{db_c.DELETED: False}]}

            if request.args.get(api_c.WORKED_BY) and validation.validate_bool(
                request.args.get(api_c.WORKED_BY)
            ):
                query_filter["$and"].extend(
                    [
                        {
                            "$or": [
                                {db_c.CREATED_BY: user[api_c.USER_NAME]},
                                {db_c.UPDATED_BY: user[api_c.USER_NAME]},
                            ]
                        }
                    ]
                )

            attribute_list = request.args.getlist(api_c.ATTRIBUTE)
            if attribute_list:
                if api_c.AUDIENCE_FILTER_CONTACT_PREFERENCE in attribute_list:
                    query_filter["$and"].extend(
                        [
                            {
                                "$or": [
                                    {
                                        db_c.LOOKALIKE_ATTRIBUTE_FILTER_FIELD: {
                                            "$regex": re.compile(
                                                rf"^{attribute}$(?i)"
                                            )
                                        }
                                    }
                                    for attribute in api_c.AUDIENCE_FILTER_CONTACT_PREFERENCES_CDM
                                ]
                            }
                        ]
                    )
                    # remove the contact_preference filter from the
                    # attribute_list
                    attribute_list.remove(
                        api_c.AUDIENCE_FILTER_CONTACT_PREFERENCE
                    )

                if attribute_list:
                    query_filter["$and"].extend(
                        [
                            {
                                "$and": [
                                    {
                                        db_c.LOOKALIKE_ATTRIBUTE_FILTER_FIELD: {
                                            "$regex": re.compile(
                                                rf"^{attribute}$(?i)"
                                            )
                                        }
                                    }
                                    for attribute in attribute_list
                                ]
                            }
                        ]
                    )

            if industry_tag_list:
                query_filter["$and"].extend(
                    [
                        {
                            "$or": [
                                {
                                    db_c.INDUSTRY_TAG_FIELD: {
                                        "$regex": re.compile(
                                            rf"^{industry_tag}$(?i)"
                                        )
                                    }
                                }
                                for industry_tag in industry_tag_list
                            ]
                        }
                    ]
                )

            if request.args.get(api_c.FAVORITES) and validation.validate_bool(
                request.args.get(api_c.FAVORITES)
            ):
                query_filter[db_c.ID] = {"$in": favorite_lookalike_audiences}

            lookalikes = cm.get_documents(
                database,
                db_c.LOOKALIKE_AUDIENCE_COLLECTION,
                query_filter,
                {db_c.DELETED: 0},
            )

            # get total lookalike audiences count to add it to response for
            # pagination request
            lookalikes_count = (
                0
                if lookalikes is None
                else lookalikes.get(api_c.TOTAL_RECORDS, 0)
            )

            # query for lookalike audiences only if required number of regular
            # audiences are not fetched based on the batch offset values passed
            # in the request
            if fetch_lookalike_audiences:
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

                for lookalike in lookalikes:
                    lookalike = {
                        **lookalike,
                        api_c.LOOKALIKEABLE: False,
                        api_c.IS_LOOKALIKE: True,
                        db_c.STATUS: lookalike.get(
                            db_c.STATUS, db_c.AUDIENCE_STATUS_ERROR
                        ),
                        db_c.AUDIENCE_LAST_DELIVERED: lookalike[
                            db_c.CREATE_TIME
                        ],
                        db_c.DESTINATIONS: (
                            [facebook_destination]
                            if facebook_destination
                            else []
                        ),
                        api_c.FAVORITE: bool(
                            lookalike[db_c.ID] in favorite_lookalike_audiences
                        ),
                    }
                    if db_c.LOOKALIKE_SOURCE_AUD_FILTERS in lookalike:
                        # convert contact preference in lookalike audience
                        # filters back to be compatible for Unified UI
                        convert_filters_for_contact_preference(
                            filters={
                                api_c.AUDIENCE_FILTERS: lookalike.get(
                                    db_c.LOOKALIKE_SOURCE_AUD_FILTERS, None
                                )
                            }
                        )

                        # rename the key
                        lookalike[db_c.AUDIENCE_FILTERS] = lookalike.pop(
                            db_c.LOOKALIKE_SOURCE_AUD_FILTERS
                        )

                    # add the built lookalike dict to the list of audiences to
                    # be returned
                    audiences.append(lookalike)

        elif lookalikeable:
            # if lookalikeable is set to true, filter out the audiences that
            # are not lookalikeable.
            audiences = [
                x
                for x in audiences
                if x[api_c.LOOKALIKEABLE] == api_c.STATUS_ACTIVE
            ]

        audiences_batch = {
            api_c.TOTAL_RECORDS: audiences_count + lookalikes_count,
            api_c.AUDIENCES: audiences,
        }

        return HuxResponse.OK(
            data=audiences_batch, data_schema=AudiencesBatchGetSchema()
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
    def get(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Retrieves an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Audience, HTTP status code.
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
                return HuxResponse.NOT_FOUND(api_c.AUDIENCE_NOT_FOUND)

            lookalike[api_c.IS_LOOKALIKE] = True
            # set source audience attribute filters for the lookalike
            lookalike[db_c.AUDIENCE_FILTERS] = lookalike[
                db_c.LOOKALIKE_SOURCE_AUD_FILTERS
            ]
            lookalike[db_c.SIZE] = lookalike[db_c.LOOKALIKE_SOURCE_AUD_SIZE]
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

        # add insights
        audience[api_c.AUDIENCE_INSIGHTS] = Caching.check_and_return_cache(
            {
                api_c.ENDPOINT: f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.OVERVIEW}",
                **{
                    api_c.AUDIENCE_FILTERS: audience.get(
                        api_c.AUDIENCE_FILTERS, None
                    )
                },
            },
            get_customers_overview,
            {
                api_c.AUTHENTICATION_TOKEN: token_response[0],
                api_c.AUDIENCE_FILTERS: {
                    api_c.AUDIENCE_FILTERS: audience.get(
                        api_c.AUDIENCE_FILTERS, None
                    )
                },
            },
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
                destination = destination_management.get_delivery_platform(
                    database, lookalike_audience.get(db_c.DELIVERY_PLATFORM_ID)
                )
                if not destination:
                    logger.warning(
                        "Destination %s could not be found.",
                        destination.get(api_c.ID),
                    )
                lookalike_audience[
                    db_c.DELIVERY_PLATFORM_TYPE
                ] = destination.get(db_c.DELIVERY_PLATFORM_TYPE)
                lookalike_audience[
                    api_c.DELIVERY_PLATFORM_NAME
                ] = destination.get(db_c.NAME)
                lookalike_audience[
                    api_c.DELIVERY_PLATFORM_LINK
                ] = destination.get(db_c.LINK)

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
            ).get(
                audience_id,
                {db_c.DELIVERIES: [], api_c.AUDIENCE_LAST_DELIVERED: None},
            )

            audience_deliveries = [audience_deliveries] + standalone_deliveries
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
                    user, api_c.AUDIENCES, str(audience_id)
                )
                or is_component_favorite(
                    user, api_c.LOOKALIKE, str(audience_id)
                ),
            }
        )

        # convert contact preference in audience filters back to be compatible
        # for Unified UI
        convert_filters_for_contact_preference(
            filters={
                api_c.AUDIENCE_FILTERS: audience.get(
                    api_c.AUDIENCE_FILTERS, None
                )
            }
        )

        return HuxResponse.OK(
            data=audience, data_schema=AudienceGetSchema(unknown=INCLUDE)
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
    def get(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Retrieves audience insights for an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user (dict): user object.

        Returns:
            Tuple[Response, int]: AudienceInsights, HTTP status code.
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
            return HuxResponse.NOT_FOUND(api_c.AUDIENCE_NOT_FOUND)

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

        return HuxResponse.OK(
            data=audience_insights,
            data_schema=AudienceInsightsGetSchema(unknown=INCLUDE),
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
                api_c.TAGS: {api_c.INDUSTRY: api_c.ALL_INDUSTRY_TYPES},
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
    def post(self, user: dict) -> Tuple[Response, int]:
        """Creates a new audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Created audience, HTTP status code.
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
                    return HuxResponse.NOT_FOUND(api_c.DESTINATION_NOT_FOUND)

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
                    return HuxResponse.NOT_FOUND(
                        f"Engagement with ID {engagement_id} "
                        f"does not exist."
                    )
                engagement_ids.append(engagement_id)
        audience_filters = convert_unique_city_filter(
            {api_c.AUDIENCE_FILTERS: body.get(api_c.AUDIENCE_FILTERS)}
        )

        # Fetch events from CDM. Check cache first.
        event_types = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.EVENTS}",
            get_customer_event_types,
            {"token": token_response[0]},
        )

        convert_filters_for_events(audience_filters, event_types)
        # convert contact preference in audience filters to be compatible for
        # CDM
        convert_filters_for_contact_preference(
            filters=audience_filters, convert_for_cdm=True
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
            audience_source={
                db_c.AUDIENCE_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_CDP
            },
            destination_ids=body.get(api_c.DESTINATIONS),
            user_name=user[api_c.USER_NAME],
            size=customers.get(api_c.TOTAL_CUSTOMERS, 0),
            audience_tags=body.get(api_c.TAGS, None),
        )

        # convert contact preference in audience filters back to be compatible
        # for Unified UI
        convert_filters_for_contact_preference(
            filters={
                api_c.AUDIENCE_FILTERS: audience_doc.get(
                    api_c.AUDIENCE_FILTERS, None
                )
            }
        )

        # add notification
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f'New audience named "{audience_doc[db_c.NAME]}" '
                f"added by {user[api_c.USER_NAME]}."
            ),
            db_c.NOTIFICATION_CATEGORY_AUDIENCES,
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
                db_c.NOTIFICATION_CATEGORY_ENGAGEMENTS,
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
                        database,
                        engagement[db_c.ID],
                        *pair,
                        username=user[api_c.USER_NAME],
                    )
                    batch_destination.register()
                    batch_destination.submit()

        return HuxResponse.CREATED(
            data=audience_doc, data_schema=AudienceGetSchema()
        )


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
                api_c.TAGS: {api_c.INDUSTRY: api_c.ALL_INDUSTRY_TYPES},
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
    def put(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Updates an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Audience doc, HTTP status code.
        """

        # load into the schema object
        body = AudiencePutSchema().load(request.get_json(), partial=True)
        database = get_db_client()

        if not orchestration_management.get_audience(
            database, ObjectId(audience_id)
        ):
            return HuxResponse.NOT_FOUND(api_c.AUDIENCE_NOT_FOUND)

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
                    return HuxResponse.NOT_FOUND(api_c.DESTINATION_NOT_FOUND)

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
            audience_tags=body.get(api_c.TAGS, None),
            user_name=user[api_c.USER_NAME],
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            f'Audience "{audience_doc[db_c.NAME]}" updated by {user[api_c.USER_NAME]}.',
            db_c.NOTIFICATION_CATEGORY_AUDIENCES,
            user[api_c.USER_NAME],
        )

        # check if any engagements to add, otherwise return.
        if not body.get(api_c.ENGAGEMENT_IDS):
            return HuxResponse.OK(
                data=audience_doc, data_schema=AudienceGetSchema()
            )

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

        return HuxResponse.OK(
            data=audience_doc, data_schema=AudienceGetSchema()
        )


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
    def get(self, user: dict) -> Tuple[Response, int]:
        """Retrieves all audience rules.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[Response, int]: dict of audience rules, HTTP status code.
        """

        token_response = get_token_from_request(request)

        rules_constants = {
            "text_operators": {
                "contains": "Contains",
                "not_contains": "Does not contain",
                "equals": "Equals",
                "not_equals": "Does not equal",
                "within_the_last": "Within the last",
                "not_within_the_last": "Not within the last",
                "between": "Between",
                "value": "Value",
                "decile_percentage": "Decile percentage",
            },
            "allowed_timedelta_types": [
                {api_c.KEY: api_c.AUDIENCE_RULES_DAYS, api_c.NAME: "Days"},
                {api_c.KEY: api_c.AUDIENCE_RULES_WEEKS, api_c.NAME: "Weeks"},
                {api_c.KEY: api_c.AUDIENCE_RULES_MONTHS, api_c.NAME: "Months"},
                {api_c.KEY: api_c.AUDIENCE_RULES_YEARS, api_c.NAME: "Years"},
            ],
        }

        # Fetch events from CDM. Check cache first.
        event_types = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.EVENTS}",
            get_customer_event_types,
            {"token": token_response[0]},
        )

        event_types_rules = {api_c.NAME: api_c.EVENTS.capitalize()}
        for event_type in event_types:
            event_types_rules[event_type[api_c.TYPE]] = {
                api_c.NAME: event_type[api_c.LABEL],
                api_c.TYPE: api_c.TEXT,
            }

        # Fetch countries from CDM. Check cache first.
        countries = Caching.check_and_return_cache(
            f"{api_c.CUSTOMERS_ENDPOINT}.{api_c.COUNTRIES}",
            get_customer_count_by_country,
            {"token": token_response[0]},
        )
        # filter countries list based on the response

        country_list = []
        for country in countries:
            country_list.append(
                {country[api_c.COUNTRY]: country[api_c.COUNTRY]}
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
                        "icon": "unsubscribe",
                    },
                    "ltv_predicted": {
                        "name": "Predicted lifetime value",
                        "type": "range",
                        "icon": "ltv",
                    },
                    "propensity_to_purchase": {
                        "name": "Propensity to purchase",
                        "type": "range",
                        "icon": "purchase",
                    },
                },
                "general": {
                    "age": {
                        "name": "Age",
                        "type": "range",
                    },
                    "contact_preference": {
                        "name": "Contact preference",
                        "type": "list",
                        "options": [{"email": "Email"}, {"text": "Text"}],
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
                    # TODO Remove after LP CDM Integration
                    "location": {
                        "name": "Location",
                        "country": {
                            "name": "Country",
                            "type": "list",
                            "options": country_list,
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
                    "mailing_address": {
                        "name": "Mailing address",
                        "mailing_country": {
                            "name": "Country",
                            "type": "list",
                            "options": country_list,
                        },
                        "mailing_state": {
                            "name": "State",
                            "type": "list",
                            "options": [
                                {key: value}
                                for key, value in api_c.STATE_NAMES.items()
                            ],
                        },
                        "mailing_city": {
                            "name": "City",
                            "type": "list",
                            "options": [],
                        },
                        "mailing_zip_code": {
                            "name": "Zip",
                            "type": "list",
                            "options": [],
                        },
                    },
                    "shipping_address": {
                        "name": "Shipping address",
                        "shipping_country": {
                            "name": "Country",
                            "type": "list",
                            "options": country_list,
                        },
                        "shipping_state": {
                            "name": "State",
                            "type": "list",
                            "options": [
                                {key: value}
                                for key, value in api_c.STATE_NAMES.items()
                            ],
                        },
                        "shipping_city": {
                            "name": "City",
                            "type": "list",
                            "options": [],
                        },
                        "shipping_zip_code": {
                            "name": "Zip",
                            "type": "list",
                            "options": [],
                        },
                    },
                    "events": event_types_rules,
                },
            }
        }

        rules_constants.update(rules_from_cdm)

        return HuxResponse.response(HTTPStatus.OK, data=rules_constants)


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
                api_c.DESTINATION_ID: [
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
    def post(self, user: dict) -> Tuple[Response, int]:
        """Create lookalike audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[Response, int]: lookalike audience configuration,
                HTTP status code.

        Raises:
            FailedDestinationDependencyError: Destination Dependency
                error.
        """

        body = LookalikeAudiencePostSchema().load(
            request.get_json(), partial=True
        )
        source_audience_id = body[api_c.AUDIENCE_ID]
        engagement_ids = body.get(api_c.ENGAGEMENT_IDS, [])

        database = get_db_client()
        source_audience = orchestration_management.get_audience(
            database, ObjectId(source_audience_id)
        )

        if not source_audience:
            logger.error("Audience %s not found.", body[api_c.AUDIENCE_ID])
            return HuxResponse.NOT_FOUND(api_c.AUDIENCE_NOT_FOUND)

        # TODO: Update destination handling when more lookalikable
        #  destinations are available and param accepted from request
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

        recent_jobs_filter = {
            db_c.DELIVERY_PLATFORM_ID: destination[db_c.ID],
            db_c.AUDIENCE_ID: ObjectId(source_audience_id),
            db_c.STATUS: {
                "$in": [
                    db_c.STATUS_SUCCEEDED,
                    db_c.AUDIENCE_STATUS_DELIVERED,
                ]
            },
        }

        if engagement_ids:
            recent_jobs_filter.update(
                {
                    db_c.ENGAGEMENT_ID: {
                        "$in": [ObjectId(x) for x in engagement_ids]
                    },
                }
            )

        most_recent_job = destination_management.get_all_delivery_jobs(
            database,
            recent_jobs_filter,
            limit=1,
        )

        # cursor returns a list, lets take the first one if data exist.
        most_recent_job = most_recent_job[0] if most_recent_job else None
        if most_recent_job is None:
            logger.error("%s.", api_c.SUCCESSFUL_DELIVERY_JOB_NOT_FOUND)
            return HuxResponse.NOT_FOUND(
                api_c.SUCCESSFUL_DELIVERY_JOB_NOT_FOUND
            )

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
            return HuxResponse.NOT_FOUND(
                f"Failed to create a lookalike audience, "
                f"{body[api_c.NAME]}: the selected audience "
                f"to create a lookalike from is inactive or unusable."
            )

        for engagement_id in engagement_ids:
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
            db_c.NOTIFICATION_CATEGORY_AUDIENCES,
            user[api_c.USER_NAME],
        )
        return HuxResponse.ACCEPTED(
            data=lookalike_audience, data_schema=LookalikeAudienceGetSchema()
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
                api_c.TAGS: {api_c.INDUSTRY: api_c.ALL_INDUSTRY_TYPES},
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
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
    def put(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Edits lookalike audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): ID of the audience to be deleted.
            user (dict): user object.

        Returns:
            Tuple[Response, int]: lookalike audience configuration,
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
            database=database,
            audience_id=ObjectId(audience_id),
            name=body.get(api_c.NAME, None),
            user_name=user[api_c.USER_NAME],
            audience_tags=body.get(api_c.TAGS, None),
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f'Lookalike audience "{update_doc[db_c.NAME]}" '
                f"edited by {user[api_c.USER_NAME]}."
            ),
            db_c.NOTIFICATION_CATEGORY_AUDIENCES,
            user[api_c.USER_NAME],
        )

        return HuxResponse.OK(
            data=update_doc, data_schema=LookalikeAudienceGetSchema()
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
    def delete(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Deletes an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): ID of the audience to be deleted.
            user (dict): user object.

        Returns:
            Tuple[Response, int]: response dict, HTTP status code.
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
            # remove the audience from all users favorites
            delete_favorite_from_all_users(
                database,
                component_name=db_c.AUDIENCES,
                component_id=ObjectId(audience_id),
            )
            deleted_audience = orchestration_management.delete_audience(
                database, ObjectId(audience_id)
            )

            if deleted_audience:
                return HuxResponse.NO_CONTENT()
            logger.info(
                "Failed to delete audience %s by user %s.",
                audience_id,
                user[api_c.USER_NAME],
            )
            return HuxResponse.INTERNAL_SERVER_ERROR(api_c.OPERATION_FAILED)

        # attempt to delete the audience from lookalike_audiences collection
        # if audience not found in audiences collection
        audience = cm.get_document(
            database,
            db_c.LOOKALIKE_AUDIENCE_COLLECTION,
            {db_c.ID: ObjectId(audience_id)},
        )

        if not audience:
            # remove the lookalike audience from all users favorites
            delete_favorite_from_all_users(
                get_db_client(),
                component_name=db_c.LOOKALIKE,
                component_id=ObjectId(audience_id),
            )
            return HuxResponse.NO_CONTENT()

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
            return HuxResponse.INTERNAL_SERVER_ERROR(api_c.OPERATION_FAILED)

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
            return HuxResponse.INTERNAL_SERVER_ERROR(api_c.OPERATION_FAILED)

        logger.info(
            "Successfully deleted audience %s by user %s.",
            audience_id,
            user[api_c.USER_NAME],
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            f'Audience "{audience[db_c.NAME]}" successfully deleted by {user[api_c.USER_NAME]}.',
            db_c.NOTIFICATION_CATEGORY_AUDIENCES,
            user[api_c.USER_NAME],
        )

        return HuxResponse.NO_CONTENT()


@add_view_to_blueprint(
    orchestration_bp,
    f"{api_c.AUDIENCE_ENDPOINT}/upload",
    "AudienceS3UploadPostView",
)
class AudienceS3UploadPostView(SwaggerView):
    """Audience S3 Upload Post view class."""

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
    def post(self, user: dict) -> Tuple[Response, int]:
        """Creates a new audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Created audience, HTTP status code.
        """

        body = AudiencePostSchema().load(request.get_json(), partial=True)

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
                    return HuxResponse.NOT_FOUND(api_c.DESTINATION_NOT_FOUND)

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
                    return HuxResponse.NOT_FOUND(
                        f"Engagement with ID {engagement_id} "
                        f"does not exist."
                    )
                engagement_ids.append(engagement_id)

        audience_file = request.files["filename"]

        if not CloudClient().upload_file(
            file_name=str(audience_file),
            bucket=get_config().S3_DATASET_BUCKET,
            object_name=audience_file,
            user_name=user[api_c.USER_NAME],
            file_type=api_c.AUDIENCE_UPLOAD,
        ):
            logger.error(
                "Could not load file into S3.",
            )
            return HuxResponse.BAD_REQUEST("File can not be uploaded.")

        source = {
            db_c.AUDIENCE_SOURCE_TYPE: db_c.DATA_SOURCE_PLATFORM_AMAZONS3,
            db_c.AUDIENCE_SOURCE_BUCKET: get_config().S3_DATASET_BUCKET,
            db_c.AUDIENCE_SOURCE_KEY: audience_file,
        }
        # create the audience
        audience_doc = orchestration_management.create_audience(
            database=database,
            name=body[api_c.AUDIENCE_NAME],
            audience_filters=[],
            audience_source=source,
            destination_ids=body.get(api_c.DESTINATIONS),
            user_name=user[api_c.USER_NAME],
        )

        # add notification
        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f'New audience named "{audience_doc[db_c.NAME]}" '
                f"added by {user[api_c.USER_NAME]}."
            ),
            db_c.NOTIFICATION_CATEGORY_AUDIENCES,
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
                db_c.NOTIFICATION_CATEGORY_ENGAGEMENTS,
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
                        database,
                        engagement[db_c.ID],
                        *pair,
                        username=user[api_c.USER_NAME],
                    )
                    batch_destination.register()
                    batch_destination.submit()

        return HuxResponse.CREATED(
            data=audience_doc, data_schema=AudienceGetSchema()
        )
