# pylint: disable=no-self-use
"""Paths for Configurations API"""
from http import HTTPStatus
from typing import Tuple, List
from flask import Blueprint, jsonify, request
from flasgger import SwaggerView

from huxunifylib.database import (
    constants as db_c,
    collection_management,
)
from huxunify.api.schema.configurations import (
    ConfigurationsSchema,
)
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
)
from huxunify.api.route.utils import get_db_client
from huxunify.api import constants as api_c

from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
    FAILED_DEPENDENCY_424_RESPONSE,
)

# setup the configurations blueprint
configurations_bp = Blueprint(
    api_c.CONFIGURATIONS_ENDPOINT, import_name=__name__
)


@configurations_bp.before_request
@secured()
def before_request():
    """Protect all of the configurations endpoints."""

    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    configurations_bp, f"/{api_c.CONFIGURATIONS_ENDPOINT}", "ConfigurationsSearch"
)
class ConfigurationsSearch(SwaggerView):
    """Configurations search class."""

    parameters = [
        {
            "name": api_c.STATUS,
            "in": "query",
            "type": "array",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "description": "Model status.",
            "example": "Requested",
            "required": False,
        }
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "List of configurations.",
            "schema": {"type": "array", "items": ConfigurationsSchema},
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CONFIGURATIONS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self) -> Tuple[List[dict], int]:
        """Retrieves all configurations.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[List[dict], int]: list containing dict of configurations,
                HTTP status code.
        """

        status = request.args.getlist(api_c.STATUS)
        config_models = collection_management.get_documents(
            get_db_client(),
            db_c.CONFIGURATIONS_COLLECTION,
            query_filter={db_c.STATUS: {"$in": status}} if status else {},
        )

        return (
            jsonify(
                ConfigurationsSchema(many=True).dump(config_models[db_c.DOCUMENTS])
            ),
            HTTPStatus.OK.value,
        )
