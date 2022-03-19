# pylint: disable=no-self-use
"""Schemas for the Engagements API"""
from datetime import datetime
from bson import ObjectId
from flask_marshmallow import Schema
from marshmallow import fields, validate, pre_load, post_dump
from marshmallow.fields import Nested, List, Int

from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import (
    must_not_be_blank,
    validate_object_id,
    get_next_schedule,
)
from huxunify.api.schema.custom_schemas import DateTimeWithZ
from huxunify.api.schema.destinations import DeliveryScheduleSchema


class DeliverySchedule(Schema):
    """Delivery Schedule schema"""

    start_date = DateTimeWithZ(allow_none=True)
    end_date = DateTimeWithZ(allow_none=True)
    schedule = fields.Nested(DeliveryScheduleSchema)
    schedule_cron = fields.String(example="")


class EngagementPostSchema(Schema):
    """Engagement post schema class"""

    name = fields.String(required=True, validate=must_not_be_blank)
    description = fields.String()
    delivery_schedule = fields.Nested(DeliverySchedule)
    audiences = fields.List(
        fields.Dict(),
        attribute=api_c.AUDIENCES,
        example=[
            {
                api_c.ID: "60ae035b6c5bf45da27f17d6",
                api_c.DESTINATIONS: [
                    {
                        api_c.ID: "60ae035b6c5bf45da27f17e5",
                        "data_extension_id": "data_extension_id",
                    },
                    {
                        api_c.ID: "60ae035b6c5bf45da27f17e6",
                    },
                ],
            }
        ],
    )

    @pre_load
    # pylint: disable=unused-argument
    def pre_process_details(self, data, **kwargs):
        """Process the schema before loading.

        Args:
            data (dict): The Engagement data source object
            **kwargs (dict): Field-specific keyword arguments.
        Returns:
            Response: Returns a Engagement data source object

        """
        # handle null delivery schedule
        delivery_schedule = data.get(api_c.DELIVERY_SCHEDULE)
        if not delivery_schedule:
            data.pop(api_c.DELIVERY_SCHEDULE, None)

        for audience in data[api_c.AUDIENCES]:
            audience[api_c.ID] = ObjectId(audience[api_c.ID])
            for destination in audience[api_c.DESTINATIONS]:
                destination[api_c.ID] = ObjectId(destination[api_c.ID])
        return data


class EngagementPutSchema(Schema):
    """Engagement put schema class"""

    name = fields.String(required=False)
    description = fields.String(required=False, allow_none=True)
    audiences = fields.List(
        fields.Dict(),
        attribute=api_c.AUDIENCES,
        example=[
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
        required=False,
    )
    delivery_schedule = fields.Nested(DeliverySchedule, required=False)
    status = fields.String(
        attribute=api_c.STATUS,
        required=False,
        validate=validate.OneOf(
            choices=[
                api_c.STATUS_ACTIVE,
                api_c.STATUS_INACTIVE,
                api_c.STATUS_DELIVERING,
                api_c.STATUS_ERROR,
            ]
        ),
    )

    @pre_load
    # pylint: disable=unused-argument
    def pre_process_details(self, data: dict, **kwargs):
        """Process the schema before loading.

        Args:
            data (dict): The Engagement data source object
            **kwargs (dict): Field-specific keyword arguments.
        Returns:
            Response: Returns a Engagement data source object

        """
        # handle null delivery schedule
        delivery_schedule = data.get(api_c.DELIVERY_SCHEDULE)
        if not delivery_schedule:
            data.pop(api_c.DELIVERY_SCHEDULE, None)

        if not data.get(api_c.AUDIENCES):
            data.pop(api_c.AUDIENCES, None)
        else:
            for audience in data[api_c.AUDIENCES]:
                audience[api_c.ID] = ObjectId(audience[api_c.ID])
                for destination in audience[api_c.DESTINATIONS]:
                    destination[api_c.ID] = ObjectId(destination[api_c.ID])

                    # check if there is a delivery job id to convert.
                    if db_c.DELIVERY_JOB_ID in destination:
                        destination[db_c.DELIVERY_JOB_ID] = ObjectId(
                            destination[db_c.DELIVERY_JOB_ID]
                        )
        return data


class AudienceEngagementSchema(Schema):
    """Schema for adding/deleting audience to engagement"""

    audiences = fields.List(
        fields.Dict(),
        example=[
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
    )

    @pre_load
    # pylint: disable=unused-argument
    def pre_process_details(self, data, **kwargs):
        """Process the schema before loading.

        Args:
            data (dict): The Engagement data source object
            **kwargs (dict): Field-specific keyword arguments.
        Returns:
            Response: Returns a Engagement data source object

        """
        for audience in data[api_c.AUDIENCES]:
            audience[api_c.ID] = ObjectId(audience[api_c.ID])
            for destination in audience[api_c.DESTINATIONS]:
                destination[api_c.ID] = ObjectId(destination[api_c.ID])
        return data


class AudienceEngagementDeleteSchema(Schema):
    """Schema for adding/deleting audience to engagement"""

    audience_ids = fields.List(
        fields.String,
        example=[
            "60ae035b6c5bf45da27f17e5",
            "60ae035b6c5bf45da27f17e6",
        ],
    )


class DestinationEngagedAudienceSchema(Schema):
    """Schema for adding destination to engagement audience"""

    id = fields.String(
        example="60ae035b6c5bf45da27f17e5",
        required=True,
    )
    delivery_platform_config = fields.Dict(
        example={db_c.DATA_EXTENSION_NAME: "SFMC Date Extension"},
        required=False,
        default=None,
    )


class DisplayAdsSummary(Schema):
    """Schema for Display Ads Summary"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    spend = fields.Float()
    reach = fields.Integer()
    impressions = fields.Integer()
    conversions = fields.Integer()
    clicks = fields.Integer()
    frequency = fields.Float()
    cost_per_thousand_impressions = fields.Float()
    click_through_rate = fields.Float()
    cost_per_action = fields.Float()
    cost_per_click = fields.Float()
    engagement_rate = fields.Float()


class DispAdIndividualCampaignSummary(DisplayAdsSummary):
    """Schema for Individual Campaign Summary"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    name = fields.String()
    id = fields.String()
    is_mapped = fields.Boolean(default=False)


class DispAdIndividualDestinationSummary(DisplayAdsSummary):
    """Schema for Individual Campaign Summary"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    name = fields.String()
    id = fields.String()
    is_mapped = fields.Boolean(default=False)
    delivery_platform_type = fields.String()
    campaigns = fields.List(fields.Nested(DispAdIndividualCampaignSummary))


class DispAdIndividualAudienceSummary(DisplayAdsSummary):
    """Schema for Individual Audience Summary"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    name = fields.String()
    id = fields.String()
    destinations = fields.List(fields.Nested(DispAdIndividualDestinationSummary))


class AudiencePerformanceDisplayAdsSchema(Schema):
    """Schema for Performance Metrics of Display Ads"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    summary = fields.Nested(DisplayAdsSummary)
    audience_performance = fields.List(fields.Nested(DispAdIndividualAudienceSummary))


class EmailSummary(Schema):
    """Schema for Summary Performance Metrics of Email"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    sent = fields.Integer()
    hard_bounces = fields.Integer()
    hard_bounces_rate = fields.Float()
    delivered = fields.Integer()
    delivered_rate = fields.Float()
    open = fields.Integer()
    open_rate = fields.Float()
    clicks = fields.Integer()
    conversions = fields.Integer()
    click_through_rate = fields.Float()
    click_to_open_rate = fields.Float()
    unique_clicks = fields.Integer()
    unique_opens = fields.Integer()
    unsubscribe = fields.Integer()
    unsubscribe_rate = fields.Float()


class EmailIndividualDestinationSummary(EmailSummary):
    """Schema for Individual Campaign Summary of Email"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    name = fields.String()
    id = fields.String()
    is_mapped = fields.Boolean(default=False)
    delivery_platform_type = fields.String()


class EmailIndividualAudienceSummary(EmailSummary):
    """Schema for Individual Audience Summary of Email"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    name = fields.String()
    id = fields.String()
    destinations = fields.List(fields.Nested(EmailIndividualDestinationSummary))


class AudiencePerformanceEmailSchema(Schema):
    """Schema for Performance Metrics of Email"""

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    summary = fields.Nested(EmailSummary)
    audience_performance = fields.List(fields.Nested(EmailIndividualAudienceSummary))


class FacebookCampaignSchema(Schema):
    """Schema for Campaigns"""

    class Meta:
        """Set Order for the Campaign Response"""

        ordered = True

    id = fields.String(
        example="5f5f7262997acad4bac4373b",
        validate=validate_object_id,
    )
    ad_set_id = fields.String(
        example="5f5f7262997acad4bac4373b",
        validate=validate_object_id,
    )
    name = fields.String()
    ad_set_name = fields.String()


class CampaignSchema(Schema):
    """Schema for Campaigns"""

    class Meta:
        """Set Order for the Campaign Response"""

        ordered = True

    id = fields.String(
        example="5f5f7262997acad4bac4373b",
        validate=validate_object_id,
    )
    name = fields.String()
    ad_set_name = fields.String()
    ad_set_id = fields.String()
    delivery_job_id = fields.String(
        example="5f5f7262997acad4bac4373b",
        validate=validate_object_id,
    )
    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME, allow_none=True)


class CampaignPutSchema(Schema):
    """Schema for Campaigns PUT."""

    class Meta:
        """Set Order for the Campaigns Response"""

        ordered = True

    campaigns = fields.List(
        fields.Dict,
        example=[
            {
                api_c.NAME: "Test Campaign",
                api_c.ID: "campaign_id",
                api_c.AD_SET_ID: "ad_set_id",
                api_c.AD_SET_NAME: "Test Adset",
                api_c.DELIVERY_JOB_ID: "delivery_job_id",
            }
        ],
    )


class DeliveryJobSchema(Schema):
    """Schema for Campaigns"""

    class Meta:
        """Set Order for the Campaign Response"""

        ordered = True

    _id = fields.String(
        data_key=api_c.ID,
        example="5f5f7262997acad4bac4373b",
        validate=validate_object_id,
    )
    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME, allow_none=True)


class CampaignMappingSchema(Schema):
    """Schema for Campaigns"""

    class Meta:
        """Set Order for the Campaign Response"""

        ordered = True

    campaigns = fields.List(fields.Nested(FacebookCampaignSchema))
    delivery_jobs = fields.List(fields.Nested(DeliveryJobSchema))


class EngagementDataExtensionSchema(Schema):
    """Engagement Audience Destination Data Extension Schema"""

    data_extension_name = fields.String()


class LatestDeliverySchema(Schema):
    """Engagement Audience Destination Delivery Schema"""

    id = fields.String()
    status = fields.String()
    update_time = DateTimeWithZ()
    size = fields.Int(default=0)
    match_rate = fields.Float(default=0, example=0.21)
    next_delivery = DateTimeWithZ()
    delivery_schedule = fields.String()


class EngagementAudienceDestinationSchema(Schema):
    """Engagement Audience Destination Schema"""

    name = fields.String()
    id = fields.String()
    delivery_job_id = fields.String()
    delivery_platform_config = fields.Nested(EngagementDataExtensionSchema)
    delivery_platform_type = fields.String()
    delivery_schedule = fields.Dict()
    latest_delivery = fields.Nested(LatestDeliverySchema)
    data_added = DateTimeWithZ(allow_none=True)


class EngagementAudienceSchema(Schema):
    """Engagement Audience Schema"""

    name = fields.String()
    id = fields.String()
    status = fields.String()
    is_lookalike = fields.Boolean(default=False)
    size = fields.Integer(default=0)
    filters = fields.List(
        fields.Dict(),
        attribute=api_c.AUDIENCE_FILTERS,
        example=[
            {
                api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                api_c.AUDIENCE_SECTION_FILTERS: [
                    {
                        api_c.AUDIENCE_FILTER_FIELD: "gender",
                        api_c.AUDIENCE_FILTER_TYPE: "equals",
                        api_c.AUDIENCE_FILTER_VALUE: "female",
                    }
                ],
            }
        ],
    )
    destinations = fields.Nested(EngagementAudienceDestinationSchema, many=True)
    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME)
    created_by = fields.String(attribute=db_c.CREATED_BY)
    update_time = DateTimeWithZ(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = fields.String(attribute=db_c.UPDATED_BY, allow_none=True)


class EngagementDestinationAudienceSchema(Schema):
    """Engagement Destination Audience Schema"""

    id = fields.String(
        required=True,
        validate=validate_object_id,
    )
    name = fields.String()
    is_lookalike = fields.Boolean(default=False)
    size = fields.Integer(default=0)
    latest_delivery = fields.Nested(LatestDeliverySchema)


class EngagementDestinationSchema(Schema):
    """Engagement Destination Schema"""

    id = fields.String(
        required=True,
        validate=validate_object_id,
    )
    name = fields.String()
    destination_audiences = fields.List(
        fields.Nested(EngagementDestinationAudienceSchema)
    )
    type = fields.String()
    link = fields.String(default=None)


class EngagementDestinationCategorySchema(Schema):
    """Engagement Destination Category Schema"""

    category = fields.String()
    destinations = fields.List(fields.Nested(EngagementDestinationSchema))


class EngagementGetSchema(Schema):
    """Engagement get schema class"""

    _id = fields.String(
        data_key=api_c.ID,
        example="5f5f7262997acad4bac4373b",
        required=True,
        validate=validate_object_id,
    )
    name = fields.String(attribute=api_c.NAME, required=True)
    description = fields.String(attribute=api_c.DESCRIPTION)

    audiences = fields.Nested(
        EngagementAudienceSchema, many=True, attribute=api_c.AUDIENCES
    )

    destinations_category = fields.List(
        fields.Nested(EngagementDestinationCategorySchema),
        attribute=api_c.DESTINATION_CATEGORIES,
    )

    status = fields.String(
        attribute=api_c.STATUS,
        required=True,
        validate=validate.OneOf(
            choices=[
                api_c.STATUS_ACTIVE,
                api_c.STATUS_INACTIVE,
                api_c.STATUS_DELIVERING,
                api_c.STATUS_DRAFT,
                api_c.STATUS_ERROR,
            ]
        ),
        default=api_c.STATUS_DRAFT,
    )
    delivery_schedule = fields.Nested(
        DeliverySchedule,
        required=False,
        attribute=api_c.DELIVERY_SCHEDULE,
    )
    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME)
    created_by = fields.String(attribute=db_c.CREATED_BY)
    update_time = DateTimeWithZ(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = fields.String(attribute=db_c.UPDATED_BY, allow_none=True)
    favorite = fields.Boolean(required=False, default=False)

    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    @post_dump
    def post_serialize(self, engagement: dict, many: bool = False) -> dict:
        """process the schema before serializing.

        Args:
            engagement (dict): The engagement object
            many (bool): If there are many to process

        Returns:
            dict: Returns an engagement object

        """
        # Set delivery_schedule as null if delivery schedule is not available
        if not engagement.get(api_c.DELIVERY_SCHEDULE):
            engagement[api_c.DELIVERY_SCHEDULE] = None

        return engagement


class EngagementsBatchGetSchema(Schema):
    """Engagements batch schema to get engagements in batches."""

    total_engagements = Int(
        attribute=api_c.TOTAL_RECORDS,
        example=1,
    )
    engagements = List(Nested(EngagementGetSchema))


# pylint: disable=too-many-branches,too-many-statements
def weighted_engagement_status(engagements: list) -> list:
    """Returns a weighted engagement status by rolling up the individual
    destination status values.

    Args:
        engagements (list): input engagement list.

    Returns:
        list: list of engagement documents.

    Capturing details as to how status is calculated for Engagement,
            Audience and destinations
        Data Model :
            Engagement has [audiences]
                - Engagement has a Status field
            Each audience has [destinations]
            Each destination can have a latest_delivery object
                - Latest_delivery object has Status field

        UI needs:
            Show status for Engagement
            Show status for audience
            Show status for audience / destination

        Application Logic :
            Show status for audience/destination
                If there is at least one delivery for the destination,
                engagement.audience.destination.latest_delivery SHOULD exist
                    status = latest_delivery.status
                If not : status = NOT_DELIVERED
                status need to be one [delivering, delivered,
                not delivered, delivery paused, error]
            Show status for audience
                status needs to be one [delivering - 8, delivered - 10,
                not delivered - 9, delivery paused - 7, error - 0]
                GET all status of audience.destinations.status ->
                A list of status values use the weighted status in
                api/constants.py to pick status with least weight
            Show status for engagement
                status need to be one [active - 11, inactive - 5,
                delivering - 8, error - 0]
                GET status of each audience for this engagement -> list
                Use the weighted status in api/constants.py to pick
                status with least weight
                How do we map audience status to engagement status??
                    - If audience.status list has delivering / error,
                        status = delivering / error
                    - else current_time falls with in delivery_schedule,
                        status = active
                    - else current_time falls with in delivery_schedule,
                        status = inactive
    """

    # process each engagement and calculated the weights status value
    for engagement in engagements:

        status_ranks = []

        # process each audience
        audiences = []
        for audience in engagement[api_c.AUDIENCES]:
            if db_c.OBJECT_ID not in audience:
                # only add audience if it is valid and has an id.
                continue

            audience_status_rank = []

            # process each destination
            destinations = []
            for destination in audience[api_c.DESTINATIONS]:
                if db_c.OBJECT_ID not in destination:
                    # only add destination if it is valid and has an id.
                    continue

                if api_c.LATEST_DELIVERY not in destination:
                    continue

                # check if status is in the latest delivery.
                if api_c.STATUS not in destination[api_c.LATEST_DELIVERY]:
                    destination[api_c.LATEST_DELIVERY][
                        api_c.STATUS
                    ] = api_c.STATUS_NOT_DELIVERED
                    # if status is not set, it is considered as not-delivered
                    break

                # TODO after ORCH-285 so no status mapping needed.
                status = api_c.STATUS_MAPPING.get(
                    destination[api_c.LATEST_DELIVERY][api_c.STATUS],
                    api_c.STATUS_ERROR,
                )
                destination[api_c.LATEST_DELIVERY][api_c.STATUS] = status

                if engagement.get(db_c.ENGAGEMENT_DELIVERY_SCHEDULE):
                    destination[api_c.LATEST_DELIVERY][
                        db_c.ENGAGEMENT_DELIVERY_SCHEDULE
                    ] = (
                        engagement.get(db_c.ENGAGEMENT_DELIVERY_SCHEDULE)
                        .get(api_c.SCHEDULE)
                        .get(api_c.PERIODICIY)
                        if engagement.get(db_c.ENGAGEMENT_DELIVERY_SCHEDULE).get(
                            api_c.SCHEDULE
                        )
                        else None
                    )

                    destination[api_c.LATEST_DELIVERY][
                        api_c.NEXT_DELIVERY
                    ] = get_next_schedule(
                        engagement[db_c.ENGAGEMENT_DELIVERY_SCHEDULE].get(
                            api_c.SCHEDULE_CRON
                        ),
                        engagement[db_c.ENGAGEMENT_DELIVERY_SCHEDULE].get(
                            api_c.START_DATE
                        ),
                    )
                status_rank = {
                    api_c.STATUS: status,
                    api_c.WEIGHT: api_c.STATUS_WEIGHTS.get(status, 0),
                }
                audience_status_rank.append(status_rank)
                destinations.append(destination)

            audience[api_c.DESTINATIONS] = destinations

            # sort delivery status list of destinations by weight.
            audience_status_rank.sort(key=lambda x: x[api_c.WEIGHT])

            # take the first item in the sorted list, and grab the status
            audience[api_c.STATUS] = (
                audience_status_rank[0][api_c.STATUS]
                if audience_status_rank
                else api_c.STATUS_NOT_DELIVERED
            )

            status_rank = {
                api_c.STATUS: audience[api_c.STATUS],
                api_c.WEIGHT: api_c.STATUS_WEIGHTS.get(audience[api_c.STATUS], 0),
            }
            status_ranks.append(status_rank)
            audiences.append(audience)

        engagement[api_c.AUDIENCES] = audiences

        # Set engagement status.
        # Order in which these checks are made ensures correct engagement status.
        status = engagement.get(api_c.STATUS)
        status_values = [x[api_c.STATUS] for x in status_ranks]

        if status is not None and status == api_c.STATUS_INACTIVE:
            engagement[api_c.STATUS] = api_c.STATUS_INACTIVE
        elif api_c.STATUS_DELIVERING in status_values:
            engagement[api_c.STATUS] = api_c.STATUS_DELIVERING
        elif engagement.get(db_c.ENGAGEMENT_DELIVERY_SCHEDULE):
            if (
                engagement[db_c.ENGAGEMENT_DELIVERY_SCHEDULE].get(api_c.START_DATE)
                and engagement[db_c.ENGAGEMENT_DELIVERY_SCHEDULE].get(api_c.END_DATE)
                and engagement[db_c.ENGAGEMENT_DELIVERY_SCHEDULE][api_c.START_DATE]
                <= datetime.now()
                <= engagement[db_c.ENGAGEMENT_DELIVERY_SCHEDULE][api_c.END_DATE]
            ):
                engagement[api_c.STATUS] = api_c.STATUS_ACTIVE
            else:
                engagement[api_c.STATUS] = api_c.STATUS_INACTIVE
        elif api_c.STATUS_NOT_DELIVERED in status_values:
            engagement[api_c.STATUS] = api_c.STATUS_INACTIVE
        elif all(
            status_value == api_c.STATUS_DELIVERED for status_value in status_values
        ):
            engagement[api_c.STATUS] = api_c.STATUS_ACTIVE
        else:
            engagement[api_c.STATUS] = api_c.STATUS_ERROR

    return engagements


def weight_delivery_status(audience: list) -> str:
    """Returns a weighted delivery status by rolling up the individual
    delivery status values.

    Args:
        audience (list): input engagement delivery list.

    Returns:
        str: a string denoting engagement status.
    """

    # generate a list of dict objects with status and weight
    # used later to sort by the weight integer value.
    status_ranks = [
        {
            api_c.STATUS: x[api_c.STATUS],
            api_c.WEIGHT: api_c.STATUS_WEIGHTS.get(x[api_c.STATUS], 0),
        }
        for x in audience[api_c.DELIVERIES]
        if api_c.STATUS in x
    ]

    # sort delivery status list of dict by weight.
    status_ranks.sort(key=lambda x: x[api_c.WEIGHT])

    # take the first item in the sorted list, and grab the status
    return status_ranks[0][api_c.STATUS] if status_ranks else api_c.STATUS_NOT_DELIVERED
