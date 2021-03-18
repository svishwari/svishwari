"""
purpose of this script is for housing the cdm routes for the API
"""
import json
from http import HTTPStatus
from flask import Blueprint, jsonify
from flasgger import swag_from
from huxunify.api.model.cdm import CdmModel
from huxunify.api.schema.cdm import CdmSchema, Fieldmapping

cdm_bp = Blueprint('cdm_bp', __name__)


@cdm_bp.route('/')
@swag_from({
    "tags": ["cdm"],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'cdm api',
            'schema': CdmSchema
        }
    }
})
def index():
    """
    cdm api landing
    ---
    """
    result = CdmModel()
    return CdmSchema().dump(result), 200


@cdm_bp.route('/ingested_data', methods=['get'])
@swag_from("../spec/cdm/ingested_data_search.yaml")
def get_ingested_data():
    """
    List all ingested data, record count and blob path.

    Returns:
        Response: The return list of ingested data.

    """
    return json.dumps(CdmModel().get_data_sources()), 200


@cdm_bp.route("/datafeeds", methods=["get"])
@swag_from("../spec/cdm/datafeeds_search.yaml")
def datafeeds_search():
    """Endpoint returning a list of datafeeds.

    Returns:
        datafeeds (Response): List of datafeeds.
    """
    datafeeds = CdmModel().read_datafeeds()
    return json.dumps(datafeeds), 200


@cdm_bp.route("/datafeeds/<feed_id>", methods=["get"])
@swag_from("../spec/cdm/datafeeds_get.yaml")
def datafeeds_get(feed_id: int):
    """Endpoint returning a datafeed by ID.

    Args:
        feed_id (int): The datafeed ID.

    Returns:
        Response: Returns a datafeed by ID.

    """
    datafeed = CdmModel().read_datafeed_by_id(feed_id)

    if not datafeed:
        return "Data feed not found", 404

    return json.dumps(datafeed), 200


@cdm_bp.route("/fieldmappings", methods=["get"])
@swag_from(dict(
    responses={
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": {
                    "$ref": Fieldmapping,
                },
            }
        },
    },
    tags=["cdm"],
))
def fieldmappings_search():
    """Endpoint returning a list of fieldmappings.

    Returns:
        Response: List of fieldmappings.

    """
    fieldmappings = CdmModel().read_fieldmappings()
    response = [
        Fieldmapping().dump(fieldmapping)
        for fieldmapping in fieldmappings
    ]
    return jsonify(response), 200


@cdm_bp.route("/fieldmappings/<fieldmapping_id>", methods=["get"])
@swag_from(dict(
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
            "schema": Fieldmapping
        },
    },
    tags=["cdm"],
))
def fieldmappings_get(fieldmapping_id: int):
    """Endpoint returning a fieldmapping by ID.

    Args:
        fieldmapping_id (int): The fieldmapping ID.

    Returns:
        Response: Returns a fieldmapping by ID.

    """
    fieldmapping = CdmModel().read_fieldmapping_by_id(fieldmapping_id)

    if not fieldmapping:
        return "Fieldmapping not found", 404

    return Fieldmapping().dump(fieldmapping), 200
