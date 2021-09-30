"""Schemas for API error responses"""

from http import HTTPStatus
from flask_marshmallow import Schema
from marshmallow.fields import Dict, Int, Str


class Error(Schema):
    """General schema for errors"""

    code = Int(required=True)
    message = Str(required=True)


class NotFoundError(Error):
    """The specified resource was not found"""

    code = Int(default=HTTPStatus.NOT_FOUND.value)
    message = Str(default=HTTPStatus.NOT_FOUND.description)


class RequestError(Error):
    """Incorrect request syntax or unsupported method"""

    code = Int(default=HTTPStatus.BAD_REQUEST.value)
    message = Str(default=HTTPStatus.BAD_REQUEST.description)
    errors = Dict()
