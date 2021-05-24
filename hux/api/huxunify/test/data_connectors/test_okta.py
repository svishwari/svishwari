"""
purpose of this file is to house all the okta tests
"""
import json
import requests
from unittest import TestCase
import requests_mock
from requests_mock import Mocker
from bson import json_util
from huxunify.api import constants
from huxunify.api.config import get_config
from huxunify.api.data_connectors import tecton


class OktaTest(TestCase):
    """
    Test Okta request methods
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.config = get_config()

    # @requests_mock.Mocker()
    def test_introspection(self): #, request_mocker: Mocker):
        """Test token introspection

        Args:
            request_mocker (str): Request mock object.

        Returns:

        """

        # setup the request mock post
        # requests.post(
        #     self.config.TECTON_FEATURE_SERVICE,
        #     text=json.dumps(MOCK_MODEL_RESPONSE, default=json_util.default),
        #     headers=self.config.TECTON_API_HEADERS,
        # )

        issuer = "https://deloittedigital-ms.okta.com"
        client_id = "0oab1i3ldgYyRvk5r2p7"
        
        access_token = ""
        payload = requests.post(
            
            url=f"{issuer}/oauth2/v1/introspect?client_id={client_id}",
            data={
                constants.AUTHENTICATION_TOKEN: access_token,
                constants.AUTHENTICATION_TOKEN_TYPE_HINT: constants.AUTHENTICATION_ACCESS_TOKEN,
            },
        ).json()

        print(payload)
