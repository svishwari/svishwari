"""Purpose of this file is for housing pytest startup scripts"""
from os import getenv, environ
from requests.exceptions import MissingSchema
from _pytest.config import Config
from get_okta_token import OktaOIDC

# ENV VARS
OKTA_PARAM_DICT = {
    "org_url": getenv("OKTA_ISSUER"),
    "user": getenv("OKTA_TEST_USER_NAME"),
    "pw": getenv("OKTA_TEST_USER_PW"),
    "client_id": getenv("OKTA_CLIENT_ID"),
    "scopes": "openid+profile+email",
    "redirect_uri": getenv("OKTA_REDIRECT_URI"),
}
ACCESS_TOKEN = "ACCESS_TOKEN"


# pylint: disable=unused-argument
def pytest_configure(config: Config):
    """Override the pytest plugin. This hook is called for every plugin and
        initial conftest file after command line options have been parsed.

    Args:
        config (Config): Existing pytest config.


    """

    try:
        # setup the oidc class.
        okta_oidc = OktaOIDC(**OKTA_PARAM_DICT)

        # set the token for pytest usage.
        environ[ACCESS_TOKEN] = okta_oidc.get_access_token()
    except MissingSchema:
        pass
