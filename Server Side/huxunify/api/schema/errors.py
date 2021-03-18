"""
Schemas for API error responses
"""

from http import HTTPStatus
from flask_marshmallow import Schema
from marshmallow.fields import Int, Str


class NotFoundError(Schema):
    """The specified resource was not found"""

    code = Int(required=True, default=HTTPStatus.NOT_FOUND.value)
    message = Str(required=True, default=HTTPStatus.NOT_FOUND.description)
