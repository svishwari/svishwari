# pylint: disable=invalid-name,line-too-long,too-many-lines
"""
purpose of this file is housing shared components for tests
"""
from datetime import datetime
import time
from http import HTTPStatus
from typing import Generator

import pandas as pd
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
CDM_HEALTHCHECK_CALL = f"{TEST_CONFIG.CDP_SERVICE}/healthcheck"
CUSTOMER_PROFILE_API = f"{TEST_CONFIG.CDP_SERVICE}"

CDM_HEALTHCHECK_RESPONSE = {
    "code": 200,
    "status": "success",
    "message": "ok",
    "hostname": "localhost",
    "timestamp": time.time(),
    "environment": "Development",
    "body": [
        {
            "checker": "check_snowflake_connection",
            "output": "Snowflake up and running.",
            "passed": True,
            "timestamp": time.time(),
            "expires": time.time() + 3600,
            "response_time": 0.012,
        }
    ],
}

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

MOCKED_GENDER_SPENDING = {
    "code": 200,
    "body": [
        {
            "month": 4,
            "year": 2021,
            "avg_spent_men": 231.34,
            "avg_spent_women": 231.34,
            "avg_spent_other": 231.34,
            "gender_men": 542,
            "gender_women": 558,
            "gender_other": 13,
        }
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

MOCKED_MODEL_VERSION_HISTORY_RESPONSE = [
    {
        api_c.ID: 1,
        api_c.LAST_TRAINED: datetime.utcnow(),
        api_c.DESCRIPTION: "Predicts the propensity of a customer",
        api_c.FULCRUM_DATE: datetime.utcnow(),
        api_c.LOOKBACK_WINDOW: 90,
        api_c.NAME: "Propensity",
        api_c.TYPE: api_c.PURCHASE,
        api_c.OWNER: "Susan Miller",
        api_c.STATUS: api_c.STATUS_ACTIVE,
        api_c.CURRENT_VERSION: "21.7.28",
        api_c.PREDICTION_WINDOW: 90,
    },
    {
        api_c.ID: 1,
        api_c.LAST_TRAINED: datetime.utcnow(),
        api_c.DESCRIPTION: "Predicts the propensity of a customer",
        api_c.FULCRUM_DATE: datetime.utcnow(),
        api_c.LOOKBACK_WINDOW: 90,
        api_c.NAME: "Propensity",
        api_c.TYPE: api_c.PURCHASE,
        api_c.OWNER: "Susan Miller",
        api_c.STATUS: api_c.STATUS_ACTIVE,
        api_c.CURRENT_VERSION: "21.7.29",
        api_c.PREDICTION_WINDOW: 90,
    },
    {
        api_c.ID: 1,
        api_c.LAST_TRAINED: datetime.utcnow(),
        api_c.DESCRIPTION: "Predicts the propensity of a customer",
        api_c.FULCRUM_DATE: datetime.utcnow(),
        api_c.LOOKBACK_WINDOW: 90,
        api_c.NAME: "Propensity",
        api_c.TYPE: api_c.PURCHASE,
        api_c.OWNER: "Susan Miller",
        api_c.STATUS: api_c.STATUS_ACTIVE,
        api_c.CURRENT_VERSION: "21.7.30",
        api_c.PREDICTION_WINDOW: 90,
    },
]

MOCKED_MODEL_PROPENSITY_FEATURES = {
    api_c.RESULTS: [
        {
            api_c.FEATURES: [
                "2021-07-28",
                "1to2y-COGS-sum",
                1165.89062,
                "Propensity to Unsubscribe",
                api_c.UNSUBSCRIBE,
                "21.7.28",
            ],
            api_c.JOIN_KEYS: ["21.7.28"],
        },
        {
            api_c.FEATURES: [
                "2021-07-29",
                "1to2y-data_source-orders",
                880.273438,
                "Propensity to Unsubscribe",
                api_c.UNSUBSCRIBE,
                "21.7.29",
            ],
            api_c.JOIN_KEYS: ["21.7.29"],
        },
        {
            api_c.FEATURES: [
                "2021-07-30",
                "1to2y-ITEMQTY-avg",
                210.867187,
                "Propensity to Unsubscribe",
                api_c.UNSUBSCRIBE,
                "21.7.30",
            ],
            api_c.JOIN_KEYS: ["21.7.30"],
        },
        {
            api_c.FEATURES: [
                "2021-07-31",
                "1to2y-COGS-sum",
                364.695312,
                "Propensity to Unsubscribe",
                api_c.UNSUBSCRIBE,
                "21.7.31",
            ],
            api_c.JOIN_KEYS: ["21.7.31"],
        },
    ]
}

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

DATASOURCE_DATA_FEEDS_RESPONSE = {
    "code": 200,
    "message": "ok",
    "body": [
        {
            "datasource_name": "test_data_source",
            "datasource_label": "Test data source",
            "name": "test_datafeed",
            "records_received": 2000000,
            "records_processed": 1800000,
            "thirty_days_avg": 75,
            "processed_at": "2021-08-05T14:44:42.694Z",
            "status": "Active",
        }
    ],
}

CUSTOMER_PROFILE_AUDIENCES_RESPONSE = {
    "code": 200,
    "body": [
        {
            "hux_id": "HUX000000000000001",
            "city_hashed": "0f5d983d203189bbffc5f686d01f6680bc6a83718a515fe42639347efc92478e",
            "country_code_hashed": "c59dc4e44ff99288156d4dff2168f6ac7ddee6b1fc7ccc0754656ffaa6d351ea",
            "date_of_birth_day_hashed": "624b60c58c9d8bfb6ff1886c2fd605d2adeb6ea4da576068201b6c6958ce93f4",
            "date_of_birth_month_hashed": "7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451",
            "date_of_birth_year_hashed": "483029d526219f816e8e8f6a9de07b422633dba180ffc26faac22862a017519f",
            "email_address": "Jesse_Werner@fake.com",
            "email_address_hashed": "96037ced8eee4e0b3517e749e2fd35db6f7dbd6ecda9f20ecda176ffb84c3aab",
            "email_preference": None,
            "first_name": "Jesse",
            "first_name_hashed": "1ecb9e6bdf6cc8088693c11e366415fe5c73662ecdf08f3df337924d8ea26adc",
            "first_name_initial_hashed": "1a24b7688c199c24d87b5984d152b37d1d528911ec852d9cdf98c3ef29b916ea",
            "gender_hashed": "08f271887ce94707da822d5263bae19d5519cb3614e0daedc4c7ce5dab7473f1",
            "last_name": "Werner",
            "last_name_hashed": "31185f00de3ac3ba045fda08bdd47880c3c0820ceebf078c82f05f5b92b0538e",
            "mobile_device_id": "2.64E+12",
            "phone_number_digits_only_hashed": "f068d0cae1fed87a68f1c63e2df680c451de9a124665bbdf8b9054ec2fa92910",
            "postal_code_hashed": "b08fada07188a0a600c2995c16d995e523643b459e3593a44a5f1d7936e1d617",
            "state_or_province_hashed": "9b90fa7f6a8a28309589fcc3dfa530a8dc6b8c2ca9e9cbea3df02f21cd1ca331",
        },
        {
            "hux_id": "HUX000000000000002",
            "city_hashed": "f38ed02476dea1c92ad2dac4aecbc24d2dbc8189fc180e01c97b3096b87daf36",
            "country_code_hashed": "c59dc4e44ff99288156d4dff2168f6ac7ddee6b1fc7ccc0754656ffaa6d351ea",
            "date_of_birth_day_hashed": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
            "date_of_birth_month_hashed": "6b51d431df5d7f141cbececcf79edf3dd861c3b4069f0b11661a3eefacbba918",
            "date_of_birth_year_hashed": "4dea5c7cb70f50322ec9d734aa4aa078be9227c05251e18991c596f387552370",
            "email_address": "Eddie_Pruitt@fake.com",
            "email_address_hashed": "935267d72fd10951be54a353a3e098d2e9ca9a3e856dbf26ecc79bc08ac88652",
            "email_preference": None,
            "first_name": "Eddie",
            "first_name_hashed": "72f1935f451506ea984df8b6026f1f91136db9d3854bcb98e289e52ee392e0cd",
            "first_name_initial_hashed": "1a24b7688c199c24d87b5984d152b37d1d528911ec852d9cdf98c3ef29b916ea",
            "gender_hashed": "08f271887ce94707da822d5263bae19d5519cb3614e0daedc4c7ce5dab7473f1",
            "last_name": "Pruitt",
            "last_name_hashed": "6136ce1b6ce6fd788927800c45bb9cbad2aaf6046f8726da66d235fd9c385769",
            "mobile_device_id": "1.51E+12",
            "phone_number_digits_only_hashed": "71be5464bd0448379dca466293cde3106ebefd6384135e4ee528edd02d9c1af1",
            "postal_code_hashed": "e7c27dc6621e908242f41e8ba9da13916c24167bb901319acc26ba5952dcf711",
            "state_or_province_hashed": "536939ed0e78c5b5d2ee7e26767bbad66290547f9fa1fc6602a1aa95cc61b959",
        },
        {
            "hux_id": "HUX000000000000003",
            "city_hashed": "753cdb88284c6a957ebc2028fa7bc3031a992bd7522db1c400aaacc4180b98ba",
            "country_code_hashed": "c59dc4e44ff99288156d4dff2168f6ac7ddee6b1fc7ccc0754656ffaa6d351ea",
            "date_of_birth_day_hashed": "f5ca38f748a1d6eaf726b8a42fb575c3c71f1864a8143301782de13da2d9202b",
            "date_of_birth_month_hashed": "6b51d431df5d7f141cbececcf79edf3dd861c3b4069f0b11661a3eefacbba918",
            "date_of_birth_year_hashed": "ed823ec32c5d4e9ca9dd968bb0fe9366b7d904ce0cae615308ddd5b89f0e6a3a",
            "email_address": "Rebekah_Walton@fake.com",
            "email_address_hashed": "09adb5f4c9fefd1c750b4bd13b2f0b5947f2bdd0846a1ecc78bc6a4888ea601f",
            "email_preference": None,
            "first_name": "Rebekah",
            "first_name_hashed": "7dd266f4eed4ced1a38c5f2d881711a806136d4790201f22fd624c0fe3296c5e",
            "first_name_initial_hashed": "1a24b7688c199c24d87b5984d152b37d1d528911ec852d9cdf98c3ef29b916ea",
            "gender_hashed": "08f271887ce94707da822d5263bae19d5519cb3614e0daedc4c7ce5dab7473f1",
            "last_name": "Walton",
            "last_name_hashed": "78e7f4c3ed00275487ee8256603813c389495cf825a92335c94046c0a4a99b26",
            "mobile_device_id": "2.32E+12",
            "phone_number_digits_only_hashed": "7982164dd044894ca71a03537e7eca85a9262baee13f4a0ed2281c9b8615148d",
            "postal_code_hashed": "1a72b1e6fb7a12b166b9b25179c8fbaa305c3bd2873786d4611748fadf964bad",
            "state_or_province_hashed": "124e0b7201b0388d7c07f43194b9645d162b77005b66fef7283c689a69ff7c56",
        },
        {
            "hux_id": "HUX000000000000004",
            "city_hashed": "f35b9639a8c001bba5a4d0d2c416e37c3bf5b1b33ca40362e3c858baf12ce0cb",
            "country_code_hashed": "c59dc4e44ff99288156d4dff2168f6ac7ddee6b1fc7ccc0754656ffaa6d351ea",
            "date_of_birth_day_hashed": "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
            "date_of_birth_month_hashed": "19581e27de7ced00ff1ce50b2047e7a567c76b1cbaebabe5ef03f7c3017bb5b7",
            "date_of_birth_year_hashed": "d7c7673ba8ca7b0f04b1af4df026cbea7fed5b8acf59b27d33ef988c60eff054",
            "email_address": "Adam_Rojas@fake.com",
            "email_address_hashed": "2a8cb9f430146c69d7b0838f196fde06c2bd805b5ae0a161787e8546d850c582",
            "email_preference": None,
            "first_name": "Adam",
            "first_name_hashed": "3f0c9b03e8e39b03773c7ea7621035cb6fc947cd41ca7c44056d7e7bbaebb3d4",
            "first_name_initial_hashed": "4da30add745f4fed2dd00bb903b6b092515cce53527ae4b55553db25494f7d9b",
            "gender_hashed": "08f271887ce94707da822d5263bae19d5519cb3614e0daedc4c7ce5dab7473f1",
            "last_name": "Rojas",
            "last_name_hashed": "69eabae5f70de3feb719eb6a56830e8f5813d0aedc70662cdff573d40972adf1",
            "mobile_device_id": "8.05E+12",
            "phone_number_digits_only_hashed": "41b619382e951a396ad2780611b86e52bd6d5a0bf46429281c87d06f71448b0f",
            "postal_code_hashed": "22e4d594b4eca022db5d3098d1762ed191ea8ccabacaa61389928247a6f34e99",
            "state_or_province_hashed": "4b650e5c4785025dee7bd65e3c5c527356717d7a1c0bfef5b4ada8ca1e9cbe17",
        },
        {
            "hux_id": "HUX000000000000005",
            "city_hashed": "8b6e04947230473368190a71c95399a7e9a0c12faa28b04a2dd5a1cc4350a9a9",
            "country_code_hashed": "c59dc4e44ff99288156d4dff2168f6ac7ddee6b1fc7ccc0754656ffaa6d351ea",
            "date_of_birth_day_hashed": "7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451",
            "date_of_birth_month_hashed": "d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
            "date_of_birth_year_hashed": "e78f27ab3ef177a9926e6b90e572b9853ce6cf4d87512836e9ae85807ec9d7fe",
            "email_address": "Robert_Miller@fake.com",
            "email_address_hashed": "8ee0f1c048c2cd72c234600c7384174e3051b4f65fad562811b18a00308fd1c5",
            "email_preference": None,
            "first_name": "Robert",
            "first_name_hashed": "2238dd61a1bf83816b40ad894518814b8edf7221d84d897ffd2c0466ace07c41",
            "first_name_initial_hashed": "1a24b7688c199c24d87b5984d152b37d1d528911ec852d9cdf98c3ef29b916ea",
            "gender_hashed": "08f271887ce94707da822d5263bae19d5519cb3614e0daedc4c7ce5dab7473f1",
            "last_name": "Miller",
            "last_name_hashed": "716545ea5827317b597b9f531b753bb931989bbe63df4307ef312fdb7374a154",
            "mobile_device_id": "7.86E+12",
            "phone_number_digits_only_hashed": "1ff0c029a038e144e194539378b7d9f6d4d5f3ed2093f4a042683ad0bd7c83f1",
            "postal_code_hashed": "6ad677efeef896f3f5b0953333ceea96daad1d68db16431eff436161ef7c4fcb",
            "state_or_province_hashed": "4b650e5c4785025dee7bd65e3c5c527356717d7a1c0bfef5b4ada8ca1e9cbe17",
        },
    ],
    "message": "ok",
}

GOOGLE_ADS_CUSTOMER_DATA = [
    {
        "Email": "935267d72fd10951be54a353a3e098d2e9ca9a3e856dbf26ecc79bc08ac88652",
        "First Name": "72f1935f451506ea984df8b6026f1f91136db9d3854bcb98e289e52ee392e0cd",
        "First Name Initial": "1a24b7688c199c24d87b5984d152b37d1d528911ec852d9cdf98c3ef29b916ea",
        "Last Name": "6136ce1b6ce6fd788927800c45bb9cbad2aaf6046f8726da66d235fd9c385769",
        "Mobile Device ID": 1510000000000.0,
        "Phone": "71be5464bd0448379dca466293cde3106ebefd6384135e4ee528edd02d9c1af1",
        "Zip": "e7c27dc6621e908242f41e8ba9da13916c24167bb901319acc26ba5952dcf711",
    },
    {
        "Email": "927f0a896512fec82acef2f0724387d1afdac73450a0b081ad5ca88d5d38fab2",
        "First Name": "7e11046321fdc323224dd2758e18438c9ebe9f555e71a5ccef31c2cdbe4472ff",
        "First Name Initial": "1a24b7688c199c24d87b5984d152b37d1d528911ec852d9cdf98c3ef29b916ea",
        "Last Name": "266a7b5eddfcd6b1f5dd142fada6c3f6f202056170bda4afc64094ff578edddb",
        "Mobile Device ID": 6310000000000.0,
        "Phone": "14da5103185312fe79204f5dd40ef12acb663820c73b3185fd1f20a6b03ff701",
        "Zip": "4197947a45e5e649e8aeac2dafdabf5b7e59dc2065e27d813fef4cc4bdc4e6ff",
    },
    {
        "Email": "c26b72715ead05ffd3f85a179287d86c8701ae599e2cf67dc8d1c2ba0e39b328",
        "First Name": "9ff18ebe7449349f358e3af0b57cf7a032c1c6b2272cb2656ff85eb112232f16",
        "First Name Initial": "4da30add745f4fed2dd00bb903b6b092515cce53527ae4b55553db25494f7d9b",
        "Last Name": "a15ece678377ef522114d54d7128fca2efac0c818f31bb58102d88105daea9dd",
        "Mobile Device ID": 7460000000000.0,
        "Phone": "8f12a626f14b2240ad54b383699d3d68a32666e9fb3263a2105ce0d4fd8fe785",
        "Zip": "1828f3582065d29550ebab4b20841f7fe0206dfccf74479e5ce5978f5354e614",
    },
    {
        "Email": "fb7b1e8cccdcd0517e9829ac90d7c2c130e4a317158098810b68f1cb9bee5c93",
        "First Name": "a226a2084c6d83e72278aa2c0544817a6b22f4b76cfbf502178c6364abadc75f",
        "First Name Initial": "1a24b7688c199c24d87b5984d152b37d1d528911ec852d9cdf98c3ef29b916ea",
        "Last Name": "2d08caaf28294760dfc04523f37c7c61e8c48d84e54a91e2a41bed6183a6d372",
        "Mobile Device ID": 7320000000000.0,
        "Phone": "bcfcd404f0030389a4fc6a357d492eb0105d4ba43f6ecf798014c18d908a39b7",
        "Zip": "9e1d982069b8a1fc02178003f63bac7fdf8f702a4953cc296111db1c5d421518",
    },
    {
        "Email": "cb6106634ce9cc540b7b83bfa498dbf4bc25a6cff04f59063b944e539609548f",
        "First Name": "ca70c45c591efa030d9425c1337e2dfa14bb4cd096059fcf36be2dde1d253b53",
        "First Name Initial": "1a24b7688c199c24d87b5984d152b37d1d528911ec852d9cdf98c3ef29b916ea",
        "Last Name": "6ca9429ccc8edb19a03022f7c745a0d2c1003a4027da2d85ac58e5d6baae47ff",
        "Mobile Device ID": 7810000000000.0,
        "Phone": "50850b6611eefa86be55172ef5464490dd8ad2ca759d5429d071850de061c607",
        "Zip": "7424fb83627656dd5a2696e4de1c46255cab6eda250046a24b31503460979e10",
    },
]

AMAZON_ADS_CUSTOMER_DATA = [
    {
        "city": "ca32c23c27432bb36ff2ea671ef17063d2b00cc30bb335b27266788daedbbe7f",
        "email": "b5ac494570a6d8220f306d83c45a4d21a63cff4f3eff4a749c86e98d3af38bb6",
        "first_name": "5714e04739071aabdf34a209fcec4c33976a969dd2ca1c5007b406b2d8642bc5",
        "last_name": "c625ca57418821d8e717df1b71bf589a042d8fc0f0a2c3776090e155d2d377d3",
        "phone": "61ea0fd7cf7fa31b9ed691bf423ff9e94b5547839a789b797d6d2376c95e5d05",
        "state": "004c75c4a5cf6faaa9c8a200457de7a8bc4845becf71d5ef6883ef5d3f1caf70",
        "zip": "0ffc78927cb76b71eaae2fda31691eff6eb62fbcc63358749b572419b438e2e9",
    },
    {
        "city": "9e08c091f5c6fb8cd00a45529b46831a620c2cdb68d105d074d7234d771abfc4",
        "email": "bfdcc4b37800bb7552822df775478ddad10faf3cbb6a173bc38a9a2d295fbba8",
        "first_name": "a27f2f3186b073db08c884b76a1a67ab08748cd4249f7a8a4688c71fef588b2e",
        "last_name": "d5f8a8117809078ab45cdd195a22061c2e552c85a3672c89a5fb19f0050eeab3",
        "phone": "52cba7fef1232549a0ff04fb548ef09eb53d7b8fbd55cae80239e0ea95f47d39",
        "state": "004c75c4a5cf6faaa9c8a200457de7a8bc4845becf71d5ef6883ef5d3f1caf70",
        "zip": "93261ebd193cc920ebe6c45ddb8e0ce3405c92af571677a333b6c0500ea61358",
    },
    {
        "city": "2e1efccbeb1a9fdc2340b55cc89db5ca35dadd135b82149a597d4005a2468e78",
        "email": "95942460393ef1b0006b6ddc5157e1839df6dc4759e28db901b30c4bd6f2332f",
        "first_name": "6307ab01368bdf95d382b574131d1223a6ebc16f44394d0dc0fa9361e432434a",
        "last_name": "ceb32b93931ce2ef0af1fcefb67c2e5ea38d67d3fb9424c53d53a0688381636f",
        "phone": "e8d5941e57fe5b2107954e362846a8039e894e8bc9ae949641869a5e7a63b531",
        "state": "004c75c4a5cf6faaa9c8a200457de7a8bc4845becf71d5ef6883ef5d3f1caf70",
        "zip": "876d9daa0b9632d6ad81fb4931cbcf65824374306be20e7f530563db6c3b561f",
    },
    {
        "city": "b34f861bb86dc6d4cdecd92681796397d00f42d67a729fc21b5a595d07dce153",
        "email": "6bbab1b4e28b75ad1b34d5dbce12a6c05c5f17e9652ebbc83c1e8949da2c0869",
        "first_name": "864282b76c39e6748fa8b9accb2953bc89a3ec4f6c5ca1627624d6a58edd5619",
        "last_name": "c78391151cabce66e5d59d7d66ca887f73faaf2d4ddc63e712caa9fbb03f2c0e",
        "phone": "53ca075b81281354ba8bff366a2aa8d55e51c360ff3105db9eb94a18bd4e404e",
        "state": "004c75c4a5cf6faaa9c8a200457de7a8bc4845becf71d5ef6883ef5d3f1caf70",
        "zip": "3a4d4cb0054e390d365952fd4849735694518b5be6eb2d4a961957181fb5974e",
    },
    {
        "city": "1be71e6a8923b2e5c2f0e023fc8d815041d62a0821077b13703e25e43d9d8120",
        "email": "3a98424ef09ac279426a942a6748d564d95ca10ce2afcef14e53ead62e28136e",
        "first_name": "a6b54c20a7b96eeac1a911e6da3124a560fe6dc042ebf270e3676e7095b95652",
        "last_name": "683313d69084379711e47f9e23cc8d7a4cf1a3fac5b48a8b6c560232ef7619a6",
        "phone": "99e3858eb867d7d97b7cf516d184963838ff609e69239dfe67123a40cfe9c222",
        "state": "004c75c4a5cf6faaa9c8a200457de7a8bc4845becf71d5ef6883ef5d3f1caf70",
        "zip": "9b39d0e97edaca4e11daabe538e7faf8a2bffe5d75afe78327409a2c4a820cde",
    },
]

IDR_MATCHING_TRENDS_BY_DAY_DATA = {
    "code": 200,
    "message": "ok",
    api_c.BODY: [
        {
            api_c.DAY: "2021-08-01",
            api_c.UNIQUE_HUX_IDS: 890,
            api_c.ANONYMOUS_IDS: 97,
            api_c.KNOWN_IDS: 890,
        },
        {
            api_c.DAY: "2021-08-02",
            api_c.UNIQUE_HUX_IDS: 906,
            api_c.ANONYMOUS_IDS: 104,
            api_c.KNOWN_IDS: 906,
        },
    ],
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


def dataframe_generator(
    download_type: str, columns: list
) -> Generator[pd.DataFrame, None, None]:
    """Generator yielding data batch from CDP API service.

    Args:
        download_type (str): Download type
        columns (list): column set

    Yields:
        Generator[pd.DataFrame, None, None]: Data batch.
    """

    if download_type == api_c.GOOGLE_ADS:
        yield pd.DataFrame(GOOGLE_ADS_CUSTOMER_DATA, columns=columns)
    elif download_type == api_c.AMAZON_ADS:
        yield pd.DataFrame(AMAZON_ADS_CUSTOMER_DATA, columns=columns)
