"""
Paths for the User API
"""

from http import HTTPStatus
from typing import List, Tuple
from flask import Blueprint
from marshmallow.exceptions import ValidationError
from flask_apispec import marshal_with
from flasgger import SwaggerView
from huxunify.api.model.cdm import CdmModel
from huxunify.api.schema.errors import NotFoundError, RequestError
from huxunify.api.schema.cdm import Datafeed, Fieldmapping, ProcessedData
from huxunify.api.route.utils import add_view_to_blueprint

USER_TAG = "user"
USER_DESCRIPTION = "USER API"
USER_TAG = "user"
USER_ENDPOINT = "user"
DATAFEEDS_TAG = "datafeeds"
DATAFEEDS_ENDPOINT = "datafeeds"
FIELDMAPPINGS_TAG = "fieldmappings"
FIELDMAPPINGS_ENDPOINT = "fieldmappings"
PROCESSED_ITEMS_TAG = "processeditems"
PROCESSED_ITEMS_ENDPOINT = "processeditems"

# setup the cdm blueprint
user_bp = Blueprint("user", import_name=__name__)


@add_view_to_blueprint(user_bp, f"/{USER_ENDPOINT}", "UserSearch")
class UserSearch(SwaggerView):
    """
    User Search Class
    """

    parameters = []
    responses = {
        HTTPStatus.OK.value: { "description": "List of users.", "schema": int } # TODO create User Schema!
    }
    tags = [USER_TAG]
