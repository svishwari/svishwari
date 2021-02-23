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
    create data source
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
    update data source
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
def delete_data_source():
    """
    delete data source
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
    star data source
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
    validate data source
    ---
    """
    result = AdvertisingModel()
    data_source = result.validate_data_source(data_source_id)
    return json.dumps(data_source), 200


@advertising_bp.route('/destinations/count', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'destination count',
            'schema': AdvertisingSchema
        }
    }
})
def get_destination_count():
    """
    get destination count
    ---
    """
    result = AdvertisingModel()
    data_source = result.get_destination_count()
    return json.dumps(data_source), 200


@advertising_bp.route('/delivery-platforms', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get delivery platforms',
            'schema': AdvertisingSchema
        }
    }
})
def get_delivery_platforms():
    """
    get delivery platforms
    ---
    """
    result = AdvertisingModel()
    data_source = result.get_delivery_platforms()
    return json.dumps(data_source), 200


@advertising_bp.route('/delivery-platforms', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'create delivery platform',
            'schema': AdvertisingSchema
        }
    }
})
def create_delivery_platforms():
    """
    create delivery platform
    ---
    """
    result = AdvertisingModel()
    data_source = result.create_delivery_platform(request.json)
    return json.dumps(data_source), 200


@advertising_bp.route('/delivery-platforms', methods=['PUT'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'update delivery platform',
            'schema': AdvertisingSchema
        }
    }
})
def update_delivery_platforms():
    """
    update delivery platform
    ---
    """
    result = AdvertisingModel()
    data_source = result.update_delivery_platform(request.json)
    return json.dumps(data_source), 200


@advertising_bp.route('/delivery-platforms/<delivery_platform_id>/star', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'star delivery platform',
            'schema': AdvertisingSchema
        }
    }
})
def star_delivery_platforms():
    """
    star delivery platform
    ---
    """
    result = AdvertisingModel()
    data_source = result.star_delivery_platform(request.json)
    return json.dumps(data_source), 200


@advertising_bp.route('/delivery-platforms/<delivery_platform_id>/validate', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'validate delivery platform',
            'schema': AdvertisingSchema
        }
    }
})
def validate_delivery_platforms():
    """
    validate delivery platform
    ---
    """
    result = AdvertisingModel()
    data_source = result.validate_delivery_platform(request.json)
    return json.dumps(data_source), 200


@advertising_bp.route('/audiences', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get count of all audiences',
            'schema': AdvertisingSchema
        }
    }
})
def audience_count():
    """
    audience count
    ---
    """
    result = AdvertisingModel()
    data_source = result.get_audience_count()
    return json.dumps(data_source), 200


@advertising_bp.route('/audience', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get all audiences',
            'schema': AdvertisingSchema
        }
    }
})
def get_audiences():
    """
    get all audiences
    ---
    """
    result = AdvertisingModel()
    data_source = result.get_audiences()
    return json.dumps(data_source), 200


@advertising_bp.route('/audience', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'create audience',
            'schema': AdvertisingSchema
        }
    }
})
def create_audiences():
    """
    create audience
    ---
    """
    result = AdvertisingModel()
    data_source = result.create_audiences(request.json)
    return json.dumps(data_source), 200


@advertising_bp.route('/audience', methods=['PUT'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'update audience',
            'schema': AdvertisingSchema
        }
    }
})
def update_audience():
    """
    update audience
    ---
    """
    result = AdvertisingModel()
    data_source = result.update_audiences(request.json)
    return json.dumps(data_source), 200


@advertising_bp.route('/audience/<audience_id>', methods=['DELETE'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'delete audience',
            'schema': AdvertisingSchema
        }
    }
})
def delete_audience(audience_id):
    """
    delete audience
    ---
    """
    result = AdvertisingModel()
    data_source = result.delete_audiences(audience_id)
    return json.dumps(data_source), 200


@advertising_bp.route('/audience/<audience_id>/star', methods=['DELETE'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'star audience',
            'schema': AdvertisingSchema
        }
    }
})
def star_audience(audience_id):
    """
    star audience
    ---
    """
    result = AdvertisingModel()
    data_source = result.star_audiences(audience_id)
    return json.dumps(data_source), 200


@advertising_bp.route('/audience/recent', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get recent audiences',
            'schema': AdvertisingSchema
        }
    }
})
def recent_audiences():
    """
    get recent audiences
    ---
    """
    result = AdvertisingModel()
    data_source = result.get_recent_audiences()
    return json.dumps(data_source), 200


@advertising_bp.route('/audience/star', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get star audiences',
            'schema': AdvertisingSchema
        }
    }
})
def get_star_audiences():
    """
    get star audiences
    ---
    """
    result = AdvertisingModel()
    data_source = result.get_star_audiences()
    return json.dumps(data_source), 200


@advertising_bp.route('/audience/<audience_id>/delivery_jobs', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get delivery jobs for an audience',
            'schema': AdvertisingSchema
        }
    }
})
def get_audience_delivery_jobs(audience_id):
    """
    get audience delivery jobs
    ---
    """
    result = AdvertisingModel()
    data_source = result.get_audience_delivery_jobs(audience_id)
    return json.dumps(data_source), 200
