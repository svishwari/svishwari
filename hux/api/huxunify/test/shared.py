"""
purpose of this file is housing shared components for tests
"""
from marshmallow import Schema, ValidationError

BASE_ENDPOINT = "/api/v1"
TEST_AUTH_TOKEN = "Bearer 12345678"
AUTH_HEADER = {
    "Authorization": TEST_AUTH_TOKEN,
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
