# pylint: disable=no-self-use
"""
Paths for the CDM API
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


CDM_TAG = "cdm"
CDM_DESCRIPTION = "CDM API"
DATAFEEDS_TAG = "datafeeds"
DATAFEEDS_ENDPOINT = "datafeeds"
FIELDMAPPINGS_TAG = "fieldmappings"
FIELDMAPPINGS_ENDPOINT = "fieldmappings"
PROCESSED_ITEMS_TAG = "processeditems"
PROCESSED_ITEMS_ENDPOINT = "processeditems"

# setup the cdm blueprint
cdm_bp = Blueprint("cdm", import_name=__name__)


@add_view_to_blueprint(cdm_bp, f"/{DATAFEEDS_ENDPOINT}", "DatafeedSearch")
class DatafeedSearch(SwaggerView):
    """
    Datafeed search class
    """

    parameters = []
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of datafeeds.",
            "schema": Datafeed,
        }
    }
    tags = [DATAFEEDS_TAG]

    @marshal_with(Datafeed(many=True))
    def get(self) -> Tuple[List[dict], int]:
        """Retrieves the data feed catalog.

        ---

        Returns:
            Response: List of datafeeds.

        """
        datafeeds = CdmModel().read_datafeeds()
        return datafeeds, HTTPStatus.OK.value


@add_view_to_blueprint(cdm_bp, f"/{DATAFEEDS_ENDPOINT}/<feed_id>", "DatafeedView")
class DatafeedView(SwaggerView):
    """
    Datafeed view class
    """

    parameters = [
        {
            "name": "feed_id",
            "description": "ID of the datafeed",
            "type": "integer",
            "in": "path",
            "required": "true",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": Datafeed,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    tags = [DATAFEEDS_TAG]

    @marshal_with(Datafeed)
    def get(self, feed_id: int) -> Tuple[List[dict], int]:
        """Retrieves the data feed configuration by ID.

        ---

        Returns:
            Response: Returns a datafeed by ID.

        """
        try:
            valid_id = (
                Datafeed().load({"feed_id": feed_id}, partial=True).get("feed_id")
            )
            data = CdmModel().read_datafeed_by_id(valid_id)

            if not data:
                error = NotFoundError().dump({"message": "Datafeed not found"})
                return error, error["code"]

            return data, HTTPStatus.OK.value

        except ValidationError as err:
            error = RequestError().dump({"errors": err.messages})
            return error, error["code"]


@add_view_to_blueprint(cdm_bp, f"/{FIELDMAPPINGS_ENDPOINT}", "FieldmappingSearch")
class FieldmappingSearch(SwaggerView):
    """
    Fieldmapping Search class
    """

    parameters = []
    responses = {
        HTTPStatus.OK.value: {
            "description": "Returns a datafeed by ID.",
            "schema": Fieldmapping,
        }
    }
    tags = [FIELDMAPPINGS_TAG]

    @marshal_with(Fieldmapping(many=True))
    def get(self) -> Tuple[List[dict], int]:
        """Retrieves the data feed's PII field mappings.

        ---

        Returns:
            Response: Returns a datafeed by ID.

        """
        fieldmappings = CdmModel().read_fieldmappings()
        return fieldmappings, HTTPStatus.OK.value


@add_view_to_blueprint(
    cdm_bp, f"/{FIELDMAPPINGS_ENDPOINT}/<field_id>", "FieldmappingView"
)
class FieldmappingView(SwaggerView):
    """
    Fieldmapping View class
    """

    parameters = [
        {
            "name": "field_id",
            "description": "ID of the fieldmapping",
            "type": "integer",
            "in": "path",
            "required": "true",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": Fieldmapping,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    tags = [FIELDMAPPINGS_TAG]

    @marshal_with(Fieldmapping)
    def get(self, field_id: int) -> Tuple[List[dict], int]:
        """Retrieves the data feed's PII field mapping by ID.

        ---

        Returns:
            Response: Returns a fieldmapping by ID.

        """
        try:
            valid_id = (
                Fieldmapping()
                .load({"field_id": field_id}, partial=True)
                .get("field_id")
            )
            data = CdmModel().read_fieldmapping_by_id(valid_id)

            if not data:
                error = NotFoundError().dump({"message": "Fieldmapping not found"})
                return error, error["code"]

            return data, HTTPStatus.OK.value

        except ValidationError as err:
            error = RequestError().dump({"errors": err.messages})
            return error, error["code"]


@add_view_to_blueprint(cdm_bp, f"/{PROCESSED_ITEMS_ENDPOINT}", "ProcessedDataSearch")
class ProcessedDataSearch(SwaggerView):
    """
    ProcessedData search class
    """

    parameters = []
    responses = {
        HTTPStatus.OK.value: {
            "description": "List of processed data sources.",
            "schema": ProcessedData,
        }
    }
    tags = [PROCESSED_ITEMS_TAG]

    @marshal_with(ProcessedData(many=True))
    def get(self) -> Tuple[List[dict], int]:
        """Retrieves the processed data source catalog.

        ---

        Returns:
            Response: List of processed data sources.

        """
        return CdmModel().read_processed_sources(), HTTPStatus.OK.value


@add_view_to_blueprint(
    cdm_bp, f"/{PROCESSED_ITEMS_ENDPOINT}/<source_name>", "ProcessedDataView"
)
class ProcessedDataView(SwaggerView):
    """
    ProcessedData view class
    """

    parameters = [
        {
            "name": "source_name",
            "description": "name of the data source",
            "type": "string",
            "in": "path",
            "required": "true",
        }
    ]
    responses = {
        HTTPStatus.OK.value: {
            "schema": ProcessedData,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    tags = [PROCESSED_ITEMS_TAG]

    @marshal_with(ProcessedData)
    def get(self, source_name: str) -> Tuple[List[dict], int]:
        """Retrieves the processed data source by name.

        ---

        Returns:
            Response: Returns a processed data source by ID.

        """
        try:
            valid_name = (
                ProcessedData()
                .load({"source_name": source_name}, partial=True)
                .get("source_name")
            )
            data = CdmModel().read_processed_source_by_name(valid_name)

            if not data:
                error = NotFoundError().dump(
                    {"message": "ProcessedData source not found"}
                )
                return error, error["code"]

            return data, HTTPStatus.OK.value

        except ValidationError as err:
            error = RequestError().dump({"errors": err.messages})
            return error, error["code"]
