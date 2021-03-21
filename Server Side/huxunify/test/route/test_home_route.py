"""
Purpose of this script for testing the home route
"""
from unittest import TestCase
from huxunify.app import create_app


class TestHome(TestCase):
    """
    test all welcome routes
    """

    def setUp(self):
        """
        setup the initial test client
        """
        self.app = create_app().test_client()

    def test_home(self):
        """
        Tests the route screen message
        """
        api_route = self.app.get("/api/")

        # If we recalculate the hash on the block we should get the same result as we have stored
        self.assertEqual(
            {"message": "Hello Hux Unified Solution"}, api_route.get_json()
        )
