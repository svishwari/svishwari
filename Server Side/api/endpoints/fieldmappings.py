"""API endpoints for fieldmappings"""
from . import database


def search() -> list:
    """Endpoint returning a list of fieldmappings.

    Returns:
        fieldmappings (Response): List of fieldmappings.
    """
    fieldmappings = database.read_fieldmappings()

    return fieldmappings, 200


def post():
    raise NotImplementedError


def get(id:int):
    fieldmapping = database.read_fieldmapping_by_id(id)

    return fieldmapping, 200


def put(id:int):
    raise NotImplementedError
