"""
purpose of this script is for housing the advertising routes for the API
"""
import json
from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from
from huxunify.api.model.advertising import AdvertisingModel
from huxunify.api.schema.advertising import AdvertisingSchema

advertising_bp = Blueprint("advertising_bp", __name__)


@advertising_bp.route("/data-sources", methods=["GET"])
@swag_from(
    {
        "tags": ["advertising performance", "data-sources"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "get all data sources",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def get_data_sources():
    """
    get data sources
    ---
    """
    result = AdvertisingModel()
    data_sources = result.get_data_sources()
    return json.dumps(data_sources), 200


@advertising_bp.route("/data-sources/count", methods=["GET"])
@swag_from(
    {
        "tags": ["advertising performance", "data-sources"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "get count of data sources",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def get_data_sources_count():
    """
    get data sources count
    ---
    """
    result = AdvertisingModel()
    data_sources = result.get_data_sources(count=True)
    return json.dumps(data_sources), 200


@advertising_bp.route("/data-sources", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": "true",
                "schema": {
                    "id": "createDataSource",
                    "required": [],
                    "example": {
                        "data_source_id": "",
                        "data_source_name": "Hux Unified Test",
                        "data_source_type": 1,
                        "data_source_format": "CSV",
                        "fields": [],
                        "location_type": "S3",
                        "location_details": {
                            "BUCKET": "xspdev-amc-pipeline",
                            "KEY": "customers_names_e2e.csv",
                        },
                        "recent_ingestion_job_id": "",
                    },
                },
            },
        ],
        "tags": ["advertising performance", "data-sources"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "create data source",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def create_data_sources():
    """
    create data source
    ---
    """
    result = AdvertisingModel()
    data_sources = result.create_data_source(request.json)
    return json.dumps(data_sources), 200


@advertising_bp.route("/data-sources/<data_source_id>", methods=["PUT"])
@swag_from(
    {
        "parameters": [
            {
                "name": "data_source_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "ID of data source",
                "default": "60382f755830d0e0c6898c53",
            },
            {
                "name": "body",
                "in": "body",
                "required": "true",
                "schema": {
                    "id": "updateDataSource",
                    "required": [],
                    "example": {
                        "data_source_format": "CSV",
                        "data_source_id": "60382f755830d0e0c6898c53",
                        "data_source_name": "Hux Unified Test",
                        "data_source_type": 1,
                        "fields": [],
                        "location_details": {
                            "BUCKET": "xspdev-amc-pipeline",
                            "KEY": "customers_names_e2e.csv",
                        },
                        "location_type": "S3",
                    },
                },
            },
        ],
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "update data source",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def update_data_sources(data_source_id):
    """
    update data source
    ---
    """
    result = AdvertisingModel()
    data_sources = result.update_data_source(data_source_id, request.json)
    return json.dumps(data_sources), 200


@advertising_bp.route("/data-sources", methods=["DELETE"])
@swag_from(
    {
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "delete data source",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def delete_data_source():
    """
    delete data source
    ---
    """
    result = AdvertisingModel()
    data_sources = result.delete_data_source(request.json)
    return json.dumps(data_sources), 200


@advertising_bp.route("/data-sources/<data_source_id>/star", methods=["GET"])
@swag_from(
    {
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "star data source",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def star_data_sources(data_source_id):
    """
    star data source
    ---
    """
    result = AdvertisingModel()
    data_source = result.star_data_source(data_source_id)
    return json.dumps(data_source), 200


@advertising_bp.route("/data-sources/<data_source_id>", methods=["GET"])
@swag_from(
    {
        "parameters": [
            {
                "name": "data_source_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "ID of data source",
                "default": "60382f755830d0e0c6898c53",
            },
        ],
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "validate data source",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def validate_data_source(data_source_id):
    """
    validate data source
    ---
    """
    result = AdvertisingModel()
    data_source = result.validate_data_source(data_source_id)
    return json.dumps(data_source), 200


@advertising_bp.route("/destinations/count", methods=["GET"])
@swag_from(
    {
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "destination count",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def get_destination_count():
    """
    get destination count
    ---
    """
    result = AdvertisingModel()
    data_source = result.get_destination_count()
    return json.dumps(data_source), 200


@advertising_bp.route("/delivery-platforms", methods=["GET"])
@swag_from(
    {
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "get delivery platforms",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def get_delivery_platforms():
    """
    get delivery platforms
    ---
    """
    result = AdvertisingModel()
    data_source = result.get_delivery_platforms()
    return json.dumps(data_source), 200


@advertising_bp.route("/delivery-platforms", methods=["POST"])
@swag_from(
    {
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": "true",
                "schema": {
                    "id": "createDeliveryPlatform",
                    "required": [],
                    "example": {
                        "authentication_details": {
                            "access_token": "MkU!3Ojgwm",
                            "ad_account_id": "111333777",
                            "app_id": "2951925002021888",
                            "app_secret": "717bdOQqZO99",
                        },
                        "delivery_platform_name": "Hux Unified",
                        "delivery_platform_type": "Facebook",
                    },
                },
            },
        ],
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "create delivery platform",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def create_delivery_platforms():
    """
    create delivery platform
    ---
    """
    result = AdvertisingModel()
    data_source = result.create_delivery_platform(request.json)
    return json.dumps(data_source), 200


@advertising_bp.route(
    "/delivery-platforms/<delivery_platform_id>", methods=["PUT"]
)
@swag_from(
    {
        "parameters": [
            {
                "name": "delivery_platform_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "ID of delivery platform",
                "default": "603835e55830d0e0c6898c54",
            },
            {
                "name": "body",
                "in": "body",
                "required": "true",
                "schema": {
                    "id": "updateDeliveryPlatform",
                    "required": [],
                    "example": {
                        "delivery_platform_id": "603835e55830d0e0c6898c54",
                        "delivery_platform_name": "Hux Unified",
                        "delivery_platform_status": "Pending",
                        "delivery_platform_type": "Facebook",
                    },
                },
            },
        ],
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "update delivery platform",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def update_delivery_platforms(delivery_platform_id):
    """
    update delivery platform
    ---
    """
    result = AdvertisingModel()
    data_source = result.update_delivery_platform(
        delivery_platform_id, request.json
    )
    return json.dumps(data_source), 200


@advertising_bp.route(
    "/delivery-platforms/<delivery_platform_id>/star", methods=["POST"]
)
@swag_from(
    {
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "star delivery platform",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def star_delivery_platforms():
    """
    star delivery platform
    ---
    """
    result = AdvertisingModel()
    data_source = result.star_delivery_platform(request.json)
    return json.dumps(data_source), 200


@advertising_bp.route(
    "/delivery-platforms/<delivery_platform_id>", methods=["GET"]
)
@swag_from(
    {
        "parameters": [
            {
                "name": "delivery_platform_id",
                "in": "path",
                "type": "string",
                "required": "true",
                "description": "ID of delivery platform",
                "default": "603835e55830d0e0c6898c54",
            },
        ],
        "tags": ["advertising performance"],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "validate delivery platform",
                "schema": AdvertisingSchema,
            }
        },
    }
)
def validate_delivery_platforms(delivery_platform_id):
    """
    validate delivery platform
    ---
    """
    result = AdvertisingModel()
    data_source = result.validate_delivery_platform(delivery_platform_id)
    return json.dumps(data_source), 200
