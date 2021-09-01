"""
Purpose of this file is for holding methods to query and pull data from CDP Connections.
"""
from typing import Tuple, Union

import requests

from huxunifylib.util.general.logging import logger

from huxunify.api.config import get_config


def check_cdp_connections_api_connection() -> Tuple[Union[int, bool], str]:
    """Validate the cdp connections api connection.
    Args:

    Returns:
        tuple[Union[int,bool], str]: Returns if the connection is valid, and the message.
    """
    # get config
    config = get_config()

    # submit the post request to get documentation
    try:
        response = requests.get(
            f"{config.CDP_CONNECTION_SERVICE}/healthcheck",
            timeout=5,
        )
        return response.status_code, "CDP connections available."

    except Exception as exception:  # pylint: disable=broad-except
        # report the generic error message
        logger.error(
            "CDP Connections Health Check failed with %s.", repr(exception)
        )
        return response.status_code, getattr(
            exception, "message", repr(exception)
        )
