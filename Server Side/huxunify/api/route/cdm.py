"""
purpose of this script is for housing the cdm routes for the API
"""
from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from api.model.cdm import CdmModel
from api.schema.cdm import CdmSchema

cdm_bp = Blueprint('cdm_bp', __name__)


@cdm_bp.route('/')
@swag_from({
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
