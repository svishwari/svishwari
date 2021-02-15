"""API endpoints for datafeeds"""
from . import database


def search():
    """Endpoint returning a list of datafeeds.

    Returns:
        datafeeds (Response): List of datafeeds.
    """
    datafeeds = database.read_datafeeds()

    return datafeeds, 200


def get(feed_id: int):
    """Endpoint returning a datafeed by ID.

    Returns:
        datafeed (Response): Return a datafeed by ID.
    """
    datafeed = database.read_datafeed_by_id(feed_id)

    if not datafeed:
        return "Data feed not found", 404

    return datafeed, 200
