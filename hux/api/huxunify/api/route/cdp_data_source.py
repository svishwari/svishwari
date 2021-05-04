# pylint: disable=no-self-use
"""
Paths for the cdp data sources API
"""
import logging
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from connexion.exceptions import ProblemException
from flask import Blueprint, request
from flask_apispec import marshal_with
from flasgger import SwaggerView
from pymongo import MongoClient

from huxunify.api.schema.cdp_data_source import CdpDataSourceSchema
from huxunifylib.database import constants as db_constants
from huxunifylib.database.cdp_data_source_management import (
    get_all_data_sources,
    get_data_source,
    create_data_source,
    delete_data_source
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import add_view_to_blueprint
from huxunify.api.schema.user import UserSchema
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c

CDP_DATA_SOURCES_TAG = "cdp data sources"
CDP_DATA_SOURCES_DESCRIPTION = "CDP DATA SOURCES API"
CDP_DATA_SOURCES_ENDPOINT = "cdp_data_source"

# setup cdp data sources endpoint
cdp_data_sources_bp = Blueprint(CDP_DATA_SOURCES_ENDPOINT, import_name=__name__)


def get_db_client() -> MongoClient:
    """Get DB client.
    Returns:
        MongoClient: DB client
    """
    # TODO - hook-up when ORCH-94 HUS-262 are completed
    return MongoClient()


@add_view_to_blueprint(cdp_data_sources_bp, f"/{CDP_DATA_SOURCES_ENDPOINT}", "DataSourceSearch")
class DataSourceSearch(SwaggerView):
    """
    Data Source Search class
    """

    parameters = []
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of cdp data sources.",
            "schema": {"type": "array", "items": CdpDataSourceSchema}
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [CDP_DATA_SOURCES_TAG]

    @marshal_with(CdpDataSourceSchema(many=True))
    def get(self) -> Tuple[list, int]:
        """Retrieves all data sources

        ---

        Returns:
            Tuple[list, int] list of cdp data sources and http code

        """

        try:
            return get_all_data_sources(get_db_client()), HTTPStatus.OK.value

        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail="Unable to get cdp data sources.",
            ) from exc


@add_view_to_blueprint(cdp_data_sources_bp, f"/{CDP_DATA_SOURCES_ENDPOINT}/<id>", "IndividualDataSourceSearch")
class IndividualDataSourceSearch(SwaggerView):
    """
    Individual cdp data source search class
    """

    parameters = [
        {
            "name": db_constants.CDP_DATA_SOURCE_ID,
            "description": "Cdp Data Source ID.",
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
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [CDP_DATA_SOURCES_TAG]

    @marshal_with(CdpDataSourceSchema)
    def get(self, data_source_id: str):
        """Retrieves a cdp data source by id

        ---
        Args:
            data_source_id (str): id of cdp data source

        Returns:
            Tuple[dict, int]: dict of data source and http code

        """

        if ObjectId.is_valid(data_source_id):
            data_source_id = ObjectId(data_source_id)
        else:
            return {
                       "message": f"Invalid cdp data source ID received {data_source_id}."
                   }, HTTPStatus.BAD_REQUEST

        try:
            return get_data_source(get_db_client(), data_source_id=data_source_id)
        except Exception as exc:

            logging.error(
                "%s: %s.",
                exc.__class__,
                exc,
            )

            raise ProblemException(
                status=HTTPStatus.BAD_REQUEST.value,
                title=HTTPStatus.BAD_REQUEST.description,
                detail=f"Unable to get cdp data source with ID {data_source_id}.",
            ) from exc


@add_view_to_blueprint(cdp_data_sources_bp, f"/{CDP_DATA_SOURCES_ENDPOINT}", "CreateCdpDataSource")
class CreateCdpDataSource(SwaggerView):
    """
    Create new cdp data source class
    """

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": api_c.CDP_DATA_SOURCE_DESCRIPTION,
            "example": {
                api_c.CDP_DATA_SOURCE_NAME: "Facebook",
                api_c.CDP_DATA_SOURCE_CATEGORY: "Web Events"
            },
            api_c.CDP_DATA_SOURCE_NAME: api_c.CDP_DATA_SOURCE_NAME_DESCRIPTION,
            api_c.CDP_DATA_SOURCE_CATEGORY: api_c.CDP_DATA_SOURCE_CATEGORY_DESCRIPTION
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of cdp data sources.",
            "schema": CdpDataSourceSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create cdp data source",
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [CDP_DATA_SOURCES_TAG]

    def post(self) -> Tuple[dict, int]:
        """Create a new Cdp Data Source

        ---
        Returns:
            Tuple[dict, int]: Cdp Data source dict, http code

        """

        request_data = request.get_json()
        data_source_name = request_data[api_c.CDP_DATA_SOURCE_NAME]
        data_source_category = request_data[api_c.CDP_DATA_SOURCE_CATEGORY]

        if data_source_name is None or data_source_category is None:
            return {
                "message": f"Did not receive data source name or data source category"
                }, HTTPStatus.BAD_REQUEST

        response = create_data_source(get_db_client(), name=data_source_name, category=data_source_category)

        return response, HTTPStatus.OK


@add_view_to_blueprint(cdp_data_sources_bp, f"{CDP_DATA_SOURCES_ENDPOINT}/<id>", "DeleteCdpDataSource")
class DeleteCdpDataSource(SwaggerView):
    """
    Delete cdp data source class
    """

    parameters = [
        {
            "name": db_constants.CDP_DATA_SOURCE_ID,
            "description": "Cdp Data Source ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Delete single cdp data source.",
            "schema": CdpDataSourceSchema,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [CDP_DATA_SOURCES_TAG]

    def delete(self, data_source_id: str) -> Tuple[dict, int]:
        """Delete a cdp data source

        ---
        Args:
            data_source_id (str): cdp data source id

        Returns:
            Tuple[dict, int]: cdp data source dict, http code
        """

        if ObjectId.is_valid(data_source_id):
            data_source_id = ObjectId(data_source_id)
        else:
            return {
                       "message": f"Invalid cdp data source ID received {data_source_id}."
                   }, HTTPStatus.BAD_REQUEST

        success_flag = delete_data_source(get_db_client(), data_source_id)

        if success_flag:
            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK
        else:
            return {"message": api_c.OPERATION_FAILED}, HTTPStatus.INTERNAL_SERVER_ERROR
