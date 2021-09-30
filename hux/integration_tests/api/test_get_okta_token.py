"""
Purpose of this file is to house the get okta token test.
"""
from unittest import TestCase

import requests_mock

from get_okta_token import PasswordType, OktaOIDC


class TestOktaTokenGet(TestCase):
    """
    Test OKTA token get.
    """

    def test_password_type_cls(self) -> None:
        """
        Test the password type class.

        Returns:

        """

        self.assertEqual(PasswordType("empty").value, "empty")

    @requests_mock.Mocker()
    def test_okta_oidc_setup(
        self, request_mocker: requests_mock.Mocker
    ) -> None:
        """
        Test the password type class.

        Args:
            request_mocker (Mocker): Request mock object.

        Returns:

        """

        # setup the request mock post
        request_mocker.post(
            "https://fake.com/api/v1/authn", json={"sessionToken": "fake"}
        )

        # setup the oidc class.
        okta_oidc = OktaOIDC(
            "https://fake.com",
            "test_user",
            "test_pw",
            "test_clientId",
            "test_scopes",
            "test_redirect",
        )
        self.assertEqual(okta_oidc.get_session_token(), "fake")
