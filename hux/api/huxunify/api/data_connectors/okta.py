"""
Purpose of this file is for holding methods to query and pull data from OKTA.
"""
from typing import Tuple

import requests
from flask import request

from huxunify.api.config import get_config
from huxunify.api import constants as api_c


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
        return response.status_code, "OKTA available."

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        return False, getattr(exception, "message", repr(exception))


def introspect_token(access_token: str) -> dict:
    """Calls Okta's introspect endpoint and returns the token's payload when
    the token is valid and active.
    Args:
        access_token (str): The encoded JWT access token, provided by Okta.
    Returns:
        payload (dict): The decoded payload data from the Okta access token.
    """

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

    return requests.get(
        url=f"{get_config().OKTA_ISSUER}" f"/oauth2/v1/userinfo",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    ).json()


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
        # no authorization header, return a generic 401.
        return api_c.INVALID_AUTH_HEADER, 401

    # split the header
    parts = auth_header.split()
    if parts[0] != "Bearer" or len(parts) != 2:
        # user submitted an invalid authorization header.
        # return a generic 401
        return api_c.INVALID_AUTH_HEADER, 401

    return parts[1], 200
