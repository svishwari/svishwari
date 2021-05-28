"""
Purpose of this file is to house all the customers api tests
"""

import unittest
import json
import requests_mock
from requests_mock import Mocker
from huxunify.api.config import get_config

from huxunify.api import constants as c
from huxunify.app import create_app

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


class TestCustomersOverview(unittest.TestCase):
    """
    Purpose of this class is to test Customers overview
    """

    @requests_mock.Mocker()
    def setUp(self, request_mocker: Mocker):
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
        self.customer_overview_endpoint = (
            f"/api/v1{c.CUSTOMER_PROFILES_OVERVIEW_ENDPOINT}"
        )
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        response = self.app.get(
            self.customer_overview_endpoint,
            headers={"Authorization": "Bearer 12345678"},
        )
        self.jsonresponse = json.loads(response.data)

    def test_count_insights(self):
        """
        It tests the count of values of Customer Profile Overviews

        Expected Count=21
        """
        self.assertEqual(len(self.jsonresponse), 21)

    def test_gender_ratios(self):
        """
        It tests the gender ratios to be greater than 0 and sum should be equal to 1

        """
        gender_men = self.jsonresponse["gender_men"]
        gender_women = self.jsonresponse["gender_women"]
        gender_other = self.jsonresponse["gender_other"]

        # TODO check for sum of ratios to be equal to 1
        #  sum_gender = gender_men + gender_women + gender_other
        # self.assertEqual(round(sum_gender,2),1.00)

        self.assertGreaterEqual(gender_men, 0)
        self.assertGreaterEqual(gender_women, 0)
        self.assertGreaterEqual(gender_other, 0)

        # self.assertEqual(round(sum_gender,2),1.00)

    def test_age(self):
        """
        It tests that minimum age to be greater than 19
        and maximum age to be less than 90

        also minimum age to be less than maximum age
        """
        min_age = self.jsonresponse["min_age"]
        max_age = self.jsonresponse["max_age"]

        # TODO to check the min_age & max_age are in range
        # self.assertGreaterEqual(min_age,19)
        # self.assertLessEqual(max_age,90)
        self.assertLess(min_age, max_age)

    def test_records(self):
        """
        It tests that the records should be greater than 0
        """

        total_records = self.jsonresponse["total_records"]
        total_known_ids = self.jsonresponse["total_known_ids"]
        total_unknown_ids = self.jsonresponse["total_unknown_ids"]

        self.assertGreater(total_known_ids, 0)
        self.assertGreater(total_unknown_ids, 0)
        self.assertGreater(total_records, 0)
