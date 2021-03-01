"""
purpose of this script is for housing the decision routes for the API
"""
from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from
from huxunify.api.model.decision import DecisionModel, CustomerFeatureModel
from huxunify.api.schema.decision import DecisionSchema, CustomerFeatureSchema


decision_bp = Blueprint('decision_bp', __name__)


@decision_bp.route('/')
@swag_from({
    "tags": ["decisioning"],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'decision api',
            'schema': DecisionSchema
        }
    }
})
def index():
    """
    decision api landing
    ---
    """
    result = DecisionModel()
    return DecisionSchema().dump(result), 200


@decision_bp.route('/features/<cluster_id>/<feature_service_name>/<customer_id>',
                   methods=['GET'])
@swag_from({
    "parameters": [
        {
            "name": "cluster_id",
            "in": "path",
            "type": "string",
            "required": "true",
            "description": "the tecton cluster name",
            "default": "us-east-1.decisioning-internal"
        },
        {
            "name": "feature_service_name",
            "in": "path",
            "type": "string",
            "required": "true",
            "description": "name of the feature service",
            "default": "impression_click_feature_service"
        },
        {
            "name": "customer_id",
            "in": "path",
            "type": "string",
            "description": "customer id",
            "required": "true",
            "default": ""
        }
    ],
    "tags": ["decisioning"],
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'list all features per customer',
            'schema': CustomerFeatureSchema
        }
    }
})
def customer_features(cluster_id, feature_service_name, customer_id):
    """
    get customer features
    ---
    """
    result = CustomerFeatureModel(cluster_id, feature_service_name, customer_id)
    result.get_features()
    result.get_feature_vectors()
    return CustomerFeatureSchema().dump(result), 200
