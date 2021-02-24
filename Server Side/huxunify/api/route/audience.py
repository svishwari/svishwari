"""
purpose of this script is for housing the audience routes for the API
"""
import json
from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from
from api.model.audience import AudienceModel
from api.schema.audience import AudienceSchema, audience_schema, audiences_schema
from flask import jsonify

audience_bp = Blueprint('audience_bp', __name__)

@audience_bp.route('/audience', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get all audiences',
            'schema': AudienceSchema
        }
    }
})
def get_audiences():
    """
    get all audiences
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_audiences()
    print(data_source)
    return jsonify(audiences_schema.dump(data_source)), 200

@audience_bp.route('/audience/<audience_id>', methods=['GET'])
@swag_from({
    "parameters": [
        {
            "name": "audience_id",
            "in": "path",
            "type": "string",
            "required": "true",
            "description": "Audiencce id",
            "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0"
        },
    ],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get audience by id  ',
            'schema': AudienceSchema
        }
    }
})
def get_audience(audience_id):
    """
    get audience by audience id
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_audience_by_id(audience_id)
    return jsonify(audience_schema.dump(data_source)), 200


@audience_bp.route('/count', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get count of all audiences',
            'schema': AudienceSchema
        }
    }
})
def audience_count():
    """
    audience count
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_audience_count()
    return json.dumps(data_source), 200


@audience_bp.route('/audience', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'create audience',
            'schema': AudienceSchema
        }
    }
})
def create_audiences():
    """
    create audience
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.create_audiences(request.json)
    return json.dumps(data_source), 200


@audience_bp.route('/audience', methods=['PUT'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'update audience',
            'schema': AudienceSchema
        }
    }
})
def update_audience():
    """
    update audience
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.update_audiences(request.json)
    return json.dumps(data_source), 200


@audience_bp.route('/audience/<audience_id>', methods=['DELETE'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'delete audience',
            'schema': AudienceSchema
        }
    }
})
def delete_audience(audience_id):
    """
    delete audience
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.delete_audiences(audience_id)
    return json.dumps(data_source), 200


@audience_bp.route('/audience/<audience_id>/star', methods=['DELETE'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'star audience',
            'schema': AudienceSchema
        }
    }
})
def star_audience(audience_id):
    """
    star audience
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.star_audiences(audience_id)
    return json.dumps(data_source), 200


@audience_bp.route('/audience/recent', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get recent audiences',
            'schema': AudienceSchema
        }
    }
})
def recent_audiences():
    """
    get recent audiences
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_recent_audiences()
    return json.dumps(data_source), 200


@audience_bp.route('/audience/star', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get star audiences',
            'schema': AudienceSchema
        }
    }
})
def get_star_audiences():
    """
    get star audiences
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_star_audiences()
    return json.dumps(data_source), 200


@audience_bp.route('/audience/<audience_id>/delivery_jobs', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'get delivery jobs for an audience',
            'schema': AudienceSchema
        }
    }
})
def get_audience_delivery_jobs(audience_id):
    """
    get audience delivery jobs
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_audience_delivery_jobs(audience_id)
    return json.dumps(data_source), 200
