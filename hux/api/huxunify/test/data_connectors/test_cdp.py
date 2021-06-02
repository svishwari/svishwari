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
                api_c.MOCK_CUSTOMER_PROFILE_RESPONSE, default=json_util.default
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
