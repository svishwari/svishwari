"""
purpose of this file is for testing that the app can be created without any issues.
"""
from unittest import TestCase

from flask.testing import FlaskClient

from huxunify.api.config import get_config
from huxunify.app import create_app


class CreateAppTest(TestCase):
    """
    Test Creating an App.
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.config = get_config("TEST")

    def test_secured_all_endpoints_invalid_response(self):
        """Test Creating the APP test client

        Args:

        Returns:

        """
        self.assertIsInstance(create_app().test_client(), FlaskClient)
