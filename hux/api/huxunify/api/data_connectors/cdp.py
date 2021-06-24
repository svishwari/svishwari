"""
Purpose of this file is for holding methods to query and pull data from CDP.
"""
from typing import Tuple

import requests

from huxunify.api.config import get_config
from huxunify.api import constants as api_c
from huxunify.api.schema.utils import redact_fields


def check_cdm_api_connection() -> Tuple[bool, str]:
    """Validate the cdm api connection.
    Args:

    Returns:
        tuple[bool, str]: Returns if the connection is valid, and the message.
    """
    # get config
    config = get_config()

    # submit the post request to get documentation
    try:
        response = requests.get(
            f"{config.CDP_SERVICE}/docs",
            headers=config.CDP_HEADERS,
            verify=False,
            timeout=5,
        )
        return response.status_code, "CDM available."

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        return False, getattr(exception, "message", repr(exception))


def get_customer_profile(customer_body: dict) -> dict:
    """Retrieves a customer profile.

    Args:
        customer_body (dict): customer dict.

    Returns:
        dict: dictionary containing the customer profile

    """
    # TODO: hookup in HUS-360
    return redact_fields(customer_body, api_c.CUSTOMER_PROFILE_REDACTED_FIELDS)
