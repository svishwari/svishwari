"""
purpose of this script is for housing the advertising routes for the API
"""
import json
from http import HTTPStatus
from flask import Blueprint, request
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


@advertising_bp.route('/data-sources', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get all data sources',
            'schema': AdvertisingSchema
        }
    }
})
def get_data_sources():
    """
    get data sources
    ---
    """
    result = AdvertisingModel()
    data_sources = result.get_data_sources()
    return json.dumps(data_sources), 200


@advertising_bp.route('/data-sources', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'create data source',
            'schema': AdvertisingSchema
        }
    }
})
def create_data_sources():
    """
    get data sources
    ---
    """
    result = AdvertisingModel()
    data_sources = result.create_data_source(request.json)
    return json.dumps(data_sources), 200


@advertising_bp.route('/data-sources', methods=['PUT'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'update data source',
            'schema': AdvertisingSchema
        }
    }
})
def update_data_sources():
    """
    get data sources
    ---
    """
    result = AdvertisingModel()
    data_sources = result.update_data_source(request.json)
    return json.dumps(data_sources), 200


@advertising_bp.route('/data-sources', methods=['DELETE'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'delete data source',
            'schema': AdvertisingSchema
        }
    }
})
def update_data_sources():
    """
    get data sources
    ---
    """
    result = AdvertisingModel()
    data_sources = result.delete_data_source(request.json)
    return json.dumps(data_sources), 200


@advertising_bp.route('/data-sources/<data_source_id>/star', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'star data source',
            'schema': AdvertisingSchema
        }
    }
})
def star_data_sources(data_source_id):
    """
    get data sources
    ---
    """
    result = AdvertisingModel()
    data_source = result.star_data_source(data_source_id)
    return json.dumps(data_source), 200


@advertising_bp.route('/data-sources/<data_source_id>/validate', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'validate data source',
            'schema': AdvertisingSchema
        }
    }
})
def validate_data_source(data_source_id):
    """
    get data sources
    ---
    """
    result = AdvertisingModel()
    data_source = result.validate_data_source(data_source_id)
    return json.dumps(data_source), 200


@advertising_bp.route('/data-sources/<data_source_id>/validate', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'validate data source',
            'schema': AdvertisingSchema
        }
    }
})
def validate_data_source(data_source_id):
    """
    get data sources
    ---
    """
    result = AdvertisingModel()
    data_source = result.validate_data_source(data_source_id)
    return json.dumps(data_source), 200