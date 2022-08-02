# pylint: disable=unused-argument,too-many-lines
"""Paths for Orchestration API."""
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from http import HTTPStatus
from itertools import repeat
from pathlib import Path
from typing import Tuple, Union, Iterator, Optional

import pandas as pd
from pandas import DataFrame
from flasgger import SwaggerView
from bson import ObjectId
from flask import Blueprint, Response, request, jsonify

from huxunifylib.database.delivery_platform_management import (
    get_delivery_platform,
    get_delivery_platforms_by_id,
)
from huxunifylib.database.orchestration_management import (
    get_audience,
    append_destination_to_standalone_audience,
    remove_destination_from_audience,
)
from huxunifylib.connectors import connector_cdp
from huxunifylib.database import (
    orchestration_management,
)
from huxunifylib.database.notification_management import create_notification
from huxunifylib.database import constants as db_c
from huxunifylib.database.transform.transform_dataframe import (
    transform_fields_google_file,
    transform_fields_amazon_file,
)


import huxunify.api.constants as api_c
from huxunify.api.config import get_config
from huxunify.api.data_connectors.cdp import (
    get_city_ltvs,
    get_demographic_by_state,
    get_demographic_by_country,
    get_customers_insights_count_by_day,
    get_revenue_by_day,
    get_age_histogram_data,
    get_histogram_data,
)
from huxunify.api.data_connectors.okta import get_token_from_request
from huxunify.api.data_connectors.cache import Caching
from huxunify.api.route.decorators import (
    add_view_to_blueprint,
    secured,
    api_error_handler,
    validate_engagement_and_audience,
    requires_access_levels,
)
from huxunify.api.route.return_util import HuxResponse

from huxunify.api.schema.customers import (
    CustomersInsightsCitiesSchema,
    CustomersInsightsStatesSchema,
    CustomersInsightsCountriesSchema,
    TotalCustomersInsightsSchema,
    CustomerRevenueInsightsSchema,
)
from huxunify.api.schema.engagement import DestinationEngagedAudienceSchema
from huxunify.api.schema.errors import NotFoundError
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
    get_start_end_dates,
    generate_audience_file,
    convert_cdp_buckets_to_histogram,
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
    f"{api_c.AUDIENCE_ENDPOINT}/<audience_id>/download",
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
            "name": api_c.DOWNLOAD_TYPES,
            "description": "Download Type",
            "type": "array",
            "in": "query",
            "items": {"type": "string"},
            "collectionFormat": "multi",
            "required": True,
            "example": [api_c.GOOGLE_ADS, api_c.AMAZON_ADS, api_c.GENERIC_ADS],
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
    def get(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Downloads an audience.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID.
            user (dict): User object.

        Returns:
            Tuple[Response, int]: File Object Response, HTTP status code.
        """
        download_types = request.args.getlist(api_c.DOWNLOAD_TYPES)

        applicable_download_types = {
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

        for download_type in download_types:
            if download_type not in applicable_download_types:
                return (
                    jsonify(
                        {
                            "message": f"{download_type} download type is "
                            f"either invalid or not supported yet"
                        }
                    ),
                    HTTPStatus.BAD_REQUEST,
                )

        database = get_db_client()
        audience = orchestration_management.get_audience(
            database, ObjectId(audience_id)
        )

        if not audience:
            logger.error("Audience with ID %s not found.", audience_id)
            return (
                jsonify({"message": api_c.AUDIENCE_NOT_FOUND}),
                HTTPStatus.NOT_FOUND,
            )

        # get environment config
        config = get_config()

        if config.RETURN_EMPTY_AUDIENCE_FILE:
            logger.info(
                "%s config set to %s, will generate empty %s type audience files.",
                api_c.RETURN_EMPTY_AUDIENCE_FILE,
                config.RETURN_EMPTY_AUDIENCE_FILE,
                ",".join(download_types),
            )
            for download_type in download_types:
                data_batches = [
                    pd.DataFrame(
                        columns=applicable_download_types.get(download_type)[1]
                    )
                ]
                # change transform function to not transform any fields if config
                # is set to download empty audience file
                transform_function = do_not_transform_fields
                generate_audience_file(
                    database=database,
                    user_name=user[db_c.USER_NAME],
                    download_type=download_type,
                    audience_id=audience_id,
                    data_batches=data_batches,
                    transform_function=transform_function,
                )
        else:
            logger.info(
                "%s config set to %s, will generate %s type audience files with content.",
                api_c.RETURN_EMPTY_AUDIENCE_FILE,
                config.RETURN_EMPTY_AUDIENCE_FILE,
                ",".join(download_types),
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

            for download_type in download_types:
                # set transform function based on download type in request
                transform_function = applicable_download_types.get(
                    download_type
                )[0]
                generate_audience_file(
                    database=database,
                    user_name=user[db_c.USER_NAME],
                    download_type=download_type,
                    audience_id=audience_id,
                    data_batches=data_batches,
                    transform_function=transform_function,
                )

        create_notification(
            database,
            db_c.NOTIFICATION_TYPE_INFORMATIONAL,
            f'{user[api_c.USER_NAME]} downloaded the audience, "{audience[db_c.NAME]}"'
            f" with formats {','.join(download_types)}",
            db_c.NOTIFICATION_CATEGORY_AUDIENCES,
            user[api_c.USER_NAME],
        )

        zipfile_name = (
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}_"
            f"{audience_id}_audience_data.zip"
        )
        folder_name = "downloadaudiences"
        # zip all the audiences which are inside in the folder
        with zipfile.ZipFile(
            zipfile_name, "w", compression=zipfile.ZIP_STORED
        ) as zipfolder:

            folder = Path(__file__).parent.parent.joinpath(folder_name)
            for file in folder.rglob("**/*.csv"):
                zipfolder.write(file, arcname=file.name)
                file.unlink()

        zip_file = Path(zipfile_name)
        data = zip_file.read_bytes()
        zip_file.unlink()

        return (
            Response(
                data,
                headers={
                    "Content-Type": "application/zip",
                    "Access-Control-Expose-Headers": "Content-Disposition",
                    "Content-Disposition": f"attachment; filename={zipfile_name};",
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
            logger.error("Audience with ID %s not found.", audience_id)
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
            logger.error("Audience with ID %s not found.", audience_id)
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
        HTTPStatus.NOT_FOUND.value: {
            "description": "Data not found for field type.",
            "schema": NotFoundError,
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

        token_response = get_token_from_request(request)

        if field_type not in api_c.AUDIENCE_RULES_HISTOGRAM_DATA:
            return HuxResponse.NOT_FOUND(f"Data not found for {field_type}")

        if field_type == api_c.AGE:
            bucket_data = Caching.check_and_return_cache(
                cache_key=f"{api_c.CUSTOMERS_ENDPOINT}/customer-profiles/insights/count-by-age",
                method=get_age_histogram_data,
                keyword_arguments={"token": token_response[0]},
            )

            if not bucket_data:
                return HuxResponse.NOT_FOUND(
                    f"Data not found for {field_type}"
                )

            histogram_data = convert_cdp_buckets_to_histogram(
                bucket_data=bucket_data, field=field_type
            )
            api_c.AUDIENCE_RULES_HISTOGRAM_DATA[api_c.AGE][
                api_c.VALUES
            ] = histogram_data.values

        if field_type == api_c.MODEL:
            model_name = request.args.get(api_c.MODEL_NAME, "")
            if model_name in list(
                api_c.AUDIENCE_RULES_HISTOGRAM_DATA[api_c.MODEL]
            ):
                bucket_data = Caching.check_and_return_cache(
                    cache_key=f"{api_c.CUSTOMERS_ENDPOINT}/customer-profiles/"
                    f"insights/counts/by-float-field?model_name={model_name}",
                    method=get_histogram_data,
                    keyword_arguments={
                        "field_name": model_name,
                        "token": token_response[0],
                    },
                )

                if not bucket_data:
                    return HuxResponse.NOT_FOUND(
                        f"Data not found for {model_name}"
                    )

                histogram_data = convert_cdp_buckets_to_histogram(
                    bucket_data=bucket_data
                )
                api_c.AUDIENCE_RULES_HISTOGRAM_DATA[api_c.MODEL][model_name][
                    api_c.VALUES
                ] = histogram_data.values

                api_c.AUDIENCE_RULES_HISTOGRAM_DATA[api_c.MODEL][model_name][
                    api_c.MAX
                ] = round(histogram_data.max_val, 1)

                return (
                    api_c.AUDIENCE_RULES_HISTOGRAM_DATA[api_c.MODEL][
                        model_name
                    ],
                    HTTPStatus.OK,
                )

            return HuxResponse.NOT_FOUND(f"Data not found for {model_name}")

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
            "description": "Destination added to Audience.",
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
    @validate_engagement_and_audience()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def post(self, audience_id: ObjectId, user: dict) -> Tuple[Response, int]:
        """Adds Destination to Audience

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (ObjectId): Audience Id
            user (dict): User Object

        Returns:
            Tuple[Response, int]: Destination Audience added,
                HTTP status code.
        """

        database = get_db_client()

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
            audience_id=audience_id,
            destination=destination,
            user_name=user[api_c.USER_NAME],
        )

        destination_ids = [
            x[db_c.OBJECT_ID] for x in audience[db_c.DESTINATIONS]
        ]

        destinations_list = get_delivery_platforms_by_id(
            database, destination_ids
        )
        audience[db_c.DESTINATIONS] = destinations_list

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
            db_c.NOTIFICATION_CATEGORY_AUDIENCES,
            user[api_c.USER_NAME],
        )

        return (
            AudienceGetSchema().dump(audience),
            HTTPStatus.CREATED.value,
        )


@add_view_to_blueprint(
    audience_bp,
    f"/{api_c.AUDIENCE_ENDPOINT}/<audience_id>/destinations",
    "DeleteDestinationAudience",
)
class DeleteDestinationAudience(SwaggerView):
    """Delete destination to Audience"""

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
            },
        },
    ]
    responses = {
        HTTPStatus.NO_CONTENT.value: {
            "schema": AudienceGetSchema,
            "description": "Destination successfully deleted from audience.",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to delete destination from the audience",
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.ORCHESTRATION_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @validate_engagement_and_audience()
    @requires_access_levels([api_c.EDITOR_LEVEL, api_c.ADMIN_LEVEL])
    def delete(
        self, audience_id: ObjectId, user: dict
    ) -> Tuple[Response, int]:
        """Remove Destination from Audience

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (ObjectId): Audience Id
            user (dict): User Object

        Returns:
            Tuple[Response, int]: Destination Audience added,
                HTTP status code.
        """

        database = get_db_client()

        destination = DestinationEngagedAudienceSchema().load(
            request.get_json(), partial=True
        )
        destination[api_c.ID] = ObjectId(destination.get(api_c.ID))

        audience = remove_destination_from_audience(
            database=database,
            audience_id=audience_id,
            destination_id=destination[api_c.ID],
            user_name=user[api_c.USER_NAME],
        )
        if audience:
            logger.info(
                "Destination %s removed from audience %s.",
                destination[api_c.ID],
                audience[db_c.NAME],
            )

            create_notification(
                database,
                db_c.NOTIFICATION_TYPE_SUCCESS,
                (
                    f'Destination "{destination[api_c.ID]}" removed from '
                    f'audience "{audience[db_c.NAME]}" '
                ),
                db_c.NOTIFICATION_CATEGORY_AUDIENCES,
                user[api_c.USER_NAME],
            )

            return Response(), HTTPStatus.NO_CONTENT

        logger.info("Could not delete engagement with ID %s.", audience_id)
        return {api_c.MESSAGE: api_c.OPERATION_FAILED}, HTTPStatus.BAD_REQUEST


@add_view_to_blueprint(
    audience_bp,
    f"/{api_c.AUDIENCE_ENDPOINT}/<audience_id>/{api_c.TOTAL}",
    "AudienceTrendGraphView",
)
class TotalAudienceGraphView(SwaggerView):
    """Total audience insights graph view class."""

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": {"type": "array", "items": TotalCustomersInsightsSchema},
            "description": "Total Audience Insights .",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Total Audience Insights."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Retrieves total audience insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID
            user (dict): User doc

        Returns:
            Tuple[Response, int]: Response list of total audience trend data,
                HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)

        start_date, end_date = get_start_end_dates(request, 9)
        # create a dict for date_filters required by cdp endpoint
        date_filters = {
            api_c.START_DATE: start_date,
            api_c.END_DATE: end_date,
        }

        # get the audience
        audience_id = ObjectId(audience_id)

        audience = get_audience(get_db_client(), audience_id)

        audience_insights_total = get_customers_insights_count_by_day(
            token_response[0],
            date_filters,
            audience.get(db_c.AUDIENCE_FILTERS),
        )

        return (
            jsonify(
                TotalCustomersInsightsSchema().dump(
                    audience_insights_total,
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )


@add_view_to_blueprint(
    audience_bp,
    f"/{api_c.AUDIENCE_ENDPOINT}/<audience_id>/{api_c.REVENUE}",
    "CustomersRevenueInsightsGraphView",
)
class AudienceRevenueInsightsGraphView(SwaggerView):
    """Audience revenue insights graph view class."""

    parameters = [
        {
            "name": api_c.AUDIENCE_ID,
            "description": "Audience ID.",
            "type": "string",
            "in": "path",
            "required": "true",
            "example": "5f5f7262997acad4bac4373b",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": CustomerRevenueInsightsSchema,
            },
            "description": "Audience Revenue Insights .",
        },
        HTTPStatus.BAD_REQUEST.value: {
            "description": "Failed to get Audience Revenue Insights."
        },
    }
    responses.update(AUTH401_RESPONSE)
    responses.update(FAILED_DEPENDENCY_424_RESPONSE)
    tags = [api_c.CUSTOMERS_TAG]

    # pylint: disable=no-self-use
    @api_error_handler()
    @requires_access_levels(api_c.USER_ROLE_ALL)
    def get(self, audience_id: str, user: dict) -> Tuple[Response, int]:
        """Retrieves audience revenue insights.

        ---
        security:
            - Bearer: ["Authorization"]

        Args:
            audience_id (str): Audience ID
            user (dict): User doc

        Returns:
            Tuple[Response, int]: Response list of revenue details by date,
                HTTP status code.
        """

        # get auth token from request
        token_response = get_token_from_request(request)

        start_date, end_date = get_start_end_dates(request, 6)

        audience_id = ObjectId(audience_id)

        audience = get_audience(get_db_client(), audience_id)

        audience_revenue_insight = get_revenue_by_day(
            token_response[0],
            start_date,
            end_date,
            {api_c.AUDIENCE_FILTERS: audience[db_c.AUDIENCE_FILTERS]},
        )

        return (
            jsonify(
                CustomerRevenueInsightsSchema().dump(
                    audience_revenue_insight,
                    many=True,
                )
            ),
            HTTPStatus.OK,
        )
