"""
purpose of this script is for housing the audience routes for the API
"""
import json
from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from huxunify.api.model.audience import AudienceModel
from huxunify.api.schema.audience import (
    AudienceSchema,
    audience_schema,
    audiences_schema,
    AudienceDeliverySchema,
    audience_delivery_schema,
    audience_delivery_schemas,
    AudienceInsightsSchema,
    audience_insights_schema,
    AudienceDeliveryInsightsSchema,
    audience_delivery_insights_schema,
)

audience_bp = Blueprint("audience_bp", __name__)


@audience_bp.route("/", methods=["GET"])
@swag_from(
    {
        "responses": {
            HTTPStatus.OK.value: {
                "description": "get all audiences",
                "schema": AudienceSchema,
            }
        }
    }
)
def get_audiences():
    """
    get all audiences
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_audiences()
    return jsonify(audiences_schema.dump(data_source)), 200


@audience_bp.route("/<audience_id>", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "audience_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "Audiencce id",
                "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
            },
        ],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "get audience by id  ",
                "schema": AudienceSchema,
            }
        },
    }
)
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


@audience_bp.route("/", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": "true",
                "schema": {
                    "id": "createAudience",
                    "required": [],
                    "example": {
                        "audience_name": "My new audience",
                        "ingestion_job_id": "5f8d9aa93bdaa787b1879242",
                    },
                },
            },
        ],
        "tags": ["advertising performance", "data-sources"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "create audience",
                "schema": AudienceSchema,
            }
        },
    }
)
def create_audiences():
    """
    create audience
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.create_audiences(request.json)
    return jsonify(audience_schema.dump(data_source)), 200


@audience_bp.route("/<audience_id>", methods=["PUT"])
@swag_from(
    {
        "parameters": [
            {
                "name": "audience_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "Audiencce id",
                "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
            },
            {
                "name": "body",
                "in": "body",
                "required": "true",
                "schema": {
                    "id": "updateAudience",
                    "required": [],
                    "example": {
                        "audience_filters": [
                            {"field": "age", "type": "max", "value": 60}
                        ],
                        "audience_name": "string",
                        "audience_type": "string",
                        "created": "2020-10-17T21:54:53.495000+00:00",
                        "updated": "2020-10-17T21:54:53.495000+00:00",
                    },
                },
            },
        ],
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "update audience",
                "schema": AudienceSchema,
            }
        },
    }
)
def update_audience():
    """
    update audience
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.update_audiences(request.json)
    return jsonify(audience_schema.dump(data_source)), 200


@audience_bp.route("/<audience_id>", methods=["DELETE"])
@swag_from(
    {
        "parameters": [
            {
                "name": "audience_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "Audiencce id",
                "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
            },
        ],
        "responses": {HTTPStatus.OK.value: {"description": "delete audience by id  "}},
    }
)
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


@audience_bp.route("/<audience_id>/deliveries", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "audience_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "Audiencce id",
                "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
            },
        ],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "get delivery jobs for an audience",
                "schema": AudienceDeliverySchema,
            }
        },
    }
)
def get_audience_delivery_jobs(audience_id):
    """
    get audience delivery jobs
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_audience_delivery_jobs(audience_id)
    return jsonify(audience_delivery_schemas.dump(data_source)), 200


@audience_bp.route("/<audience_id>/deliveries", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": "true",
                "schema": {
                    "id": "createAudienceDeliveryJob",
                    "required": [],
                    "example": {
                        "delivery_platform_id": "5f5f7262997acad4bac4373b",
                        "created": "2020-10-17T21:54:53.495000+00:00",
                        "updated": "2020-10-17T21:54:53.495000+00:00",
                    },
                },
            },
        ],
        "tags": ["advertising performance", "data-sources"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "create audience delivery job",
                "schema": AudienceDeliverySchema,
            }
        },
    }
)
def create_audience_delivery_job(audience_id):
    """
    create audience
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.create_audience_delivery_job(audience_id, request.json)
    return jsonify(audience_delivery_schema.dump(data_source)), 200


@audience_bp.route("/<audience_id>/deliveries/<delivery_job_id>", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "audience_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "Audience id",
                "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
            },
            {
                "name": "delivery_job_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "Delivery job id",
                "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
            },
        ],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "get delivery job for an audience by id",
                "schema": AudienceDeliverySchema,
            }
        },
    }
)
def get_delivery_job_by_audience_id(audience_id, delivery_job_id):
    """
    get audience delivery jobs
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_delivery_job_by_audience_id(audience_id, delivery_job_id)
    return jsonify(audience_delivery_schema.dump(data_source)), 200


@audience_bp.route("/<audience_id>/insights", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "audience_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "Audiencce id",
                "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
            },
        ],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "retrieve audience insights",
                "schema": AudienceInsightsSchema,
            }
        },
    }
)
def get_audience_insights(audience_id):
    """
    get audience delivery jobs
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_audience_insights(audience_id)
    return jsonify(audience_insights_schema.dump(data_source)), 200


@audience_bp.route(
    "/<audience_id>/deliveries/<delivery_job_id>/insights", methods=["GET"]
)
@swag_from(
    {
        "parameters": [
            {
                "name": "audience_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "Audiencce id",
                "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
            },
            {
                "name": "delivery_job_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "Delivery job id",
                "default": "fdc59077-2c39-4f2b-8cb6-e6b837d93ac0",
            },
        ],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "get delivery job for an audience by id",
                "schema": AudienceDeliveryInsightsSchema,
            }
        },
    }
)
def get_insights_delivery_job_audience_id(audience_id, delivery_job_id):
    """
    get audience delivery job insights
    ---
    tags:
      - Audience API
    """
    result = AudienceModel()
    data_source = result.get_insights_delivery_job_audience_id(
        audience_id, delivery_job_id
    )
    return jsonify(audience_delivery_insights_schema.dump(data_source)), 200


if __name__ == "__main__":
    pass
