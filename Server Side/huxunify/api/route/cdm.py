"""
Paths for the CDM API
"""
from http import HTTPStatus
from flask import Blueprint
from marshmallow.exceptions import ValidationError
from flask_apispec import marshal_with
from huxunify.api.model.cdm import CdmModel
from huxunify.api.schema.errors import NotFoundError, RequestError
from huxunify.api.schema.cdm import Datafeed, Fieldmapping


CDM_TAG = "cdm"
CDM_DESCRIPTION = "customer data portal API"
DATAFEEDS_TAG = "datafeeds"
FIELDMAPPINGS_TAG = "fieldmappings"

# setup the cdm blueprint
cdm_bp = Blueprint("cdm", import_name=__name__)


@cdm_bp.route("/datafeeds", methods=["get"])
@marshal_with(Datafeed(many=True))
def datafeeds_search():
    """
    ---
    get:
      description: Retrieves the data feed catalog.
      responses:
        '200':
          description: List of datafeeds.
          content:
            application/json:
              schema: Datafeed
      tags:
          - Datafeeds
    """
    datafeeds = CdmModel().read_datafeeds()
    return datafeeds, HTTPStatus.OK.value


@cdm_bp.route("/datafeeds/<feed_id>", endpoint="datafeeds_get")
@marshal_with(Datafeed)
def datafeeds_get(feed_id: int):
    """
    ---
    get:
      description: Retrieves the data feed configuration by ID.
      parameters:
      - name: feed_id
        in: path
        description: ID of the datafeed
        required: true
        type: integer
      responses:
        '200':
          description: Returns a datafeed by ID.
          content:
            application/json:
              schema: Datafeed
        '404':
          content:
            application/json:
              schema: NotFoundError
      tags:
          - Datafeeds
    """
    try:
        valid_id = Datafeed().load({"feed_id": feed_id}, partial=True).get("feed_id")
        data = CdmModel().read_datafeed_by_id(valid_id)

        if not data:
            error = NotFoundError().dump({"message": "Datafeed not found"})
            return error, error["code"]

        return data, HTTPStatus.OK.value

    except ValidationError as err:
        error = RequestError().dump({"errors": err.messages})
        return error, error["code"]


@cdm_bp.route("/fieldmappings", methods=["get"])
@marshal_with(Fieldmapping(many=True))
def fieldmappings_search():
    """
    ---
    get:
      description: Retrieves the data feed's PII field mappings.
      responses:
        '200':
          description: List of fieldmappings.
          content:
            application/json:
              schema: Fieldmapping
      tags:
          - Fieldmappings
    """
    fieldmappings = CdmModel().read_fieldmappings()
    return fieldmappings, HTTPStatus.OK.value


@cdm_bp.route("/fieldmappings/<field_id>", endpoint="fieldmappings_get")
@marshal_with(Fieldmapping)
def fieldmappings_get(field_id: int):
    """
    ---
    get:
      description: Retrieves the data feed's PII field mapping by ID.
      parameters:
      - name: field_id
        in: path
        description: ID of the fieldmapping
        required: true
        type: integer
      responses:
        '200':
          description: Returns a fieldmapping by ID.
          content:
            application/json:
              schema: Fieldmapping
        '404':
          content:
            application/json:
              schema: NotFoundError
      tags:
          - Fieldmappings
    """
    try:
        valid_id = (
            Fieldmapping().load({"field_id": field_id}, partial=True).get("field_id")
        )
        data = CdmModel().read_fieldmapping_by_id(valid_id)

        if not data:
            error = NotFoundError().dump({"message": "Fieldmapping not found"})
            return error, error["code"]

        return data, HTTPStatus.OK.value

    except ValidationError as err:
        error = RequestError().dump({"errors": err.messages})
        return error, error["code"]
