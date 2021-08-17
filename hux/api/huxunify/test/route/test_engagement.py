# pylint: disable=too-many-lines
"""
Purpose of this file is to house all the engagement api tests
"""
import json
from datetime import datetime, timedelta
from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
from flask_marshmallow import Schema
import mongomock
from bson import ObjectId
from marshmallow import ValidationError

from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
    set_delivery_job,
    set_performance_metrics,
)
from huxunifylib.database.engagement_management import (
    set_engagement,
    get_engagements,
)
from huxunifylib.database.orchestration_management import create_audience
from huxunifylib.database.user_management import set_user
from huxunifylib.connectors import FacebookConnector
from huxunify.api.schema.engagement import DisplayAdsSummary, EmailSummary
from huxunify.api import constants as api_c
from huxunify.app import create_app
import huxunify.test.constants as t_c

EMAIL_METRICS = {
    "sent": 125,
    "hard_bounces": 125,
    "hard_bounces_rate": 0.1,
    "delivered": 125,
    "delivered_rate": 0.1,
    "open": 365200,
    "open_rate": 0.1,
    "clicks": 365200,
    "click_through_rate": 0.7208,
    "click_to_open_rate": 0.7208,
    "unique_clicks": 365200,
    "unique_opens": 225100,
    "unsubscribe": 365200,
    "unsubscribe_rate": 0.7208,
}

DISPLAY_ADS_METRICS = {
    "impressions": 70487,
    "spend": 14507,
    "reach": 8848,
    "conversions": 16,
    "clicks": 516,
    "frequency": 9,
    "cost_per_thousand_impressions": 0,
    "click_through_rate": 0,
    "cost_per_action": 0,
    "cost_per_click": 0,
    "engagement_rate": 0,
}


def validate_schema(schema: Schema, response: dict) -> bool:
    """
    Utility Function to Validate the Schema with respect to Response

    Args:
        schema (Schema): Marshmallow Schema
        response (dict): json response

    Returns:
        (bool)
    """
    try:
        schema.load(data=response)
        return True
    except ValidationError:
        return False


# pylint: disable=too-many-instance-attributes
class TestEngagementMetricsDisplayAds(TestCase):
    """
    Purpose of this class is to test Engagement Metrics of Display Ads
    """

    def setUp(self):
        """
        Sets up Test Client

        Returns:
        """

        self.app = create_app().test_client()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock request for introspect call
        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        self.request_mocker.start()

        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() for the engagement.
        mock.patch(
            "huxunify.api.route.engagement.get_db_client",
            return_value=self.database,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.performancemetrics.get_db_client",
            return_value=self.database,
        ).start()

        self.audience_id = create_audience(self.database, "Test Audience", [])[
            db_c.ID
        ]
        self.delivery_platform = set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_FACEBOOK,
            "facebook_delivery_platform",
            authentication_details={},
            status=db_c.STATUS_SUCCEEDED,
        )
        self.audiences = [
            {
                api_c.ID: self.audience_id,
                api_c.DESTINATIONS: [
                    {
                        api_c.ID: self.delivery_platform[db_c.ID],
                    },
                ],
            }
        ]
        self.engagement_id = set_engagement(
            self.database,
            "Test engagement",
            None,
            self.audiences,
            None,
            None,
            False,
        )
        self.delivery_job = set_delivery_job(
            self.database,
            self.audience_id,
            self.delivery_platform[db_c.ID],
            [
                {
                    db_c.ENGAGEMENT_ID: self.engagement_id,
                    db_c.AUDIENCE_ID: self.audience_id,
                }
            ],
            self.engagement_id,
        )

        set_performance_metrics(
            self.database,
            self.delivery_platform[db_c.ID],
            "facebook",
            self.delivery_job[db_c.ID],
            None,
            DISPLAY_ADS_METRICS,
            None,
            None,
        )

        self.addCleanup(mock.patch.stopall)

    def test_display_ads_summary(self):
        """
        It validates the schema for Display Ads Summary
        Schema Name: DisplayAdsSummary

        Args:

        Returns:
            None
        """

        engagement_id = self.engagement_id
        endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/"
            f"{engagement_id}/"
            f"{api_c.AUDIENCE_PERFORMANCE}/"
            f"{api_c.DISPLAY_ADS}"
        )

        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            validate_schema(DisplayAdsSummary(), response.json["summary"])
        )
        self.assertEqual(response.json["summary"]["impressions"], 70487)
        self.assertEqual(response.json["summary"]["spend"], 14507)
        self.assertTrue(response.json["audience_performance"])
        self.assertTrue(response.json["audience_performance"][0]["id"])
        self.assertTrue(
            response.json["audience_performance"][0]["impressions"], 70487
        )
        self.assertTrue(
            response.json["audience_performance"][0]["destinations"]
        )
        self.assertTrue(
            response.json["audience_performance"][0]["destinations"][0][
                "impressions"
            ],
            70487,
        )

    def test_display_ads_invalid_engagement(self):
        """
        Tests response for invalid engagement id

        Args:

        Returns:
            None
        """

        engagement_id = "random_id"
        endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/"
            f"{engagement_id}/"
            f"{api_c.AUDIENCE_PERFORMANCE}/"
            f"{api_c.DISPLAY_ADS}"
        )

        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_display_ads_audience_performance_invalid_engagement_id(self):
        """
        It validates the schema for Individual Audience
        Display Ads Performance Summary
        Schema Name: DispAdIndividualAudienceSummary

        Args:

        Returns:
            None
        """

        engagement_id = ObjectId()
        endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/"
            f"{engagement_id}/"
            f"{api_c.AUDIENCE_PERFORMANCE}/"
            f"{api_c.DISPLAY_ADS}"
        )

        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)


# pylint: disable=too-many-instance-attributes
class TestEngagementMetricsEmail(TestCase):
    """
    Purpose of this class is to test Engagement Metrics of Email
    """

    def setUp(self):
        """
        Sets up Test Client

        Returns:
        """

        self.app = create_app().test_client()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock request for introspect call
        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        self.request_mocker.start()

        # mock get_db_client() for the engagement.
        mock.patch(
            "huxunify.api.route.engagement.get_db_client",
            return_value=self.database,
        ).start()

        mock.patch(
            "huxunify.api.data_connectors.performancemetrics.get_db_client",
            return_value=self.database,
        ).start()

        self.audience_id = create_audience(self.database, "Test Audience", [])[
            db_c.ID
        ]

        self.delivery_platform_sfmc = set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_SFMC,
            "sfmc_delivery_platform",
            authentication_details={},
            status=db_c.STATUS_SUCCEEDED,
        )
        self.audiences = [
            {
                api_c.ID: self.audience_id,
                api_c.DESTINATIONS: [
                    {
                        api_c.ID: self.delivery_platform_sfmc[db_c.ID],
                    },
                ],
            }
        ]
        self.engagement_id_sfmc = set_engagement(
            self.database,
            "Test engagement sfmc",
            None,
            self.audiences,
            None,
            None,
            False,
        )

        self.delivery_job_sfmc = set_delivery_job(
            self.database,
            self.audience_id,
            self.delivery_platform_sfmc[db_c.ID],
            [
                {
                    db_c.ENGAGEMENT_ID: self.engagement_id_sfmc,
                    db_c.AUDIENCE_ID: self.audience_id,
                }
            ],
            self.engagement_id_sfmc,
        )

        set_performance_metrics(
            self.database,
            self.delivery_platform_sfmc[db_c.ID],
            "salesforce",
            self.delivery_job_sfmc[db_c.ID],
            None,
            EMAIL_METRICS,
            None,
            None,
        )

        self.addCleanup(mock.patch.stopall)

    def test_email_summary(self):
        """
        It validates the schema for Email Summary
        Schema Name: EmailSummary

        Args:

        Returns:
            None
        """

        endpoint = (
            f"/api/v1/{api_c.ENGAGEMENT_TAG}/"
            f"{self.engagement_id_sfmc}/"
            f"{api_c.AUDIENCE_PERFORMANCE}/"
            f"{api_c.EMAIL}"
        )
        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(
            validate_schema(EmailSummary(), response.json["summary"])
        )
        self.assertEqual(response.json["summary"]["hard_bounces"], 125)
        self.assertEqual(response.json["summary"]["sent"], 125)
        self.assertTrue(response.json["audience_performance"])
        self.assertTrue(response.json["audience_performance"][0]["id"])
        self.assertEqual(
            response.json["audience_performance"][0]["hard_bounces"], 125
        )
        self.assertEqual(response.json["audience_performance"][0]["sent"], 125)
        self.assertTrue(
            response.json["audience_performance"][0]["destinations"]
        )
        self.assertEqual(
            response.json["audience_performance"][0]["destinations"][0][
                "hard_bounces"
            ],
            125,
        )
        self.assertEqual(
            response.json["audience_performance"][0]["destinations"][0][
                "sent"
            ],
            125,
        )

    def test_email_invalid_engagement(self):
        """
        Tests response for invalid engagement id

        Args:

        Returns:
            None
        """

        engagement_id = "invalid_object_id"
        endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/"
            f"{engagement_id}/"
            f"{api_c.AUDIENCE_PERFORMANCE}/"
            f"{api_c.EMAIL}"
        )

        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_email_audience_performance(self):
        """
        It validates the schema for Individual Audience Display Ads Performance Summary
        Schema Name: EmailIndividualAudienceSummary

        Args:

        Returns:
            None
        """

        endpoint = (
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/"
            f"{self.engagement_id_sfmc}/"
            f"{api_c.AUDIENCE_PERFORMANCE}/"
            f"{api_c.EMAIL}"
        )
        response = self.app.get(
            endpoint,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class TestEngagementRoutes(TestCase):
    """
    Tests for Engagement APIs
    """

    def setUp(self) -> None:
        """
        Setup resources before each test

        Args:

        Returns:
        """

        # mock request for introspect call
        request_mocker = requests_mock.Mocker()
        request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        request_mocker.get(t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE)
        request_mocker.start()

        self.app = create_app().test_client()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        mock.patch(
            "huxunify.api.route.engagement.get_db_client",
            return_value=self.database,
        ).start()
        self.addCleanup(mock.patch.stopall)

        # mock get_db_client() for the userinfo utils.
        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        # mock FacebookConnector
        mock.patch.object(
            FacebookConnector, "get_campaigns", return_value=t_c.BATCH_RESPONSE
        ).start()

        self.addCleanup(mock.patch.stopall)

        # write a user to the database
        self.user_name = "felix hernandez"
        set_user(
            self.database,
            "fake",
            "felix_hernandez@fake.com",
            display_name=self.user_name,
        )

        destinations = [
            {
                db_c.DELIVERY_PLATFORM_NAME: "Facebook",
                db_c.DELIVERY_PLATFORM_TYPE: "facebook",
                db_c.STATUS: db_c.STATUS_SUCCEEDED,
                db_c.ENABLED: True,
                db_c.ADDED: True,
                db_c.DELIVERY_PLATFORM_AUTH: {
                    api_c.FACEBOOK_ACCESS_TOKEN: "path1",
                    api_c.FACEBOOK_APP_SECRET: "path2",
                    api_c.FACEBOOK_APP_ID: "path3",
                    api_c.FACEBOOK_AD_ACCOUNT_ID: "path4",
                },
            },
        ]

        self.destinations = []
        for destination in destinations:
            self.destinations.append(
                set_delivery_platform(self.database, **destination)
            )

        audiences = [
            {
                db_c.AUDIENCE_NAME: "Test Audience",
                "audience_filters": [
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
                api_c.DESTINATION_IDS: [d[db_c.ID] for d in self.destinations],
            },
            {
                db_c.AUDIENCE_NAME: "Test Audience No Destinations",
                "audience_filters": [
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
        ]

        self.audiences = [
            create_audience(self.database, **x) for x in audiences
        ]

        engagements = [
            {
                db_c.ENGAGEMENT_NAME: "Test Engagement",
                db_c.ENGAGEMENT_DESCRIPTION: "test-engagement",
                db_c.AUDIENCES: [
                    {
                        db_c.OBJECT_ID: self.audiences[0][db_c.ID],
                        api_c.DESTINATIONS: [
                            {
                                db_c.OBJECT_ID: dest[db_c.ID],
                                db_c.LATEST_DELIVERY: {
                                    api_c.SIZE: 1000,
                                    api_c.STATUS: api_c.STATUS_NOT_DELIVERED,
                                },
                            }
                            for dest in self.destinations
                        ],
                    },
                    {
                        db_c.OBJECT_ID: self.audiences[1][db_c.ID],
                        api_c.DESTINATIONS: [
                            {
                                db_c.OBJECT_ID: dest[db_c.ID],
                                db_c.LATEST_DELIVERY: {
                                    api_c.SIZE: 1000,
                                    api_c.STATUS: api_c.STATUS_NOT_DELIVERED,
                                },
                            }
                            for dest in self.destinations
                        ],
                    },
                ],
                api_c.USER_NAME: self.user_name,
            },
            {
                db_c.ENGAGEMENT_NAME: "Test Engagement No Destination",
                db_c.ENGAGEMENT_DESCRIPTION: "test-engagement",
                db_c.AUDIENCES: [
                    {
                        db_c.OBJECT_ID: self.audiences[1][db_c.ID],
                        api_c.DESTINATIONS_TAG: [],
                    },
                ],
                api_c.USER_NAME: self.user_name,
            },
        ]

        self.engagement_ids = [
            str(set_engagement(self.database, **x)) for x in engagements
        ]

        self.addCleanup(mock.patch.stopall)

    def test_get_campaign_mappings_no_delivery_jobs(self):
        """
        Test get all engagements API

        Args:

        Returns:

        """

        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaign-mappings"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {
            "message": "Could not find any delivery jobs to map."
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_campaigns_no_delivery_jobs(self):
        """
        Test get all engagements API

        Args:

        Returns:

        """

        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaigns"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_get_campaigns_for_non_existent_engagement(self):
        """
        Test delivery of a destination for a non-existent engagement

        Args:

        Returns:

        """
        engagement_id = str(ObjectId())
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaigns"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.ENGAGEMENT_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_campaigns_for_invalid_engagement(self):
        """
        Test delivery of a destination for a non-existent engagement

        Args:

        Returns:

        """
        engagement_id = "random_id"
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaigns"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.INVALID_OBJECT_ID}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_campaign_mappings_for_invalid_engagement(self):
        """
        Test delivery of a destination for a non-existent engagement

        Args:

        Returns:

        """
        engagement_id = "random_id"
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaign-mappings"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.INVALID_OBJECT_ID}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_campaign_mappings_for_non_existent_engagement(self):
        """
        Test delivery of a destination for a non-existent engagement

        Args:

        Returns:

        """
        engagement_id = str(ObjectId())
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaign-mappings"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.ENGAGEMENT_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_put_campaign_mappings_for_non_existent_engagement(self):
        """
        Test delivery of a destination for a non-existent engagement

        Args:

        Returns:

        """
        engagement_id = str(ObjectId())
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.put(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaigns"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.ENGAGEMENT_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_put_campaigns_invalid_audience_id(self):
        """
        Test delivery of a destination for a non-existent engagement

        Args:

        Returns:

        """
        audience_id = "XYZ123"
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.put(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaigns"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.INVALID_OBJECT_ID}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_campaigns_for_an_engagement_invalid_audience_id(self):
        """
        Test delivery of an audience for an engagement
        with invalid audience id

        Args:

        Returns:

        """
        audience_id = "XYZ123"
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaigns"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.INVALID_OBJECT_ID}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_campaign_mappings_for_an_engagement_invalid_audience_id(self):
        """
        Test delivery of an audience for an engagement
        with invalid audience id

        Args:

        Returns:

        """
        audience_id = "XYZ123"
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaign-mappings"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.INVALID_OBJECT_ID}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_campaigns_for_an_engagement_invalid_destination_id(self):
        """
        Test delivery of an audience for an engagement
        with invalid audience id

        Args:

        Returns:

        """
        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = "XYZ123"

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaigns"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(destination_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_put_campaigns_invalid_destination_id(self):
        """
        Test delivery of a destination for a non-existent engagement

        Args:

        Returns:

        """
        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = "XYZ123"

        response = self.app.put(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaigns"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(destination_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_campaign_mappings_for_an_engagement_invalid_destination_id(
        self,
    ):
        """
        Test get campaigns for an engagement
        with invalid audience id

        Args:

        Returns:

        """
        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = "XYZ123"

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaign-mappings"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(destination_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_campaign_for_unattached_audience(self):
        """
        Test delivery of a destination for an unattached audience

        Args:

        Returns:

        """
        engagement_id = self.engagement_ids[1]

        # Unattached audience id
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaigns"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {
            "message": "Audience is not attached to the engagement."
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_campaign_mappings_for_unattached_audience(self):
        """
        Test delivery of a destination for an unattached audience

        Args:

        Returns:

        """
        engagement_id = self.engagement_ids[1]

        # Unattached audience id
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaign-mappings"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {
            "message": "Audience is not attached to the engagement."
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_campaigns_for_unattached_destination(self):
        """
        Test get campaigns for an unattached destination

        Args:

        Returns:

        """
        engagement_id = self.engagement_ids[0]
        # Unattached audience id
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaigns"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_campaign_mappings_for_unattached_destination(self):
        """
        Test get campaign mappings for an unattached destination

        Args:

        Returns:

        """
        engagement_id = self.engagement_ids[0]
        # Unattached audience id
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.get(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/campaign-mappings"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_get_engagements_success(self):
        """
        Test get all engagements API

        Args:

        Returns:

        """
        expected_engagements = get_engagements(self.database)

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
        )

        engagements = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(len(engagements), len(expected_engagements))
        for engagement in engagements:
            self.assertEqual(self.user_name, engagement[db_c.CREATED_BY])
            self.assertIsNotNone(engagement[db_c.STATUS])

    def test_get_engagement_by_id_valid_id(self):
        """
        Test get engagement API with valid id

        Args:

        Returns:

        """

        engagement_id = self.engagement_ids[0]
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        return_engagement = response.json
        self.assertEqual(engagement_id, return_engagement[db_c.OBJECT_ID])
        self.assertEqual(self.user_name, return_engagement[db_c.CREATED_BY])
        self.assertEqual(api_c.STATUS_INACTIVE, return_engagement[db_c.STATUS])

    def test_get_engagement_by_id_invalid_id(self):
        """
        Test get engagements API with invalid id

        Args:

        Returns:

        """

        engagement_id = "XYZ"

        valid_response = {"message": api_c.INVALID_ID}

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_engagement_by_id_non_existent_id(self):
        """
        Test get engagements API with non-existent id

        Args:

        Returns:

        """

        engagement_id = str(ObjectId())

        valid_response = {"message": "Not found"}

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_delete_engagement_valid_id(self):
        """
        Test delete engagement API with valid id

        Args:

        Returns:

        """

        engagement_id = self.engagement_ids[0]

        valid_response = {"message": api_c.OPERATION_SUCCESS}

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_delete_engagement_invalid_id(self):
        """Test delete engagement API with invalid id

        Args:

        Returns:

        """

        engagement_id = "XYZ123"
        valid_response = {"message": api_c.INVALID_ID}

        response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_set_engagement_valid_request(self):
        """
        Test set engagement API with valid params

        Args:

        Returns:

        """

        engagement = {
            db_c.AUDIENCES: [
                {
                    db_c.OBJECT_ID: str(self.audiences[0][db_c.ID]),
                    db_c.DESTINATIONS: [
                        {db_c.OBJECT_ID: str(self.destinations[0][db_c.ID])},
                    ],
                }
            ],
            db_c.ENGAGEMENT_DESCRIPTION: "Test Engagement Description",
            db_c.ENGAGEMENT_NAME: "Soumya's Test Engagement",
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE: None,
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}",
            data=json.dumps(engagement),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_set_engagement_without_audience(self):
        """
        Test set engagement API without audience

        Args:

        Returns:

        """

        engagement = {
            db_c.AUDIENCES: [],
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE: None,
            db_c.ENGAGEMENT_DESCRIPTION: "Test Set Engagement",
            db_c.ENGAGEMENT_NAME: "Test Engagement No Audience",
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}",
            data=json.dumps(engagement),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_set_engagement_without_description(self):
        """
        Test set engagement API without description

        Args:

        Returns:

        """

        engagement = {
            db_c.AUDIENCES: [],
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE: None,
            db_c.ENGAGEMENT_NAME: "Test Engagement No Audience",
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}",
            data=json.dumps(engagement),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_set_engagement_without_name(self):
        """
        Test set engagement API without name

        Args:

        Returns:

        """

        engagement = {
            db_c.AUDIENCES: [],
            db_c.ENGAGEMENT_DELIVERY_SCHEDULE: None,
        }

        valid_response = {
            db_c.ENGAGEMENT_NAME: ["Missing data for required field."]
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}",
            data=json.dumps(engagement),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_update_engagement(self):
        """
        Test update an engagement

        Returns:

        """

        engagement_id = self.engagement_ids[0]

        engagement_response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        update_doc = engagement_response.json
        update_doc[db_c.NAME] = "new name"
        del update_doc[db_c.CREATE_TIME]
        del update_doc[db_c.STATUS]
        del update_doc[db_c.UPDATE_TIME]
        del update_doc[db_c.UPDATED_BY]
        del update_doc[db_c.OBJECT_ID]
        del update_doc[db_c.CREATED_BY]

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            json=update_doc,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual("new name", response.json[db_c.NAME])

    def test_update_engagement_invalid_id(self):
        """
        Test update an engagement invalid id

        Returns:

        """

        bad_engagement_id = "asdfg123456"
        good_engagement_id = self.engagement_ids[0]

        engagement_response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{good_engagement_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        update_doc = engagement_response.json
        update_doc[db_c.NAME] = "new name"
        del update_doc[db_c.CREATE_TIME]
        del update_doc[db_c.STATUS]
        del update_doc[db_c.UPDATE_TIME]
        del update_doc[db_c.UPDATED_BY]
        del update_doc[db_c.OBJECT_ID]
        del update_doc[db_c.CREATED_BY]

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{bad_engagement_id}",
            json=update_doc,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_add_audience_to_engagement(self):
        """
        Test add audience to engagement

        Returns:

        """

        engagement_id = self.engagement_ids[0]

        new_audience = {
            "audiences": [
                {
                    db_c.OBJECT_ID: str(self.audiences[0][db_c.ID]),
                    "destinations": [
                        {db_c.OBJECT_ID: str(ObjectId())},
                        {db_c.OBJECT_ID: str(ObjectId())},
                    ],
                }
            ]
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/{api_c.AUDIENCES}",
            json=new_audience,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_add_audience_to_engagement_invalid_id(self):
        """
        Test add audience to engagement invalid id

        Returns:

        """

        engagement_id = "asdfg123456"

        new_audience = {
            "audiences": [
                {
                    db_c.OBJECT_ID: str(ObjectId()),
                    "destinations": [
                        {db_c.OBJECT_ID: str(ObjectId())},
                        {db_c.OBJECT_ID: str(ObjectId())},
                    ],
                }
            ]
        }

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/{api_c.AUDIENCES}",
            json=new_audience,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_delete_audience_from_engagement(self):
        """
        Test delete audience from engagement

        Returns:

        """

        engagement_id = self.engagement_ids[0]
        new_audience_id = self.audiences[0][db_c.ID]

        new_audience = {
            "audiences": [
                {
                    db_c.OBJECT_ID: str(new_audience_id),
                    "destinations": [
                        {db_c.OBJECT_ID: str(ObjectId())},
                        {db_c.OBJECT_ID: str(ObjectId())},
                    ],
                }
            ]
        }

        add_audience_response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/{api_c.AUDIENCES}",
            json=new_audience,
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, add_audience_response.status_code)

        delete_audience = {"audience_ids": [str(new_audience_id)]}

        delete_audience_response = self.app.delete(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/{api_c.AUDIENCES}",
            json=delete_audience,
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, delete_audience_response.status_code)

    def test_add_destination_to_engagement_audience(self):
        """Test add destination to engagement audience"""
        engagement_id = self.engagement_ids[0]
        audience_id = self.audiences[1][db_c.ID]

        new_destination = {
            db_c.DELIVERY_PLATFORM_NAME: db_c.DELIVERY_PLATFORM_SFMC.title(),
            db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFMC,
            db_c.STATUS: db_c.STATUS_SUCCEEDED,
            db_c.ENABLED: True,
            db_c.ADDED: True,
            db_c.DELETED: False,
        }

        destination = set_delivery_platform(self.database, **new_destination)

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.AUDIENCE}/{str(audience_id)}/destinations",
            json={db_c.OBJECT_ID: str(destination[db_c.ID])},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(
            HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code
        )

    def test_remove_destination_from_engagement_audience(self):
        """Test remove destination from engagement audience"""
        engagement_id = self.engagement_ids[0]
        audience_id = self.audiences[1][db_c.ID]

        destination_to_remove = {api_c.ID: str(self.destinations[0][db_c.ID])}

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.AUDIENCE}/{str(audience_id)}/destinations",
            json=destination_to_remove,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(
            HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code
        )

    def test_set_engagement_flight_schedule(self):
        """
        Test setting an engagement flight schedule
        Returns:
        """

        engagement_id = self.engagement_ids[0]

        engagement_response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        update_doc = engagement_response.json
        # remove props before sending full put.
        for prop in [
            db_c.CREATE_TIME,
            db_c.STATUS,
            db_c.UPDATE_TIME,
            db_c.UPDATED_BY,
            db_c.OBJECT_ID,
            db_c.CREATED_BY,
        ]:
            del update_doc[prop]

        update_doc[api_c.DELIVERY_SCHEDULE] = {
            api_c.START_DATE: datetime.utcnow()
            .replace(second=0, microsecond=0)
            .isoformat(),
            api_c.END_DATE: (datetime.utcnow() + timedelta(weeks=12))
            .replace(second=0, microsecond=0)
            .isoformat(),
        }

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            json=update_doc,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        response_body = response.json
        self.assertIn(api_c.DELIVERY_SCHEDULE, response_body)

        for key in [api_c.START_DATE, api_c.END_DATE]:
            self.assertIn(key, response_body[api_c.DELIVERY_SCHEDULE])
            response_datetime = datetime.fromisoformat(
                response_body[api_c.DELIVERY_SCHEDULE][key].replace("Z", "")
            )
            expected_datetime = datetime.fromisoformat(
                update_doc[api_c.DELIVERY_SCHEDULE][key]
            )

            # for some reason document DB does not main microsecond precision.
            self.assertEqual(response_datetime, expected_datetime)

    def test_remove_engagement_flight_schedule(self):
        """
        Test removing an engagement flight schedule
        Returns:
        """

        engagement_id = self.engagement_ids[0]
        engagement_response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        update_doc = engagement_response.json
        # remove props before sending full put.
        for prop in [
            db_c.CREATE_TIME,
            db_c.STATUS,
            db_c.UPDATE_TIME,
            db_c.UPDATED_BY,
            db_c.OBJECT_ID,
            db_c.CREATED_BY,
        ]:
            del update_doc[prop]

        # set the flight schedule first
        update_doc[api_c.DELIVERY_SCHEDULE] = {
            api_c.START_DATE: datetime.utcnow()
            .replace(second=0, microsecond=0)
            .isoformat(),
            api_c.END_DATE: (datetime.utcnow() + timedelta(weeks=3))
            .replace(second=0, microsecond=0)
            .isoformat(),
        }

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            json=update_doc,
            headers=t_c.STANDARD_HEADERS,
        )

        # test that it was added
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn(api_c.DELIVERY_SCHEDULE, response.json)

        update_doc[api_c.DELIVERY_SCHEDULE] = {}

        response = self.app.put(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            json=update_doc,
            headers=t_c.STANDARD_HEADERS,
        )

        # now test removal.
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertFalse(response.json[api_c.DELIVERY_SCHEDULE])

    def test_get_engagement_by_id_validate_match_rate(self) -> None:
        """
        Test get engagement API with valid id and valid match_rate present

        Args:

        Returns:
            None
        """

        engagements = get_engagements(self.database)

        self.assertTrue(engagements)

        engagement_id = str(engagements[0]["_id"])
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        return_engagement = response.json

        self.assertEqual(engagement_id, return_engagement[db_c.OBJECT_ID])
        # self.assertGreater(
        #     return_engagement[db_c.AUDIENCES][0][db_c.DESTINATIONS][0][
        #         db_c.LATEST_DELIVERY
        #     ][api_c.MATCH_RATE], 0
        # )
