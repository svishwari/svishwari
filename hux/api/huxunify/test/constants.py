# pylint: disable=invalid-name
"""
purpose of this file is housing shared components for tests
"""
from http import HTTPStatus
from dateutil import parser

from marshmallow import Schema, ValidationError

from huxunify.api.config import get_config
import huxunify.api.constants as api_c

BASE_ENDPOINT = "/api/v1"
TEST_AUTH_TOKEN = "Bearer 12345678"
AUTH_HEADER = {
    "Authorization": TEST_AUTH_TOKEN,
}
STANDARD_HEADERS = {
    "Authorization": TEST_AUTH_TOKEN,
    "Content-Type": "application/json",
}
VALID_RESPONSE = {
    "active": True,
    "scope": "openid email profile",
    "username": "davesmith",
    "exp": 1234,
    "iat": 12345,
    "sub": "davesmith@fake",
    "aud": "sample_aud",
    "iss": "sample_iss",
    "jti": "sample_jti",
    "token_type": "Bearer",
    "client_id": "1234",
    "uid": "1234567",
}
VALID_USER_RESPONSE = {
    api_c.OKTA_ID_SUB: "8548bfh8d",
    api_c.EMAIL: "davesmith@fake.com",
    api_c.NAME: "dave smith",
}
# response missing some fields
INVALID_USER_RESPONSE = {
    api_c.EMAIL: "davesmith@fake.com",
}
BATCH_RESPONSE = {"ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value}}
TEST_CONFIG = get_config("TEST")
INTROSPECT_CALL = "{}/oauth2/v1/introspect?client_id={}".format(
    TEST_CONFIG.OKTA_ISSUER, TEST_CONFIG.OKTA_CLIENT_ID
)
USER_INFO_CALL = f"{TEST_CONFIG.OKTA_ISSUER}/oauth2/v1/userinfo"

CUSTOMER_INSIGHT_RESPONSE = {
    "code": 200,
    "body": {
        "total_records": 20238,
        "match_rate": 0.05,
        "total_unique_ids": 14238,
        "total_unknown_ids": 4515,
        "total_known_ids": 13620,
        "total_individual_ids": 313,
        "total_household_ids": 9927,
        "updated": "2021-05-24",
        "total_customers": 3329,
        "total_countries": 2,
        "total_us_states": 44,
        "total_cities": 2513,
        "min_age": 18,
        "max_age": 66,
        "gender_women": 0.42,
        "gender_men": 0.52,
        "gender_other": 0.06,
    },
    "message": "ok",
}

CUSTOMER_GEO_RESPONSE = [
    {
        "name": "Alabama",
        "population_percentage": "0.046",
        "size": "123456",
        "women": "0.6057",
        "men": "0.6057",
        "others": "0.6057",
        "ltv": "1234.5",
    }
]

MOCKED_MODEL_RESPONSE = [
    {
        api_c.ID: 1,
        api_c.NAME: "Model1",
        api_c.DESCRIPTION: "Test Model",
        api_c.STATUS: api_c.OPERATION_SUCCESS.lower(),
        api_c.LATEST_VERSION: "0.1.1",
        api_c.PAST_VERSION_COUNT: 0,
        api_c.LAST_TRAINED: parser.isoparse("2021-06-22T11:33:19.658Z"),
        api_c.OWNER: "HUX Unified",
        api_c.LOOKBACK_WINDOW: 365,
        api_c.PREDICTION_WINDOW: 365,
        api_c.FULCRUM_DATE: parser.isoparse("2021-06-22T11:33:19.658Z"),
        api_c.TYPE: "test",
    },
    {
        api_c.ID: 2,
        api_c.NAME: "Model2",
        api_c.DESCRIPTION: "Test Model",
        api_c.STATUS: api_c.OPERATION_SUCCESS.lower(),
        api_c.LATEST_VERSION: "0.1.1",
        api_c.PAST_VERSION_COUNT: 0,
        api_c.LAST_TRAINED: parser.isoparse("2021-06-22T11:33:19.658Z"),
        api_c.OWNER: "HUX Unified",
        api_c.LOOKBACK_WINDOW: 365,
        api_c.PREDICTION_WINDOW: 365,
        api_c.FULCRUM_DATE: parser.isoparse("2021-06-22T11:33:19.658Z"),
        api_c.TYPE: "test",
    },
]

MOCKED_MODEL_VERSION_HISTORY = {
    "results": [
        {
            "features": [
                "2021-07-28",
                "Propensity of a customer unsubscribing after "
                "receiving an email.",
                "2021-07-14",
                "90",
                "HUS",
                "Propensity to Unsubscribe",
                "unsubscribe",
                "Susan Miller",
                "smiller@xyz.com",
                "Stopped",
            ],
            "joinKeys": ["21.7.28"],
        },
        {
            "features": [
                "2021-07-29",
                "Propensity of a customer unsubscribing after "
                "receiving an email.",
                "2021-07-15",
                "90",
                "HUS",
                "Propensity to Unsubscribe",
                "unsubscribe",
                "Susan Miller",
                "smiller@xyz.com",
                "Active",
            ],
            "joinKeys": ["21.7.29"],
        },
        {
            "features": [
                "2021-07-30",
                "Propensity of a customer unsubscribing after "
                "receiving an email.",
                "2021-07-16",
                "90",
                "HUS",
                "Propensity to Unsubscribe",
                "unsubscribe",
                "Susan Miller",
                "smiller@xyz.com",
                "Active",
            ],
            "joinKeys": ["21.7.30"],
        },
        {
            "features": [
                "2021-07-31",
                "Propensity of a customer unsubscribing after "
                "receiving an email.",
                "2021-07-17",
                "90",
                "HUS",
                "Propensity to Unsubscribe",
                "unsubscribe",
                "Susan Miller",
                "smiller@xyz.com",
                "Active",
            ],
            "joinKeys": ["21.7.31"],
        },
    ]
}

MOCKED_CITY_LTVS_RESPONSE = {
    "code": 200,
    "body": [
        {
            "city": "Santa Anna",
            "state": "TX",
            "country": "US",
            "avg_ltv": 668.03003,
        },
        {
            "city": "Solon Springs",
            "state": "WI",
            "country": "US",
            "avg_ltv": 648.8791640000001,
        },
        {
            "city": "Gays Mills",
            "state": "WI",
            "country": "US",
            "avg_ltv": 587.3708300000001,
        },
        {
            "city": "Hodgen",
            "state": "OK",
            "country": "US",
            "avg_ltv": 573.278802,
        },
        {
            "city": "Noonan",
            "state": "ND",
            "country": "US",
            "avg_ltv": 554.679386,
        },
    ],
    "message": "ok",
}

MOCKED_MODEL_PERFORMANCE_LTV = {
    "results": [
        {
            "features": [
                233.5,
                "2021-07-28",
                "Lifetime Value",
                "ltv",
                "21.7.28",
            ],
            "joinKeys": ["21.7.28"],
        },
        {
            "features": [
                263.3,
                "2021-07-29",
                "Lifetime Value",
                "ltv",
                "21.7.29",
            ],
            "joinKeys": ["21.7.29"],
        },
        {
            "features": [
                215.5,
                "2021-07-30",
                "Lifetime Value",
                "ltv",
                "21.7.30",
            ],
            "joinKeys": ["21.7.30"],
        },
    ]
}
MOCKED_MODEL_LTV_PAYLOAD = {
    "params": {
        "feature_service_name": "ui_metadata_model_metrics_regression_service",
        "join_key_map": {"model_id": "2"},
    }
}
MOCKED_MODEL_PERFORMANCE_UNSUBSCRIBE = {
    "results": [
        {
            "features": [
                0.84,
                "2021-07-28",
                "Propensity to Unsubscribe",
                "unsubscribe",
                "21.7.28",
                0.71,
                0.65,
            ],
            "joinKeys": ["21.7.28"],
        },
        {
            "features": [
                0.86,
                "2021-07-29",
                "Propensity to Unsubscribe",
                "unsubscribe",
                "21.7.29",
                0.72,
                0.6,
            ],
            "joinKeys": ["21.7.29"],
        },
        {
            "features": [
                0.81,
                "2021-07-30",
                "Propensity to Unsubscribe",
                "unsubscribe",
                "21.7.30",
                0.68,
                0.63,
            ],
            "joinKeys": ["21.7.30"],
        },
        {
            "features": [
                0.85,
                "2021-07-31",
                "Propensity to Unsubscribe",
                "unsubscribe",
                "21.7.31",
                0.71,
                0.58,
            ],
            "joinKeys": ["21.7.31"],
        },
    ]
}
MOCKED_MODEL_UNSUBSCRIBE_PAYLOAD = {
    "params": {
        "feature_service_name": "ui_metadata_model_metrics_classification_service",
        "join_key_map": {"model_id": "1"},
    }
}
MOCKED_MODEL_LIFT_CHART = {
    "results": [
        {
            "features": [
                473,
                "2021-07-28",
                9.8904656039,
                10.9989444799,
                "Propensity to Unsubscribe",
                "unsubscribe",
                "21.7.28",
                1.1080349364,
                524.1005,
                "929",
                0.5091496233,
                0.5641555704,
                None,
                0.010112885,
            ],
            "joinKeys": ["21.7.28"],
        },
        {
            "features": [
                409,
                "2021-07-29",
                11.6350193534,
                11.3862761707,
                "Propensity to Unsubscribe",
                "unsubscribe",
                "21.7.29",
                1.0195305785,
                416.988,
                "801",
                0.5106117353,
                0.5205842779,
                None,
                0.0086094779,
            ],
            "joinKeys": ["21.7.29"],
        },
        {
            "features": [
                1564,
                "2021-07-30",
                4.6436564324,
                4.3823760685,
                "Propensity to Unsubscribe",
                "unsubscribe",
                "21.7.30",
                0.9998591977,
                1563.7798,
                "9471",
                0.1651356773,
                0.1651124258,
                0.4643705463,
                None,
            ],
            "joinKeys": ["21.7.30"],
        },
        {
            "features": [
                1205,
                "2021-07-31",
                4.6310044773,
                4.6780061124,
                "Propensity to Unsubscribe",
                "unsubscribe",
                "21.7.31",
                1.0585924331,
                1275.6039,
                "9537",
                0.1263500052,
                0.1337531595,
                0.4631053036,
                None,
            ],
            "joinKeys": ["21.7.31"],
        },
    ]
}


def validate_schema(
    schema: Schema, response_json: dict, is_multiple: bool = False
) -> bool:
    """
    Validate if the response confirms with the given schema

    Args:
        schema (Schema): Instance of the Schema to validate against
        response_json (dict): Response json as dict
        is_multiple (bool): If response is a collection of objects

    Returns:
        (bool): True/False
    """

    try:
        schema.load(response_json, many=is_multiple)
        return True
    except ValidationError:
        return False
