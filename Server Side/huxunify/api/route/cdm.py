"""
purpose of this script is for housing the cdm routes for the API
"""
import json
from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from huxunify.api.model.cdm import CdmModel
from huxunify.api.schema.cdm import CdmSchema

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
    list all ingested data, record count and blob path

    Args:
    Returns:
        The return list of ingested data from the snowflake database API

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

    Returns:
        datafeed (Response): Return a datafeed by ID.
    """
    datafeed = CdmModel().read_datafeed_by_id(feed_id)

    if not datafeed:
        return "Data feed not found", 404

    return json.dumps(datafeed), 200


if __name__ == '__main__':
    pass
