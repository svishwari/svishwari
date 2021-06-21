# pylint: disable=no-self-use
"""
Paths for the CDP data sources API
"""
import logging
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from connexion.exceptions import ProblemException
from flask import Blueprint, request, jsonify
from flasgger import SwaggerView
from marshmallow import ValidationError


from huxunifylib.database import constants as db_constants
from huxunifylib.database.cdp_data_source_management import (
    get_all_data_sources,
    get_data_source,
    create_data_source,
    delete_data_source,
    update_data_sources,
)
from huxunify.api.schema.cdp_data_source import (
    CdpDataSourceSchema,
    CdpDataSourcePostSchema,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import (
    add_view_to_blueprint,
    get_db_client,
    secured,
)
from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api import constants as api_c


# setup CDP data sources endpoint
cdp_data_sources_bp = Blueprint(
    api_c.CDP_DATA_SOURCES_ENDPOINT, import_name=__name__, url_prefix="/cdp"
)


@cdp_data_sources_bp.before_request
@secured()
def before_request():
    """Protect all of the data source endpoints."""
    pass  # pylint: disable=unnecessary-pass


@add_view_to_blueprint(
    cdp_data_sources_bp, api_c.CDP_DATA_SOURCES_ENDPOINT, "DataSourceSearch"
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
    tags = [api_c.CDP_DATA_SOURCES_TAG]

    def get(self) -> Tuple[list, int]:
        """Retrieves all CDP data sources.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int] list of CDP data sources and http code

        """

        try:
            data_sources = get_all_data_sources(get_db_client())
            return (
                jsonify(CdpDataSourceSchema().dump(data_sources, many=True)),
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
    f"{api_c.CDP_DATA_SOURCES_ENDPOINT}/<{db_constants.CDP_DATA_SOURCE_ID}>",
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
    tags = [api_c.CDP_DATA_SOURCES_TAG]

    def get(self, data_source_id: str):
        """Retrieves a CDP data source.

        ---
        security:
            - Bearer: ["Authorization"]

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
                CdpDataSourceSchema().dump(data_source),
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
    cdp_data_sources_bp, api_c.CDP_DATA_SOURCES_ENDPOINT, "CreateCdpDataSource"
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
            "schema": CdpDataSourceSchema,
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create CDP data source",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CDP_DATA_SOURCES_TAG]

    def post(self) -> Tuple[str, int]:
        """Creates a new CDP data source.

        ---
        security:
            - Bearer: ["Authorization"]

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

        return CdpDataSourceSchema().dump(response), HTTPStatus.OK


@add_view_to_blueprint(
    cdp_data_sources_bp,
    f"{api_c.CDP_DATA_SOURCES_ENDPOINT}/<data_source_id>",
    "DeleteCdpDataSource",
)
class DeleteCdpDataSource(SwaggerView):
    """
    Deletes a CDP data source
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
            "description": "Deletes a CDP data source.",
            "schema": CdpDataSourceSchema,
        },
        HTTPStatus.NOT_FOUND.value: {"schema": NotFoundError},
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CDP_DATA_SOURCES_TAG]

    def delete(self, data_source_id: str) -> Tuple[dict, int]:
        """Deletes a CDP data source.

        ---
        security:
            - Bearer: ["Authorization"]

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


@add_view_to_blueprint(
    cdp_data_sources_bp,
    f"{api_c.CDP_DATA_SOURCES_ENDPOINT}",
    "BatchUpdateDataSources",
)
class BatchUpdateDataSources(SwaggerView):
    """
    Class to partially batch update data sources
    """

    parameters = [
        {
            "name": api_c.BODY,
            "in": api_c.BODY,
            "type": "object",
            "description": "Input Batch data source body.",
            "example": {
                api_c.CDP_DATA_SOURCE_IDS: ["60ae035b6c5bf45da27f17d6"],
                api_c.BODY: {
                    api_c.IS_ADDED: True,
                    api_c.STATUS: api_c.STATUS_PENDING,
                },
            },
        },
    ]

    responses = {
        HTTPStatus.OK.value: {
            "description": "Data source(s) updated.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to update data source(s).",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CDP_DATA_SOURCES_TAG]

    def patch(self) -> Tuple[dict, int]:
        """Updates a list of data sources.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:

        Returns:
            Tuple[dict, int]: Data source updated, HTTP status code.

        """

        data = request.get_json()

        # validate fields
        if api_c.CDP_DATA_SOURCE_IDS not in data and api_c.BODY not in data:
            return (
                self.responses[HTTPStatus.BAD_REQUEST.value],
                HTTPStatus.BAD_REQUEST.value,
            )

        # validate data source ids
        data_source_ids = [
            ObjectId(x)
            for x in data[api_c.CDP_DATA_SOURCE_IDS]
            if ObjectId.is_valid(x)
        ]
        if not data_source_ids or len(data_source_ids) != len(
            data[api_c.CDP_DATA_SOURCE_IDS]
        ):
            return (
                self.responses[HTTPStatus.BAD_REQUEST.value],
                HTTPStatus.BAD_REQUEST.value,
            )

        # keep only allowed fields
        data = {
            k: v
            for k, v in data[api_c.BODY].items()
            if k in [api_c.IS_ADDED, api_c.STATUS]
        }
        if not data:
            return (
                self.responses[HTTPStatus.BAD_REQUEST.value],
                HTTPStatus.BAD_REQUEST.value,
            )

        # rename key from is_added to added for DB.
        data[db_constants.ADDED] = data.pop(api_c.IS_ADDED)

        try:
            # update the data sources.
            if update_data_sources(get_db_client(), data_source_ids, data):
                return self.responses[HTTPStatus.OK.value], HTTPStatus.OK.value

            return (
                self.responses[HTTPStatus.BAD_REQUEST.value],
                HTTPStatus.BAD_REQUEST.value,
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
