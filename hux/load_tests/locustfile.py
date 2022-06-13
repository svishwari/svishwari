# pylint: disable=too-many-public-methods
"""Locust file."""
import logging
from datetime import datetime, timedelta
from http import HTTPStatus
from os import getenv
from time import time

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

        # get an engagement and an audience associated to it
        engagements = self.client.get(
            "/engagements",
            headers=self.headers,
        ).json()

        self.engagement_id = None
        self.audience_id = None
        self.facebook_destination_id = None

        for engagement in engagements:
            for audience in engagement["audiences"]:
                for destination in audience["destinations"]:
                    # ensure the destination exists
                    get_destination = self.client.get(
                        f'/destinations/{destination["id"]}',
                        headers=self.headers,
                    )
                    if get_destination.status_code == 404:
                        continue
                    # fetch only facebook's destination_id
                    if get_destination.json()["name"] != "Facebook":
                        continue
                    # ensure that the audience is not a lookalike audience
                    # since delivery requires regular audience
                    get_audience = self.client.get(
                        f'/audiences/{audience["id"]}',
                        headers=self.headers,
                    )
                    get_audience_response = get_audience.json()
                    if (
                        get_audience.status_code == 200
                        and get_audience_response
                        and "is_lookalike" in get_audience_response
                        and get_audience_response["is_lookalike"]
                    ):
                        continue
                    self.engagement_id = engagement["id"]
                    self.audience_id = audience["id"]
                    self.facebook_destination_id = destination["id"]
                    break
                else:
                    continue
                break
            else:
                continue
            break

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
                    "/audiences/" + response.json()["audiences"][0]["id"],
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
                response.failure(response.status_code)
            else:
                with self.client.delete(
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
                audience_id = response.json()["audiences"][0]["id"]
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
                audience_id = response.json()["audiences"][0]["id"]
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
            "category": "load_test_category",
            "name": "load_test_create_application",
            "url": "www.loadtestapplication.com",
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
            "category": "load_test_category",
            "name": "load_test_create_application",
            "url": "www.loadtestapplication.com",
        }
        with self.client.post(
            "/applications", headers=self.headers, json=payload, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.CREATED:
                response.failure(response.status_code)
            else:
                payload = {"url": "www.loadtestupdateapplication2.com"}
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

        start_date = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
        end_date = datetime.utcnow().strftime("%Y-%m-%d")

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

        start_date = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
        end_date = datetime.utcnow().strftime("%Y-%m-%d")

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

    @task
    def create_data_source(self):
        """Test creating a datasource."""

        with self.client.post(
            "/data-sources",
            headers=self.headers,
            catch_response=True,
            json=[
                {
                    "name": "Load Test Data source",
                    "type": "dataSource",
                    "status": "Active",
                    "category": "load-test",
                }
            ],
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                self.client.delete(
                    "/data-sources?datasources=dataSource",
                    headers=self.headers,
                    catch_response=True,
                )

    @task
    def create_model(self):
        """Test creating an model."""

        with self.client.post(
            "/models",
            headers=self.headers,
            catch_response=True,
            json=[
                {
                    "type": "load-test",
                    "name": "Load Test to Purchase",
                    "id": "9a44c346ba034ac8a699ae0ab3314003",
                    "status": "requested",
                },
                {
                    "type": "load-test",
                    "name": "Load Test to Unsubscribe",
                    "id": "eb5f35e34c0047d3b9022ef330952dd1",
                    "status": "requested",
                },
            ],
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                model_id = response.json()["id"]
                self.client.delete(
                    f"/models?model_id={model_id}",
                    headers=self.headers,
                    catch_response=True,
                )

    @task
    def get_models(self):
        """Test get all models."""

        with self.client.get(
            "/models", headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def update_model(self):
        """Test updating an model."""

        with self.client.post(
            "/models",
            headers=self.headers,
            catch_response=True,
            json=[
                {
                    "type": "Load test",
                    "name": "Propensity to Purchase",
                    "category": "Email",
                    "description": "Likelihood of customer to purchase",
                    "status": "requested",
                    "is_added": True,
                }
            ],
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                model_id = response.json()["id"]
                with self.client.patch(
                    "/models",
                    headers=self.headers,
                    catch_response=True,
                    json=[
                        {
                            "id": model_id,
                            "type": "Load test",
                            "name": "Propensity to Purchase - Updated",
                            "category": "Email",
                            "description": "Likelihood of customer to purchase",
                            "status": "requested",
                            "is_added": True,
                        }
                    ],
                ) as response:
                    if response.status_code != HTTPStatus.OK:
                        response.failure(response.status_code)
                self.client.delete(
                    f"/models?model_id={model_id}",
                    headers=self.headers,
                    catch_response=True,
                )

    @task
    def get_engagement_delivery_history(self):
        """Test get engagement delivery history."""

        with self.client.get(
            f"/engagements/{self.engagement_id}/delivery-history",
            headers=self.headers,
            catch_response=True,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_audience_delivery_history(self):
        """Test get audience delivery history."""

        with self.client.get(
            f"/audiences/{self.audience_id}/delivery-history",
            headers=self.headers,
            catch_response=True,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def deliver_audience_to_destination(self):
        """Test deliver audience to a destination."""

        with self.client.post(
            f"/audiences/{self.audience_id}/deliver",
            headers=self.headers,
            catch_response=True,
            json={
                "destinations": [
                    {
                        "id": self.facebook_destination_id,
                    },
                ],
            },
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def deliver_audience_in_engagement(self):
        """Test deliver audience that is part of an engagement."""

        with self.client.post(
            f"/engagements/{self.engagement_id}/deliver?"
            f"destinations={self.facebook_destination_id}&"
            f"audiences={self.audience_id}",
            headers=self.headers,
            catch_response=True,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def deliver_engagement_audience_to_destination(self):
        """Test deliver an engagement audience to a destination."""

        with self.client.post(
            f"/engagements/{self.engagement_id}/audience{self.audience_id}/destination/"
            f"{self.facebook_destination_id}/deliver",
            headers=self.headers,
            catch_response=True,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def update_and_delete_destination_delivery_schedule_in_engagement_audience(
        self,
    ):
        """Test updating and followed by deleting delivery schedule for a
        destination in an engagement audience."""

        with self.client.post(
            f"/engagements/{self.engagement_id}/"
            f"audience/{self.audience_id}/destination/"
            f"{self.facebook_destination_id}/schedule",
            headers=self.headers,
            catch_response=True,
            json={
                "periodicity": "Daily",
                "every": 21,
                "hour": 11,
                "minute": 15,
                "period": "PM",
            },
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                self.client.delete(
                    f"/engagements/{self.engagement_id}/"
                    f"audience/{self.audience_id}/destination/"
                    f"{self.facebook_destination_id}/schedule",
                    headers=self.headers,
                )

    @task
    def create_engagement(self):
        """Test creating an engagement."""

        with self.client.post(
            "/engagements",
            json={
                "name": f"load test engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"Load Test Engagement Desc-" f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.facebook_destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=self.headers,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                engagement_id = response.json()["id"]
                self.client.delete(
                    f"/engagements/{engagement_id}",
                    headers=self.headers,
                )

    @task
    def get_engagements(self):
        """Test get all engagements."""

        with self.client.post(
            "/engagements/",
            headers=self.headers,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_engagement_by_id(self):
        """Test get engagement by ID."""

        with self.client.post(
            f"/engagements/{self.engagement_id}",
            headers=self.headers,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def distinct_users(self) -> None:
        """Test GET /notifications/users"""

        with self.client.get(
            "/notifications/users",
            headers=self.headers,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def create_notification(self) -> None:
        """Test create a notification"""

        with self.client.post(
            "/notifications",
            json={
                "category": "delivery",
                "type": "success",
                "description": "Load test create notification.",
            },
            headers=self.headers,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
            else:
                notification_id = response.json()["id"]
                self.client.delete(
                    f"/notifications/{notification_id}",
                    headers=self.headers,
                )

    @task
    def get_notifications(self) -> None:
        """Test get a notification"""

        with self.client.get(
            "/notifications",
            headers=self.headers,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_trust_id_user_filters(self):
        """Test get trust ID user filters."""

        with self.client.get(
            "/trust_id/user_filters",
            headers=self.headers,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_trust_id_attributes(self):
        """Test get trust ID attributes data."""

        with self.client.get(
            "/trust_id/attributes",
            headers=self.headers,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)

    @task
    def get_trust_id_comparison(self):
        """Test get trust ID comparison."""

        with self.client.get(
            "/trust_id/comparison",
            headers=self.headers,
        ) as response:
            if response.status_code != HTTPStatus.OK:
                response.failure(response.status_code)
