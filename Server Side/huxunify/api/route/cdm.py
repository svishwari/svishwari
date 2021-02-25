"""
purpose of this script is for housing the cdm routes for the API
"""
import json
from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from api.model.cdm import CdmModel
from api.schema.cdm import CdmSchema

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
@swag_from({
    "parameters": [],
    "tags": ["cdm"],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'list all ingested data',
        }
    }
})
def get_ingested_data():
    """
    list all ingested data, record count and blob path

    Args:
    Returns:
        The return list of ingested data from the snowflake database API

    """
    return json.dumps(CdmModel().get_data_sources()), 200
