"""
Purpose of this file is for holding methods to query and pull data from CDP.
"""

from huxunify.api import constants as api_c
from huxunify.api.schema.utils import redact_fields


def get_customer_profile(customer_body: dict, redact: bool = True) -> dict:
    """Retrieves a customer profile.

    Args:
        customer_body (dict): customer dict.
        redact (bool): redact fields.

    Returns:
        dict: dictionary containing the customer profile

    """
    return (
        redact_fields(customer_body, api_c.CUSTOMER_PROFILE_REDACTED_FIELDS)
        if redact
        else customer_body
    )
