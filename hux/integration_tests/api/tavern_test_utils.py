"""
purpose of this file is to house external function utilities needed for tavern integration tests
"""
from typing import Union
from box import Box


def get_destination_id(response: object, **kwargs: dict) -> Union[Box, None]:
    """
    Purpose of this function is to get the destination id from the response object based on the
    passed in destination_type key in the kwargs dict and return it wrapped in a Box object.

    Args:
        response (object): response object.
        **kwargs (dict): function keyword arguments.

    Returns:
        Box: destination_id of the requested destination type facebook.
    """

    destination_type = kwargs.get("destination_type", None)

    for json in response.json():
        if json["type"] == "facebook" and destination_type == "facebook":
            return Box({"facebook_destination_id": json["id"]})
        if json["type"] == "sfmc" and destination_type == "sfmc":
            return Box({"sfmc_destination_id": json["id"]})
    return None
