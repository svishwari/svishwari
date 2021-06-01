"""
purpose of this file is to house all the cdp tests.
"""
import json
from unittest import TestCase
import requests_mock
from bson import json_util
from requests_mock import Mocker

from huxunify.api.config import get_config
from huxunify.api.data_connectors import cdp
from huxunify.api import constants as api_c

MOCK_CUSTOMER_PROFILE_RESPONSE = {
    "id": "1531-2039-22",
    "first_name": "Bertie",
    "last_name": "Fox",
    "match_confidence": 0.96666666661,
    "since": "2020-02-20T20:02:02.202000Z",
    "ltv_actual": 60.22,
    "ltv_predicted": 59.55,
    "conversion_time": "2020-02-20T20:02:02.202000Z",
    "churn_rate": 5,
    "last_click": "2020-02-20T20:02:02.202000Z",
    "last_purchase": "2020-02-20T20:02:02.202000Z",
    "last_email_open": "2020-02-20T20:02:02.202000Z",
    "email": "bertiefox@mail.com",
    "phone": "(555)555-1231",
    "age": 53,
    "gender": "Female",
    "address": "4364 Pursglove Court",
    "city": "Dayton",
    "state": "Ohio",
    "zip": "45402-1317",
    "preference_email": False,
    "preference_push": False,
    "preference_sms": False,
    "preference_in_app": False,
    "identity_resolution": {
        "name": {
            "percentage": "0.26",
            "data_sources": [
                {
                    "id": "585t749997acad4bac4373b",
                    "name": "Adobe Experience",
                    "type": "adobe-experience",
                    "percentage": 0.49,
                },
                {
                    "id": "685t749997acad4bac4373b",
                    "name": "Google Analytics",
                    "type": "google-analytics",
                    "percentage": 0.51,
                },
            ],
        },
        "address": {"percentage": 0.2, "data_sources": []},
        "email": {"percentage": 0.34, "data_sources": []},
        "phone": {"percentage": 0.1, "data_sources": []},
        "cookie": {"percentage": 0.1, "data_sources": []},
    },
    "propensity_to_unsubscribe": 1,
    "propensity_to_purchase": 0,
}


class CDPTest(TestCase):
    """
    Test CDP request methods
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.config = get_config()

    @requests_mock.Mocker()
    def test_get_customer_profiles(self, request_mocker: Mocker):
        """Test get customer profiles

        Args:
            request_mocker (str): Request mock object.

        Returns:

        """

        request_mocker.get(
            f"{self.config.CDP_SERVICE}/5f5f7262997acad4bac4373b",
            text=json.dumps(
                MOCK_CUSTOMER_PROFILE_RESPONSE, default=json_util.default
            ),
            headers=self.config.CDP_HEADERS,
        )

        profile = cdp.get_customer_profile(
            customer_id="5f5f7262997acad4bac4373b"
        )

        self.assertEqual(request_mocker.call_count, 1)
        self.assertTrue(request_mocker.called)

        self.assertEqual(profile[api_c.FIRST_NAME], "Bertie")
        self.assertEqual(profile[api_c.LAST_NAME], "Fox")
