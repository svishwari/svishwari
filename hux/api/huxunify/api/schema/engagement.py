# pylint: disable=no-self-use
"""
Schemas for the Engagements API
"""
from bson import ObjectId
from flask_marshmallow import Schema
from marshmallow import fields, validate, pre_load, pre_dump
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import must_not_be_blank, validate_object_id


class DeliverySchedule(Schema):
    """
    Delivery Schedule schema
    """

    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)


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

    audiences = fields.List(
        fields.Dict(),
        attribute=api_c.AUDIENCES,
        example=[
            {
                api_c.ID: "60ae035b6c5bf45da27f17d6",
                api_c.DESTINATIONS: [
                    {
                        "id": "60ae035b6c5bf45da27f17d6",
                        # TODO - hook up extension for HUS-458
                        "contact_list": "sfmc_extension_name",
                    },
                ],
                api_c.DELIVERIES: [
                    "60ae035b6c5bf45da27f17e5",
                    "60ae035b6c5bf45da27f17e6",
                ],
            }
        ],
    )
    status = fields.String(
        attribute=api_c.STATUS,
        required=True,
        validate=validate.OneOf(api_c.ENGAGEMENT_STATUSES),
    )
    delivery_schedule = fields.Nested(
        DeliverySchedule,
        required=False,
        attribute=api_c.DELIVERY_SCHEDULE,
    )
    create_time = fields.DateTime(attribute=db_c.CREATE_TIME)
    created_by = fields.String(attribute=db_c.CREATED_BY)
    update_time = fields.DateTime(attribute=db_c.UPDATE_TIME, allow_none=True)
    updated_by = fields.String(attribute=db_c.UPDATED_BY, allow_none=True)

    @pre_dump
    # pylint: disable=unused-argument
    def pre_process_details(self, data, **kwarg):
        """process the schema before serializing.

        Args:
            data (dict): The Engagement data source object
            many (bool): If there are many to process
        Returns:
            Response: Returns a Engagement data source object

        """
        for audience in data[api_c.AUDIENCES]:
            audience[api_c.ID] = str(audience[api_c.ID])
            for destination in audience[api_c.DESTINATIONS]:
                destination[api_c.ID] = str(destination[api_c.ID])
        return data


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
            data.pop(api_c.DELIVERY_SCHEDULE)

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


class DisplayAdsSummary(Schema):
    """
    Schema for Display Ads Summary
    """

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

    name = fields.String()
    is_mapped = fields.Boolean()


class DispAdIndividualAudienceSummary(DisplayAdsSummary):
    """
    Schema for Individual Audience Summary
    """

    name = fields.String()
    campaigns = fields.List(fields.Nested(DispAdIndividualCampaignSummary))


class AudiencePerformanceDisplayAdsSchema(Schema):
    """
    Schema for Performance Metrics of Display Ads
    """

    summary = fields.Nested(DisplayAdsSummary)
    audience_performance = fields.List(
        fields.Nested(DispAdIndividualAudienceSummary)
    )


class EmailSummary(Schema):
    """
    Schema for Summary Performance Metrics of Email
    """

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

    name = fields.String()
    is_mapped = fields.Boolean()


class EmailIndividualAudienceSummary(EmailSummary):
    """
    Schema for Individual Audience Summary of Email
    """

    name = fields.String()
    campaigns = fields.List(fields.Nested(EmailIndividualCampaignSummary))


class AudiencePerformanceEmailSchema(Schema):
    """
    Schema for Performance Metrics of Email
    """

    summary = fields.Nested(EmailSummary)
    audience_performance = fields.List(
        fields.Nested(EmailIndividualAudienceSummary)
    )
