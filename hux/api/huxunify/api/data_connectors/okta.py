"""
Purpose of this file is for holding methods to query and pull data from OKTA.
"""
from typing import Tuple

import requests

from huxunify.api.config import get_config
from huxunify.api import constants


def check_okta_connection() -> Tuple[bool, str]:
    """Validate the OKTA connection.
    Args:

    Returns:
        tuple[bool, str]: Returns if the connection is valid, and the message.
    """
    # get config
    config = get_config()

    # submit the post request to get models
    try:
        response = requests.get(
            f"{config.OKTA_ISSUER}/oauth2/v1/keys?client_id={config.OKTA_CLIENT_ID}"
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
        url=f"{config.OKTA_ISSUER}/oauth2/v1/introspect?client_id={config.OKTA_CLIENT_ID}",
        data={
            constants.AUTHENTICATION_TOKEN: access_token,
            constants.AUTHENTICATION_TOKEN_TYPE_HINT: constants.AUTHENTICATION_ACCESS_TOKEN,
        },
    ).json()

    print(payload)

    # check if a valid token
    if "active" in payload and not payload["active"]:
        return None

    # extract user info
    return {"user_name": payload["username"], "user_id": payload["uid"]}
