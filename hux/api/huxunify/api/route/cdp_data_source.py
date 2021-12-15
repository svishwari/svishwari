# pylint: disable=no-self-use,disable=unused-argument
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
    update_data_sources,
    bulk_write_data_sources,
    bulk_delete_data_sources,
)
from huxunifylib.database.notification_management import create_notification

from huxunify.api import constants as api_c
from huxunify.api.data_connectors.cdp_connection import (
    get_data_source_data_feeds,
    get_data_sources,
)
from huxunify.api.data_connectors.okta import get_token_from_request

from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    requires_access_levels,
)
from huxunify.api.route.utils import (
    get_db_client,
    Validation as validation,
)

from huxunify.api.schema.cdp_data_source import (
    CdpDataSourceSchema,
    CdpDataSourcePostSchema,
    DataSourceDataFeedsGetSchema,
    CdpConnectionsDataSourceSchema,
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

    parameters = [
        {
            "name": api_c.ONLY_ADDED,
            "description": "Flag to specify if only added data sources are to be fetched.",
            "type": "boolean",
            "in": "query",
            "required": False,
            "example": "true",
            "default": "true",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of CDP data sources.",
            "schema": {"type": "array", "items": CdpDataSourceSchema},
        }
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CDP_DATA_SOURCES_TAG]

    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, user: dict) -> Tuple[list, int]:
        """Retrieves all CDP data sources.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[list, int]: list of CDP data sources, HTTP status code.

        Raises:
            ProblemException: Any exception raised during endpoint execution.
        """
        only_added = (
            validation.validate_bool(request.args.get(api_c.ONLY_ADDED))
            if request.args
            else False
        )

        data_sources = get_all_data_sources(get_db_client())
        connections_data_sources = []
        if not only_added:
            token_response = get_token_from_request(request)
            connections_data_sources = CdpConnectionsDataSourceSchema().load(
                get_data_sources(token_response[0]), many=True
            )
            added_data_source_types = [
                data_source[db_c.TYPE] for data_source in data_sources
            ]
            data_sources.extend(
                [
                    data_source
                    for data_source in connections_data_sources
                    if data_source[api_c.TYPE] not in added_data_source_types
                ]
            )

        for data_source in data_sources:
            data_source[
                db_c.CATEGORY
            ] = api_c.CDP_DATA_SOURCE_CATEGORY_MAP.get(
                data_source[api_c.TYPE], db_c.CATEGORY_UNKNOWN
            )
            for connection_ds in connections_data_sources:
                if connection_ds.get(api_c.TYPE) == data_source.get(
                    api_c.TYPE
                ):
                    data_source[
                        db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT
                    ] = connection_ds.get(
                        db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT
                    )

        return (
            jsonify(CdpDataSourceSchema().dump(data_sources, many=True)),
            HTTPStatus.OK,
        )


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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, data_source_id: str, user: dict):
        """Retrieves a CDP data source.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            data_source_id (str): id of CDP data source.
            user (dict): User object

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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def post(self, user: dict) -> Tuple[list, int]:
        """Creates new CDP data sources.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[list, int]: List of CDP Data sources created, HTTP status code.
        """

        database = get_db_client()
        new_data_sources = CdpDataSourcePostSchema().load(
            request.get_json(), many=True
        )

        data_sources = bulk_write_data_sources(
            database=database, data_sources=new_data_sources
        )

        if data_sources:
            logger.info(
                "Successfully created %s data source(s).",
                ", ".join(
                    [
                        data_source[api_c.NAME]
                        for data_source in new_data_sources
                    ]
                ),
            )
            create_notification(
                database,
                db_c.NOTIFICATION_TYPE_SUCCESS,
                f"{user[api_c.USER_NAME]} created the following CDP Data Sources: "
                f"{'. '.join([data_source[api_c.NAME] for data_source in new_data_sources])}",
                api_c.CDP_DATA_SOURCES_TAG,
                user[api_c.USER_NAME],
            )
        else:
            logger.info(
                "Failed to create %s data source(s).",
                ", ".join(
                    [
                        data_source[api_c.NAME]
                        for data_source in new_data_sources
                    ]
                ),
            )
            create_notification(
                database,
                db_c.NOTIFICATION_TYPE_CRITICAL,
                f"Failed to create the following CDP Data Sources: "
                f"{'. '.join([data_source[api_c.NAME] for data_source in new_data_sources])}",
                api_c.CDP_DATA_SOURCES_TAG,
                user[api_c.USER_NAME],
            )

        return (
            jsonify(
                CdpDataSourceSchema().dump(
                    data_sources,
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    cdp_data_sources_bp,
    f"{api_c.CDP_DATA_SOURCES_ENDPOINT}",
    "DeleteCdpDataSource",
)
class DeleteCdpDataSources(SwaggerView):
    """Deletes CDP data sources."""

    parameters = [
        {
            "name": api_c.DATASOURCES,
            "description": "Comma-separated data source types to be deleted.",
            "type": "string",
            "in": "query",
            "required": True,
            "example": "datasource1,datasource2",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Deletes CDP data sources.",
            "schema": CdpDataSourceSchema,
        },
        HTTPStatus.NOT_FOUND.value: {"schema": NotFoundError},
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.CDP_DATA_SOURCES_TAG]

    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def delete(self, user: dict) -> Tuple[dict, int]:
        """Deletes CDP data sources.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

        Returns:
            Tuple[str, int]: Message, HTTP status code.
        """
        data_source_types = request.args.get(api_c.DATASOURCES)

        if data_source_types:
            database = get_db_client()
            success_flag = bulk_delete_data_sources(
                database, data_source_types.replace(" ", "").split(",")
            )

            if success_flag:
                logger.info(
                    "Successfully deleted data sources - %s.",
                    data_source_types,
                )
                create_notification(
                    database,
                    db_c.NOTIFICATION_TYPE_SUCCESS,
                    f"{user[api_c.USER_NAME]} deleted the following CDP Data Sources: "
                    f"{data_source_types}",
                    api_c.CDP_DATA_SOURCES_TAG,
                    user[api_c.USER_NAME],
                )
                return {
                    "message": api_c.DELETE_DATASOURCES_SUCCESS.format(
                        data_source_types
                    )
                }, HTTPStatus.OK

            logger.error(
                "Could not delete data sources - %s.", data_source_types
            )
            create_notification(
                database,
                db_c.NOTIFICATION_TYPE_CRITICAL,
                f"Failed to delete the following CDP Data Sources: "
                f"{data_source_types}",
                api_c.CDP_DATA_SOURCES_TAG,
                user[api_c.USER_NAME],
            )
            return {
                "message": api_c.CANNOT_DELETE_DATASOURCES.format(
                    data_source_types
                )
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {
            api_c.MESSAGE: api_c.EMPTY_OBJECT_ERROR_MESSAGE
        }, HTTPStatus.BAD_REQUEST


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
    @requires_access_levels([api_c.ADMIN_LEVEL, api_c.EDITOR_LEVEL])
    def patch(self, user: dict) -> Tuple[dict, int]:
        """Updates a list of data sources.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            user (dict): User object.

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

        if data[api_c.IS_ADDED]:
            update_action = (
                api_c.ACTION_REQUESTED
                if data[api_c.STATUS] == api_c.STATUS_PENDING
                else api_c.ACTION_ACTIVATED
            )
        else:
            update_action = api_c.ACTION_REMOVED

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

                updated_data_source_names = ", ".join(
                    [x[api_c.NAME] for x in updated_data_sources]
                )

                logger.info(
                    "Successfully %s data sources with data source(s) %s.",
                    update_action,
                    updated_data_source_names,
                )

                create_notification(
                    database,
                    db_c.NOTIFICATION_TYPE_SUCCESS,
                    (
                        f"Data source(s) {updated_data_source_names} "
                        f"{update_action} by {user[api_c.DISPLAY_NAME]}"
                    ),
                    api_c.CDP_DATA_SOURCES_TAG,
                    user[api_c.USER_NAME],
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
            "example": db_c.DATA_SOURCE_PLATFORM_BLUECORE,
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
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, datasource_type: str, user: dict) -> Tuple[str, int]:
        """Retrieve data feeds for data source.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            datasource_type (str): Data source type.
            user (dict): User object.

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
