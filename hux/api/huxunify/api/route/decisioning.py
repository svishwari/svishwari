"""
purpose of this script is for housing the decision routes for the API
"""
import json
from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from
from huxunify.api.model.decisioning import (
    CustomerFeatureModel,
    AlgorithmiaModel,
)
from huxunify.api.schema.decisioning import CustomerFeatureSchema


decision_bp = Blueprint("decision_bp", __name__)


@decision_bp.route("/algorithms", methods=["get"])
@swag_from("../spec/decisioning/algorithms_search.yaml")
def algorithms_search():
    """
    list all available algorithms

    Args:
    Returns:
        The return list of algorithms from algorithmia

    """
    return json.dumps(AlgorithmiaModel().get_algorithms()), 200


@decision_bp.route("/algorithms/<algorithm_name>", methods=["get"])
@swag_from("../spec/decisioning/algorithms_get.yaml")
def algorithm_get(algorithm_name):
    """
    get single algorithm information

    Args:
    Returns:
        The return algorithm information

    """
    return (
        json.dumps(AlgorithmiaModel().get_algorithm(algorithm_name.replace(":", "/"))),
        200,
    )


@decision_bp.route("/algorithms", methods=["post"])
@swag_from("../spec/decisioning/algorithms_post.yaml")
def invoke_algorithm():
    """
    invoke algorithm

    Args:
    Returns:
        The return algorithm information

    """
    # extract params
    algo_name = request.json["algorithm_name"].replace(":", "/")
    params = request.json["params"]

    # run the model
    algo_result = AlgorithmiaModel().invoke_algorithm(algo_name, params)

    # return results
    return json.dumps(algo_result), 200


@decision_bp.route(
    "/features/<cluster_id>/<feature_service_name>/" "<customer_id>", methods=["GET"]
)
@swag_from(
    {
        "parameters": [
            {
                "name": "cluster_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "the tecton cluster name",
                "default": "us-east-1.decisioning-internal",
            },
            {
                "name": "feature_service_name",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "name of the feature service",
                "default": "impression_click_feature_service",
            },
            {
                "name": "customer_id",
                "in": "path",
                "type": "string",
                "description": "customer id",
                "required": "true",
                "default": "",
            },
        ],
        "tags": ["decisioning"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "list all features per customer",
                "schema": CustomerFeatureSchema,
            }
        },
    }
)
def customer_features(cluster_id, feature_service_name, customer_id):
    """
    get customer features
    ---
    """
    result = CustomerFeatureModel(cluster_id, feature_service_name, customer_id)
    result.get_features()
    result.get_feature_vectors()
    return CustomerFeatureSchema().dump(result), 200
