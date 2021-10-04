"""Contracts for CDPs customer-profile-api."""
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
    """Generate pact contracts for customer-profile-api endpoints."""

    def setUp(self) -> None:
        """Setup tests."""

        self.hux_id = "HUX000000000000001"

    def test_get_count_by_state(self):
        """Test get count by state endpoint to generate pact contract."""

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

    def test_get_customer_profile_events(self):
        """Test get customer profile events endpoint to generate pact contract."""

        expected = {
            "code": 200,
            "body": EachLike(
                {
                    "total_event_count": Like(25),
                    "event_type_counts": {
                        "abandoned_cart": Like(5),
                        "customer_login": Like(5),
                        "item_purchased": Like(4),
                        "trait_computed": Like(6),
                        "viewed_cart": Like(3),
                        "viewed_checkout": Like(2),
                        "viewed_sale_item": Like(1),
                    },
                    "date": Like("2021-05-24T14:35:12.001Z"),
                }
            ),
            "message": "ok",
        }

        (
            pact.given("No filters passed.")
            .upon_receiving("A request for customer profile events.")
            .with_request(
                method="POST",
                path=t_c.CDP_CUSTOMER_PROFILE_BASE_ENDPOINT
                + self.hux_id
                + "/events",
                body={},
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with pact:
            result = requests.post(
                pact.uri
                + t_c.CDP_CUSTOMER_PROFILE_BASE_ENDPOINT
                + self.hux_id
                + "/events",
                json={},
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))

    def test_get_customer_profile_audience_count(self):
        """Test get customer profile audience count endpoint to generate pact contract."""

        expected = {
            "code": 200,
            "body": Like({"total_count": Like(5)}),
            "message": "ok",
        }

        (
            pact.given("No filters passed.")
            .upon_receiving("A request for audience count.")
            .with_request(
                method="POST",
                path=t_c.CDP_CUSTOMER_PROFILES_AUDIENCE_COUNT,
                body={},
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with pact:
            result = requests.post(
                pact.uri + t_c.CDP_CUSTOMER_PROFILES_AUDIENCE_COUNT,
                json={},
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))

    def test_get_profile_by_huxid(self):
        """Test get customer profile by huxid endpoint to generate pact contract."""

        expected = {
            "code": 200,
            "body": Like(
                {
                    "id": Like("1531-2039-11"),
                    "first_name": Like("John"),
                    "last_name": Like("Doe"),
                    "match_confidence": Like(3),
                    "since": Like("2021-05-24T00:00:00.000"),
                    "ltv_actual": Like(5.07),
                    "ltv_predicted": Like(6.28),
                    "conversion_time": Like(3.48),
                    "churn_rate": Like(5),
                    "last_click": Like("2021-04-18T15:23:00.000z"),
                    "last_purchase": Like("2021-01-21T12:52:00.000z"),
                    "last_email_open": Like("2021-05-22T14:02:00.000z"),
                    "email": Like("john.doe@microsoft.com"),
                    "phone": Like("+19995551234"),
                    "age": Like(43),
                    "gender": Like("M"),
                    "address": Like("Silence st., 5 apt 4"),
                    "city": Like("New Springs"),
                    "state": Like("CO"),
                    "zip": Like("80013"),
                    "preference_email": Like(True),
                    "preference_push": Like(True),
                    "preference_sms": Like(True),
                    "preference_in_app": Like(False),
                    "identity_resolution": Like(
                        {
                            "name": Like(
                                {
                                    "percentage": Like(0.26),
                                    "count": Like(52),
                                    "data_sources": EachLike(
                                        [
                                            {
                                                "id": Like(
                                                    "585t749997acad4bac4373b"
                                                ),
                                                "name": Like("Netsuite"),
                                                "type": Like("net-suite"),
                                                "percentage": Like(0.26),
                                                "count": Like(52),
                                            }
                                        ]
                                    ),
                                    "cooccurrences": EachLike(
                                        [
                                            {
                                                "identifier": Like("address"),
                                                "count": Like(12),
                                                "percentage": Like(0.5),
                                            }
                                        ]
                                    ),
                                }
                            ),
                            "address": Like(
                                {
                                    "percentage": Like(0.26),
                                    "count": Like(52),
                                    "data_sources": EachLike(
                                        [
                                            {
                                                "id": Like(
                                                    "585t749997acad4bac4373b"
                                                ),
                                                "name": Like("Netsuite"),
                                                "type": Like("net-suite"),
                                                "percentage": Like(0.26),
                                                "count": Like(52),
                                            }
                                        ]
                                    ),
                                    "cooccurrences": EachLike(
                                        [
                                            {
                                                "identifier": Like("address"),
                                                "count": Like(12),
                                                "percentage": Like(0.5),
                                            }
                                        ]
                                    ),
                                }
                            ),
                            "email": Like(
                                {
                                    "percentage": Like(0.26),
                                    "count": Like(52),
                                    "data_sources": EachLike(
                                        [
                                            {
                                                "id": Like(
                                                    "585t749997acad4bac4373b"
                                                ),
                                                "name": Like("Netsuite"),
                                                "type": Like("net-suite"),
                                                "percentage": Like(0.26),
                                                "count": Like(52),
                                            }
                                        ]
                                    ),
                                    "cooccurrences": EachLike(
                                        [
                                            {
                                                "identifier": Like("address"),
                                                "count": Like(12),
                                                "percentage": Like(0.5),
                                            }
                                        ]
                                    ),
                                }
                            ),
                            "phone": Like(
                                {
                                    "percentage": Like(0.26),
                                    "count": Like(52),
                                    "data_sources": EachLike(
                                        [
                                            {
                                                "id": Like(
                                                    "585t749997acad4bac4373b"
                                                ),
                                                "name": Like("Netsuite"),
                                                "type": Like("net-suite"),
                                                "percentage": Like(0.26),
                                                "count": Like(52),
                                            }
                                        ]
                                    ),
                                    "cooccurrences": EachLike(
                                        [
                                            {
                                                "identifier": Like("address"),
                                                "count": Like(12),
                                                "percentage": Like(0.5),
                                            }
                                        ]
                                    ),
                                }
                            ),
                            "cookie": Like(
                                {
                                    "percentage": Like(0.26),
                                    "count": Like(52),
                                    "data_sources": EachLike(
                                        [
                                            {
                                                "id": Like(
                                                    "585t749997acad4bac4373b"
                                                ),
                                                "name": Like("Netsuite"),
                                                "type": Like("net-suite"),
                                                "percentage": Like(0.26),
                                                "count": Like(52),
                                            }
                                        ]
                                    ),
                                    "cooccurrences": EachLike(
                                        [
                                            {
                                                "identifier": Like("address"),
                                                "count": Like(12),
                                                "percentage": Like(0.5),
                                            }
                                        ]
                                    ),
                                }
                            ),
                        }
                    ),
                    "propensity_to_unsubscribe": Like(4),
                    "propensity_to_purchase": Like(6.5),
                }
            ),
            "message": "ok",
        }

        (
            pact.given("HUX ID exists.")
            .upon_receiving("A request for customer profile by hux id.")
            .with_request(
                method="GET",
                path=t_c.CDP_CUSTOMER_PROFILE_BASE_ENDPOINT + self.hux_id,
                body={},
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with pact:
            result = requests.get(
                pact.uri
                + t_c.CDP_CUSTOMER_PROFILE_BASE_ENDPOINT
                + self.hux_id,
                json={},
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))
