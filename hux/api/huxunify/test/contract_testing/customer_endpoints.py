"""Contracts for CDPs customer-profile-api."""
import datetime
import unittest
import atexit
from pathlib import Path
import requests
from dateutil.relativedelta import relativedelta
from pact import Consumer, Provider
from pact import EachLike, Like, Term
from pact.matchers import get_generated_values

import huxunify.test.constants as t_c
import huxunify.api.constants as api_c

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

    def test_get_count_by_day(self):
        """Test get count by day endpoint to generate pact contract."""
        end_date = datetime.datetime.utcnow()
        start_date = end_date - relativedelta(years=1)
        filters = {
            api_c.START_DATE: start_date.strftime(api_c.DEFAULT_DATE_FORMAT),
            api_c.END_DATE: end_date.strftime(api_c.DEFAULT_DATE_FORMAT),
        }

        expected = {
            "code": 200,
            "body": EachLike(
                {
                    "recorded": Term(r"\d+-\d+-\d+", "2021-06-20"),
                    "total_count": Like(71000),
                    "diff_count": Like(70000),
                }
            ),
            "message": "ok",
        }

        (
            pact.given("Start date and end date passed.")
            .upon_receiving("A request for count by day.")
            .with_request(
                method="POST",
                path=t_c.CUSTOMER_PROFILE_COUNT_BY_DAY,
                body=filters,
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with pact:
            result = requests.post(
                pact.uri + t_c.CUSTOMER_PROFILE_COUNT_BY_DAY,
                json=filters,
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))

    def test_get_spending_by_month(self):
        """Test get spending by month endpoint to generate pact contract."""

        # TODO Fix the producer side response to return 0 instead of null.

        end_date = datetime.datetime.utcnow()
        start_date = end_date - relativedelta(years=1)

        filters = api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER

        # Adding start and end date to filters.
        filters[api_c.START_DATE] = start_date.strftime(
            api_c.DEFAULT_DATE_FORMAT
        )
        filters[api_c.END_DATE] = end_date.strftime(api_c.DEFAULT_DATE_FORMAT)

        # Adding state to filters.
        filters[api_c.AUDIENCE_FILTERS][0][
            api_c.AUDIENCE_SECTION_FILTERS
        ].append(t_c.AUDIENCE_STATE_FILTER)

        expected = {
            "code": 200,
            "body": EachLike(
                {
                    "month": Like(10),
                    "year": Like(2020),
                    "avg_spent_men": Like(11.166666666666666),
                    "avg_spent_women": Like(32.86),
                    "avg_spent_other": Like(18.099999999999998),
                    "gender_men": Like(6),
                    "gender_women": Like(5),
                    "gender_other": Like(3),
                }
            ),
            "message": "ok",
        }

        (
            pact.given("Start date, end date, country, state filter passed.")
            .upon_receiving("A request for spending by month.")
            .with_request(
                method="POST",
                path=t_c.CUSTOMER_PROFILE_SPENDING_BY_MONTH,
                body=filters,
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with pact:
            result = requests.post(
                pact.uri + t_c.CUSTOMER_PROFILE_SPENDING_BY_MONTH,
                json=filters,
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))

    def test_get_city_ltvs(self):
        """Test get city ltvs endpoint to generate pact contract."""

        expected = {
            "code": 200,
            "body": EachLike(
                {
                    "city": Like("Santa Anna"),
                    "state": Like("TX"),
                    "country": Like("US"),
                    "customer_count": Like(5),
                    "avg_ltv": Like(668.03003),
                },
            ),
            "message": "ok",
        }

        (
            pact.given("No filters passed.")
            .upon_receiving("A request for city ltvs.")
            .with_request(
                method="POST",
                path=t_c.CUSTOMER_PROFILE_CITY_LTVS,
                query={"limit": "100", "offset": "0"},
                body={},
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with pact:
            result = requests.post(
                pact.uri + t_c.CUSTOMER_PROFILE_CITY_LTVS,
                params={"limit": "100", "offset": "0"},
                json={},
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))

    def test_get_customer_insights(self):
        """Test get customer insights to generate pact contract."""

        expected = {
            "code": 200,
            "body": {
                "total_records": Like(316574),
                "match_rate": Like(0.5),
                "total_unique_ids": Like(156485),
                "total_unknown_ids": Like(0),
                "total_known_ids": Like(156485),
                "total_individual_ids": Like(126629),
                "total_household_ids": Like(31658),
                "updated": Term(
                    r"\d+-\d+-\d+T\d+:\d+:\d+\.\d+Z",
                    "2021-07-30T11:28:49.109Z",
                ),
                "total_customers": Like(156485),
                "total_countries": Like(1),
                "total_us_states": Like(52),
                "total_cities": Like(14659),
                "min_age": Like(14),
                "max_age": Like(79),
                "avg_age": Like(38),
                "gender_women": Like(62647),
                "gender_men": Like(86029),
                "gender_other": Like(7809),
                "max_ltv_actual": Like(998.79824),
                "max_ltv_predicted": Like(1069.68824),
                "min_ltv_actual": Like(0.00072),
                "min_ltv_predicted": Like(70.89072),
            },
            "message": "ok",
        }

        (
            pact.given("Default filters passed.")
            .upon_receiving("A request for customer insights.")
            .with_request(
                method="POST",
                path=t_c.CDP_CUSTOMER_PROFILE_BASE_ENDPOINT + "insights",
                body=api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER,
                headers={"Content-Type": "application/json"},
            )
            .will_respond_with(200, body=expected)
        )

        with pact:
            result = requests.post(
                pact.uri + t_c.CDP_CUSTOMER_PROFILE_BASE_ENDPOINT + "insights",
                json=api_c.CUSTOMER_OVERVIEW_DEFAULT_FILTER,
                headers={
                    "Content-Type": "application/json",
                },
            )

        self.assertEqual(result.json(), get_generated_values(expected))
