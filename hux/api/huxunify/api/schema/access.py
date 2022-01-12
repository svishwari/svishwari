"""Purpose of this file is to house schemas related to access control."""

from flask_marshmallow import Schema
from marshmallow.fields import Str
from marshmallow.validate import OneOf

from huxunify.api import constants as api_c


class ResourceAttributes(Schema):
    """Resource Attributes Schema"""

    name = Str(validate=OneOf(api_c.ALLOWED_RESOURCES_FOR_ABAC))
    owner_name = Str()
