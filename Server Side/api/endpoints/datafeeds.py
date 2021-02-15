"""API endpoints for datafeeds"""
from . import database

def search():
    """Endpoint returning a list of datafeeds.

    Returns:
        datafeeds (Response): List of datafeeds.
    """
    datafeeds = database.read_data_feed_catalog()

    return datafeeds, 200


def get(feed_id: int):
    """Endpoint returning a datafeed by ID.

    Returns:
        datafeed (Response): Return a datafeed by ID.
    """
    datafeed = database.read_data_feed_catalog_by_id(feed_id)

    if not datafeed:
        return "Data feed not found", 404

    return datafeed, 200


def post():
    raise NotImplementedError


def put(feed_id: int):
    raise NotImplementedError


def delete(feed_id: int):
    raise NotImplementedError

