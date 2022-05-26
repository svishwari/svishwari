"""Purpose of this file is for holding methods to query and pull data from
OKTA.
"""
import json
import re
import ssl
import urllib
from typing import Tuple, Union

import certifi
import requests
from flask import request
from huxunifylib.util.general.logging import logger

from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.api.prometheus import record_health_status, Connections


@record_health_status(Connections.OKTA)
def check_okta_connection() -> Tuple[bool, str]:
    """Validate the OKTA connection.
    Args:

    Returns:
        tuple[bool, str]: Returns if the connection is valid, and the message.
    """
    # get config
    config = get_config()

    # submit the get request to test if we can talk to OKTA.
    try:
        response = requests.get(
            f"{config.OKTA_ISSUER}"
            f"/oauth2/v1/keys?client_id="
            f"{config.OKTA_CLIENT_ID}"
        )

        if response.status_code == 200:
            logger.info("OKTA is available.")
            return True, "OKTA available."
        logger.error(
            "OKTA is unavailable, returned a %s response.",
            {response.status_code},
        )
        return (
            False,
            f"Received status code: {response.status_code}, "
            f"Received message: {response.json()}",
        )

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        logger.exception("OKTA Health Check failed.")
        return False, getattr(exception, "message", repr(exception))


def introspect_token(access_token: str) -> dict:
    """Calls Okta's introspect endpoint and returns the token's payload when
    the token is valid and active.
    Args:
        access_token (str): The encoded JWT access token, provided by Okta.
    Returns:
        payload (dict): The decoded payload data from the Okta access token.
    """

    logger.info("Attempting to introspect access token.")

    # get config
    config = get_config()

    payload = requests.post(
        url=f"{config.OKTA_ISSUER}"
        f"/oauth2/v1/introspect?client_id="
        f"{config.OKTA_CLIENT_ID}",
        data={
            api_c.AUTHENTICATION_TOKEN: access_token,
            api_c.AUTHENTICATION_TOKEN_TYPE_HINT: api_c.AUTHENTICATION_ACCESS_TOKEN,
        },
    ).json()

    # check if a valid token
    if "active" in payload and not payload["active"]:
        logger.warning(
            "Failure during introspection of token, not an active user."
        )
        return None

    # extract user info
    return {"user_name": payload["username"], "user_id": payload["uid"]}


def get_user_info(access_token: str) -> dict:
    """Calls Okta's user_info endpoint and returns user_info object

    Args:
        access_token (str): The encoded JWT access token, provided by Okta.

    Returns:
        payload (dict): The decoded payload user info data from Okta.
    """

    if access_token is None:
        return {}

    # replace invalid header characters
    access_token = str(access_token).replace("\r", "")

    try:
        return requests.get(
            url=f"{get_config().OKTA_ISSUER}/oauth2/v1/userinfo",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        ).json()
    except requests.exceptions.InvalidHeader:
        return {}


def get_token_from_request(flask_request: request) -> tuple:
    """Validate the OKTA connection.

    Args:
        flask_request (request): flask request.

    Returns:
        tuple[str, int]: Returns a string message or token and a response code.

    """

    # check if flask_request has headers attribute
    if not hasattr(flask_request, "headers"):
        return api_c.INVALID_AUTH_HEADER, 401

    # get the auth token
    auth_header = flask_request.headers.get("Authorization", None)
    if not auth_header:
        logger.error(
            "Auth header not obtained while trying to get token from request."
        )
        # no authorization header, return a generic 401.
        return api_c.INVALID_AUTH_HEADER, 401

    # split the header
    parts = auth_header.split()
    if parts[0] != "Bearer" or len(parts) != 2:
        logger.error(
            "Invalid auth header while trying to get token from request."
        )
        # user submitted an invalid authorization header.
        # return a generic 401
        return api_c.INVALID_AUTH_HEADER, 401

    return parts[1], 200


# pylint:disable=broad-except,too-many-locals
def get_env_okta_user_bearer_token() -> Union[str, None]:
    """Get the access bearer token of the current environment's okta user.

    Returns:
        str: access bearer token of the current environment's okta user.
    """

    try:
        # get config
        config = get_config()

        headers = {
            "content-type": "application/json",
        }
        token_regex = r"access_token=(.*)&token_type"

        okta_org_url = config.OKTA_ISSUER
        okta_client_id = config.OKTA_CLIENT_ID
        okta_redirect_uri = config.OKTA_REDIRECT_URI
        env_okta_user = config.OKTA_TEST_USER_NAME
        env_okta_user_pw = config.OKTA_TEST_USER_PW

        # call the auth url to get the session token
        response = requests.post(
            f"{okta_org_url}/api/v1/authn",
            headers=headers,
            data=json.dumps(
                {
                    "username": env_okta_user,
                    "password": str(env_okta_user_pw),
                    "options": {
                        "warnBeforePasswordExpired": True,
                        "multiOptionalFactorEnroll": False,
                    },
                }
            ),
        )
        response.raise_for_status()
        session_token = response.json().get("sessionToken")

        # build the authorize url
        authorize_url = (
            f"{okta_org_url}/oauth2/v1/authorize?sessionToken={session_token}"
            f"&client_id={okta_client_id}&scope=openid+profile+email"
            f"&response_type=token&response_mode=fragment&nonce=staticNonce"
            f"&redirect_uri={okta_redirect_uri}&state=staticState"
        )

        # grab the authorize url via get
        req = urllib.request.Request(authorize_url)

        # build a context with certificate to pass in as context argument for
        # urlopen request function below
        context = ssl.create_default_context(cafile=certifi.where())

        # open the url, and force the redirect
        with urllib.request.urlopen(req, context=context) as redirect:  # nosec
            # grab the token using a regex
            matches = re.findall(token_regex, str(redirect.geturl()))
            token = matches[0] if matches else None

            return token
    except Exception as exc:
        logger.error(
            "Failed to get env okta user access bearer token with %s.",
            repr(exc),
        )

    return None
