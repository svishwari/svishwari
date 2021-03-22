"""
Paths for the CDM API
"""
from http import HTTPStatus
from flask import Blueprint
from marshmallow.exceptions import ValidationError
from flask_apispec import marshal_with, doc
from huxunify.api.model.cdm import CdmModel
from huxunify.api.schema.errors import NotFoundError, RequestError
from huxunify.api.schema.cdm import Datafeed, Fieldmapping


CDM_TAG = "cdm"
CDM_DESCRIPTION = "customer data portal API"
DATAFEEDS_TAG = "datafeeds"
FIELDMAPPINGS_TAG = "fieldmappings"

# setup the cdm blueprint
cdm_bp = Blueprint("cdm", __name__, url_prefix="/")


@cdm_bp.route("/datafeeds", methods=["get"], provide_automatic_options=False)
@doc(description="Retrieves the data feed catalog.", tags=[DATAFEEDS_TAG])
@marshal_with(Datafeed(many=True))
def datafeeds_search():
    """Retrieves the data feed catalog.

    ---

    Returns:
        Response: List of datafeeds.

    """
    datafeeds = CdmModel().read_datafeeds()
    return datafeeds, HTTPStatus.OK.value


@cdm_bp.route(
    "/datafeeds/<feed_id>", endpoint="datafeeds_get", provide_automatic_options=False
)
@doc(
    description="Retrieves the data feed configuration by ID.",
    tags=[DATAFEEDS_TAG],
    parameters=[
        {
            "name": "feed_id",
            "description": "ID of the datafeed",
            "type": "integer",
            "in": "path",
            "required": "true",
        }
    ],
    responses={
        HTTPStatus.OK.value: {
            "schema": Datafeed,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    },
)
@marshal_with(Datafeed)
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

        return data, HTTPStatus.OK.value

    except ValidationError as err:
        error = RequestError().dump({"errors": err.messages})
        return error, error["code"]


@cdm_bp.route("/fieldmappings", methods=["get"], provide_automatic_options=False)
@doc(
    description="Retrieves the data feed's PII field mappings",
    tags=[FIELDMAPPINGS_TAG],
    responses={
        HTTPStatus.OK.value: {
            "schema": {
                "type": "array",
                "items": Fieldmapping,
            },
        },
    },
)
@marshal_with(Fieldmapping(many=True))
def fieldmappings_search():
    """Retrieves the data feed's PII field mappings

    ---

    Returns:
        Response: List of fieldmappings.

    """
    fieldmappings = CdmModel().read_fieldmappings()
    return fieldmappings, HTTPStatus.OK.value


@cdm_bp.route(
    "/fieldmappings/<field_id>",
    endpoint="fieldmappings_get",
    provide_automatic_options=False,
)
@doc(
    description="Retrieves the data feed's PII field mapping by ID",
    tags=[FIELDMAPPINGS_TAG],
    params={
        "field_id": {
            "description": "ID of the fieldmapping",
            "type": "integer",
            "in": "path",
            "required": "true",
        },
    },
    responses={
        HTTPStatus.OK.value: {
            "schema": Fieldmapping,
        },
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    },
)
@marshal_with(Fieldmapping)
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

        return data, HTTPStatus.OK.value

    except ValidationError as err:
        error = RequestError().dump({"errors": err.messages})
        return error, error["code"]
