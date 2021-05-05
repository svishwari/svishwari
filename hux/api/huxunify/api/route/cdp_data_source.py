# pylint: disable=no-self-use
"""
Paths for the CDP data sources API
"""
import logging
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from connexion.exceptions import ProblemException
from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView
from marshmallow import ValidationError

from pymongo import MongoClient

from huxunifylib.database import constants as db_constants
from huxunifylib.database.cdp_data_source_management import (
    get_all_data_sources,
    get_data_source,
    create_data_source,
    delete_data_source,
)
from huxunify.api.schema.cdp_data_source import (
    CdpDataSourceSchema,
    CdpDataSourcePostSchema,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import add_view_to_blueprint
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c

CDP_DATA_SOURCES_TAG = "CDP data sources"
CDP_DATA_SOURCES_DESCRIPTION = "CDP DATA SOURCES API"
CDP_DATA_SOURCES_ENDPOINT = "cdp_data_source"

# setup CDP data sources endpoint
cdp_data_sources_bp = Blueprint(
    CDP_DATA_SOURCES_ENDPOINT, import_name=__name__
)


def get_db_client() -> MongoClient:
    """Get DB client.
    Returns:
        MongoClient: DB client
    """
    # TODO - hook-up when ORCH-94 HUS-262 are completed
    return MongoClient()


@add_view_to_blueprint(
    cdp_data_sources_bp, f"/{CDP_DATA_SOURCES_ENDPOINT}", "DataSourceSearch"
)
class DataSourceSearch(SwaggerView):
    """
    Data Source Search class
    """

    parameters = []
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of CDP data sources.",
            "schema": {"type": "array", "items": CdpDataSourceSchema},
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [CDP_DATA_SOURCES_TAG]

    @marshal_with(CdpDataSourceSchema(many=True))
    def get(self) -> Tuple[list, int]:
        """Retrieves all data sources

        ---

        Returns:
            Tuple[list, int] list of CDP data sources and http code

        """

        try:
            data_sources = get_all_data_sources(get_db_client())
            return (
                CdpDataSourceSchema().dumps(data_sources),
                HTTPStatus.OK.value,
            )

        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail="Unable to get CDP data sources.",
            ) from exc


@add_view_to_blueprint(
    cdp_data_sources_bp,
    f"/{CDP_DATA_SOURCES_ENDPOINT}/<{db_constants.CDP_DATA_SOURCE_ID}>",
    "IndividualDataSourceSearch",
)
class IndividualDataSourceSearch(SwaggerView):
    """
    Individual CDP data source search class
    """

    parameters = [
        {
            "name": db_constants.CDP_DATA_SOURCE_ID,
            "description": "CDP data source ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Retrieve single data source.",
            "schema": CdpDataSourceSchema,
        },
        HTTPStatus.NOT_FOUND.value: {"schema": NotFoundError},
    }
    responses.update(AUTH401_RESPONSE)
    tags = [CDP_DATA_SOURCES_TAG]

    @marshal_with(CdpDataSourceSchema)
    def get(self, data_source_id: str):
        """Retrieves a CDP data source by id

        ---
        Args:
            data_source_id (str): id of CDP data source

        Returns:
            Tuple[dict, int]: dict of data source and http code

        """

        if ObjectId.is_valid(data_source_id):
            data_source_id = ObjectId(data_source_id)
        else:
            return {
                "message": f"Invalid CDP data source ID received {data_source_id}."
            }, HTTPStatus.BAD_REQUEST

        try:
            data_source = get_data_source(
                get_db_client(), data_source_id=data_source_id
            )
            return (
                CdpDataSourceSchema().dumps(data_source),
                HTTPStatus.OK.value,
            )
        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail=f"Unable to get CDP data source with ID {data_source_id}.",
            ) from exc


@add_view_to_blueprint(
    cdp_data_sources_bp, f"/{CDP_DATA_SOURCES_ENDPOINT}", "CreateCdpDataSource"
)
class CreateCdpDataSource(SwaggerView):
    """
    Create new CDP data source class
    """

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": api_c.CDP_DATA_SOURCE_DESCRIPTION,
            "example": {
                api_c.CDP_DATA_SOURCE_NAME: "Facebook",
                api_c.CDP_DATA_SOURCE_CATEGORY: "Web Events",
            },
            api_c.CDP_DATA_SOURCE_NAME: api_c.CDP_DATA_SOURCE_NAME_DESCRIPTION,
            api_c.CDP_DATA_SOURCE_CATEGORY: api_c.CDP_DATA_SOURCE_CATEGORY_DESCRIPTION,
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "CDP data source created.",
            "schema": CdpDataSourceSchema
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create CDP data source",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [CDP_DATA_SOURCES_TAG]

    def post(self) -> Tuple[str, int]:
        """Create a new CDP Data Source

        ---
        Returns:
            Tuple[str, int]: ID of CDP Data source, http code

        """
        try:
            body = CdpDataSourcePostSchema().load(request.get_json())
        except ValidationError as validation_error:
            return validation_error.messages, HTTPStatus.BAD_REQUEST

        response = create_data_source(
            get_db_client(),
            name=body[api_c.CDP_DATA_SOURCE_NAME],
            category=body[api_c.CDP_DATA_SOURCE_CATEGORY],
        )

        return CdpDataSourceSchema().dumps(response), HTTPStatus.OK


@add_view_to_blueprint(
    cdp_data_sources_bp,
    f"{CDP_DATA_SOURCES_ENDPOINT}/<data_source_id>",
    "DeleteCdpDataSource",
)
class DeleteCdpDataSource(SwaggerView):
    """
    Delete CDP data source class
    """

    parameters = [
        {
            "name": db_constants.CDP_DATA_SOURCE_ID,
            "description": "CDP Data Source ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Delete single CDP data source.",
            "schema": CdpDataSourceSchema,
        },
        HTTPStatus.NOT_FOUND.value: {"schema": NotFoundError},
    }
    responses.update(AUTH401_RESPONSE)
    tags = [CDP_DATA_SOURCES_TAG]

    def delete(self, data_source_id: str) -> Tuple[dict, int]:
        """Delete a CDP data source

        ---
        Args:
            data_source_id (str): CDP data source id

        Returns:
            Tuple[dict, int]: CDP data source dict, http code
        """

        if ObjectId.is_valid(data_source_id):
            data_source_id = ObjectId(data_source_id)
        else:
            return {
                "message": f"Invalid CDP data source ID received {data_source_id}."
            }, HTTPStatus.BAD_REQUEST

        success_flag = delete_data_source(get_db_client(), data_source_id)

        if success_flag:
            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK

        return {
            "message": api_c.OPERATION_FAILED
        }, HTTPStatus.INTERNAL_SERVER_ERROR
