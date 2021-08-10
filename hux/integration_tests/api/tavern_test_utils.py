"""
Purpose of this file is to house external function utilities needed for
tavern integration tests
"""
from typing import Union
from box import Box


# TODO: Change the constants like "sfmc", "facebook" in this method by
# importing and referencing if from huxunifylib.database.constants
def get_destination_id(response: object, **kwargs: dict) -> Union[Box, None]:
    """
    Purpose of this function is to get the destination id from the response
    object based on the passed in destination_type key in the kwargs dict
    and return it wrapped in a Box object.

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


def get_audience_id(response: object) -> Union[Box, None]:
    """
    Purpose of this function is to get the audience id from the response
    object with some destinations as well and take one destination_id as well.

    Args:
        response (object): response object.

    Returns:
        Box: engagement_audience_id and engagement_destination_id.
    """
    for json in response.json():
        if len(json["destinations"]) > 0:
            return Box(
                {
                    "engagement_audience_id": json["id"],
                    "engagement_destination_id": json["destinations"][0]["id"],
                }
            )
    return None
