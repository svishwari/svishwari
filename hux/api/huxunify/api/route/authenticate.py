"""
Paths for Authentication api
"""
import logging
from os import getenv
from http import HTTPStatus
from typing import Tuple
import requests
from mongomock import MongoClient
from flasgger import SwaggerView
from flask import Blueprint

from huxunifylib.database.user_management import get_user, set_user
from connexion.exceptions import ProblemException

from huxunify.api.schema.utils import AUTH401_RESPONSE
from huxunify.api.schema.errors import NotFoundError
from huxunify.api.route.utils import add_view_to_blueprint
import huxunify.api.constants as api_c

ISSUER = getenv(api_c.AUTHENTICATION_OKTA_ISSUER)
CLIENT_ID = getenv(api_c.AUTHENTICATION_OKTA_CLIENT_ID)

# setup authentication blueprint
auth_bp = Blueprint(api_c.AUTHENTICATION_ENDPOINT, import_name=__name__)


def get_db_client() -> MongoClient:
    """Get DB client.
    Returns:
        MongoClient: DB client
    """
    # TODO - hook-up when ORCH-94 HUS-262 are completed
    return MongoClient()


def introspect_token(access_token: str, issuer: str, client_id: str) -> dict:
    """Calls Okta's introspect endpoint and returns the token's payload when
    the token is valid and active.
    Args:
        access_token (str): The encoded JWT access token, provided by Okta.
        issuer (str): The Okta issuer URL.
        client_id (str): The Okta application client ID.
    Returns:
        payload (dict): The decoded payload data from the Okta access token.
    """
    payload = requests.post(
        url=f"{issuer}/oauth2/v1/introspect?client_id={client_id}",
        data={
            api_c.AUTHENTICATION_TOKEN: access_token,
            api_c.AUTHENTICATION_TOKEN_TYPE_HINT: api_c.AUTHENTICATION_ACCESS_TOKEN,
        },
    ).json()

    return payload if payload.get("active") else None


@add_view_to_blueprint(
    auth_bp,
    f"{api_c.AUTHENTICATION_ENDPOINT}/<access_token>",
    "AuthenticationView",
)
class AuthenticationView(SwaggerView):
    """Authentication View Class"""

    parameters = [
        {
            "name": api_c.AUTHENTICATION_TOKEN,
            "in": "path",
            "type": "string",
            "description": "Access Token.",
            "example": "efb9823ru328fh3928rfh3918",
            "required": True,
        }
    ]

    responses = {
        HTTPStatus.OK.value: {"description": "Authenticated User"},
        HTTPStatus.NOT_FOUND.value: {
            "schema": NotFoundError,
        },
    }
    responses.update(AUTH401_RESPONSE)
    tags = [api_c.AUTHENTICATION_TAG]

    # pylint: disable=no-self-use
    def authorize(self, access_token: str) -> Tuple[dict, int]:
        """Validates the provided JWT access token and authorizes the user to
        access the HUX API.
        Args:
            access_token (str): The encoded JWT access token, provided by Okta.
        Returns:
            Tuple[dict, int]: dict of user and http code
        """

        try:
            payload = introspect_token(
                access_token=access_token,
                issuer=ISSUER,
                client_id=CLIENT_ID,
            )

            if payload is not None:
                user = get_user(get_db_client(), okta_id=payload.uid)
                if user is None:
                    set_user(
                        get_db_client(),
                        okta_id=payload.uid,
                        email_address=payload.email,
                    )
                return HTTPStatus.OK
            return HTTPStatus.NOT_FOUND
        except Exception as exception:
            # raises a general OAuth problem exception to respond with a 401
            logging.error(
                "%s. Reason:[%s: %s].",
                api_c.CANNOT_AUTHENTICATE_USER,
                exception.__class__,
                exception,
            )
            raise ProblemException(
                status=int(HTTPStatus.BAD_REQUEST.value),
                title=HTTPStatus.BAD_REQUEST.description,
                detail=api_c.CANNOT_AUTHENTICATE_USER,
            ) from exception
