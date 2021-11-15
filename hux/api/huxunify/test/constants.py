# pylint: disable=invalid-name,line-too-long,too-many-lines
"""Purpose of this file is housing shared components for tests."""
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
INVALID_OKTA_RESPONSE = {"active": False}
VALID_USER_RESPONSE = {
    api_c.OKTA_ID_SUB: "8548bfh8d",
    api_c.EMAIL: "davesmith@fake.com",
    api_c.NAME: "dave smith",
    api_c.USER_PII_ACCESS: True,
}
# response missing some fields
INVALID_USER_RESPONSE = {
    api_c.EMAIL: "davesmith@fake.com",
}
INVALID_ID = "invalid_id"
BATCH_RESPONSE = {"ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value}}
TEST_CONFIG = get_config(api_c.TEST_MODE)
INTROSPECT_CALL = f"{TEST_CONFIG.OKTA_ISSUER}/oauth2/v1/introspect?client_id={TEST_CONFIG.OKTA_CLIENT_ID}"
USER_INFO_CALL = f"{TEST_CONFIG.OKTA_ISSUER}/oauth2/v1/userinfo"
CDM_HEALTHCHECK_CALL = f"{TEST_CONFIG.CDP_SERVICE}/healthcheck"
CUSTOMER_PROFILE_API = f"{TEST_CONFIG.CDP_SERVICE}"

HUX = "HUX"
CDP_CUSTOMER_PROFILE = "CDP_CUSTOMER_PROFILE"
CDP_CONNECTIONS = "CDP_CONNECTIONS"
CONTRACTS_DIR = "contracts"
CDP_CUSTOMERS_CONTRACTS_DIR = "cdp_customers"
CDP_CONNECTIONS_CONTRACTS_DIR = "cdp_connections"
TECTON_CONTRACTS_DIR = "tecton"
CUSTOMER_PROFILE_COUNT_BY_STATE_ENDPOINT = (
    "/customer-profiles/insights/count-by-state"
)
CDP_CUSTOMER_PROFILES_AUDIENCE_COUNT = "/customer-profiles/audience/count"
CDP_CUSTOMER_PROFILE_BASE_ENDPOINT = "/customer-profiles/"
CUSTOMER_PROFILE_COUNT_BY_DAY = "/customer-profiles/insights/count-by-day"
CUSTOMER_PROFILE_SPENDING_BY_MONTH = (
    "/customer-profiles/insights/spending-by-month"
)
CUSTOMER_PROFILE_CITY_LTVS = "/customer-profiles/insights/city-ltvs"
CDP_CONNECTIONS_DATA_SOURCES_ENDPOINT = "/connections/datasources"
CDP_CONNECTIONS_DATA_SOURCE_DATA_FEEDS_ENDPOINT = (
    "/connections/{data_source_name}/data_feeds"
)
CDP_IDENTITY_DATA_FEEDS_ENDPOINT = "/identity/datafeeds"
CDP_IDENTITY_DATA_FEEDS_FEED_ID_ENDPOINT = "/identity/datafeeds/{feed_id}"
CDP_IDENTITY_ID_COUNT_BY_DAY_ENDPOINT = "/identity/id-count-by-day"

AUDIENCE_STATE_FILTER = {"field": "state", "type": "equals", "value": "HI"}

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
        api_c.ID: "1",
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
        api_c.ID: "2",
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
    "2": {
        api_c.MODEL_TYPE: api_c.LTV,
        api_c.NAME: "Lifetime value",
        api_c.DESCRIPTION: "Predicts the lifetime value of a customer based on models",
        api_c.CURRENT_VERSION: "21.7.28",
        api_c.RMSE: 233.5,
        api_c.AUC: -1,
        api_c.PRECISION: -1,
        api_c.RECALL: -1,
    },
    "1": {
        api_c.MODEL_TYPE: api_c.UNSUBSCRIBE,
        api_c.NAME: "Propensity to Unsubscribe",
        api_c.DESCRIPTION: "Predicts how likely a customer will unsubscribe from an email list",
        api_c.CURRENT_VERSION: "21.7.31",
        api_c.RMSE: -1,
        api_c.AUC: 0.79,
        api_c.PRECISION: 0.82,
        api_c.RECALL: 0.65,
    },
    "3": {
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
        "feature_service_name": api_c.FEATURE_DRIFT_REGRESSION_MODEL_SERVICE,
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
        "feature_service_name": api_c.FEATURE_DRIFT_CLASSIFICATION_MODEL_SERVICE,
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

MOCKED_MODEL_PROPENSITY_FEATURES_NEGATIVE_SCORE = {
    api_c.RESULTS: [
        {
            api_c.FEATURES: [
                "2021-07-28",
                "1to2y-COGS-sum",
                -1165.89062,
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
                -880.273438,
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
                -210.867187,
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
                -364.695312,
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

CUSTOMERS_INSIGHTS_BY_COUNTRIES_RESPONSE = {
    "code": 200,
    "body": [
        {api_c.NAME: "Test Country", api_c.SIZE: 1234, api_c.LTV: 324.45}
    ],
    "message": "ok",
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

DATASOURCES_RESPONSE = {
    "code": 200,
    "message": "Data Sources Fetched successfully",
    "body": [
        {
            api_c.LABEL: "Data source 1",
            api_c.NAME: "test_data_source_1",
            api_c.STATUS: "Active",
        },
        {
            api_c.LABEL: "Data source 2",
            api_c.NAME: "test_data_source_2",
            api_c.STATUS: "Active",
        },
        {
            api_c.LABEL: "Data source 3",
            api_c.NAME: "test_data_source_3",
            api_c.STATUS: "Pending",
        },
        {
            api_c.LABEL: "Data source 4",
            api_c.NAME: "test_data_source_4",
            api_c.STATUS: "Pending",
        },
    ],
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
            "address": "791 Alvarez Lodge Suite 915",
            "address_hashed": "af40e2a7215b360de090234869aa4d93863128763f98c4b122f22af9b0619a74",
            "city_hashed": "0f5d983d203189bbffc5f686d01f6680bc6a83718a515fe42639347efc92478e",
            "country_code_hashed": "c59dc4e44ff99288156d4dff2168f6ac7ddee6b1fc7ccc0754656ffaa6d351ea",
            "date_of_birth_day_hashed": "624b60c58c9d8bfb6ff1886c2fd605d2adeb6ea4da576068201b6c6958ce93f4",
            "date_of_birth_month_hashed": "7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451",
            "date_of_birth_year_hashed": "483029d526219f816e8e8f6a9de07b422633dba180ffc26faac22862a017519f",
            "email_address": "Jesse_Werner@fake.com",
            "email_address_hashed": "96037ced8eee4e0b3517e749e2fd35db6f7dbd6ecda9f20ecda176ffb84c3aab",
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
            "address": "055 Andrew Forge Apt. 751",
            "address_hashed": "5b25653aed93a58635872f27657f4f758db72a5dbbf14398d2b36674ee9cdc2e",
            "city_hashed": "f38ed02476dea1c92ad2dac4aecbc24d2dbc8189fc180e01c97b3096b87daf36",
            "country_code_hashed": "c59dc4e44ff99288156d4dff2168f6ac7ddee6b1fc7ccc0754656ffaa6d351ea",
            "date_of_birth_day_hashed": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
            "date_of_birth_month_hashed": "6b51d431df5d7f141cbececcf79edf3dd861c3b4069f0b11661a3eefacbba918",
            "date_of_birth_year_hashed": "4dea5c7cb70f50322ec9d734aa4aa078be9227c05251e18991c596f387552370",
            "email_address": "Eddie_Pruitt@fake.com",
            "email_address_hashed": "935267d72fd10951be54a353a3e098d2e9ca9a3e856dbf26ecc79bc08ac88652",
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
            "address": "79871 Valerie Lock Apt. 414",
            "address_hashed": "bcbdc1b0d8da208ad44418dc2205556bedf83489b862c28625b189710eb4347e",
            "city_hashed": "753cdb88284c6a957ebc2028fa7bc3031a992bd7522db1c400aaacc4180b98ba",
            "country_code_hashed": "c59dc4e44ff99288156d4dff2168f6ac7ddee6b1fc7ccc0754656ffaa6d351ea",
            "date_of_birth_day_hashed": "f5ca38f748a1d6eaf726b8a42fb575c3c71f1864a8143301782de13da2d9202b",
            "date_of_birth_month_hashed": "6b51d431df5d7f141cbececcf79edf3dd861c3b4069f0b11661a3eefacbba918",
            "date_of_birth_year_hashed": "ed823ec32c5d4e9ca9dd968bb0fe9366b7d904ce0cae615308ddd5b89f0e6a3a",
            "email_address": "Rebekah_Walton@fake.com",
            "email_address_hashed": "09adb5f4c9fefd1c750b4bd13b2f0b5947f2bdd0846a1ecc78bc6a4888ea601f",
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
            "address": "2681 Debra Harbor Suite 978",
            "address_hashed": "f0b3644678262a73f927925849fa0be497279e325ee43a5671134127a234beab",
            "city_hashed": "f35b9639a8c001bba5a4d0d2c416e37c3bf5b1b33ca40362e3c858baf12ce0cb",
            "country_code_hashed": "c59dc4e44ff99288156d4dff2168f6ac7ddee6b1fc7ccc0754656ffaa6d351ea",
            "date_of_birth_day_hashed": "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
            "date_of_birth_month_hashed": "19581e27de7ced00ff1ce50b2047e7a567c76b1cbaebabe5ef03f7c3017bb5b7",
            "date_of_birth_year_hashed": "d7c7673ba8ca7b0f04b1af4df026cbea7fed5b8acf59b27d33ef988c60eff054",
            "email_address": "Adam_Rojas@fake.com",
            "email_address_hashed": "2a8cb9f430146c69d7b0838f196fde06c2bd805b5ae0a161787e8546d850c582",
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
            "address": "1953 Peter Roads Apt. 807",
            "address_hashed": "044d8cbd63d727f0bde5dd18da809912165cc55a6f9f6c0385e88f1589aecbe4",
            "city_hashed": "8b6e04947230473368190a71c95399a7e9a0c12faa28b04a2dd5a1cc4350a9a9",
            "country_code_hashed": "c59dc4e44ff99288156d4dff2168f6ac7ddee6b1fc7ccc0754656ffaa6d351ea",
            "date_of_birth_day_hashed": "7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451",
            "date_of_birth_month_hashed": "d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
            "date_of_birth_year_hashed": "e78f27ab3ef177a9926e6b90e572b9853ce6cf4d87512836e9ae85807ec9d7fe",
            "email_address": "Robert_Miller@fake.com",
            "email_address_hashed": "8ee0f1c048c2cd72c234600c7384174e3051b4f65fad562811b18a00308fd1c5",
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

SCHEDULES = [
    {
        api_c.PERIODICIY: api_c.DAILY,
        api_c.EVERY: 2,
        api_c.HOUR: 3,
        api_c.MINUTE: 4,
        api_c.PERIOD: api_c.PM,
    },
    {
        api_c.PERIODICIY: api_c.WEEKLY,
        api_c.EVERY: 2,
        api_c.HOUR: 3,
        api_c.MINUTE: 4,
        api_c.PERIOD: api_c.PM,
        api_c.DAY_OF_WEEK: api_c.DAY_LIST[0:2],
    },
]

DAILY_SCHEDULE_INVALID = {
    api_c.PERIODICIY: api_c.DAILY,
    api_c.EVERY: 2,
    api_c.HOUR: 300,
    api_c.MINUTE: 400,
    api_c.PERIOD: api_c.PM,
}

BATCH_NUMBER_BAD_PARAM = "12a"
BATCH_SIZE_BAD_PARAM = "100@"

REVENUE = "revenue"


def validate_schema(
    schema: Schema, response_json: dict, is_multiple: bool = False
) -> bool:
    """Validate if the response confirms with the given schema.

    Args:
        schema (Schema): Instance of the Schema to validate against.
        response_json (dict): Response json as dict.
        is_multiple (bool): If response is a collection of objects.

    Returns:
        (bool): True/False.
    """

    try:
        schema.load(response_json, many=is_multiple)
        return True
    except ValidationError:
        return False


def dataframe_generator() -> Generator[pd.DataFrame, None, None]:
    """Generator yielding data batch from CDP API service.

    Args:


    Yields:
        Generator[pd.DataFrame, None, None]: Data batch.
    """

    yield pd.DataFrame(CUSTOMER_PROFILE_AUDIENCES_RESPONSE.get(api_c.BODY))


def dataframe_method() -> pd.DataFrame:
    """Method returning data batch from CDP API service.

    Args:


    Returns:
        pd.DataFrame: Data batch.
    """
    return pd.DataFrame(CUSTOMER_PROFILE_AUDIENCES_RESPONSE.get(api_c.BODY))
