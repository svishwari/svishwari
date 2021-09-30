"""Contracts for CDPs customer-profile-api"""
import unittest
import atexit
from pathlib import Path
import requests
from pact import Consumer, Provider
from pact import EachLike, Like
from pact.matchers import get_generated_values
import huxunify.test.constants as t_c

# Folder where generated pacts are stored.
contracts_folder = Path(__file__).parent.joinpath(t_c.CONTRACTS_FOLDER)

# Initializing pact
pact = Consumer(t_c.HUX).has_pact_with(
    Provider(t_c.CDP_CUSTOMER_PROFILE), pact_dir=str(contracts_folder)
)
pact.start_service()

atexit.register(pact.stop_service)


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
                path=t_c.CUSTOMER_PROFILE_COUNT_BY_STATE_ENDPOINT,
                body={},
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with pact:
            result = requests.post(
                pact.uri + t_c.CUSTOMER_PROFILE_COUNT_BY_STATE_ENDPOINT,
                json={},
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))
