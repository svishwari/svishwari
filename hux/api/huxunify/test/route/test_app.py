"""Purpose of this file is for testing that the app can be created without any
issues."""
from unittest import TestCase

from flask.testing import FlaskClient

from huxunify.api.config import get_config
from huxunify.app import create_app
from huxunify.api import constants as api_c


class CreateAppTest(TestCase):
    """Test Creating an App."""

    def setUp(self) -> None:
        """Setup tests."""

        self.config = get_config(api_c.TEST_MODE)

    def test_creating_flask_app(self):
        """Test Creating the APP test client."""

        self.assertIsInstance(create_app().test_client(), FlaskClient)
