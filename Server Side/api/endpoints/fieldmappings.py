"""API endpoints for fieldmappings"""


def search(feed_id: int) -> list:
    """Endpoint returning a list of fieldmappings.

    Returns:
        fieldmappings (Response): List of fieldmappings.
    """
    fieldmappings = []

    return fieldmappings, 200


def post(feed_id: int):
    raise NotImplementedError


def put(feed_id: int):
    raise NotImplementedError


def delete(feed_id: int):
    raise NotImplementedError
