"""Purpose of this file is to test customers."""
import datetime
from http import HTTPStatus
from unittest import TestCase
import pytest
import requests


class TestCustomers(TestCase):
    """Test Customers"""

    CUSTOMERS = "customers"
    CUSTOMERS_INSIGHTS = "customers-insights"
    IDR = "idr"
    AUDIENCES = "audiences"

    def test_customers_insights_countries(self):
        """Testing customers insights countries."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS_INSIGHTS}/countries",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_customers_insights_revenue(self):
        """Testing customers insights revenue."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS_INSIGHTS}/revenue",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_customers_insights_states(self):
        """Testing customers insights states."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS_INSIGHTS}/states",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_customers_insights_cities(self):
        """Testing customers insights cities."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS_INSIGHTS}/cities",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_customers_insights_total(self):
        """Testing customers insights total."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS_INSIGHTS}/total",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_customers_insights_demo(self):
        """Testing customers insights demo."""

        start_date = (
            datetime.datetime.utcnow() - datetime.timedelta(days=90)
        ).strftime("%Y-%m-%d")
        end_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")

        response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS_INSIGHTS}/demo?"
            f"start_date={start_date}&end_date={end_date}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_customers_insights_geo(self):
        """Testing customers insights geo."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS_INSIGHTS}/geo",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_customers_overview(self):
        """Testing customers overview endpoint."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS}/overview",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_post_customers_overview(self):
        """Testing Post customer overview endpoint."""

        response = requests.post(
            f"{pytest.API_URL}/{self.CUSTOMERS}/overview",
            json={
                "filters": [
                    {
                        "section_aggregator": "ALL",
                        "section_filters": [
                            {
                                "field": "country",
                                "type": "equals",
                                "value": "US",
                            }
                        ],
                    }
                ]
            },
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_customers_list(self):
        """Test customers list."""

        response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS}?batch_size=1000&batch_number=1",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_customers_events(self):
        """Test Customer events."""

        customers_list_response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS}", headers=pytest.HEADERS
        )

        start_date = (
            datetime.datetime.utcnow() - datetime.timedelta(days=90)
        ).strftime("%Y-%m-%d")
        end_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")

        response = requests.post(
            f"{pytest.API_URL}/{self.CUSTOMERS}/"
            f'{customers_list_response.json()["customers"][0]["hux_id"]}'
            f"/events?interval=day",
            json={"start_date": start_date, "end_date": end_date},
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_customer_profile(self):
        """Test Customer profile."""

        customers_list_response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS}", headers=pytest.HEADERS
        )

        response = requests.get(
            f"{pytest.API_URL}/{self.CUSTOMERS}/"
            f'{customers_list_response.json()["customers"][0]["hux_id"]}',
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_idr_matching_trends(self):
        """Testing idr matching trends."""

        response = requests.get(
            f"{pytest.API_URL}/{self.IDR}/matching-trends",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_idr_datafeeds(self):
        """Testing idr datafeeds."""

        response = requests.get(
            f"{pytest.API_URL}/{self.IDR}/datafeeds", headers=pytest.HEADERS
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_idr_overview(self):
        """Testing idr overview."""

        response = requests.get(
            f"{pytest.API_URL}/{self.IDR}/overview", headers=pytest.HEADERS
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_idr_datafeed(self):
        """Testing idr datafeed."""

        datafeeds_response = requests.get(
            f"{pytest.API_URL}/{self.IDR}/datafeeds", headers=pytest.HEADERS
        )

        response = requests.get(
            f"{pytest.API_URL}/{self.IDR}/datafeeds/"
            f"{str(datafeeds_response.json()[0]['datafeed_id'])}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_audience_insights_revenue(self):
        """Testing audience insights revenue."""

        audience_id = requests.get(
            f"{pytest.API_URL}/audiences",
            headers=pytest.HEADERS,
        ).json()[0]["id"]

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/revenue",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_audience_insights_total(self):
        """Testing audience insights total."""

        audience_id = requests.get(
            f"{pytest.API_URL}/audiences",
            headers=pytest.HEADERS,
        ).json()[0]["id"]

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{audience_id}/total",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
