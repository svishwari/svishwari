"""Purpose of this file is to test customers"""

from unittest import TestCase
import pytest
import requests
from hux.integration_tests.api.test.conftest import Crud

class TestCustomers(TestCase):
    """Test Customers"""

    CUSTOMERS = "customers"

    def test_customers_overview(self):
        """Testing customers overview endpoint"""

        response = requests.get(f"{pytest.API_URL}/{self.CUSTOMERS}/overview",
                                headers=pytest.HEADERS)

        self.assertEqual(200, response.status_code)
