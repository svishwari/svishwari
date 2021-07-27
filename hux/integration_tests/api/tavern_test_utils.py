"""
purpose of this file is to house external function utilities needed for tavern integration tests
"""
from box import Box

# TODO: Check to see if there is a way to pass in other arguments
# along with response for better modular functions
# It doesn't look like it is currently supported as called out in
# the "Note" section of the official documentation at
# https://tavern.readthedocs.io/en/latest/basics.html?highlight=calling%20external#using-external-functions-for-other-things
def get_facebook_destination_id(response):
    """
    Purpose of this function is to get the facebook destination id,
    from the response object and return it wrapped in a Box object
    Args:
        response: response object

    Returns:
        Box(ObjectId): destination_id of destination type facebook
    """
    for json in response.json():
        if json["type"] == "facebook":
            return Box({"facebook_destination_id": json["id"]})
    return None


def get_sfmc_destination_id(response):
    """
    Purpose of this function is to get the sfmc destination id,
    from the response object and return it wrapped in a Box object
    Args:
        response: response object

    Returns:
        Box(ObjectId): destination_id of destination type sfmc
    """
    for json in response.json():
        if json["type"] == "sfmc":
            return Box({"sfmc_destination_id": json["id"]})
    return None
