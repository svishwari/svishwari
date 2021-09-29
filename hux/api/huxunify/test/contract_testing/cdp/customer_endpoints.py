"""Contracts for CDPs customer-profile-api"""
import unittest
import requests

from pact import EachLike, Like
from pact.matchers import get_generated_values

from huxunify.test.contract_testing.cdp import hux_cdp_pact as pact


class CDPCustomersContracts(unittest.TestCase):
    """
    Generate pact contracts for customer-profile-api endpoints.
    """

    def test_get_count_by_state(self):
        """
        Test get count by state endpoint to generate pact contract.

        Args:

        Returns:
            None
        """
        expected = {
            "code": 200,
            "body": EachLike(
                {
                    "state": Like("IN"),
                    "country": Like("US"),
                    "gender_men": Like(2028),
                    "gender_women": Like(1461),
                    "gender_other": Like(191),
                    "size": Like(3680),
                    "avg_ltv": Like(240.05151167119567),
                }
            ),
            "message": "ok",
        }

        (
            pact.given("No filters passed.")
            .upon_receiving("A request for count by state.")
            .with_request(
                method="POST",
                path="/customer-profiles/insights/count-by-state",
                body={},
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with pact:
            result = requests.post(
                pact.uri + "/customer-profiles/insights/count-by-state",
                json={},
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))
