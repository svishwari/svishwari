"""Purpose of this file is to house schemas related to Open API Spec"""

from flask_marshmallow import Schema
from marshmallow.fields import Str, Dict, Nested, List


class InfoSchema(Schema):
    """API Spec's Info Schema"""

    version = Str()
    title = Str()
    description = Str()
    termsOfService = Str()


class ApiSpecSchema(Schema):
    """Api Spec Schema"""

    info = Nested(InfoSchema())
    paths = Dict()
    definitions = Dict()
    swagger = Str()
    schemes = List(Str)
    securityDefinitions = Dict()
