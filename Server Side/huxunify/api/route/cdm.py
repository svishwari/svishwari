"""
Paths for the CDM API
"""
import json
from http import HTTPStatus
from flask import Blueprint, jsonify
from flasgger import swag_from
from huxunify.api.model.cdm import CdmModel
from huxunify.api.schema.errors import NotFoundError
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
    datafeed = CdmModel().read_datafeed_by_id(feed_id)

    if not datafeed:
        return (
            NotFoundError().dump({"message": "Datafeed not found"}),
            HTTPStatus.NOT_FOUND.value,
        )

    return Datafeed().dump(datafeed), HTTPStatus.OK.value


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


@cdm_bp.route("/fieldmappings/<fieldmapping_id>", methods=["get"])
@swag_from(
    dict(
        parameters=[
            {
                "name": "fieldmapping_id",
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
def fieldmappings_get(fieldmapping_id: int):
    """Retrieves the data feed's PII field mapping by ID

    ---

    Args:
        fieldmapping_id (int): The fieldmapping ID.

    Returns:
        Response: Returns a fieldmapping by ID.

    """
    fieldmapping = CdmModel().read_fieldmapping_by_id(fieldmapping_id)

    if not fieldmapping:
        return (
            NotFoundError().dump({"message": "Fieldmapping not found"}),
            HTTPStatus.NOT_FOUND.value,
        )

    return Fieldmapping().dump(fieldmapping), HTTPStatus.OK.value
