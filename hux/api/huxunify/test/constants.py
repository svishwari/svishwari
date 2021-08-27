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
INVALID_ID = "invalid_id"
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
        "gender_women": 42345,
        "gender_men": 52567,
        "gender_other": 6953,
    },
    "message": "ok",
}

CUSTOMER_EVENT_RESPONSE = {
    "code": 200,
    "body": [
        {
            "total_event_count": 1,
            "event_type_counts": {
                "abandoned_cart": 0,
                "customer_login": 0,
                "item_purchased": 0,
                "trait_computed": 1,
                "viewed_cart": 0,
                "viewed_checkout": 0,
                "viewed_sale_item": 0,
            },
            "date": "2021-01-01T00:00:00.000Z",
        },
        {
            "total_event_count": 1,
            "event_type_counts": {
                "abandoned_cart": 0,
                "customer_login": 0,
                "item_purchased": 0,
                "trait_computed": 1,
                "viewed_cart": 0,
                "viewed_checkout": 0,
                "viewed_sale_item": 0,
            },
            "date": "2021-01-02T00:00:00.000Z",
        },
    ],
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

SUPPORTED_MODELS = {
    2: {
        api_c.MODEL_TYPE: api_c.LTV,
        api_c.NAME: "Lifetime value",
        api_c.DESCRIPTION: "Predicts the lifetime value of a customer based on models",
        api_c.CURRENT_VERSION: "21.7.28",
        api_c.RMSE: 233.5,
        api_c.AUC: -1,
        api_c.PRECISION: -1,
        api_c.RECALL: -1,
    },
    1: {
        api_c.MODEL_TYPE: api_c.UNSUBSCRIBE,
        api_c.NAME: "Propensity to Unsubscribe",
        api_c.DESCRIPTION: "Predicts how likely a customer will unsubscribe from an email list",
        api_c.CURRENT_VERSION: "21.7.31",
        api_c.RMSE: -1,
        api_c.AUC: 0.79,
        api_c.PRECISION: 0.82,
        api_c.RECALL: 0.65,
    },
    3: {
        api_c.MODEL_TYPE: api_c.PURCHASE,
        api_c.NAME: "Propensity to Purchase",
        api_c.DESCRIPTION: "Propensity of a customer making purchase after receiving an email ",
        api_c.CURRENT_VERSION: "3.1.2",
        api_c.RMSE: -1,
        api_c.AUC: 0.79,
        api_c.PRECISION: 0.82,
        api_c.RECALL: 0.65,
    },
}

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

MOCKED_MODEL_DRIFT = {
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
MOCKED_MODEL_LIFT_CHART = [
    {
        api_c.BUCKET: 100,
        api_c.ACTUAL_VALUE: 2602,
        api_c.ACTUAL_LIFT: 1,
        api_c.PREDICTED_LIFT: 1.0000000895,
        api_c.PREDICTED_VALUE: 2726.7827,
        api_c.PROFILE_COUNT: 95369,
        api_c.ACTUAL_RATE: 0.0272834988,
        api_c.PREDICTED_RATE: 0.0285919189,
        api_c.PROFILE_SIZE_PERCENT: 0,
    }
]

CUSTOMER_INSIGHTS_COUNT_BY_DAY_RESPONSE = {
    "code": 200,
    "body": [
        {
            api_c.RECORDED: "2021-04-01",
            api_c.TOTAL_COUNT: 105080,
            api_c.DIFFERENCE_COUNT: 4321,
        },
        {
            api_c.RECORDED: "2021-04-06",
            api_c.TOTAL_COUNT: 108200,
            api_c.DIFFERENCE_COUNT: 3120,
        },
        {
            api_c.RECORDED: "2021-04-08",
            api_c.TOTAL_COUNT: 111100,
            api_c.DIFFERENCE_COUNT: 2900,
        },
        {
            api_c.RECORDED: "2021-04-11",
            api_c.TOTAL_COUNT: 112300,
            api_c.DIFFERENCE_COUNT: 1200,
        },
        {
            api_c.RECORDED: "2021-05-12",
            api_c.TOTAL_COUNT: 116300,
            api_c.DIFFERENCE_COUNT: 4000,
        },
    ],
}

CUSTOMERS_INSIGHTS_BY_CITY_RESPONSE = {
    "code": 200,
    "body": [
        {
            "city": "New York",
            "state": "NY",
            "country": "US",
            "customer_count": 4321,
            "avg_ltv": 4.0066,
        },
        {
            "city": "Santa Anna",
            "state": "TX",
            "country": "US",
            "customer_count": 4312,
            "avg_ltv": 668.03003,
        },
        {
            "city": "Solon Springs",
            "state": "WI",
            "country": "US",
            "customer_count": 4231,
            "avg_ltv": 648.8791640000001,
        },
        {
            "city": "Gays Mills",
            "state": "WI",
            "country": "US",
            "customer_count": 4213,
            "avg_ltv": 587.3708300000001,
        },
        {
            "city": "Hodgen",
            "state": "OK",
            "country": "US",
            "customer_count": 4132,
            "avg_ltv": 573.278802,
        },
    ],
}

CUSTOMERS_INSIGHTS_BY_STATES_RESPONSE = {
    "code": 200,
    "body": [
        {
            api_c.STATE: "CO",
            api_c.COUNTRY: "US",
            api_c.GENDER_MEN: 2656,
            api_c.GENDER_WOMEN: 2344,
            api_c.GENDER_OTHER: 12,
            api_c.SIZE: 5012,
            api_c.AVG_LTV: 123.43,
        },
        {
            api_c.STATE: "NY",
            api_c.COUNTRY: "US",
            api_c.GENDER_MEN: 605,
            api_c.GENDER_WOMEN: 589,
            api_c.GENDER_OTHER: 40,
            api_c.SIZE: 1234,
            api_c.AVG_LTV: 132.34,
        },
    ],
    "message": "ok",
}

CUSTOMERS_INSIGHTS_BY_CITIES_RESPONSE = {
    "code": 200,
    "body": [
        {
            api_c.CITY: "Bakersfield",
            api_c.STATE: "MD",
            api_c.COUNTRY: "US",
            api_c.CUSTOMER_COUNT: 731098,
            api_c.AVG_LTV: 731000,
        },
        {
            api_c.CITY: "Berkeley",
            api_c.STATE: "CA",
            api_c.COUNTRY: "US",
            api_c.CUSTOMER_COUNT: 4614342,
            api_c.AVG_LTV: 4632145,
        },
    ],
    "message": "ok",
}

IDR_DATAFEEDS_RESPONSE = {
    "code": 200,
    "message": "ok",
    "body": [
        {
            "id": "3",
            "name": "bluecore_email_clicks",
            "datasource_name": "bluecore",
            "new_ids_generated": 1159,
            "total_rec_processed": 1159,
            "match_rate": 0.888,
            "timestamp": "2021-08-05T14:44:42.694Z",
            "datasource_label": "Bluecore",
        },
        {
            "id": "4",
            "name": "bluecore_email_clicks",
            "datasource_name": "bluecore",
            "new_ids_generated": 1133,
            "total_rec_processed": 1133,
            "match_rate": 0.825,
            "timestamp": "2021-08-16T14:45:10.283Z",
            "datasource_label": "Bluecore",
        },
    ],
}

IDR_DATAFEED_DETAILS_RESPONSE = {
    "code": 200,
    "message": "ok",
    "body": {
        "pinning": {
            "input_records": 38,
            "output_records": 28,
            "empty_records": 5,
            "individual_id_match": 5,
            "household_id_match": 6,
            "company_id_match": 47,
            "address_id_match": 35,
            "db_reads": 9,
            "db_writes": 21,
            "filename": "email_analytics_extract_clicks_2021841437.csv",
            "new_individual_ids": 27,
            "new_household_ids": 34,
            "new_company_ids": 46,
            "new_address_ids": 27,
            "process_time": 1.46,
            "pinning_timestamp": "2021-08-05T14:44:42.694Z",
        },
        "stitched": {
            "digital_ids_added": 12,
            "digital_ids_merged": 21,
            "match_rate": 66,
            "merge_rate": 0,
            "records_source": "input waterfall",
            "stitched_timestamp": "2021-08-05T14:44:42.694Z",
        },
    },
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
