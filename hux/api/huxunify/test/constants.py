# pylint: disable=invalid-name,line-too-long,too-many-lines
"""Purpose of this file is housing shared components for tests."""
from datetime import datetime
import time
from http import HTTPStatus
from typing import Generator

import pandas as pd
from dateutil import parser

from marshmallow import Schema, ValidationError

import huxunifylib.database.constants as db_c
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
VALID_INTROSPECTION_RESPONSE = {
    "active": True,
    "scope": "openid email profile",
    "username": "user1",
    "exp": 1234,
    "iat": 12345,
    "sub": "user1_admin@deloitte.com",
    "aud": "sample_aud",
    "iss": "sample_iss",
    "jti": "sample_jti",
    "token_type": "Bearer",
    "client_id": "1234",
    "uid": "00u7acrr5pEmJ09lc2p7",
}
VALID_VIEWER_INTROSPECTION_RESPONSE = {
    "active": True,
    "scope": "openid email profile",
    "username": "user1",
    "exp": 1234,
    "iat": 12345,
    "sub": "user1_viewer@deloitte.com",
    "aud": "sample_aud",
    "iss": "sample_iss",
    "jti": "sample_jti",
    "token_type": "Bearer",
    "client_id": "1234",
    "uid": "00u7acrr5pEmJ09lc2p7",
}
VALID_EDITOR_INTROSPECTION_RESPONSE = {
    "active": True,
    "scope": "openid email profile",
    "username": "user1",
    "exp": 1234,
    "iat": 12345,
    "sub": "user1_editor@deloitte.com",
    "aud": "sample_aud",
    "iss": "sample_iss",
    "jti": "sample_jti",
    "token_type": "Bearer",
    "client_id": "1234",
    "uid": "00u7acrr5pEmJ09lc2p7",
}
INVALID_INTROSPECTION_RESPONSE = {"active": False}
VALID_USER_RESPONSE = {
    api_c.OKTA_ID_SUB: VALID_INTROSPECTION_RESPONSE[api_c.OKTA_UID],
    api_c.EMAIL: VALID_INTROSPECTION_RESPONSE[api_c.OKTA_ID_SUB],
    api_c.NAME: "USER 1",
    api_c.ROLE: db_c.USER_ROLE_ADMIN,
    api_c.USER_PII_ACCESS: True,
}
VALID_VIEWER_USER_RESPONSE = {
    api_c.OKTA_ID_SUB: VALID_INTROSPECTION_RESPONSE[api_c.OKTA_UID],
    api_c.EMAIL: VALID_INTROSPECTION_RESPONSE[api_c.OKTA_ID_SUB],
    api_c.NAME: "VIEWER USER",
    api_c.ROLE: db_c.USER_ROLE_VIEWER,
    api_c.USER_PII_ACCESS: True,
}
VALID_EDITOR_USER_RESPONSE = {
    api_c.OKTA_ID_SUB: VALID_EDITOR_INTROSPECTION_RESPONSE[api_c.OKTA_UID],
    api_c.EMAIL: VALID_EDITOR_INTROSPECTION_RESPONSE[api_c.OKTA_ID_SUB],
    api_c.NAME: "EDITOR USER",
    api_c.ROLE: db_c.USER_ROLE_EDITOR,
    api_c.USER_PII_ACCESS: True,
}
VALID_TRUSTID_USER_RESPONSE = {
    api_c.OKTA_ID_SUB: VALID_EDITOR_INTROSPECTION_RESPONSE[api_c.OKTA_UID],
    api_c.EMAIL: VALID_EDITOR_INTROSPECTION_RESPONSE[api_c.OKTA_ID_SUB],
    api_c.NAME: "TRUSTID USER",
    api_c.ROLE: db_c.USER_ROLE_TRUSTID,
    api_c.USER_PII_ACCESS: True,
}
# response missing some fields
INVALID_USER_RESPONSE = {
    api_c.EMAIL: "davesmith@fake.com",
}
TEST_USER_NAME = "test_user"

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
CITY_ZIP_STUB_DATA = [
    "33332,Fort Lauderdale,FL",
    "60305,River Forest,IL",
    "30417,Claxton,GA",
]

SOURCE_NAME = "source_name"
SOURCE_SIZE = "source_size"
SOURCE_ID = "source_id"

TICKETS = "tickets"

TRAINED_DATE = "trained_date"

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
        "total_customers": 3329,
        "total_countries": 2,
        "total_us_states": 44,
        "total_cities": 2513,
        "min_age": 18,
        "max_age": 66,
        "avg_age": 40,
        "gender_women": 42345,
        "gender_men": 52567,
        "gender_other": 6953,
        "max_ltv_actual": 998.79824,
        "max_ltv_predicted": 1069.68824,
        "min_ltv_actual": 0.00072,
        "min_ltv_predicted": 70.89072,
    },
    "message": "ok",
}

IDENTITY_INSIGHT_RESPONSE = {
    "code": 200,
    "body": {
        "total_records": 273326,
        "match_rate": 0.87,
        "total_unique_ids": 49974,
        "total_anonymous_ids": 6326,
        "total_address_ids": 1614,
        "total_individual_ids": 1614,
        "total_household_ids": 1760,
        "updated": "2021-12-17T02:50:52.777Z",
    },
    "message": "ok",
}
EVENT_TYPES_RESPONSE = {
    "code": 200,
    "body": [
        {api_c.TYPE: "traits_analysed", api_c.LABEL: "Traits Analysed"},
        {api_c.TYPE: "sales_made", api_c.LABEL: "Sales Made"},
    ],
}
CUSTOMER_EVENT_BY_DAY_RESPONSE = {
    "code": 200,
    "body": [
        {
            "total_event_count": 1,
            "event_type_counts": {
                api_c.ABANDONED_CART: 0,
                api_c.PRODUCT_SEARCHED: 0,
                api_c.PURCHASE: 0,
                api_c.SALE: 1,
                api_c.TRAIT: 0,
                api_c.VIEW_CONTENT: 0,
                api_c.VIEWED_CHECKOUT_EVENT: 0,
            },
            "date": "2021-01-01T00:00:00.000Z",
        },
        {
            "total_event_count": 1,
            "event_type_counts": {
                api_c.ABANDONED_CART: 0,
                api_c.PRODUCT_SEARCHED: 0,
                api_c.PURCHASE: 0,
                api_c.SALE: 1,
                api_c.TRAIT: 0,
                api_c.VIEW_CONTENT: 0,
                api_c.VIEWED_CHECKOUT_EVENT: 0,
            },
            "date": "2021-01-02T00:00:00.000Z",
        },
    ],
    "message": "ok",
}

CUSTOMER_EVENT_BY_WEEK_RESPONSE = {
    "code": 200,
    "body": [
        {
            "total_event_count": 1,
            "event_type_counts": {
                api_c.ABANDONED_CART: 0,
                api_c.PRODUCT_SEARCHED: 0,
                api_c.PURCHASE: 0,
                api_c.SALE: 1,
                api_c.TRAIT: 0,
                api_c.VIEW_CONTENT: 0,
                api_c.VIEWED_CHECKOUT_EVENT: 0,
            },
            "date": "2021-12-28T00:00:00.000Z",
        },
        {
            "total_event_count": 1,
            "event_type_counts": {
                api_c.ABANDONED_CART: 0,
                api_c.PRODUCT_SEARCHED: 0,
                api_c.PURCHASE: 0,
                api_c.SALE: 1,
                api_c.TRAIT: 0,
                api_c.VIEW_CONTENT: 0,
                api_c.VIEWED_CHECKOUT_EVENT: 0,
            },
            "date": "2021-01-18T00:00:00.000Z",
        },
    ],
    "message": "ok",
}

CUSTOMER_EVENT_BY_MONTH_RESPONSE = {
    "code": 200,
    "body": [
        {
            "total_event_count": 1,
            "event_type_counts": {
                api_c.ABANDONED_CART: 0,
                api_c.PRODUCT_SEARCHED: 0,
                api_c.PURCHASE: 0,
                api_c.SALE: 1,
                api_c.TRAIT: 0,
                api_c.VIEW_CONTENT: 0,
                api_c.VIEWED_CHECKOUT_EVENT: 0,
            },
            "date": "2021-01-01T00:00:00.000Z",
        },
        {
            "total_event_count": 1,
            "event_type_counts": {
                api_c.ABANDONED_CART: 0,
                api_c.PRODUCT_SEARCHED: 0,
                api_c.PURCHASE: 0,
                api_c.SALE: 1,
                api_c.TRAIT: 0,
                api_c.VIEW_CONTENT: 0,
                api_c.VIEWED_CHECKOUT_EVENT: 0,
            },
            "date": "2021-03-01T00:00:00.000Z",
        },
    ],
    "message": "ok",
}

SAMPLE_CUSTOMER_ID = "HUX123456789012345"
CUSTOMER_PROFILE_RESPONSE = {
    "code": 200,
    "body": {
        api_c.HUX_ID: "HUX123456789012345",
        api_c.FIRST_NAME: "Bertie",
        api_c.LAST_NAME: "Fox",
        api_c.EMAIL: "fake@fake.com",
        api_c.GENDER: "test_gender",
        api_c.CITY: "test_city",
        api_c.ADDRESS: "test_address",
        api_c.AGE: "test_age",
        api_c.IDENTITY_RESOLUTION: {
            api_c.NAME: {
                api_c.PERCENTAGE: 0.26,
                api_c.COUNT: 23,
                api_c.DATA_SOURCE: [
                    {
                        api_c.ID: "585t749997acad4bac4373b",
                        api_c.NAME: "Netsuite",
                        api_c.TYPE: "Net-suite",
                        api_c.PERCENTAGE: 0.49,
                        api_c.COUNT: 15,
                    },
                    {
                        api_c.ID: "685t749997acad4bac4373b",
                        api_c.NAME: "Aqfer",
                        api_c.TYPE: "Aqfer",
                        api_c.PERCENTAGE: 0.51,
                        api_c.COUNT: 5,
                    },
                ],
                api_c.CO_OCCURRENCES: [
                    {
                        api_c.IDENTIFIER: "address",
                        api_c.COUNT: 10,
                        api_c.PERCENTAGE: 0.5,
                    },
                    {
                        api_c.IDENTIFIER: "email",
                        api_c.COUNT: 10,
                        api_c.PERCENTAGE: 0.5,
                    },
                ],
            },
            api_c.ADDRESS: {
                api_c.PERCENTAGE: 0.2,
                api_c.COUNT: 12,
                api_c.DATA_SOURCE: [],
                api_c.CO_OCCURRENCES: [],
            },
            "email": {
                api_c.PERCENTAGE: 0.34,
                api_c.COUNT: 2,
                api_c.DATA_SOURCE: [],
                api_c.CO_OCCURRENCES: [],
            },
            "phone": {
                api_c.PERCENTAGE: 0.14,
                api_c.COUNT: 7,
                api_c.DATA_SOURCE: [],
                api_c.CO_OCCURRENCES: [],
            },
            "cookie": {
                api_c.PERCENTAGE: 0.1,
                api_c.COUNT: 5,
                api_c.DATA_SOURCE: [],
                api_c.CO_OCCURRENCES: [],
            },
        },
        api_c.PREFERENCE_EMAIL: True,
        api_c.PREFERENCE_PUSH: True,
        api_c.PREFERENCE_SMS: True,
        api_c.PREFERENCE_IN_APP: False,
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
        api_c.ID: "1",
        api_c.NAME: "Model1",
        api_c.DESCRIPTION: "Test Model",
        api_c.STATUS: api_c.STATUS_ACTIVE,
        api_c.LATEST_VERSION: "0.1.1",
        api_c.PAST_VERSION_COUNT: 0,
        api_c.LAST_TRAINED: parser.isoparse("2021-06-22T11:33:19.658Z"),
        api_c.OWNER: "HUX Unified",
        api_c.LOOKBACK_WINDOW: 365,
        api_c.PREDICTION_WINDOW: 365,
        api_c.FULCRUM_DATE: parser.isoparse("2021-06-22T11:33:19.658Z"),
        api_c.TYPE: "test",
        api_c.TAGS: dict(industry=[api_c.HEALTHCARE, api_c.RETAIL]),
    },
    {
        api_c.ID: "2",
        api_c.NAME: "Model2",
        api_c.DESCRIPTION: "Test Model",
        api_c.STATUS: api_c.STATUS_ACTIVE,
        api_c.LATEST_VERSION: "0.1.1",
        api_c.PAST_VERSION_COUNT: 0,
        api_c.LAST_TRAINED: parser.isoparse("2021-06-22T11:33:19.658Z"),
        api_c.OWNER: "HUX Unified",
        api_c.LOOKBACK_WINDOW: 365,
        api_c.PREDICTION_WINDOW: 365,
        api_c.FULCRUM_DATE: parser.isoparse("2021-06-22T11:33:19.658Z"),
        api_c.TYPE: "other",
        api_c.TAGS: dict(industry=[api_c.HOSPITALITY, api_c.AUTOMOTIVE]),
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

DEN_API_SUPPORT_MODELS = ["model-Propensity_Type_Cancelled-v5-dev"]

MOCKED_MODEL_VERSION_HISTORY = {
    "results": [
        {
            "features": [
                None,
                "2021-10-13 18:59:30",
                "Predicts the propensity of a customer to unsubscribe",
                "2021-10-05",
                "60",
                "HUS",
                "Unsubscribe Model",
                "unsubscribe",
                "Decisioning",
                "decisioning@fake.com",
                "7",
                "success",
            ],
            "joinKeys": ["21.10.12"],
        },
        {
            "features": [
                None,
                "2021-11-08 14:53:56",
                "Predicts the propensity of a customer to unsubscribe",
                "2021-10-28",
                "60",
                "HUS",
                "Unsubscribe Model",
                "unsubscribe",
                "Decisioning",
                "decisioning@fake.com",
                "7",
                "success",
            ],
            "joinKeys": ["21.11.04"],
        },
        {
            "features": [
                "2021-11-14",
                "2021-11-15 17:21:06",
                "Predicts the propensity of a customer to unsubscribe",
                "2021-11-07",
                "60",
                "HUS",
                "Unsubscribe Model",
                "unsubscribe",
                "Decisioning",
                "decisioning@fake.com",
                "7",
                "success",
            ],
            "joinKeys": ["21.11.14"],
        },
    ]
}

MOCKED_MODEL_DRIFT = {
    "results": [
        {
            "features": [
                233.5,
                None,
                "2021-07-28",
                "Lifetime Value",
                "ltv",
                "21.10.12",
            ],
            "joinKeys": ["21.10.12"],
        },
        {
            "features": [
                263.3,
                None,
                "2021-07-29",
                "Lifetime Value",
                "ltv",
                "21.11.04",
            ],
            "joinKeys": ["21.11.04"],
        },
        {
            "features": [
                215.5,
                "2021-07-30",
                "2021-07-30",
                "Lifetime Value",
                "ltv",
                "21.11.14",
            ],
            "joinKeys": ["21.11.14"],
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
            "customer_count": 123,
            "avg_ltv": 668.03003,
        },
        {
            "city": "Solon Springs",
            "state": "WI",
            "country": "US",
            "customer_count": 123,
            "avg_ltv": 648.8791640000001,
        },
        {
            "city": "Gays Mills",
            "state": "WI",
            "country": "US",
            "customer_count": 123,
            "avg_ltv": 587.3708300000001,
        },
        {
            "city": "Hodgen",
            "state": "OK",
            "country": "US",
            "customer_count": 123,
            "avg_ltv": 573.278802,
        },
        {
            "city": "Noonan",
            "state": "ND",
            "country": "US",
            "customer_count": 123,
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

MOCKED_GENDER_SPENDING_BY_DAY = {
    "code": 200,
    "body": [
        {
            "date": "2021-07-19T00:00:00.000Z",
            "avg_spent_men": 25.311363636363637,
            "avg_spent_women": 24.12727272727273,
            "avg_spent_other": 26.400000000000002,
            "gender_men": 44,
            "gender_women": 33,
            "gender_other": 2,
        }
    ],
}

MOCKED_CUSTOMER_EVENT_TYPES = {
    "code": 200,
    "body": [
        {"type": "viewed_checkout", "label": "Viewed checkout"},
        {"type": "traits_analysed", "label": "Trait"},
        {"type": "sales_made", "label": "Sale"},
    ],
}

MOCKED_MODEL_PERFORMANCE_LTV = {
    "results": [
        {
            "features": [
                233.5,
                "2021-07-28",
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
                "2021-07-30",
                "Lifetime Value",
                "ltv",
                "21.7.30",
            ],
            "joinKeys": ["21.7.30"],
        },
    ]
}

MOCKED_MODEL_PERFORMANCE_UNSUBSCRIBE = {
    "results": [
        {
            "features": [
                0.84,
                "2021-07-28",
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

MOCKED_MODEL_VERSION_HISTORY_RESPONSE_PROPENSITY = [
    {
        "data_date": "2011-06-01",
        "important_features": [
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "duration_days-order-min",
                "feature_description": "'min' days past since positive 'order' event from 'transactions' data source",
                "feature_presence": 1.0,
                "gain": 113.02790584775039,
                "lift": 113.02790584775039,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 0,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "1to2y-Quantity-min",
                "feature_description": "'min' aggregate value of 'Quantity' field in 'between last 1 to 2 years'",
                "feature_presence": 0.46885245901639344,
                "gain": 186.53200713524205,
                "lift": 87.45599023062168,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 1,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "2w-Quantity-sum",
                "feature_description": "'sum' aggregate value of 'Quantity' field in 'last 2 weeks'",
                "feature_presence": 0.19672131147540983,
                "gain": 335.1365024442348,
                "lift": 65.92849228411175,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 2,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "2w-Quantity-cnt",
                "feature_description": "'count' aggregate value of 'Quantity' field in 'last 2 weeks'",
                "feature_presence": 0.19672131147540983,
                "gain": 201.10058238181955,
                "lift": 39.56077030462024,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 3,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "1w-Type-Transaction",
                "feature_description": "count of 'Transaction' value of 'Type' field in 'last week'",
                "feature_presence": 0.0994535519125683,
                "gain": 396.93738801870495,
                "lift": 39.47683312535754,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 4,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "2w-Price-max",
                "feature_description": "'max' aggregate value of 'Price' field in 'last 2 weeks'",
                "feature_presence": 0.19672131147540983,
                "gain": 192.57344831928822,
                "lift": 37.88330130871243,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 5,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "4to8m-Quantity-max",
                "feature_description": "'max' aggregate value of 'Quantity' field in 'from last 4 to 8 months'",
                "feature_presence": 0.7213114754098361,
                "gain": 38.67998148257969,
                "lift": 27.900314512024696,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 6,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "2m-Quantity-avg",
                "feature_description": "'avg' aggregate value of 'Quantity' field in 'last 2 months'",
                "feature_presence": 0.5562841530054645,
                "gain": 46.62166872716506,
                "lift": 25.93489549959237,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 7,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "4to8m-positive-order",
                "feature_description": "'order' defined as positive event in 'transactions' in 'from last 4 to 8 months'",
                "feature_presence": 0.7136612021857923,
                "gain": 35.8568759546662,
                "lift": 25.58966120043391,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 8,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "dow-u_dow-Wednesday",
                "feature_description": "'Wednesday' 'count of all events' in 'Day of Week bucket'",
                "feature_presence": 0.5540983606557377,
                "gain": 38.207675310120656,
                "lift": 21.17081025380456,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 9,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "4m-Quantity-sum",
                "feature_description": "'sum' aggregate value of 'Quantity' field in 'last 4 months'",
                "feature_presence": 0.7825136612021858,
                "gain": 26.870200555966147,
                "lift": 21.026299014286078,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 10,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "4m-Quantity-cnt",
                "feature_description": "'count' aggregate value of 'Quantity' field in 'last 4 months'",
                "feature_presence": 0.7825136612021858,
                "gain": 23.762871099615047,
                "lift": 18.59477126483538,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 11,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "2m-Quantity-min",
                "feature_description": "'min' aggregate value of 'Quantity' field in 'last 2 months'",
                "feature_presence": 0.5562841530054645,
                "gain": 33.230965533256864,
                "lift": 18.48585951522158,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 12,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "4to8m-Price-max",
                "feature_description": "'max' aggregate value of 'Price' field in 'from last 4 to 8 months'",
                "feature_presence": 0.7202185792349727,
                "gain": 25.25336161354994,
                "lift": 18.187940222217936,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 13,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "2m-Quantity-sum",
                "feature_description": "'sum' aggregate value of 'Quantity' field in 'last 2 months'",
                "feature_presence": 0.5562841530054645,
                "gain": 30.014760699090814,
                "lift": 16.69673573315544,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 14,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "8to12m-Quantity-min",
                "feature_description": "'min' aggregate value of 'Quantity' field in 'from last 8 to 12 months'",
                "feature_presence": 0.48415300546448087,
                "gain": 34.314354668505075,
                "lift": 16.613397943330874,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 15,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "4m-Price-max",
                "feature_description": "'max' aggregate value of 'Price' field in 'last 4 months'",
                "feature_presence": 0.7781420765027323,
                "gain": 19.83633117043174,
                "lift": 15.435483927155628,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 16,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "4to8m-Quantity-cnt",
                "feature_description": "'count' aggregate value of 'Quantity' field in 'from last 4 to 8 months'",
                "feature_presence": 0.7213114754098361,
                "gain": 21.08370389532502,
                "lift": 15.207917563840999,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 17,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "4to8m-Quantity-avg",
                "feature_description": "'avg' aggregate value of 'Quantity' field in 'from last 4 to 8 months'",
                "feature_presence": 0.7213114754098361,
                "gain": 20.54412352406013,
                "lift": 14.818712050141734,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 18,
            },
            {
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "feature": "4to8m-Quantity-sum_neg",
                "feature_description": "'sum_neg' aggregate value of 'Quantity' field in 'from last 4 to 8 months'",
                "feature_presence": 0.24371584699453552,
                "gain": 57.85110028899234,
                "lift": 14.099229906497587,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "rank": 19,
            },
        ],
        "lift_chart": [
            {
                "actual": 3.0,
                "bucket": 10,
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "lift_actual": 3.060200668896321,
                "lift_predicted": 9.08771958401212,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "over_predict": 2.5400231636733177,
                "predicted": 7.620069491019954,
                "profiles": 23,
                "rate_actual": 0.13043478260869565,
                "rate_predicted": 0.3313073691747806,
                "size_actual": 0.07692307692307693,
                "size_profile": 0.025136612021857924,
                "size_profiles": 0.025136612021857924,
            },
            {
                "actual": 7.0,
                "bucket": 20,
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "lift_actual": 5.865384615384616,
                "lift_predicted": 8.380011231016788,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "over_predict": 1.2220269117844222,
                "predicted": 8.554188382490956,
                "profiles": 28,
                "rate_actual": 0.25,
                "rate_predicted": 0.30550672794610556,
                "size_actual": 0.1794871794871795,
                "size_profile": 0.030601092896174863,
                "size_profiles": 0.030601092896174863,
            },
            {
                "actual": 11.0,
                "bucket": 30,
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "lift_actual": 6.975051975051976,
                "lift_predicted": 7.421912478243285,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "over_predict": 0.9101250035398842,
                "predicted": 10.011375038938727,
                "profiles": 37,
                "rate_actual": 0.2972972972972973,
                "rate_predicted": 0.2705777037551007,
                "size_actual": 0.28205128205128205,
                "size_profile": 0.040437158469945354,
                "size_profiles": 0.040437158469945354,
            },
            {
                "actual": 15.0,
                "bucket": 40,
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "lift_actual": 6.767751479289941,
                "lift_predicted": 6.255507888199708,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "over_predict": 0.7905891299489285,
                "predicted": 11.858836949233927,
                "profiles": 52,
                "rate_actual": 0.28846153846153844,
                "rate_predicted": 0.22805455671603705,
                "size_actual": 0.38461538461538464,
                "size_profile": 0.05683060109289618,
                "size_profiles": 0.05683060109289618,
            },
            {
                "actual": 19.0,
                "bucket": 50,
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "lift_actual": 4.16606757728253,
                "lift_predicted": 4.149877433072482,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "over_predict": 0.8520039826571639,
                "predicted": 16.188075670486114,
                "profiles": 107,
                "rate_actual": 0.17757009345794392,
                "rate_predicted": 0.15129042682697302,
                "size_actual": 0.48717948717948717,
                "size_profile": 0.11693989071038251,
                "size_profiles": 0.11693989071038251,
            },
            {
                "actual": 23.0,
                "bucket": 60,
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "lift_actual": 4.351736972704715,
                "lift_predicted": 3.8033590513948616,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "over_predict": 0.7475450217629932,
                "predicted": 17.193535500548844,
                "profiles": 124,
                "rate_actual": 0.18548387096774194,
                "rate_predicted": 0.13865754435926486,
                "size_actual": 0.5897435897435898,
                "size_profile": 0.1355191256830601,
                "size_profiles": 0.1355191256830601,
            },
            {
                "actual": 27.0,
                "bucket": 70,
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "lift_actual": 3.6829159212880147,
                "lift_predicted": 3.1088442149472932,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "over_predict": 0.7220043611566573,
                "predicted": 19.494117751229748,
                "profiles": 172,
                "rate_actual": 0.1569767441860465,
                "rate_predicted": 0.11333789390249853,
                "size_actual": 0.6923076923076923,
                "size_profile": 0.18797814207650274,
                "size_profiles": 0.18797814207650274,
            },
            {
                "actual": 31.0,
                "bucket": 80,
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "lift_actual": 2.078021978021978,
                "lift_predicted": 1.9294669591570963,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "over_predict": 0.7941816982707088,
                "predicted": 24.619632646391974,
                "profiles": 350,
                "rate_actual": 0.08857142857142856,
                "rate_predicted": 0.07034180756111992,
                "size_actual": 0.7948717948717948,
                "size_profile": 0.3825136612021858,
                "size_profiles": 0.3825136612021858,
            },
            {
                "actual": 35.0,
                "bucket": 90,
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "lift_actual": 1.2040378975862849,
                "lift_predicted": 1.2168786825443905,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "over_predict": 0.8644498267380769,
                "predicted": 30.25574393583269,
                "profiles": 682,
                "rate_actual": 0.051319648093841645,
                "rate_predicted": 0.044363260902980484,
                "size_actual": 0.8974358974358975,
                "size_profile": 0.7453551912568306,
                "size_profiles": 0.7453551912568306,
            },
            {
                "actual": 39.0,
                "bucket": 100,
                "data_date": "2011-06-01",
                "date_created": "2011-06-01",
                "lift_actual": 1.0,
                "lift_predicted": 0.9999999999999998,
                "model_id": "Propensity_Type_Cancelled",
                "model_name": "Propensity Type Cancelled",
                "model_type": "binary",
                "model_version": "2011.06.01",
                "over_predict": 0.8553279524777718,
                "predicted": 33.3577901466331,
                "profiles": 915,
                "rate_actual": 0.04262295081967213,
                "rate_predicted": 0.03645660125315093,
                "size_actual": 1.0,
                "size_profile": 1.0,
                "size_profiles": 1.0,
            },
        ],
        "model_id": "Propensity_Type_Cancelled",
        "model_metadata": {
            "description": "Propensity_Type_Cancelled type: binary",
            "fulcrum_date": "2011-05-25",
            "lookback_days": "180",
            "model_metadata_client": "HUS",
            "model_name": "Propensity Type Cancelled",
            "model_type": "binary",
            "owner": "decisioning",
            "owner_email": "huxdecisiong@deloitte.com",
            "prediction_days": "7",
            "status": "Active",
        },
        "model_metrics": {
            "AUC": 0.8045749912188268,
            "data_date": "2011-06-01",
            "date_created": "2011-06-01",
            "model_id": "Propensity_Type_Cancelled",
            "model_name": "Propensity Type Cancelled",
            "model_type": "binary",
            "path": "s3://decisioning-pendleton-shared/ui-metadata/v8/metrics/classification/Propensity_Type_Cancelled_2011-06-01.json",
            "precision": 0.0,
            "recall": 0.0,
            "version_number": "2011.06.01",
        },
        "model_mode": "training",
        "model_version": "",
        "name": "Propensity_Type_Cancelled - Propensity Type Cancelled",
        "pipeline_name": "blueprints-uci-pipeline-xnvzw",
        "scheduled_date": "2011-06-01",
        "uri": "s3://decisioning-pendleton-shared/ui-metadata/v8/models/Propensity_Type_Cancelled_2011-06-01.json",
    }
]

MOCKED_MODEL_PROPENSITY_FEATURES = {
    api_c.RESULTS: [
        {
            api_c.FEATURES: [
                "2022-01-06",
                "2021-07-28",
                "1to2y-COGS-sum",
                "description",
                "Numeric",
                "52%",
                2,
                2.2,
                1.8,
                6.1,
                40,
                "Women",
                "Men",
            ],
            api_c.JOIN_KEYS: ["21.7.28"],
        },
        {
            api_c.FEATURES: [
                "2021-07-29",
                "2021-07-29",
                "1to2y-data_source-orders",
                "description",
                "Categorial",
                "52%",
                3,
                3.2,
                1.8,
                6.1,
                60,
                "Women",
                "Men",
            ],
            api_c.JOIN_KEYS: ["21.7.29"],
        },
        {
            api_c.FEATURES: [
                "2021-07-30",
                "2021-07-30",
                "1to2y-ITEMQTY-avg",
                "description",
                "Numeric",
                "52%",
                2,
                2.2,
                1.8,
                5.1,
                50,
                "Women",
                "Men",
            ],
            api_c.JOIN_KEYS: ["21.7.30"],
        },
        {
            api_c.FEATURES: [
                "2021-07-31",
                "2021-07-31",
                "1to2y-COGS-sum",
                "description",
                "Categorial",
                "32%",
                2,
                1.2,
                1.1,
                4.1,
                40,
                "Women",
                "Men",
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
        {
            api_c.COUNTRY: "Test Country",
            api_c.CUSTOMER_COUNT: 1234,
            api_c.SIZE: 1234,
            api_c.LTV: 324.45,
        }
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
            db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 13,
        },
        {
            api_c.LABEL: "Data source 2",
            api_c.NAME: "test_data_source_2",
            api_c.STATUS: "Active",
            db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 23,
        },
        {
            api_c.LABEL: "Data source 3",
            api_c.NAME: "test_data_source_3",
            api_c.STATUS: "Pending",
            db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 31,
        },
        {
            api_c.LABEL: "Data source 4",
            api_c.NAME: "test_data_source_4",
            api_c.STATUS: "Pending",
            db_c.CDP_DATA_SOURCE_FIELD_FEED_COUNT: 18,
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
AVG_SPEND = "avg_spend"

DESTINATIONS_CATEGORY = "destinations_category"

TEST_NAVIGATION_SETTINGS = {
    "settings": [
        {
            "enabled": True,
            "name": "Data Management",
            "label": "Data Management",
            "children": [
                {
                    "name": "Data Sources",
                    "label": "Data Sources",
                    "enabled": False,
                },
                {
                    "name": "Identity Resolution",
                    "label": "Identity Resolution",
                    "enabled": True,
                },
            ],
        },
        {
            "enabled": True,
            "name": "Decisioning",
            "label": "Decisioning",
            "children": [
                {"name": "Models", "label": "Models", "enabled": True}
            ],
        },
    ]
}
SAMPLE_USER_JIRA_TICKETS = {
    "expand": "names,schema",
    "startAt": 0,
    "maxResults": 50,
    "total": 1,
    "issues": [
        {
            "expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields",
            "id": "1234",
            "self": "https://jira.hux.deloitte.com/rest/api/2/issue/117518",
            "key": "HUS-0000",
            "fields": {
                "summary": "Test ticket summary",
                "created": "2021-12-01T15:35:18.000+0000",
                "status": {
                    "self": "https://jira.hux.deloitte.com/rest/api/2/status/10000",
                    "description": "",
                    "iconUrl": "https://jira.hux.deloitte.com/images/icons/statuses/open.png",
                    "name": "To Do",
                    "id": "10000",
                    "statusCategory": {
                        "self": "https://jira.hux.deloitte.com/rest/api/2/statuscategory/2",
                        "id": 2,
                        "key": "new",
                        "colorName": "blue-gray",
                        "name": "To Do",
                    },
                },
            },
        }
    ],
}

SAMPLE_USER_REQUEST_JIRA_ISSUES = {
    "expand": "schema,names",
    "startAt": 0,
    "maxResults": 50,
    "total": 3,
    "issues": [
        {
            "expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields",
            "id": "121524",
            "self": "https://jira.hux.fake.com/rest/api/2/issue/121524",
            "key": "HUS-2005",
            "fields": {
                "description": "*Project Name:* ADV \n*Required Info:* Please add Risheek New to the team-unified--base group. \n*Reason for Request:* New member to our team \n*User:* Risheek, New \n*Email:* rn@fake.com \n*Access Level:* admin \n*PII Access:* False \n*Okta Group Name:* team-unified--base \n*Okta App:* HUX Audience Builder \n*Requested by:* Risheek Chandra",
                "assignee": {
                    "self": "https://jira.hux.fake.com/rest/api/2/user?username=rgchandra%40fake.com",
                    "name": "rgchandra@fake.com",
                    "key": "JIRAUSER13410",
                    "emailAddress": "rgchandra@fake.com",
                    "avatarUrls": {
                        "48x48": "https://jira.hux.fake.com/secure/useravatar?avatarId=10338",
                        "24x24": "https://jira.hux.fake.com/secure/useravatar?size=small&avatarId=10338",
                        "16x16": "https://jira.hux.fake.com/secure/useravatar?size=xsmall&avatarId=10338",
                        "32x32": "https://jira.hux.fake.com/secure/useravatar?size=medium&avatarId=10338",
                    },
                    "displayName": "Risheek Chandra",
                    "timeZone": "America/New_York",
                },
                "updated": "2022-01-12T12:09:24.000+0000",
                "created": "2022-01-12T12:09:23.000+0000",
                "status": {
                    "self": "https://jira.hux.fake.com/rest/api/2/status/10000",
                    "description": "",
                    "iconUrl": "https://jira.hux.fake.com/images/icons/statuses/open.png",
                    "name": "To Do",
                    "id": "10000",
                    "statusCategory": {
                        "self": "https://jira.hux.fake.com/rest/api/2/statuscategory/2",
                        "id": 2,
                        "key": "new",
                        "colorName": "blue-gray",
                        "name": "To Do",
                    },
                },
            },
        },
        {
            "expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields",
            "id": "121619",
            "self": "https://jira.hux.fake.com/rest/api/2/issue/121619",
            "key": "HUS-2008",
            "fields": {
                "description": "*Project Name:* ADV \n*Required Info:* Please add Sarah Huxley to the team-unified--base group. \n*Reason for Request:* New member to our team \n*User:* Sarah, Huxley \n*Email:* sh@fake.com \n*Access Level:* admin \n*PII Access:* False \n*Okta Group Name:* team-unified--base \n*Okta App:* HUX Audience Builder \n*Requested by:* Risheek Chandra",
                "assignee": {
                    "self": "https://jira.hux.fake.com/rest/api/2/user?username=rgchandra%40fake.com",
                    "name": "rgchandra@fake.com",
                    "key": "JIRAUSER13410",
                    "emailAddress": "rgchandra@fake.com",
                    "avatarUrls": {
                        "48x48": "https://jira.hux.fake.com/secure/useravatar?avatarId=10338",
                        "24x24": "https://jira.hux.fake.com/secure/useravatar?size=small&avatarId=10338",
                        "16x16": "https://jira.hux.fake.com/secure/useravatar?size=xsmall&avatarId=10338",
                        "32x32": "https://jira.hux.fake.com/secure/useravatar?size=medium&avatarId=10338",
                    },
                    "displayName": "Risheek Chandra",
                    "timeZone": "America/New_York",
                },
                "updated": "2022-01-12T14:13:50.000+0000",
                "created": "2022-01-12T14:13:50.000+0000",
                "status": {
                    "self": "https://jira.hux.fake.com/rest/api/2/status/10000",
                    "description": "",
                    "iconUrl": "https://jira.hux.fake.com/images/icons/statuses/open.png",
                    "name": "To Do",
                    "id": "10000",
                    "statusCategory": {
                        "self": "https://jira.hux.fake.com/rest/api/2/statuscategory/2",
                        "id": 2,
                        "key": "new",
                        "colorName": "blue-gray",
                        "name": "To Do",
                    },
                },
            },
        },
        {
            "expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields",
            "id": "121621",
            "self": "https://jira.hux.fake.com/rest/api/2/issue/121621",
            "key": "HUS-2010",
            "fields": {
                "description": "*Project Name:* ADV \n*Required Info:* Please add Sarah Huxley to the team-unified--base group. \n*Reason for Request:* New member to our team \n*User:* Sarah, Huxley \n*Email:* sh@fake.com \n*Access Level:* admin \n*PII Access:* False \n*Okta Group Name:* team-unified--base \n*Okta App:* HUX Audience Builder \n*Requested by:* Risheek Chandra",
                "assignee": {
                    "self": "https://jira.hux.fake.com/rest/api/2/user?username=rgchandra%40fake.com",
                    "name": "rgchandra@fake.com",
                    "key": "JIRAUSER13410",
                    "emailAddress": "rgchandra@fake.com",
                    "avatarUrls": {
                        "48x48": "https://jira.hux.fake.com/secure/useravatar?avatarId=10338",
                        "24x24": "https://jira.hux.fake.com/secure/useravatar?size=small&avatarId=10338",
                        "16x16": "https://jira.hux.fake.com/secure/useravatar?size=xsmall&avatarId=10338",
                        "32x32": "https://jira.hux.fake.com/secure/useravatar?size=medium&avatarId=10338",
                    },
                    "displayName": "Risheek Chandra",
                    "timeZone": "America/New_York",
                },
                "updated": "2022-01-12T15:25:55.000+0000",
                "created": "2022-01-12T15:25:54.000+0000",
                "status": {
                    "self": "https://jira.hux.fake.com/rest/api/2/status/10000",
                    "description": "",
                    "iconUrl": "https://jira.hux.fake.com/images/icons/statuses/open.png",
                    "name": "In Progress",
                    "id": "10000",
                    "statusCategory": {
                        "self": "https://jira.hux.fake.com/rest/api/2/statuscategory/2",
                        "id": 2,
                        "key": "new",
                        "colorName": "blue-gray",
                        "name": "In Progress",
                    },
                },
            },
        },
    ],
}

DATAFEED_FILE_DETAILS_RESPONSE = {
    "code": 200,
    "message": "ok",
    api_c.BODY: [
        {
            api_c.INPUT_FILE: "file_1.csv",
            api_c.UNIQUE_ID: 1,
            api_c.PROCESSED_END_DATE: "2022-02-13T17:21:04.000Z",
            api_c.PROCESSED_START_DATE: "2022-02-13T16:06:40.000Z",
            api_c.RECORDS_PROCESSED: 392271,
            api_c.RECORDS_RECEIVED: 507907,
            api_c.STATUS: api_c.STATUS_RUNNING,
            api_c.SUB_STATUS: api_c.STATUS_IN_PROGRESS,
            api_c.THIRTY_DAYS_AVG: 0.94,
        },
        {
            api_c.INPUT_FILE: "file_2.csv",
            api_c.UNIQUE_ID: 2,
            api_c.PROCESSED_END_DATE: "2022-02-12T16:14:48.000Z",
            api_c.PROCESSED_START_DATE: "2022-02-12T16:06:40.000Z",
            api_c.RECORDS_PROCESSED: 424684,
            api_c.RECORDS_RECEIVED: 669920,
            api_c.STATUS: api_c.STATUS_SUCCESS,
            api_c.SUB_STATUS: api_c.STATUS_COMPLETE,
            api_c.THIRTY_DAYS_AVG: 0.94,
        },
    ],
}

TRUST_ID_SURVEY_RESPONSES = [
    {
        "responseDate": "2022-02-06T21:16:00.000Z",
        "responses": {
            "Race and Ethnicity": "White or Caucasian",
            "Age": "18-24",
            "Gender": "Female",
            "No Of Household Seniors": "3+",
            "Children in Household": "No",
            "Education": "Undergraduate Degree",
            "Household Income": "$20K-$40K",
            "Zipcode": "33407",
            "factors": {
                "HUMANITY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer quickly resolves issues with safety, security and satisfaction top of mind",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer values & respects everyone, regardless of background, identity or beliefs",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer values the good of society and the environment, not just profit",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer takes care of employees",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "RELIABILITY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer can be counted on to improve the quality of their products and services",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer consistently delivers products, services, and experiences with quality",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer facilitates digital interactions that run smoothly and work when needed",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer resolves issues in an adequate and timely manner",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "TRANSPARENCY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer's marketing and communications are accurate and honest",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer is upfront about how they make and spend money from our interactions",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "How and why my data is used is communicated in plain and easy to understand language",
                            "score": "6",
                            "short_description": "Data storage and communication",
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer is clear and upfront about fees and costs of products, services and experiences",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "CAPABILITY": {
                    "attributes": [
                        {
                            "description": "Products are good quality, accessible and safe to use",
                            "score": "7",
                            "short_description": "Product quality, accessibility and safety",
                            "rating": "1",
                        },
                        {
                            "description": "Prices of products, services, and experiences are good value for money",
                            "score": "6",
                            "short_description": "Fair product & service pricing",
                            "rating": "1",
                        },
                        {
                            "description": "Employees and leadership are competent and understand how to respond to my needs",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer creates long term solutions and improvements that work well for me",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
            },
        },
        "create_time": "2022-07-20T11:58:57.000Z",
    },
    {
        "responseDate": "2022-02-06T17:31:00.000Z",
        "responses": {
            "Race and Ethnicity": "White or Caucasian,Hispanic or Latino",
            "Age": "35-44",
            "Gender": "Female",
            "No Of Household Seniors": "1",
            "Children in Household": "No",
            "Education": "Graduate Degree",
            "Household Income": "$60K-$80K",
            "Zipcode": "33417",
            "factors": {
                "HUMANITY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer quickly resolves issues with safety, security and satisfaction top of mind",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer values & respects everyone, regardless of background, identity or beliefs",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer values the good of society and the environment, not just profit",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer takes care of employees",
                            "score": "4",
                            "short_description": None,
                            "rating": "0",
                        },
                    ],
                    "rating": "1",
                },
                "RELIABILITY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer can be counted on to improve the quality of their products and services",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer consistently delivers products, services, and experiences with quality",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer facilitates digital interactions that run smoothly and work when needed",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer resolves issues in an adequate and timely manner",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "TRANSPARENCY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer's marketing and communications are accurate and honest",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer is upfront about how they make and spend money from our interactions",
                            "score": "4",
                            "short_description": None,
                            "rating": "0",
                        },
                        {
                            "description": "How and why my data is used is communicated in plain and easy to understand language",
                            "score": "7",
                            "short_description": "Data storage and communication",
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer is clear and upfront about fees and costs of products, services and experiences",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "CAPABILITY": {
                    "attributes": [
                        {
                            "description": "Products are good quality, accessible and safe to use",
                            "score": "6",
                            "short_description": "Product quality, accessibility and safety",
                            "rating": "1",
                        },
                        {
                            "description": "Prices of products, services, and experiences are good value for money",
                            "score": "5",
                            "short_description": "Fair product & service pricing",
                            "rating": "0",
                        },
                        {
                            "description": "Employees and leadership are competent and understand how to respond to my needs",
                            "score": "5",
                            "short_description": None,
                            "rating": "0",
                        },
                        {
                            "description": "Lilly Pulitzer creates long term solutions and improvements that work well for me",
                            "score": "5",
                            "short_description": None,
                            "rating": "0",
                        },
                    ],
                    "rating": "1",
                },
            },
        },
        "create_time": "2022-07-20T11:58:57.000Z",
    },
    {
        "responseDate": "2022-02-06T17:05:00.000Z",
        "responses": {
            "Race and Ethnicity": "Prefer not to say",
            "Age": "55-64",
            "Gender": "Female",
            "No Of Household Seniors": "2",
            "Children in Household": "No",
            "Education": "Prefer not to say",
            "Household Income": "Prefer not to say",
            "Zipcode": "33407",
            "factors": {
                "HUMANITY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer quickly resolves issues with safety, security and satisfaction top of mind",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer values & respects everyone, regardless of background, identity or beliefs",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer values the good of society and the environment, not just profit",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer takes care of employees",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "RELIABILITY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer can be counted on to improve the quality of their products and services",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer consistently delivers products, services, and experiences with quality",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer facilitates digital interactions that run smoothly and work when needed",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer resolves issues in an adequate and timely manner",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "TRANSPARENCY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer's marketing and communications are accurate and honest",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer is upfront about how they make and spend money from our interactions",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "How and why my data is used is communicated in plain and easy to understand language",
                            "score": "7",
                            "short_description": "Data storage and communication",
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer is clear and upfront about fees and costs of products, services and experiences",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "CAPABILITY": {
                    "attributes": [
                        {
                            "description": "Products are good quality, accessible and safe to use",
                            "score": "7",
                            "short_description": "Product quality, accessibility and safety",
                            "rating": "1",
                        },
                        {
                            "description": "Prices of products, services, and experiences are good value for money",
                            "score": "7",
                            "short_description": "Fair product & service pricing",
                            "rating": "1",
                        },
                        {
                            "description": "Employees and leadership are competent and understand how to respond to my needs",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer creates long term solutions and improvements that work well for me",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
            },
        },
        "create_time": "2022-07-20T11:58:57.000Z",
    },
    {
        "responseDate": "2022-02-06T17:51:00.000Z",
        "responses": {
            "Race and Ethnicity": "White or Caucasian",
            "Age": "55-64",
            "Gender": "Female",
            "No Of Household Seniors": "2",
            "Children in Household": "No",
            "Education": "Vocational Training",
            "Household Income": "$150K+",
            "Zipcode": "33409",
            "factors": {
                "HUMANITY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer quickly resolves issues with safety, security and satisfaction top of mind",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer values & respects everyone, regardless of background, identity or beliefs",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer values the good of society and the environment, not just profit",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer takes care of employees",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "RELIABILITY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer can be counted on to improve the quality of their products and services",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer consistently delivers products, services, and experiences with quality",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer facilitates digital interactions that run smoothly and work when needed",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer resolves issues in an adequate and timely manner",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "-1",
                },
                "TRANSPARENCY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer's marketing and communications are accurate and honest",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer is upfront about how they make and spend money from our interactions",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "How and why my data is used is communicated in plain and easy to understand language",
                            "score": "7",
                            "short_description": "Data storage and communication",
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer is clear and upfront about fees and costs of products, services and experiences",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "CAPABILITY": {
                    "attributes": [
                        {
                            "description": "Products are good quality, accessible and safe to use",
                            "score": "7",
                            "short_description": "Product quality, accessibility and safety",
                            "rating": "1",
                        },
                        {
                            "description": "Prices of products, services, and experiences are good value for money",
                            "score": "5",
                            "short_description": "Fair product & service pricing",
                            "rating": "0",
                        },
                        {
                            "description": "Employees and leadership are competent and understand how to respond to my needs",
                            "score": "6",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer creates long term solutions and improvements that work well for me",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
            },
        },
        "create_time": "2022-07-20T11:58:57.000Z",
    },
    {
        "responseDate": "2022-02-06T17:17:00.000Z",
        "responses": {
            "Race and Ethnicity": "White or Caucasian",
            "Age": "55-64",
            "Gender": "Female",
            "No Of Household Seniors": "2",
            "Children in Household": "No",
            "Education": "Vocational Training",
            "Household Income": "$40K-$60K",
            "Zipcode": "33417",
            "factors": {
                "HUMANITY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer quickly resolves issues with safety, security and satisfaction top of mind",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer values & respects everyone, regardless of background, identity or beliefs",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer values the good of society and the environment, not just profit",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer takes care of employees",
                            "score": "4",
                            "short_description": None,
                            "rating": "0",
                        },
                    ],
                    "rating": "1",
                },
                "RELIABILITY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer can be counted on to improve the quality of their products and services",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer consistently delivers products, services, and experiences with quality",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer facilitates digital interactions that run smoothly and work when needed",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer resolves issues in an adequate and timely manner",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "TRANSPARENCY": {
                    "attributes": [
                        {
                            "description": "Lilly Pulitzer's marketing and communications are accurate and honest",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer is upfront about how they make and spend money from our interactions",
                            "score": "4",
                            "short_description": None,
                            "rating": "0",
                        },
                        {
                            "description": "How and why my data is used is communicated in plain and easy to understand language",
                            "score": "7",
                            "short_description": "Data storage and communication",
                            "rating": "1",
                        },
                        {
                            "description": "Lilly Pulitzer is clear and upfront about fees and costs of products, services and experiences",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
                "CAPABILITY": {
                    "attributes": [
                        {
                            "description": "Products are good quality, accessible and safe to use",
                            "score": "7",
                            "short_description": "Product quality, accessibility and safety",
                            "rating": "1",
                        },
                        {
                            "description": "Prices of products, services, and experiences are good value for money",
                            "score": "7",
                            "short_description": "Fair product & service pricing",
                            "rating": "1",
                        },
                        {
                            "description": "Employees and leadership are competent and understand how to respond to my needs",
                            "score": "4",
                            "short_description": None,
                            "rating": "0",
                        },
                        {
                            "description": "Lilly Pulitzer creates long term solutions and improvements that work well for me",
                            "score": "7",
                            "short_description": None,
                            "rating": "1",
                        },
                    ],
                    "rating": "1",
                },
            },
        },
        "create_time": "2022-07-20T11:58:57.000Z",
    },
]


TRUST_ID_OVERVIEW_SAMPLE_DATA = {
    "_id": None,
    "capability": {
        "rating": {
            "agree": {"count": 5, "percentage": 1.0},
            "disagree": {"count": 0, "percentage": 0.0},
            "neutral": {"count": 0, "percentage": 0.0},
        },
        "total_customers": 5,
    },
    "humanity": {
        "rating": {
            "agree": {"count": 5, "percentage": 1.0},
            "disagree": {"count": 0, "percentage": 0.0},
            "neutral": {"count": 0, "percentage": 0.0},
        },
        "total_customers": 5,
    },
    "reliability": {
        "rating": {
            "agree": {"count": 4, "percentage": 0.8},
            "disagree": {"count": 1, "percentage": 0.2},
            "neutral": {"count": 0, "percentage": 0.0},
        },
        "total_customers": 5,
    },
    "transparency": {
        "rating": {
            "agree": {"count": 5, "percentage": 1.0},
            "disagree": {"count": 0, "percentage": 0.0},
            "neutral": {"count": 0, "percentage": 0.0},
        },
        "total_customers": 5,
    },
}

TRUST_ID_AGGREGATED_OVERVIEW_SAMPLE_DATA = {
    "factors": [
        {
            "factor_description": "Humanity is demonstrating empathy and kindness towards customers, and treating everyone fairly. It is scored on a scale between -100 to 100",
            "factor_name": "humanity",
            "factor_score": 100,
            "overall_customer_rating": {
                "rating": {
                    "agree": {"count": 5, "percentage": 1.0},
                    "disagree": {"count": 0, "percentage": 0.0},
                    "neutral": {"count": 0, "percentage": 0.0},
                },
                "total_customers": 5,
            },
        },
        {
            "factor_description": "Reliability is consistently and dependably delivering on promises. It is scored on a scale between -100 to 100",
            "factor_name": "reliability",
            "factor_score": 60,
            "overall_customer_rating": {
                "rating": {
                    "agree": {"count": 4, "percentage": 0.8},
                    "disagree": {"count": 1, "percentage": 0.2},
                    "neutral": {"count": 0, "percentage": 0.0},
                },
                "total_customers": 5,
            },
        },
        {
            "factor_description": "Capability is creating quality products, services, and/or experiences. It is scored on a scale between -100 to 100",
            "factor_name": "capability",
            "factor_score": 100,
            "overall_customer_rating": {
                "rating": {
                    "agree": {"count": 5, "percentage": 1.0},
                    "disagree": {"count": 0, "percentage": 0.0},
                    "neutral": {"count": 0, "percentage": 0.0},
                },
                "total_customers": 5,
            },
        },
        {
            "factor_description": "Transparency is openly sharing all information, motives, and choices in straightforward and plain language. It is scored on a scale between -100 to 100",
            "factor_name": "transparency",
            "factor_score": 100,
            "overall_customer_rating": {
                "rating": {
                    "agree": {"count": 5, "percentage": 1.0},
                    "disagree": {"count": 0, "percentage": 0.0},
                    "neutral": {"count": 0, "percentage": 0.0},
                },
                "total_customers": 5,
            },
        },
    ],
    "trust_id_score": 90,
}

TRUST_ID_ATTRIBUTE_SAMPLE_DATA = {
    "_id": None,
    "attributes": {
        "capability": [
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            {
                "agree": {"count": 3, "percentage": 0.6},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 2, "percentage": 0.4},
            },
            {
                "agree": {"count": 3, "percentage": 0.6},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 2, "percentage": 0.4},
            },
            {
                "agree": {"count": 4, "percentage": 0.8},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 1, "percentage": 0.2},
            },
        ],
        "humanity": [
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            {
                "agree": {"count": 3, "percentage": 0.6},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 2, "percentage": 0.4},
            },
        ],
        "reliability": [
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
        ],
        "transparency": [
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            {
                "agree": {"count": 3, "percentage": 0.6},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 2, "percentage": 0.4},
            },
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
        ],
    },
    "total_customers": 5,
}

TRUST_ID_AGGREGATED_ATTRIBUTE_SAMPLE_DATA = [
    {
        "attribute_description": "Products are good quality, accessible and safe to use",
        "attribute_score": 100,
        "attribute_short_description": "Product quality, accessibility and safety",
        "factor_name": "capability",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Prices of products, services, and experiences are good value for money",
        "attribute_score": 60,
        "attribute_short_description": "Fair product & service pricing",
        "factor_name": "capability",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 3, "percentage": 0.6},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 2, "percentage": 0.4},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Employees and leadership are competent and understand how to respond to my needs",
        "attribute_score": 60,
        "attribute_short_description": "Competent leadership and employees",
        "factor_name": "capability",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 3, "percentage": 0.6},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 2, "percentage": 0.4},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer creates long term solutions and improvements that work well for me",
        "attribute_score": 80,
        "attribute_short_description": "Applicable long-term solutions & improvements",
        "factor_name": "capability",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 4, "percentage": 0.8},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 1, "percentage": 0.2},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer quickly resolves issues with safety, security and satisfaction top of mind",
        "attribute_score": 100,
        "attribute_short_description": "Quickly resolves issues",
        "factor_name": "humanity",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer values & respects everyone, regardless of background, identity or beliefs",
        "attribute_score": 100,
        "attribute_short_description": "Values & respects everyone",
        "factor_name": "humanity",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer values the good of society and the environment, not just profit",
        "attribute_score": 100,
        "attribute_short_description": "Values society & environment",
        "factor_name": "humanity",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer takes care of employees",
        "attribute_score": 60,
        "attribute_short_description": "Takes care of employees",
        "factor_name": "humanity",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 3, "percentage": 0.6},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 2, "percentage": 0.4},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer can be counted on to improve the quality of their products and services",
        "attribute_score": 100,
        "attribute_short_description": "Continuous product improvement",
        "factor_name": "reliability",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer consistently delivers products, services, and experiences with quality",
        "attribute_score": 100,
        "attribute_short_description": "Delivers quality products",
        "factor_name": "reliability",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer facilitates digital interactions that run smoothly and work when needed",
        "attribute_score": 100,
        "attribute_short_description": "Facilitates smooth digital interactions",
        "factor_name": "reliability",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer resolves issues in an adequate and timely manner",
        "attribute_score": 100,
        "attribute_short_description": "Timely issue resolution",
        "factor_name": "reliability",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": 'Lilly Pulitzer"s marketing and communications are accurate and honest',
        "attribute_score": 100,
        "attribute_short_description": "Honest communication and marketing",
        "factor_name": "transparency",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer is upfront about how they make and spend money from our interactions",
        "attribute_score": 60,
        "attribute_short_description": "Upfront spending and income",
        "factor_name": "transparency",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 3, "percentage": 0.6},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 2, "percentage": 0.4},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "How and why my data is used is communicated in plain and easy to understand language",
        "attribute_score": 100,
        "attribute_short_description": "Data storage and communication",
        "factor_name": "transparency",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
    {
        "attribute_description": "Lilly Pulitzer is clear and upfront about fees and costs of products, services and experiences",
        "attribute_score": 100,
        "attribute_short_description": "Upfront costs and fees",
        "factor_name": "transparency",
        "overall_customer_rating": {
            "rating": {
                "agree": {"count": 5, "percentage": 1.0},
                "disagree": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
            },
            "total_customers": 5,
        },
    },
]

CDP_COUNT_BY_AGE_RESONSE = {
    "code": 200,
    "body": [
        {"age": 18, "customer_count": 973},
        {"age": 19, "customer_count": 264},
        {"age": 20, "customer_count": 261},
        {"age": 21, "customer_count": 317},
        {"age": 22, "customer_count": 321},
    ],
    "message": "ok",
}

AGE_HISTOGRAM_DATA = [
    (18, 973),
    (19, 264),
    (20, 261),
    (21, 317),
    (22, 321),
]

CDP_COUNT_BY_AGE_RESONSE = {
    "code": 200,
    "body": [
        {"age": 18, "customer_count": 973},
        {"age": 19, "customer_count": 264},
        {"age": 20, "customer_count": 261},
        {"age": 21, "customer_count": 317},
        {"age": 22, "customer_count": 321},
    ],
    "message": "ok",
}

COUNTS_BY_FLOAT_HISTOGRAM_DATA = [
    (0.00072, 2158),
    (49.940596, 2220),
    (99.880472, 2032),
]

CDP_COUNTS_BY_FLOAT_RESONSE = {
    "code": 200,
    "body": [
        {"value_from": 0.00072, "value_to": 49.940596, "customer_count": 2158},
        {
            "value_from": 49.940596,
            "value_to": 99.880472,
            "customer_count": 2220,
        },
        {
            "value_from": 99.880472,
            "value_to": 149.820348,
            "customer_count": 2032,
        },
    ],
    "message": "ok",
}

TRUST_ID_SAMPLE_USER_SEGMENT = [
    {
        api_c.TRUST_ID_SEGMENT_NAME: "Segment",
        api_c.TRUST_ID_SEGMENT_FILTERS: [
            {"type": "age", "values": ["50 to 54 years"], "description": "Age"}
        ],
        api_c.DEFAULT: False,
    }
]

TRUST_ID_SAMPLE_HUMANITY_OVERVIEW = {
    "factor_name": "humanity",
    "factor_score": 100,
    "factor_description": "Humanity is demonstrating empathy and kindness "
    "towards customers, and "
    "treating everyone fairly. "
    "It is scored on a scale between -100 to 100",
    "overall_customer_rating": {
        "total_customers": 1,
        "rating": {
            "disagree": {"count": 0, "percentage": 0.0},
            "neutral": {"count": 0, "percentage": 0.0},
            "agree": {"count": 1, "percentage": 1.0},
        },
    },
}

TRUST_ID_SAMPLE_HUMANITY_ATTRIBUTE_AGG = {
    "Takes care of employees": {"neutral": 1, "score": 0}
}

TRUST_ID_SAMPLE_ATTRIBUTE = {
    "factor_name": "capability",
    "attribute_score": 81,
    "attribute_description": "Products are good quality, accessible and safe to use",
    "attribute_short_description": "Product quality, accessibility and safety",
    "overall_customer_rating": {
        "total_customers": 13266,
        "rating": {
            "agree": {"count": 11002, "percentage": 0.8293381576963667},
            "disagree": {"count": 301, "percentage": 0.02268958239107493},
            "neutral": {"count": 1963, "percentage": 0.1479722599125584},
        },
    },
}

TRUST_ID_ATTRIBUTE_DESCRIPTION_MAP = {
    "capability": [
        {
            "description": "Products are good quality, accessible and safe to use",
            "short_description": "Product quality, accessibility and safety",
        },
        {
            "description": "Prices of products, services, and experiences are good value for money",
            "short_description": "Fair product & service pricing",
        },
        {
            "description": "Employees and leadership are competent and understand how to respond to my needs",
            "short_description": "Competent leadership and employees",
        },
        {
            "description": "Lilly Pulitzer creates long term solutions and improvements that work well for me",
            "short_description": "Applicable long-term solutions & improvements",
        },
    ],
    "humanity": [
        {
            "description": "Lilly Pulitzer quickly resolves issues with safety, security and satisfaction top of mind",
            "short_description": "Quickly resolves issues",
        },
        {
            "description": "Lilly Pulitzer values & respects everyone, regardless of background, identity or beliefs",
            "short_description": "Values & respects everyone",
        },
        {
            "description": "Lilly Pulitzer values the good of society and the environment, not just profit",
            "short_description": "Values society & environment",
        },
        {
            "description": "Lilly Pulitzer takes care of employees",
            "short_description": "Takes care of employees",
        },
    ],
    "reliability": [
        {
            "description": "Lilly Pulitzer can be counted on to improve the quality of their products and services",
            "short_description": "Continuous product improvement",
        },
        {
            "description": "Lilly Pulitzer consistently delivers products, services, and experiences with quality",
            "short_description": "Delivers quality products",
        },
        {
            "description": "Lilly Pulitzer facilitates digital interactions that run smoothly and work when needed",
            "short_description": "Facilitates smooth digital interactions",
        },
        {
            "description": "Lilly Pulitzer resolves issues in an adequate and timely manner",
            "short_description": "Timely issue resolution",
        },
    ],
    "transparency": [
        {
            "description": 'Lilly Pulitzer"s marketing and communications are accurate and honest',
            "short_description": "Honest communication and marketing",
        },
        {
            "description": "Lilly Pulitzer is upfront about how they make and spend money from our interactions",
            "short_description": "Upfront spending and income",
        },
        {
            "description": "How and why my data is used is communicated in plain and easy to understand language",
            "short_description": "Data storage and communication",
        },
        {
            "description": "Lilly Pulitzer is clear and upfront about fees and costs of products, services and experiences",
            "short_description": "Upfront costs and fees",
        },
    ],
}

TRUST_ID_ATTRIBUTE_RATINGS = {
    "_id": None,
    "attributes": {
        "capability": [
            {
                "agree": {"count": 11002, "percentage": 0.8293381576963667},
                "disagree": {"count": 301, "percentage": 0.02268958239107493},
                "neutral": {"count": 1963, "percentage": 0.1479722599125584},
            },
            {
                "agree": {"count": 5811, "percentage": 0.43803708729081864},
                "disagree": {"count": 871, "percentage": 0.06565656565656566},
                "neutral": {"count": 6584, "percentage": 0.4963063470526157},
            },
            {
                "agree": {"count": 8127, "percentage": 0.6126187245590231},
                "disagree": {"count": 370, "percentage": 0.027890848786371176},
                "neutral": {"count": 4769, "percentage": 0.35949042665460573},
            },
            {
                "agree": {"count": 6132, "percentage": 0.4622342831298055},
                "disagree": {"count": 378, "percentage": 0.028493894165535955},
                "neutral": {"count": 6756, "percentage": 0.5092718227046585},
            },
        ],
        "humanity": [
            {
                "agree": {"count": 8052, "percentage": 0.6069651741293532},
                "disagree": {"count": 440, "percentage": 0.03316749585406302},
                "neutral": {"count": 4774, "percentage": 0.3598673300165838},
            },
            {
                "agree": {"count": 8928, "percentage": 0.6729986431478969},
                "disagree": {"count": 294, "percentage": 0.022161917684305744},
                "neutral": {"count": 4044, "percentage": 0.3048394391677974},
            },
            {
                "agree": {"count": 7230, "percentage": 0.5450022614201718},
                "disagree": {"count": 364, "percentage": 0.027438564751997588},
                "neutral": {"count": 5672, "percentage": 0.42755917382783054},
            },
            {
                "agree": {"count": 5076, "percentage": 0.38263229308005425},
                "disagree": {"count": 126, "percentage": 0.009497964721845319},
                "neutral": {"count": 8064, "percentage": 0.6078697421981004},
            },
        ],
        "reliability": [
            {
                "agree": {"count": 7888, "percentage": 0.5946027438564752},
                "disagree": {"count": 472, "percentage": 0.035579677370722144},
                "neutral": {"count": 4906, "percentage": 0.36981757877280264},
            },
            {
                "agree": {"count": 9701, "percentage": 0.7312679029096939},
                "disagree": {"count": 462, "percentage": 0.03482587064676617},
                "neutral": {"count": 3103, "percentage": 0.23390622644353987},
            },
            {
                "agree": {"count": 9187, "percentage": 0.6925222372983567},
                "disagree": {"count": 439, "percentage": 0.03309211518166742},
                "neutral": {"count": 3640, "percentage": 0.27438564751997585},
            },
            {
                "agree": {"count": 8188, "percentage": 0.6172169455751545},
                "disagree": {"count": 626, "percentage": 0.047188300919644204},
                "neutral": {"count": 4452, "percentage": 0.3355947535052013},
            },
        ],
        "transparency": [
            {
                "agree": {"count": 10200, "percentage": 0.7688828584350973},
                "disagree": {"count": 248, "percentage": 0.01869440675410825},
                "neutral": {"count": 2818, "percentage": 0.21242273481079452},
            },
            {
                "agree": {"count": 4825, "percentage": 0.36371174430875924},
                "disagree": {"count": 678, "percentage": 0.05110809588421529},
                "neutral": {"count": 7763, "percentage": 0.5851801598070254},
            },
            {
                "agree": {"count": 7329, "percentage": 0.552464947987336},
                "disagree": {"count": 599, "percentage": 0.045153022764963066},
                "neutral": {"count": 5338, "percentage": 0.4023820292477009},
            },
            {
                "agree": {"count": 10183, "percentage": 0.7676013870043721},
                "disagree": {"count": 336, "percentage": 0.02532790592492085},
                "neutral": {"count": 2747, "percentage": 0.20707070707070707},
            },
        ],
    },
    "total_customers": 13266,
}


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
