"""
purpose of this script is for housing the advertising routes for the API
"""
from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from api.model.advertising import AdvertisingModel
from api.schema.advertising import AdvertisingSchema

advertising_bp = Blueprint('advertising_bp', __name__)


@advertising_bp.route('/')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'advertising api',
            'schema': AdvertisingSchema
        }
    }
})
def index():
    """
    advertising api landing
    ---
    """
    result = AdvertisingModel()
    return AdvertisingSchema().dump(result), 200
