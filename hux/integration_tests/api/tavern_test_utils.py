"""Purpose of this file is to house external function utilities needed for
tavern integration tests
"""
from typing import Union
from box import Box


def get_destination_id(response: object, **kwargs: dict) -> Union[Box, None]:
    """Purpose of this function is to get the destination id from the response
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
    """Purpose of this function is to get the audience id from the response
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


def get_engagement_audience_destination_id(
    response: object,
) -> Union[Box, None]:
    """Purpose of this function is to get the engagement id from the get
    engagements response object and the corresponding audience_id and
    destination_id that are nested within the response and return it
    wrapped in a Box object.

    Args:
        response (object): response object.

    Returns:
        Box: engagement_id, and corresponding audience_id, destination_id.
    """

    for json in response.json():
        for audience in json["audiences"]:
            for destination in audience["destinations"]:
                return Box(
                    {
                        "engagement_id": json["id"],
                        "engagement_audience_id": audience["id"],
                        "engagement_destination_id": destination["id"],
                    }
                )
    return None


def get_campaign_engagement_audience_destiantion_id(
    response: object,
) -> Union[Box, None]:
    """Purpose of this function is to get the engagement id from the get
    engagements response object and the corresponding audience_id and
    destination_id that are nested within the response and return it
    wrapped in a Box object with facebook destination.

    Args:
        response (object): response object.

    Returns:
        Box: engagement_id, and corresponding audience_id, destination_id.
    """

    for json in response.json():
        for audience in json["audiences"]:
            for destination in audience["destinations"]:
                if destination["name"] == "Facebook":
                    return Box(
                        {
                            "engagement_id": json["id"],
                            "engagement_audience_id": audience["id"],
                            "engagement_destination_id": destination["id"],
                        }
                    )
    return None


def get_campaign_mapping_details(response: object) -> Union[Box, None]:
    """Purpose of this function is to get the campaign and delivery_job for
    updating campaigns and return it wrapped in a Box object

    Args:
        response (object): response object

    Returns:
        Box: campaign, delivery_job
    """

    for json in response.json():
        return Box(
            {
                "campaign": json["campaigns"][0],
                "delivery_job": json["delivery_jobs"][0],
            }
        )


def get_destination_by_name(
    response: object, **kwargs: dict
) -> Union[Box, None]:
    """Purpose of this function is to get the specifically
    requested data source by name.

    Args:
        response (object): response object
        **kwargs (dict): function keyword arguments.

    Returns:
        Box: destination
    """

    destination_name = kwargs.get("destination_name", None)

    for destination in response.json():
        if destination["name"] == destination_name:
            return Box({"destination": destination})
    return None
