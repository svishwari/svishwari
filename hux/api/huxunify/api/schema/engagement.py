# pylint: disable=no-self-use
"""
Schemas for the Engagements API
"""
from bson import ObjectId
from flask_marshmallow import Schema
from marshmallow import fields, validate, pre_load, post_dump
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import must_not_be_blank, validate_object_id
from huxunify.api.schema.custom_schemas import DateTimeWithZ


class DeliverySchedule(Schema):
    """
    Delivery Schedule schema
    """

    start_date = DateTimeWithZ(allow_none=True)
    end_date = DateTimeWithZ(allow_none=True)


class EngagementPostSchema(Schema):
    """
    Engagement post schema class
    """

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
    def pre_process_details(self, data, **kwarg):
        """process the schema before loading.

        Args:
            data (dict): The Engagement data source object
            many (bool): If there are many to process
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
    """
    Engagement put schema class
    """

    name = fields.String(required=False)
    description = fields.String(required=False)
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
    )
    delivery_schedule = fields.Nested(DeliverySchedule, required=False)


class AudienceEngagementSchema(Schema):
    """
    Schema for adding/deleting audience to engagement
    """

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
    def pre_process_details(self, data, **kwarg):
        """process the schema before loading.

        Args:
            data (dict): The Engagement data source object
            many (bool): If there are many to process
        Returns:
            Response: Returns a Engagement data source object

        """
        for audience in data[api_c.AUDIENCES]:
            audience[api_c.ID] = ObjectId(audience[api_c.ID])
            for destination in audience[api_c.DESTINATIONS]:
                destination[api_c.ID] = ObjectId(destination[api_c.ID])
        return data


class AudienceEngagementDeleteSchema(Schema):
    """
    Schema for adding/deleting audience to engagement
    """

    audience_ids = fields.List(
        fields.String,
        example=[
            "60ae035b6c5bf45da27f17e5",
            "60ae035b6c5bf45da27f17e6",
        ],
    )


class DestinationEngagedAudienceSchema(Schema):
    """
    Schema for adding destination to engagement audience
    """

    id = fields.String(
        attribute=db_c.OBJECT_ID,
        example="60ae035b6c5bf45da27f17e5",
        required=True,
    )
    delivery_platform_config = fields.Dict(
        attribute=db_c.DELIVERY_PLATFORM_CONFIG,
        example={db_c.DATA_EXTENSION_NAME: "SFMC Date Extension"},
        required=False,
        default=None,
    )


class DisplayAdsSummary(Schema):
    """
    Schema for Display Ads Summary
    """

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
    """
    Schema for Individual Campaign Summary
    """

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    name = fields.String()
    is_mapped = fields.Boolean()


class DispAdIndividualAudienceSummary(DisplayAdsSummary):
    """
    Schema for Individual Audience Summary
    """

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    name = fields.String()
    destinations = fields.List(fields.Nested(DispAdIndividualCampaignSummary))


class AudiencePerformanceDisplayAdsSchema(Schema):
    """
    Schema for Performance Metrics of Display Ads
    """

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    summary = fields.Nested(DisplayAdsSummary)
    audience_performance = fields.List(
        fields.Nested(DispAdIndividualAudienceSummary)
    )


class EmailSummary(Schema):
    """
    Schema for Summary Performance Metrics of Email
    """

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
    click_through_rate = fields.Float()
    click_to_open_rate = fields.Float()
    unique_clicks = fields.Integer()
    unique_opens = fields.Integer()
    unsubscribe = fields.Integer()
    unsubscribe_rate = fields.Float()


class EmailIndividualCampaignSummary(EmailSummary):
    """
    Schema for Individual Campaign Summary of Email
    """

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    name = fields.String()
    is_mapped = fields.Boolean()


class EmailIndividualAudienceSummary(EmailSummary):
    """
    Schema for Individual Audience Summary of Email
    """

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    name = fields.String()
    destinations = fields.List(fields.Nested(EmailIndividualCampaignSummary))


class AudiencePerformanceEmailSchema(Schema):
    """
    Schema for Performance Metrics of Email
    """

    class Meta:
        """Set Order for the Audience Response"""

        ordered = True

    summary = fields.Nested(EmailSummary)
    audience_performance = fields.List(
        fields.Nested(EmailIndividualAudienceSummary)
    )


class CampaignSchema(Schema):
    """
    Schema for Campaigns
    """

    class Meta:
        """Set Order for the Campaign Response"""

        ordered = True

    id = fields.String(
        example="5f5f7262997acad4bac4373b",
        validate=validate_object_id,
    )
    name = fields.String()
    delivery_job_id = fields.String(
        example="5f5f7262997acad4bac4373b",
        validate=validate_object_id,
    )
    create_time = DateTimeWithZ(attribute=db_c.CREATE_TIME, allow_none=True)


class CampaignPutSchema(Schema):
    """
    Schema for Campaigns PUT.
    """

    class Meta:
        """Set Order for the Campaigns Response"""

        ordered = True

    campaigns = fields.List(
        fields.Dict,
        example=[
            {
                api_c.NAME: "Test Campaign",
                api_c.ID: "campaign_id",
                api_c.DELIVERY_JOB_ID: "delivery_job_id",
            }
        ],
    )


class DeliveryJobSchema(Schema):
    """
    Schema for Campaigns
    """

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
    """
    Schema for Campaigns
    """

    class Meta:
        """Set Order for the Campaign Response"""

        ordered = True

    campaigns = fields.List(fields.Nested(CampaignSchema))
    delivery_jobs = fields.List(fields.Nested(DeliveryJobSchema))


class EngagementDataExtensionSchema(Schema):
    """
    Engagement Audience Destination Data Extension Schema
    """

    data_extension_name = fields.String()


class LatestDeliverySchema(Schema):
    """
    Engagement Audience Destination Delivery Schema
    """

    id = fields.String()
    status = fields.String()
    update_time = DateTimeWithZ()
    size = fields.Int(default=1000)


class EngagementAudienceDestinationSchema(Schema):
    """
    Engagement Audience Destination Schema
    """

    name = fields.String()
    id = fields.String()
    delivery_job_id = fields.String()
    delivery_platform_config = fields.Nested(EngagementDataExtensionSchema)
    delivery_platform_type = fields.String()
    latest_delivery = fields.Nested(LatestDeliverySchema)


class EngagementAudienceSchema(Schema):
    """
    Engagement Audience Schema
    """

    name = fields.String()
    id = fields.String()
    status = fields.String()
    destinations = fields.Nested(
        EngagementAudienceDestinationSchema, many=True
    )


class EngagementGetSchema(Schema):
    """
    Engagement get schema class
    """

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


def weighted_engagement_status(engagements: list) -> list:
    """Returns a weighted engagement status by rolling up the individual
    destination status values.

    Args:
        engagements (list): input engagement list.

    Returns:
        list: list of engagement documents.
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

                # TODO after ORCH-285 so no status mapping needed.
                status = destination[api_c.LATEST_DELIVERY][api_c.STATUS]
                if status == db_c.STATUS_IN_PROGRESS:
                    # map pending to delivering status
                    status = api_c.STATUS_DELIVERING

                elif status == db_c.STATUS_SUCCEEDED:
                    # map succeeded to delivered status
                    status = api_c.STATUS_DELIVERED

                elif status == db_c.STATUS_FAILED:
                    # map failed to delivered status
                    status = api_c.STATUS_ERROR

                destination[api_c.LATEST_DELIVERY][api_c.STATUS] = status

                status_rank = {
                    api_c.STATUS: status,
                    api_c.WEIGHT: api_c.STATUS_WEIGHTS.get(status, 0),
                }
                status_ranks.append(status_rank)
                audience_status_rank.append(status_rank)
                destinations.append(destination)

            audience[api_c.DESTINATIONS] = destinations

            # sort delivery status list of dict by weight.
            audience_status_rank.sort(key=lambda x: x[api_c.WEIGHT])

            # take the first item in the sorted list, and grab the status
            audience[api_c.STATUS] = (
                audience_status_rank[0][api_c.STATUS]
                if audience_status_rank
                else api_c.STATUS_NOT_DELIVERED
            )
            audiences.append(audience)

        engagement[api_c.AUDIENCES] = audiences

        # sort delivery status list of dict by weight.
        status_ranks.sort(key=lambda x: x[api_c.WEIGHT])

        # take the first item in the sorted list, and grab the status
        engagement[api_c.STATUS] = (
            status_ranks[0][api_c.STATUS]
            if status_ranks
            else api_c.STATUS_NOT_DELIVERED
        )

    return engagements


def weight_delivery_status(engagements: list) -> str:
    """Returns a weighted delivery status by rolling up the individual
    delivery status values.

    Args:
        engagements (list): input engagement delivery list.

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
        for x in engagements[api_c.DELIVERIES]
        if api_c.STATUS in x
    ]

    # sort delivery status list of dict by weight.
    status_ranks.sort(key=lambda x: x[api_c.WEIGHT])

    # take the first item in the sorted list, and grab the status
    return (
        status_ranks[0][api_c.STATUS]
        if status_ranks
        else api_c.STATUS_NOT_DELIVERED
    )
