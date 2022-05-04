"""Purpose of this file is for testing that the app can be created without any
issues."""
from http import HTTPStatus
from unittest import TestCase

from flask.testing import FlaskClient
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from huxunify.api.config import get_config
from huxunify.app import create_app
from huxunify.api import constants as api_c
import huxunify.test.constants as t_c


class CreateAppTest(TestCase):
    """Test Creating an App."""

    def setUp(self) -> None:
        """Setup tests."""

        self.config = get_config(api_c.TEST_MODE)

    def test_creating_flask_app(self):
        """Test Creating the APP test client."""

        self.assertIsInstance(create_app().test_client(), FlaskClient)

    def test_app_ratelimit_success(self):
        """Test rate limit success."""

        app = create_app()
        self.assertIsInstance(app.test_client(), FlaskClient)

        limiter = Limiter(
            app,
            key_func=get_remote_address,
            default_limits=["4 per day", "2 per hour"],
        )

        @app.route("/fast")
        @limiter.limit("4/day")
        # pylint: disable=missing-return-doc,missing-return-type-doc,unused-variable
        def fast():
            return (
                {"msg": "test"},
                HTTPStatus.OK,
            )

        response = app.test_client().get(
            ("/fast"),
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(response.json["msg"], "test")
        response = app.test_client().get(
            ("/fast"),
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(response.json["msg"], "test")

    def test_app_ratelimit_fail(self):
        """Test rate limit failure."""

        app = create_app()
        self.assertIsInstance(app.test_client(), FlaskClient)

        limiter = Limiter(
            app,
            key_func=get_remote_address,
            default_limits=["2 per day", "1 per hour"],
        )

        @app.route("/fast")
        @limiter.limit("1/day")
        # pylint: disable=missing-return-doc,missing-return-type-doc,unused-variable
        def fast():
            return (
                {"msg": "test"},
                HTTPStatus.OK,
            )

        response = app.test_client().get(
            ("/fast"),
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(response.json["msg"], "test")
        response = app.test_client().get(
            ("/fast"),
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(response.status_code, 429)
