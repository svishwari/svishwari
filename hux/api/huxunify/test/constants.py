# pylint: disable=invalid-name
"""
purpose of this file is housing shared components for tests
"""
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
        print(pd.DataFrame(GOOGLE_ADS_CUSTOMER_DATA))
        yield pd.DataFrame(GOOGLE_ADS_CUSTOMER_DATA, columns=columns)
    elif download_type == api_c.AMAZON_ADS:
        yield pd.DataFrame(AMAZON_ADS_CUSTOMER_DATA, columns=columns)
