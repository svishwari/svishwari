"""
Purpose of this file is to house all the engagement api tests
"""

import unittest
import json

import requests_mock
from marshmallow import ValidationError
from requests_mock import Mocker
from huxunify.api.config import get_config

from huxunify.api import constants as c
from huxunify.app import create_app

from huxunify.api.schema.engagement import (
    DisplayAdsSummary,
    DispAdIndividualAudienceSummary,
    EmailSummary,
    EmailIndividualAudienceSummary,
)

VALID_RESPONSE = {
    "active": True,
    "scope": "openid email profile",
    "username": "davesmith",
    "exp": 1234,
    "iat": 12345,
    "sub": "davesmith@fake",
    "aud": "sample_aud",
    "iss": "sample_iss",
    "jti": "sample_jti",
    "token_type": "Bearer",
    "client_id": "1234",
    "uid": "1234567",
}


class TestEngagementMetricsDisplayAds(unittest.TestCase):
    """
    Purpose of this class is to test Engagement Metrics of Display Ads
    """

    def setUp(self):  # pylint: disable=arguments-differ
        """
        Sets up Test Client

        Returns:
        """
        self.config = get_config()
        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )
        self.app = create_app().test_client()
        self.display_ads_engagement_metrics_endpoint = (
            f"/api/v1/{c.ENGAGEMENT_TAG}/"
            f"{c.AUDIENCE_PERFORMANCE}/"
            f"{c.DISPLAY_ADS}"
        )

    @staticmethod
    def validate_schema(schema, response) -> bool:
        """
        Utility Function to Validate the Schema with respect to Response

        Args:schema: Marshmallow Schema
            response:json response

        Return: Boolean
        """
        try:
            schema.load(data=response)
            return True
        except ValidationError:

            return False

    @requests_mock.Mocker()
    def test_display_ads_summary(self, request_mocker: Mocker):
        """
        It validates the schema for Display Ads Summary
        Schema Name: DisplayAdsSummary
        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = self.app.get(
            self.display_ads_engagement_metrics_endpoint,
            headers={"Authorization": "Bearer 12345678"},
        )
        jsonresponse = json.loads(response.data)

        summary = jsonresponse["summary"]
        result = self.validate_schema(DisplayAdsSummary(), summary)
        self.assertTrue(result)

    @requests_mock.Mocker()
    def test_display_ads_audience_performance(self, request_mocker: Mocker):
        """
        It validates the schema for Individual Audience
        Display Ads Performance Summary
        Schema Name: DispAdIndividualAudienceSummary
        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = self.app.get(
            self.display_ads_engagement_metrics_endpoint,
            headers={"Authorization": "Bearer 12345678"},
        )
        jsonresponse = json.loads(response.data)

        audience_performance = jsonresponse["audience_performance"][0]
        result = self.validate_schema(
            DispAdIndividualAudienceSummary(), audience_performance
        )
        self.assertTrue(result)


class TestEngagementMetricsEmail(unittest.TestCase):
    """
    Purpose of this class is to test Engagement Metrics of Email
    """

    def setUp(self):  # pylint: disable=arguments-differ
        """
        Sets up Test Client

        Returns:
        """
        self.config = get_config()
        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )
        self.app = create_app().test_client()
        self.email_engagement_metrics_endpoint = (
            f"/api/v1/{c.ENGAGEMENT_TAG}/"
            f"{c.AUDIENCE_PERFORMANCE}/"
            f"{c.EMAIL}"
        )

    @staticmethod
    def validate_schema(schema, response) -> bool:
        """
        Utility Function to Validate the Schema with respect to Response

        Args:schema: Marshmallow Schema
            response:json response

        Return: Boolean
        """
        try:
            schema.load(data=response)
            return True
        except ValidationError:
            return False

    @requests_mock.Mocker()
    def test_email_summary(self, request_mocker: Mocker):
        """
        It validates the schema for Email Summary
        Schema Name: EmailSummary
        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = self.app.get(
            self.email_engagement_metrics_endpoint,
            headers={"Authorization": "Bearer 12345678"},
        )
        jsonresponse = json.loads(response.data)

        summary = jsonresponse["summary"]
        result = self.validate_schema(EmailSummary(), summary)
        self.assertTrue(result)

    @requests_mock.Mocker()
    def test_email_audience_performance(self, request_mocker: Mocker):
        """
        It validates the schema for Individual Audience Display Ads Performance Summary
        Schema Name: EmailIndividualAudienceSummary
        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = self.app.get(
            self.email_engagement_metrics_endpoint,
            headers={"Authorization": "Bearer 12345678"},
        )
        jsonresponse = json.loads(response.data)

        audience_performance = jsonresponse["audience_performance"][0]
        result = self.validate_schema(
            EmailIndividualAudienceSummary(), audience_performance
        )
        self.assertTrue(result)
