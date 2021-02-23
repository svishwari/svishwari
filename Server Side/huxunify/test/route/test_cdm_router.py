"""
purpose of this file is testing the CDM router
"""
from unittest import TestCase
from app import create_app


class TestCdm(TestCase):
    """
    test all CDM routes
    """
    def setUp(self):
        """
        setup the initial test client
        """
        self.app = create_app().test_client()

    def test_index(self):
        """
        Tests the route screen message for the landing page
        """
        api_route = self.app.get('/api/cdm/')

        # If we recalculate the hash on the block we should get the same result as we have stored
        self.assertEqual({"message": 'Hello cdm'}, api_route.get_json())
