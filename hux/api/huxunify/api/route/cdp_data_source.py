# pylint: disable=no-self-use
"""Paths for the CDP data sources API"""
from http import HTTPStatus
from typing import Tuple

from bson import ObjectId
from connexion.exceptions import ProblemException
from flask import Blueprint, request, jsonify
from flasgger import SwaggerView

from huxunifylib.util.general.logging import logger

from huxunifylib.database import constants as db_c
from huxunifylib.database.cdp_data_source_management import (
    get_all_data_sources,
    get_data_source,
    delete_data_source,
    update_data_sources,
    bulk_write_data_sources,
)

from huxunify.api import constants as api_c
from huxunify.api.data_connectors.cdp_connection import (
    get_data_source_data_feeds,
)
from huxunify.api.data_connectors.okta import get_token_from_request

from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
)
from huxunify.api.route.utils import (
    get_db_client,
)

from huxunify.api.schema.cdp_data_source import (
    CdpDataSourceSchema,
    CdpDataSourcePostSchema,
    DataSourceDataFeedsGetSchema,
)
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
    FAILED_DEPENDENCY_424_RESPONSE,
)

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
    """Data Source Search class."""

    parameters = []
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of CDP data sources.",
            "schema": {"type": "array", "items": CdpDataSourceSchema},
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CDP_DATA_SOURCES_TAG]

    @api_error_handler()
    def get(self) -> Tuple[list, int]:
        """Retrieves all CDP data sources.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: list of CDP data sources, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        try:
            data_sources = get_all_data_sources(get_db_client())
            return (
                jsonify(CdpDataSourceSchema().dump(data_sources, many=True)),
                HTTPStatus.OK.value,
            )

        except Exception as exc:

            logger.error(
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
    f"{api_c.CDP_DATA_SOURCES_ENDPOINT}/<{db_c.CDP_DATA_SOURCE_ID}>",
    "IndividualDataSourceSearch",
)
class IndividualDataSourceSearch(SwaggerView):
    """Individual CDP data source search class."""

    parameters = [
        {
            "name": db_c.CDP_DATA_SOURCE_ID,
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

    @api_error_handler()
    def get(self, data_source_id: str):
        """Retrieves a CDP data source.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            data_source_id (str): id of CDP data source.

        Returns:
            Tuple[dict, int]: dict of data source, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        if ObjectId.is_valid(data_source_id):
            data_source_id = ObjectId(data_source_id)
        else:
            logger.error("Encountered invalid object id %s.", data_source_id)
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

            logger.error(
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
    cdp_data_sources_bp,
    api_c.CDP_DATA_SOURCES_ENDPOINT,
    "CreateCdpDataSources",
)
class CreateCdpDataSources(SwaggerView):
    """Create new CDP data source class."""

    parameters = [
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": api_c.CDP_DATA_SOURCE_DESCRIPTION,
            "example": [
                {
                    api_c.NAME: "Data source ",
                    api_c.TYPE: "dataSource",
                    api_c.STATUS: api_c.STATUS_ACTIVE,
                }
            ],
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "CDP data sources created.",
            "schema": {"type": "array", "items": CdpDataSourceSchema},
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to create CDP data sources",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CDP_DATA_SOURCES_TAG]

    @api_error_handler()
    def post(self) -> Tuple[list, int]:
        """Creates a new CDP data source.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[list, int]: List of CDP Data sources created, HTTP status code.
        """

        return (
            jsonify(
                CdpDataSourceSchema().dump(
                    bulk_write_data_sources(
                        database=get_db_client(),
                        data_sources=CdpDataSourcePostSchema().load(
                            request.get_json(), many=True
                        ),
                    ),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    cdp_data_sources_bp,
    f"{api_c.CDP_DATA_SOURCES_ENDPOINT}/<data_source_id>",
    "DeleteCdpDataSource",
)
class DeleteCdpDataSource(SwaggerView):
    """Deletes a CDP data source."""

    parameters = [
        {
            "name": db_c.CDP_DATA_SOURCE_ID,
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

    @api_error_handler()
    def delete(self, data_source_id: str) -> Tuple[dict, int]:
        """Deletes a CDP data source.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            data_source_id (str): CDP data source id.

        Returns:
            Tuple[dict, int]: CDP data source dict, HTTP status code.
        """

        if ObjectId.is_valid(data_source_id):
            data_source_id = ObjectId(data_source_id)
        else:
            logger.error(
                "Invalid CDP data source ID received %s.", data_source_id
            )
            return {
                "message": f"Invalid CDP data source ID received {data_source_id}."
            }, HTTPStatus.BAD_REQUEST
        database = get_db_client()
        success_flag = delete_data_source(database, data_source_id)

        if success_flag:
            logger.info("Successfully deleted data source %s.", data_source_id)
            return {"message": api_c.OPERATION_SUCCESS}, HTTPStatus.OK

        logger.error("Could not delete data source %s.", data_source_id)
        return {
            "message": api_c.OPERATION_FAILED
        }, HTTPStatus.INTERNAL_SERVER_ERROR


@add_view_to_blueprint(
    cdp_data_sources_bp,
    f"{api_c.CDP_DATA_SOURCES_ENDPOINT}",
    "BatchUpdateDataSources",
)
class BatchUpdateDataSources(SwaggerView):
    """Class to partially batch update data sources."""

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

    @api_error_handler()
    def patch(self) -> Tuple[dict, int]:
        """Updates a list of data sources.

        ---
        security:
            - Bearer: ["Authorization"]

        Returns:
            Tuple[dict, int]: Data source updated, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """

        data = request.get_json()

        # validate fields
        if api_c.CDP_DATA_SOURCE_IDS not in data or api_c.BODY not in data:
            logger.error(
                "Field %s not found in request data.",
                api_c.CDP_DATA_SOURCE_IDS,
            )
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
            logger.error("Invalid Object ID/IDs found.")
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
            logger.error("Data does not contain allowed fields.")
            return (
                self.responses[HTTPStatus.BAD_REQUEST.value],
                HTTPStatus.BAD_REQUEST.value,
            )

        # rename key from is_added to added for DB.
        data[db_c.ADDED] = data.pop(api_c.IS_ADDED)

        try:
            database = get_db_client()
            # update the data sources.
            if update_data_sources(database, data_source_ids, data):
                updated_data_sources = [
                    get_data_source(database, data_source_id)
                    for data_source_id in data_source_ids
                ]
                logger.info(
                    "Successfully update data sources with data source IDs %s.",
                    ",".join([str(x) for x in data_source_ids]),
                )
                return (
                    jsonify(
                        CdpDataSourceSchema().dump(
                            updated_data_sources, many=True
                        )
                    ),
                    HTTPStatus.OK.value,
                )
            logger.error("Could not update data sources.")
            return (
                self.responses[HTTPStatus.BAD_REQUEST.value],
                HTTPStatus.BAD_REQUEST.value,
            )

        except Exception as exc:

            logger.error(
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
    f"{api_c.CDP_DATA_SOURCES_ENDPOINT}/<{api_c.CDP_DATA_SOURCE_TYPE}>/{api_c.DATAFEEDS}",
    "GetConnectionsDatafeeds",
)
class GetDataSourceDatafeeds(SwaggerView):
    """Get data source data feeds class."""

    parameters = [
        {
            "name": api_c.CDP_DATA_SOURCE_TYPE,
            "in": "path",
            "type": "string",
            "description": "Data source type",
            "example": db_c.CDP_DATA_SOURCE_BLUECORE,
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "CDP data source data feeds retrieved successfully.",
            "schema": {
                "type": "array",
                "items": DataSourceDataFeedsGetSchema,
            },
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to retrieve data source data feeds",
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CDP_DATA_SOURCES_TAG]

    @api_error_handler()
    def get(self, datasource_type: str) -> Tuple[str, int]:
        """Retrieve data feeds for data source.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            datasource_type (str): Data source type.

        Returns:
            Tuple[dict, int]: Connections data feeds get object,
                HTTP status code.
        """

        token_response = get_token_from_request(request)

        data_source = get_data_source(
            get_db_client(), data_source_type=datasource_type
        )

        response = {
            api_c.NAME: data_source[db_c.NAME],
            api_c.TYPE: data_source[db_c.TYPE],
            api_c.DATAFEEDS: get_data_source_data_feeds(
                token_response[0], datasource_type
            ),
        }

        return (
            DataSourceDataFeedsGetSchema().dump(response),
            HTTPStatus.OK,
        )
