"""
purpose of this file is housing shared components for tests
"""
from marshmallow import Schema, ValidationError

BASE_ENDPOINT = "/api/v1"
TEST_AUTH_TOKEN = "Bearer 12345678"
AUTH_HEADER = {
    "Authorization": TEST_AUTH_TOKEN,
}
STANDARD_HEADERS = {
    "Authorization": TEST_AUTH_TOKEN,
    "Content-Type": "application/json"
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
