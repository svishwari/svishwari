"""
purpose of this file is housing shared components for tests
"""

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
