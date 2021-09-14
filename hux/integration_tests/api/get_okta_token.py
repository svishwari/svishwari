"""
Purpose of this file is for getting an okta access token.
https://developer.okta.com/docs/reference/api/authn/
"""
import re
import json
import urllib
from argparse import ArgumentParser
from getpass import getpass

import requests
import pyperclip


class PasswordType:
    """
    Class for handling the password type in argparse.
    """

    DEFAULT = "Prompt if not specified"

    def __init__(self, value: str):
        """init class method.

        Args:
            value (str): argparse password value.

        Returns:

        """
        if value == self.DEFAULT:
            value = getpass("Okta Password: ")
        self.value = value

    def __str__(self):
        """Get string value of password."""
        return self.value


class OktaOIDC:
    """
    purpose of this class is for housing okta OIDC workflows.
    """

    HEADERS = {
        "content-type": "application/json",
    }
    TOKEN_REGEX = r"access_token=(.*)&token_type"

    def __init__(
        self,
        org_url: str,
        user: str,
        pw: str,
        client_id: str,
        scopes: str,
        redirect_uri: str,
    ):
        """Class init

        Args:
            org_url (str): organization okta url.
            user (str): okta username.
            pw (str): okta username password.
            client_id (str): client id for okta.
            scopes (str): user auth scopes.
            redirect_uri (str): redirect uri after auth.

        Returns:

        """
        self.org_url = org_url
        self.user = user
        self.password = pw
        self.client_id = client_id
        self.scopes = scopes
        self.redirect_uri = redirect_uri
        self._session_token = self.get_session_token()

    def get_session_token(self) -> str:
        """Get the session token.

        Args:

        Returns:
            str: session token from request.
        """

        # call the auth url to get the session token.
        response = requests.post(
            f"{self.org_url}/api/v1/authn",
            headers=self.HEADERS,
            data=json.dumps(
                {
                    "username": self.user,
                    "password": str(self.password),
                    "options": {
                        "warnBeforePasswordExpired": True,
                        "multiOptionalFactorEnroll": False,
                    },
                }
            ),
        )
        response.raise_for_status()
        return response.json().get("sessionToken")

    def get_access_token(self, copy_to_clipboard: bool = True) -> str:
        """Get the access token.

        Args:
            copy_to_clipboard (bool): copy token to clipboard.

        Returns:
            str: session token from request.
        """

        # build the authorize url.
        authorize_url = (
            f"{self.org_url}/oauth2/v1/authorize?sessionToken={self._session_token}"
            f"&client_id={self.client_id}&scope={self.scopes}&response_type=token&"
            f"response_mode=fragment&nonce=staticNonce&redirect_uri={self.redirect_uri}"
            f"&state=staticState"
        )

        # grab the authorize url via get.
        req = urllib.request.Request(authorize_url)

        # open the url, and force the redirect.
        with urllib.request.urlopen(req) as redirect:
            # grab the token using a regex
            matches = re.findall(self.TOKEN_REGEX, str(redirect.geturl()))
            token = matches[0] if matches else 0

            if copy_to_clipboard:
                pyperclip.copy(token)
            return token


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "-orgUrl",
        help="Example - https://your-domain.okta.com or https://your-domain.oktapreview.com",
        required=True,
        default="https://example.okta.com",
    )

    parser.add_argument(
        "-user",
        help="Okta UserName: user@example.com",
        required=True,
        default="user@example.com",
    )

    parser.add_argument(
        "-pw",
        help="Okta Password: fake-pw",
        required=True,
        type=PasswordType,
        default="",
    )

    parser.add_argument(
        "-clientId",
        help="Okta Open ID Connect Client Id",
        required=True,
        default=":clientId",
    )

    parser.add_argument(
        "-scopes",
        help="Scopes separated with + e.g. openid+profile+email",
        required=False,
        default="openid+profile+email",
    )

    parser.add_argument(
        "-redirectUri",
        help="Redirect Uri registered in OIDC client in Okta",
        required=True,
        default="https://www.google.com/",
    )

    arguments = parser.parse_args()

    # setup the oidc class.
    okta_oidc = OktaOIDC(
        arguments.orgUrl,
        arguments.user,
        arguments.pw,
        arguments.clientId,
        arguments.scopes,
        arguments.redirectUri,
    )
    print(okta_oidc.get_access_token())
