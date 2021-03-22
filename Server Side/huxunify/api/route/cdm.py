"""
Paths for the CDM API
"""
import json
from http import HTTPStatus
from flask import Blueprint, jsonify
from flasgger import swag_from
from marshmallow.exceptions import ValidationError
from huxunify.api.model.cdm import CdmModel
from huxunify.api.schema.errors import NotFoundError, RequestError
from huxunify.api.schema.cdm import CdmSchema, Datafeed, Fieldmapping

cdm_bp = Blueprint("cdm_bp", __name__)

CDM_TAG = "cdm"


@cdm_bp.route("/")
@swag_from(
    {
        "tags": [CDM_TAG],
        "responses": {
            HTTPStatus.OK.value: {"description": "cdm api", "schema": CdmSchema}
        },
    }
)
def index():
    """
    cdm api landing
    ---
    """
    result = CdmModel()
    return CdmSchema().dump(result), HTTPStatus.OK.value


@cdm_bp.route("/ingested_data", methods=["get"])
@swag_from("../spec/cdm/ingested_data_search.yaml")
def get_ingested_data():
    """
    List all ingested data, record count and blob path.

    Returns:
        Response: The return list of ingested data.

    """
    return json.dumps(CdmModel().get_data_sources()), HTTPStatus.OK.value


@cdm_bp.route("/datafeeds", methods=["get"])
@swag_from(
    dict(
        responses={
            HTTPStatus.OK.value: {
                "schema": {
                    "type": "array",
                    "items": Datafeed,
                },
            },
        },
        tags=[CDM_TAG],
    )
)
def datafeeds_search():
    """Retrieves the data feed catalog.

    ---

    Returns:
        Response: List of datafeeds.

    """
    datafeeds = CdmModel().read_datafeeds()
    response = [Datafeed().dump(datafeed) for datafeed in datafeeds]
    return jsonify(response), HTTPStatus.OK.value


@cdm_bp.route("/datafeeds/<feed_id>", methods=["get"])
@swag_from(
    dict(
        parameters=[
            {
                "name": "feed_id",
                "description": "ID of the datafeed",
                "type": "integer",
                "in": "path",
                "required": "true",
            },
        ],
        responses={
            HTTPStatus.OK.value: {
                "schema": Datafeed,
            },
            HTTPStatus.NOT_FOUND.value: {
                "schema": NotFoundError,
            },
        },
        tags=[CDM_TAG],
    )
)
def datafeeds_get(feed_id: int):
    """Retrieves the data feed configuration by ID.

    ---

    Args:
        feed_id (int): The datafeed ID.

    Returns:
        Response: Returns a datafeed by ID.

    """
    try:
        valid_id = Datafeed().load({"feed_id": feed_id}, partial=True).get("feed_id")
        data = CdmModel().read_datafeed_by_id(valid_id)

        if not data:
            error = NotFoundError().dump({"message": "Datafeed not found"})
            return error, error["code"]

        return Datafeed().dump(data), HTTPStatus.OK.value

    except ValidationError as err:
        error = RequestError().dump({"errors": err.messages})
        return error, error["code"]


@cdm_bp.route("/fieldmappings", methods=["get"])
@swag_from(
    dict(
        responses={
            HTTPStatus.OK.value: {
                "schema": {
                    "type": "array",
                    "items": Fieldmapping,
                },
            },
        },
        tags=[CDM_TAG],
    )
)
def fieldmappings_search():
    """Retrieves the data feed's PII field mappings

    ---

    Returns:
        Response: List of fieldmappings.

    """
    fieldmappings = CdmModel().read_fieldmappings()
    response = [Fieldmapping().dump(fieldmapping) for fieldmapping in fieldmappings]
    return jsonify(response), HTTPStatus.OK.value


@cdm_bp.route("/fieldmappings/<field_id>", methods=["get"])
@swag_from(
    dict(
        parameters=[
            {
                "name": "field_id",
                "description": "ID of the fieldmapping",
                "type": "integer",
                "in": "path",
                "required": "true",
            },
        ],
        responses={
            HTTPStatus.OK.value: {
                "schema": Fieldmapping,
            },
            HTTPStatus.NOT_FOUND.value: {
                "schema": NotFoundError,
            },
        },
        tags=[CDM_TAG],
    )
)
def fieldmappings_get(field_id: int):
    """Retrieves the data feed's PII field mapping by ID

    ---

    Args:
        field_id (int): The fieldmapping ID.

    Returns:
        Response: Returns a fieldmapping by ID.

    """
    try:
        valid_id = (
            Fieldmapping().load({"field_id": field_id}, partial=True).get("field_id")
        )
        data = CdmModel().read_fieldmapping_by_id(valid_id)

        if not data:
            error = NotFoundError().dump({"message": "Fieldmapping not found"})
            return error, error["code"]

        return Fieldmapping().dump(data), HTTPStatus.OK.value

    except ValidationError as err:
        error = RequestError().dump({"errors": err.messages})
        return error, error["code"]
