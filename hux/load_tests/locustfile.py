# pylint: disable=too-many-public-methods
"""Locust file."""
import logging
from datetime import datetime
from http import HTTPStatus
from os import getenv
from dotenv import load_dotenv
from locust import HttpUser, task
from locust.log import setup_logging
from get_okta_token import OktaOIDC

load_dotenv()
setup_logging("INFO", None)


# ENV VARS
OKTA_PARAM_DICT = {
    "org_url": getenv("OKTA_ISSUER"),
    "user": getenv("OKTA_TEST_USER_NAME"),
    "pw": getenv("OKTA_TEST_USER_PW"),
    "client_id": getenv("OKTA_CLIENT_ID"),
    "scopes": "openid+profile+email",
    "redirect_uri": getenv("OKTA_REDIRECT_URI"),
}
ACCESS_TOKEN = "ACCESS_TOKEN"


class APIUser(HttpUser):
    """Load test User class."""

    def __init__(self, *args, **kwargs):
        """override the init and define custom attributes"""
        super().__init__(*args, **kwargs)
        self.headers = None

    # A User will call its on_start method when it starts running
    def on_start(self):
        logging.info("Starting load tests")
        okta_oidc = OktaOIDC(**OKTA_PARAM_DICT)
        # set the token for pytest usage.
        access_token = okta_oidc.get_access_token(False)
        # pylint: disable=attribute-defined-outside-init
        self.headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

    # When the instance of this user stops, the initialized test data is deleted.
    def on_stop(self):
        logging.info("Stopping load tests")

    # When a load test is started, an instance of a User
    # class will be created for each simulated user.
    # Each user will start running within their own green thread.
    # When these users run they pick tasks that they execute,
    # sleep for a while, and then pick a new task and so on.
    @task
    def get_audiences(self):
        """Load test method for GET all audiences."""

        with self.client.get(
            "/audiences", headers=self.headers, catch_response=True
        ) as response:
            # ensure the response is valid.
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_audience_rules(self):
        """Load test method for GET all audience rules."""

        with self.client.get(
            "/audiences/rules", headers=self.headers, catch_response=True
        ) as response:
            # ensure the response is valid.
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_audience(self):
        """Load test method for GET an audience by id."""

        with self.client.get(
            "/audiences", headers=self.headers, catch_response=True
        ) as response:
            # ensure the response is valid.
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                with self.client.get(
                    "/audiences/" + response.json[0]["_id"],
                    headers=self.headers,
                    catch_response=True,
                ) as response:
                    # ensure the response is valid.
                    if response.status_code != HTTPStatus.OK:
                        response.failure(response.status_code)

    @task
    def create_audience(self):
        """Load test method to create audiences."""

        audience_post = {
            "name": "Test Audience Create",
            "filters": [
                {
                    "section_aggregator": "ALL",
                    "section_filters": [
                        {"field": "country", "type": "equals", "value": "US"}
                    ],
                }
            ],
        }

        with self.client.get(
            "/audiences", headers=self.headers, json=audience_post, catch_response=True
        ) as response:
            # ensure the response is valid.
            if response.status_code != HTTPStatus.CREATED:
                response.failure(response.status_code)

    @task
    def delete_audience(self):
        """Load test method to delete an audiences."""

        audience_post = {
            "name": "Test Audience Create",
            "filters": [
                {
                    "section_aggregator": "ALL",
                    "section_filters": [
                        {"field": "country", "type": "equals", "value": "US"}
                    ],
                }
            ],
        }

        with self.client.get(
            "/audiences", headers=self.headers, json=audience_post, catch_response=True
        ) as response:
            # ensure the response is valid.
            if response.status_code != HTTPStatus.CREATED:
                response.failure(response.status_code)
            else:
                with self.client.get(
                    "/audiences/" + response.json["id"],
                    headers=self.headers,
                    catch_response=True,
                ) as response:
                    # ensure the response is valid.
                    if response.status_code != HTTPStatus.NO_CONTENT:
                        response.failure(response.status_code)

    @task
    def audience_insights_revenue(self):
        """Testing audience insights revenue."""

        with self.client.get(
            "/audiences", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                audience_id = response.json()[0]["id"]
                with self.client.get(
                    f"/audiences/{audience_id}/revenue",
                    headers=self.headers,
                    catch_response=True,
                ) as response:
                    if response.status_code != HTTPStatus.OK:
                        response.failure(response.status_code)

    @task
    def audience_insights_total(self):
        """Testing audience insights total."""

        with self.client.get(
            "/audiences", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                audience_id = response.json()[0]["id"]
                with self.client.get(
                    f"/audiences/{audience_id}/total",
                    headers=self.headers,
                    catch_response=True,
                ) as response:
                    if response.status_code != HTTPStatus.OK:
                        response.failure(response.status_code)

    @task
    def get_destinations(self):
        """Load test method for GET all destinations."""
        with self.client.get(
            "/destinations", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_destination_constants(self):
        """Load test method for GET destination constants."""
        with self.client.get(
            "/destinations/constants", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def validate_destination(self):
        """Load test method to validate a destination."""
        with self.client.get(
            "/destinations/constants", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_all_applications(self):
        """Test get all applications"""

        with self.client.get(
            "/applications", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def create_application(self):
        """Test create application"""

        payload = {
            "category": "test_category",
            "name": "test_create_application",
            "url": "www.testapplication.com",
        }
        with self.client.post(
            "/applications", headers=self.headers, json=payload, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.CREATED:
                response.failure(response.status_code)

    @task
    def update_application(self):
        """Test update application"""

        payload = {
            "category": "test_category",
            "name": "test_create_application",
            "url": "www.testapplication.com",
        }
        with self.client.post(
            "/applications", headers=self.headers, json=payload, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.CREATED:
                response.failure(response.status_code)
            else:
                payload = {"url": "www.testupdateapplication2.com"}
                with self.client.patch(
                    "/applications",
                    headers=self.headers,
                    json=payload,
                    catch_response=True,
                ) as response:
                    if response.status_code != HTTPStatus.OK:
                        response.failure(response.status_code)

    @task
    def get_all_configurations(self):
        """Test get all configurations."""

        with self.client.get(
            "/configurations", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_navigation_settings_type_configurations(self):
        """Test get configurations of type navigation settings."""

        with self.client.get(
            "/configurations/navigation", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def test_update_navigation_settings_type_configuration(self):
        """Test update configuration of a navigation settings type."""

        with self.client.get(
            "/configurations/navigation", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                with self.client.put(
                    "/cconfigurations/navigation",
                    headers=self.headers,
                    json=response.json(),
                    catch_response=True,
                ) as response:
                    if response.status_code != HTTPStatus.OK:
                        response.failure(response.status_code)

    @task
    def customers_insights_countries(self):
        """Testing customers insights countries."""

        with self.client.get(
            "/customers-insights/countries", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def customers_insights_revenue(self):
        """Testing customers insights revenue."""

        with self.client.get(
            "/customers-insights/revenue", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def customers_insights_states(self):
        """Testing customers insights states."""

        with self.client.get(
            "/customers-insights/states", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def customers_insights_cities(self):
        """Testing customers insights cities."""

        with self.client.get(
            "/customers-insights/cities", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def customers_insights_total(self):
        """Testing customers insights total."""

        with self.client.get(
            "/customers-insights/total", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def customers_insights_demo(self):
        """Testing customers insights demo."""

        start_date = (
            datetime.datetime.utcnow() - datetime.timedelta(days=90)
        ).strftime("%Y-%m-%d")
        end_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")

        with self.client.get(
            f"/customers-insights/demo?" f"start_date={start_date}&end_date={end_date}",
            headers=self.headers,
            catch_response=True,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def customers_insights_geo(self):
        """Testing customers insights geo."""

        with self.client.get(
            "/customers-insights/geo", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_customers_overview(self):
        """Testing customers overview endpoint."""

        with self.client.get(
            "/customers/overview", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def post_customers_overview(self):
        """Testing Post customer overview endpoint."""

        payload = {
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
        }
        with self.client.post(
            "/customers/overview",
            headers=self.headers,
            json=payload,
            catch_response=True,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def customers_list(self):
        """Test customers list."""

        with self.client.get(
            "/customers?batch_size=1000&batch_number=1",
            headers=self.headers,
            catch_response=True,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def customers_events(self):
        """Test Customer events."""

        start_date = (
            datetime.datetime.utcnow() - datetime.timedelta(days=90)
        ).strftime("%Y-%m-%d")
        end_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")

        with self.client.get(
            "/customers", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                with self.client.post(
                    f"/customers/"
                    f'{response.json()["customers"][0]["hux_id"]}'
                    f"/events?interval=day",
                    json={"start_date": start_date, "end_date": end_date},
                    headers=self.headers,
                    catch_response=True,
                ) as response:
                    if response.status_code != HTTPStatus.OK:
                        response.failure(response.status_code)

    @task
    def customer_profile(self):
        """Test Customer profile."""

        with self.client.get(
            "/customers", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                with self.client.get(
                    f"/customers/" f'{response.json()["customers"][0]["hux_id"]}',
                    headers=self.headers,
                    catch_response=True,
                ) as response:
                    if response.status_code != HTTPStatus.OK:
                        response.failure(response.status_code)

    @task
    def idr_matching_trends(self):
        """Testing idr matching trends."""

        with self.client.get(
            "/idr/matching-trends", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def idr_datafeeds(self):
        """Testing idr datafeeds."""

        with self.client.get(
            "/idr/datafeeds", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def test_idr_overview(self):
        """Testing idr overview."""

        with self.client.get(
            "/idr/overview", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def test_idr_datafeed(self):
        """Testing idr datafeed."""

        with self.client.get(
            "/idr/datafeeds", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                with self.client.get(
                    f"/idr/datafeeds" f"{str(response.json()[0]['datafeed_id'])}",
                    headers=self.headers,
                    catch_response=True,
                ) as response:
                    if response.status_code != HTTPStatus.OK:
                        response.failure(response.status_code)
