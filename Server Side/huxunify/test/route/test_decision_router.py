"""
purpose of this file is testing the decision router
"""
from unittest import TestCase
from app import create_app


class TestDecision(TestCase):
    """
    test all decision routes
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
        api_route = self.app.get('/api/decision/')

        # If we recalculate the hash on the block we should get the same result as we have stored
        self.assertEqual({"message": 'Hello Decisioning'}, api_route.get_json())
