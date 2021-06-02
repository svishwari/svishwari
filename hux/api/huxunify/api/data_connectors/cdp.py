"""
Purpose of this file is for holding methods to query and pull data from CDP.
"""

import requests

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.schema.utils import redact_fields


def get_customer_profile(customer_id: str) -> dict:
    """Retrieves a customer profile.

    Args:
        customer_id (str): id of the customer

    Returns:
        dict: dictionary containing the customer profile

    """

    config = get_config()

    response = requests.get(
        f"{config.CDP_SERVICE}/{customer_id}", headers=config.CDP_HEADERS
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to retrieve customer profile. "
            f"Received status code: {response.status_code}. "
            f"Received body: {response.json()}"
        )

    redacted_body = redact_fields(
        response.json(), api_c.CUSTOMER_PROFILE_REDACTED_FIELDS
    )
    return redacted_body
