# pylint: disable=unused-argument
"""Paths for Orchestration API"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from http import HTTPStatus
from itertools import repeat
from pathlib import Path
from typing import Tuple, Union, Iterator, Optional

import pandas as pd
from huxunifylib.database.delivery_platform_management import (
    get_delivery_platform,
)
from huxunifylib.database.orchestration_management import (
    get_audience,
    append_destination_to_standalone_audience,
)
from pandas import DataFrame
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, Response, request, jsonify

from huxunifylib.connectors import connector_cdp
from huxunifylib.database import (
    orchestration_management,
)
from huxunifylib.database.audit_management import create_audience_audit
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database import constants as db_c
from huxunifylib.database.transform.transform_dataframe import (
    transform_fields_google_file,
    transform_fields_amazon_file,
)

import huxunify.api.constants as api_c
from huxunify.api.config import get_config
from huxunify.api.data_connectors.aws import upload_file
from huxunify.api.data_connectors.cdp import (
    get_city_ltvs,
    get_demographic_by_state,
    get_demographic_by_country,
)
from huxunify.api.data_connectors.courier import toggle_event_driven_routers
from huxunify.api.data_connectors.okta import get_token_from_request
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    validate_engagement_and_audience,
    requires_access_levels,
)

from huxunify.api.schema.customers import (
    CustomersInsightsCitiesSchema,
    CustomersInsightsStatesSchema,
    CustomersInsightsCountriesSchema,
)
from huxunify.api.schema.engagement import DestinationEngagedAudienceSchema
from huxunify.api.schema.orchestration import AudienceGetSchema
from huxunify.api.schema.utils import (
    AUTH401_RESPONSE,
    FAILED_DEPENDENCY_424_RESPONSE,
)
from huxunify.api.route.utils import (
    get_db_client,
    do_not_transform_fields,
    logger,
    Validation,
)

# setup the audiences blueprint
from huxunify.api.stubbed_data import stub_city_zip_data

audience_bp = Blueprint(api_c.AUDIENCE_ENDPOINT, import_name=__name__)


@audience_bp.before_request
@secured()
def before_request():
    """Protect all of the audiences endpoints."""
    pass  # pylint: disable=unnecessary-pass


def get_batch_customers(
    cdp_connector: connector_cdp,
    location_details: dict,
    batch_size: int = api_c.CUSTOMERS_DEFAULT_BATCH_SIZE,
    offset: int = 0,
) -> Union[pd.DataFrame, None]:
    """Fetch audience batch using connector asynchronously.

    Args:
        cdp_connector (connector_cdp): Instance of CDP connector.
        location_details (dict): Audience filters to be passed.
        batch_size (int, Optional): Batch size to be fetched.
        offset (int, Optional): Offset of the batch to be fetched.

    Returns:
        pd.DataFrame: Data frame of batch information.
    """
    return cdp_connector.read_batch(
        location_details=location_details,
        batch_size=batch_size,
        offset=offset,
    )


def get_audience_data_async(
    cdp_connector: connector_cdp,
    actual_size: int,
    location_details: dict,
    batch_size: int = api_c.CUSTOMERS_DEFAULT_BATCH_SIZE,
) -> Iterator[Optional[DataFrame]]:
    """Creates a list of tasks, this is useful for asynchronous batch wise
    calls to a task.

    Args:
        cdp_connector (connector_cdp): Instance of CDP connector.
        actual_size (int): Actual size of the audience.
        location_details (dict): Audience filters to be passed.
        batch_size (int, Optional): Size of batch to be retrieved.

    Returns:
        list: list of each batch's data.
    """
    offset = 0
    if actual_size <= batch_size:
        return [
            get_batch_customers(
                cdp_connector, location_details, actual_size, offset
            )
        ]
    batch_sizes = []
    offsets = []
    while offset + batch_size <= actual_size:
        batch_sizes.append(batch_size)
        offsets.append(offset)
        offset += batch_size
    if actual_size % batch_size != 0:
        batch_sizes.append(batch_size)
        offsets.append(offset)
    with ThreadPoolExecutor(
        max_workers=api_c.MAX_WORKERS_THREAD_POOL
    ) as executor:
        return executor.map(
            get_batch_customers,
            repeat(cdp_connector),
            repeat(location_details),
            batch_sizes,
            offsets,
        )


@add_view_to_blueprint(
    audience_bp,
    f"{api_c.AUDIENCE_ENDPOINT}/<audience_id>/<download_type>",
    "AudienceDownloadView",
)
class AudienceDownload(SwaggerView):
    """Audience download by ID and download type."""

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": api_c.DOWNLOAD_TYPE,
            "description": "Download Type",
            "type": "string",
            "in": "path",
            "required": True,
            "example": api_c.GOOGLE_ADS,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Download Audience.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to download audience.",
        },
    }

    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use, too-many-locals
    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def get(
        self, audience_id: str, download_type: str, user: dict
    ) -> Tuple[Response, int]:
        """Downloads an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            download_type (str): Download type.
            user (dict): User object.

        Returns:
            Tuple[Response, int]: File Object Response, HTTP status code.
        """

        download_types = {
            api_c.GOOGLE_ADS: (
                transform_fields_google_file,
                api_c.GOOGLE_ADS_DEFAULT_COLUMNS,
            ),
            api_c.AMAZON_ADS: (
                transform_fields_amazon_file,
                api_c.AMAZON_ADS_DEFAULT_COLUMNS,
            ),
            api_c.GENERIC_ADS: (
                do_not_transform_fields,
                api_c.GENERIC_ADS_DEFAULT_COLUMNS,
            ),
        }

        token_response = get_token_from_request(request)

        if not download_types.get(download_type):
            return (
                jsonify(
                    {
                        "message": "Invalid download type or download type not supported"
                    }
                ),
                HTTPStatus.BAD_REQUEST,
            )

        database = get_db_client()
        audience = orchestration_management.get_audience(
            database, ObjectId(audience_id)
        )

        if not audience:
            return (
                jsonify({"message": api_c.AUDIENCE_NOT_FOUND}),
                HTTPStatus.NOT_FOUND,
            )

        # set transform function based on download type in request
        transform_function = download_types.get(download_type)[0]

        # get environment config
        config = get_config()

        if config.RETURN_EMPTY_AUDIENCE_FILE:
            logger.info(
                "%s config set to %s, will generate empty %s type audience file.",
                api_c.RETURN_EMPTY_AUDIENCE_FILE,
                config.RETURN_EMPTY_AUDIENCE_FILE,
                download_type,
            )
            data_batches = [
                pd.DataFrame(columns=download_types.get(download_type)[1])
            ]
            # change transform function to not transform any fields if config
            # is set to download empty audience file
            transform_function = do_not_transform_fields
        else:
            logger.info(
                "%s config set to %s, will generate %s type audience file with content.",
                api_c.RETURN_EMPTY_AUDIENCE_FILE,
                config.RETURN_EMPTY_AUDIENCE_FILE,
                download_type,
            )
            cdp = connector_cdp.ConnectorCDP(access_token=token_response[0])

            data_batches = get_audience_data_async(
                cdp,
                audience.get(api_c.SIZE),
                batch_size=api_c.CUSTOMERS_DEFAULT_BATCH_SIZE,
                location_details={
                    api_c.AUDIENCE_FILTERS: audience.get(
                        api_c.AUDIENCE_FILTERS
                    )
                },
            )

        audience_file_name = (
            f"{datetime.now().strftime('%m%d%Y%H%M%S')}"
            f"_{audience_id}_{download_type}.csv"
        )

        with open(
            audience_file_name, "w", newline="", encoding="utf-8"
        ) as csvfile:
            for dataframe_batch in data_batches:
                transform_function(dataframe_batch).to_csv(
                    csvfile,
                    mode="a",
                    index=False,
                )

        logger.info(
            "Uploading generated %s audience file to %s S3 bucket",
            audience_file_name,
            config.S3_DATASET_BUCKET,
        )
        if upload_file(
            file_name=audience_file_name,
            bucket=config.S3_DATASET_BUCKET,
            object_name=audience_file_name,
            user_name=user[api_c.USER_NAME],
            file_type=api_c.AUDIENCE,
        ):
            create_audience_audit(
                database=database,
                audience_id=audience_id,
                download_type=download_type,
                file_name=audience_file_name,
                user_name=user[api_c.USER_NAME],
            )
            logger.info(
                "Created an audit log for %s audience file creation",
                audience_file_name,
            )
        audience_file = Path(audience_file_name)
        data = audience_file.read_bytes()
        audience_file.unlink()

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            f'{user[api_c.USER_NAME]} downloaded the audience, "{audience[db_c.NAME]}"'
            f" with format {download_type}.",
            api_c.ORCHESTRATION_TAG,
            user[api_c.USER_NAME],
        )

        return (
            Response(
                data,
                headers={
                    "Content-Type": "application/csv",
                    "Access-Control-Expose-Headers": "Content-Disposition",
                    "Content-Disposition": f"attachment; filename={audience_file_name};",
                },
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    audience_bp,
    f"/{api_c.AUDIENCE_ENDPOINT}/<audience_id>/{api_c.STATES}",
    "AudienceInsightsStates",
)
class AudienceInsightsStates(SwaggerView):
    """Audience insights by state."""

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "612cd8eb6a9815be11cd6006",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": CustomersInsightsStatesSchema,
            },
            "description": "Audience Insights by states.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Audience Insights by states."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Retrieves state-level geographic customer insights for the audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Response list of spend and size data by state,
                HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)

        audience = orchestration_management.get_audience(
            get_db_client(), ObjectId(audience_id)
        )

        if not audience:
            return (
                jsonify({"message": api_c.AUDIENCE_NOT_FOUND}),
                HTTPStatus.NOT_FOUND,
            )

        return (
            jsonify(
                CustomersInsightsStatesSchema().dump(
                    get_demographic_by_state(
                        token_response[0],
                        filters=audience.get(db_c.AUDIENCE_FILTERS),
                    ),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    audience_bp,
    f"/{api_c.AUDIENCE_ENDPOINT}/<audience_id>/{api_c.CITIES}",
    "AudienceInsightsCities",
)
class AudienceInsightsCities(SwaggerView):
    """Audience insights by city."""

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "612cd8eb6a9815be11cd6006",
        },
        {
            "name": api_c.QUERY_PARAMETER_BATCH_SIZE,
            "in": "query",
            "type": "integer",
            "description": "Max number of cities to be returned.",
            "example": "5",
            "required": False,
            "default": api_c.CITIES_DEFAULT_BATCH_SIZE,
        },
        {
            "name": api_c.QUERY_PARAMETER_BATCH_NUMBER,
            "in": "query",
            "type": "integer",
            "description": "Number of which batch of cities should be returned.",
            "example": "10",
            "required": False,
            "default": api_c.DEFAULT_BATCH_NUMBER,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": CustomersInsightsCitiesSchema,
            },
            "description": "Audience Insights by cities.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Customer Insights by cities."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Retrieves city-level geographic customer insights for the audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Response list of spend and size by city, HTTP status code.
        """
        # get auth token from request
        token_response = get_token_from_request(request)

        batch_size = Validation.validate_integer(
            request.args.get(
                api_c.QUERY_PARAMETER_BATCH_SIZE,
                str(api_c.CITIES_DEFAULT_BATCH_SIZE),
            )
        )
        batch_number = Validation.validate_integer(
            request.args.get(
                api_c.QUERY_PARAMETER_BATCH_NUMBER,
                str(api_c.DEFAULT_BATCH_NUMBER),
            )
        )

        audience = orchestration_management.get_audience(
            get_db_client(), ObjectId(audience_id)
        )

        if not audience:
            return (
                jsonify({"message": api_c.AUDIENCE_NOT_FOUND}),
                HTTPStatus.NOT_FOUND,
            )

        filters = (
            {api_c.AUDIENCE_FILTERS: audience.get(db_c.AUDIENCE_FILTERS)}
            if audience.get(db_c.AUDIENCE_FILTERS)
            else None
        )

        return (
            jsonify(
                CustomersInsightsCitiesSchema().dump(
                    get_city_ltvs(
                        token_response[0],
                        filters=filters,
                        offset=int(batch_size) * (int(batch_number) - 1),
                        limit=int(batch_size),
                    ),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    audience_bp,
    f"/{api_c.AUDIENCE_ENDPOINT}/<audience_id>/{api_c.COUNTRIES}",
    "AudienceInsightsCountries",
)
class AudienceInsightsCountries(SwaggerView):
    """Audience insights by countries."""

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "612cd8eb6a9815be11cd6006",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": CustomersInsightsCountriesSchema,
            },
            "description": "Audience Insights by countries.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Audience Insights by countries."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @validate_engagement_and_audience()
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, audience_id: ObjectId, user: dict) -> Tuple[Response, int]:
        """Retrieves country-level geographic customer insights for the audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (ObjectId): Audience ID.
            user (dict): user object.

        Returns:
            Tuple[Response, int]: Response list of spend and size data by country,
                HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)

        audience = orchestration_management.get_audience(
            get_db_client(), audience_id
        )

        return (
            jsonify(
                CustomersInsightsCountriesSchema().dump(
                    get_demographic_by_country(
                        token_response[0],
                        filters={
                            api_c.AUDIENCE_FILTERS: audience.get(
                                db_c.AUDIENCE_FILTERS
                            )
                        },
                    ),
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    audience_bp,
    f"/{api_c.AUDIENCE_ENDPOINT}/rules/<field_type>/<key>",
    "AudienceRulesCities",
)
class AudienceRulesLocation(SwaggerView):
    """Audience Rules Constants for Cities & Zip"""

    parameters = [
        {
            "name": api_c.FIELD_TYPE,
            "description": "Field Type",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "cities",
        },
        {
            "name": api_c.KEY,
            "description": "Search Key",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "new",
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": "Location Constant Lists",
            },
            "description": "Location Constants List",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Audience Rules."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self, field_type: str, key: str) -> Tuple[Response, int]:
        """Retrieves Location Rules constants.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            field_type (str): Field Type
            key (str): Search Key


        Returns:
            Tuple[Response, int]: rules constants for email, Http status code
        """

        # TODO Remove stub once CDM API is integrated
        if field_type == api_c.CITY:
            data = jsonify(
                [
                    {f"{x[1]}|{x[2]}|USA": f"{x[1]}, {x[2]} USA"}
                    for x in [
                        x
                        for x in stub_city_zip_data.city_zip_data
                        if key.lower() in x[1].lower()
                    ]
                ]
            )
        elif field_type == api_c.ZIP_CODE:
            data = jsonify(
                [
                    {x[0]: f"{x[0]}, {x[1]} {x[2]}"}
                    for x in [
                        x
                        for x in stub_city_zip_data.city_zip_data
                        if key.lower() in x[0].lower()
                    ]
                ]
            )
        else:
            return (
                jsonify({"message": f"Field type received {field_type}"}),
                HTTPStatus.NOT_FOUND,
            )

        return data, HTTPStatus.OK


@add_view_to_blueprint(
    audience_bp,
    f"/{api_c.AUDIENCE_ENDPOINT}/rules/<field_type>/histogram",
    "AudienceRulesHistogram",
)
class AudienceRulesHistogram(SwaggerView):
    """Audience Rules Histogram"""

    parameters = [
        {
            "name": api_c.FIELD_TYPE,
            "description": "Field Type",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "age",
        },
        {
            "name": api_c.MODEL_NAME,
            "description": "Name of model to be fetched",
            "in": "query",
            "type": "string",
            "required": False,
        },
    ]
    responses = {
        HTTPStatus.OK.value: {
            "description": "Get audience rules " "histogram dictionary"
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Audience Rules."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    def get(self, field_type: str) -> Tuple[Response, int]:
        """Retrieves Histogram data for rules.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            field_type (str): Field Type

        Returns:
            Tuple[Response, int]: rules constants
        """

        # TODO Remove stub once CDM API is integrated
        if field_type not in api_c.AUDIENCE_RULES_HISTOGRAM_DATA:
            return (
                jsonify({"message": f"Data not found for {field_type}"}),
                HTTPStatus.NOT_FOUND,
            )

        if field_type == api_c.MODEL:
            model_name = request.args.get(api_c.MODEL_NAME, "")
            if model_name in list(
                api_c.AUDIENCE_RULES_HISTOGRAM_DATA[api_c.MODEL]
            ):
                return (
                    api_c.AUDIENCE_RULES_HISTOGRAM_DATA[api_c.MODEL][
                        model_name
                    ],
                    HTTPStatus.OK,
                )
            return (
                jsonify({"message": f"Data not found for {model_name}"}),
                HTTPStatus.NOT_FOUND,
            )

        return (
            jsonify(api_c.AUDIENCE_RULES_HISTOGRAM_DATA[field_type]),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    audience_bp,
    f"/{api_c.AUDIENCE_ENDPOINT}/<audience_id>/destinations",
    "AddDestinationAudience",
)
class AddDestinationAudience(SwaggerView):
    """Add destination to Audience"""

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience Id",
            "type": "string",
            "in": "path",
            "required": True,
            "example": "5f5f7262997acad4bac4373b",
        },
        {
            "name": "body",
            "in": "body",
            "type": "object",
            "description": "Input Destinations body.",
            "example": {
                api_c.ID: "60ae035b6c5bf45da27f17e6",
                db_c.DELIVERY_PLATFORM_CONFIG: {
                    db_c.DATA_EXTENSION_NAME: "SFMC Test Audience"
                },
            },
        },
    ]
    responses = {
        HTTPStatus.CREATED.value: {
            "schema": AudienceGetSchema,
            "description": "Destination added to Standalone Audience.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to Add destination to the audience",
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def post(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Adds Destination to Standalone Audience

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience Id
            user (dict): User Object

        Returns:
            Tuple[Response, int]: Destination Audience added,
                HTTP status code.
        """

        database = get_db_client()

        audience = get_audience(database, ObjectId(audience_id))

        if not audience:
            logger.error("Audience not found for audience ID %s.", audience_id)
            return {"message": api_c.AUDIENCE_NOT_FOUND}, HTTPStatus.NOT_FOUND

        destination = DestinationEngagedAudienceSchema().load(
            request.get_json(), partial=True
        )
        destination[api_c.ID] = ObjectId(destination.get(api_c.ID))
        destination[db_c.DATA_ADDED] = datetime.utcnow()

        # get destinations
        destination_to_attach = get_delivery_platform(
            database, destination.get(api_c.ID)
        )

        if not destination_to_attach:
            logger.error(
                "Could not find destination with id %s.", destination[api_c.ID]
            )
            return {
                "message": api_c.DESTINATION_NOT_FOUND
            }, HTTPStatus.NOT_FOUND

        audience = append_destination_to_standalone_audience(
            database=database,
            audience_id=ObjectId(audience_id),
            destination=destination,
            user_name=user[api_c.USER_NAME],
        )

        logger.info(
            "Destination %s added to audience %s.",
            destination_to_attach[db_c.NAME],
            audience[db_c.NAME],
        )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_SUCCESS,
            (
                f'Destination "{destination_to_attach[db_c.NAME]}" added to '
                f'audience "{audience[db_c.NAME]}" '
            ),
            api_c.ORCHESTRATION_TAG,
            user[api_c.USER_NAME],
        )

        return (
            AudienceGetSchema().dump(audience),
            HTTPStatus.CREATED.value,
        )
