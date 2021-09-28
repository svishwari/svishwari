"""Purpose of this file is for housing pytest startup scripts"""
from os import getenv, environ
from _pytest.config import Config
from get_okta_token import OktaOIDC

# ENV VARS
ORG_URL = getenv("OKTA_ISSUER")
CLIENT_ID = getenv("OKTA_CLIENT_ID")
USER = getenv("OKTA_TEST_USER_NAME")
PW = getenv("OKTA_TEST_USER_PW")
REDIRECT_URI = getenv("OKTA_REDIRECT_URI")
SCOPES = "openid+profile+email"
ACCESS_TOKEN = "ACCESS_TOKEN"

# pylint: disable=unused-argument
def pytest_configure(config: Config):
    """Override the pytest plugin. This hook is called for every plugin and
        initial conftest file after command line options have been parsed.

    Args:
        config (Config): Existing pytest config.

    Returns:

    """

    # setup the oidc class.
    okta_oidc = OktaOIDC(
        ORG_URL,
        USER,
        PW,
        CLIENT_ID,
        SCOPES,
        REDIRECT_URI,
    )

    # set the token for pytest usage.
    environ[ACCESS_TOKEN] = okta_oidc.get_access_token()
