"""Purpose of this file is to integration test for engagements."""
from typing import Union

from time import time
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests
from conftest import Crud
from prometheus_metrics import record_test_result, HttpMethod, Endpoints


class TestEngagements(TestCase):
    """Test Engagements."""

    ENGAGEMENTS = "engagements"
    COLLECTION = "engagements"

    def setUp(self) -> None:
        """Setup resources before each test."""

        self.audience_id = requests.get(
            f"{pytest.API_URL}/audiences",
            headers=pytest.HEADERS,
        ).json()["audiences"][0]["id"]

        self.destination_id = requests.get(
            f"{pytest.API_URL}/destinations",
            headers=pytest.HEADERS,
        ).json()[0]["id"]

    @record_test_result(
        HttpMethod.POST, Endpoints.ENGAGEMENTS.POST_CREATE_ENGAGEMENT
    )
    def test_create_engagement(self):
        """Test creating an engagement."""

        response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": f"E2E test_engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"E2E Integration Test Engagement Desc-"
                f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, response.json()["id"])]

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.GET, Endpoints.ENGAGEMENTS.GET_ALL_ENGAGEMENTS
    )
    def test_get_engagements(self):
        """Test get all engagements."""

        response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)
        self.assertIn("total_records", response.json())
        self.assertIn(self.ENGAGEMENTS, response.json())
        self.assertIsInstance(response.json()[self.ENGAGEMENTS], list)
        self.assertGreaterEqual(len(response.json()[self.ENGAGEMENTS]), 1)

    @record_test_result(HttpMethod.GET, Endpoints.ENGAGEMENTS.GET_ENGAGEMENT)
    def test_get_engagement_by_id(self):
        """Test get engagement by ID."""

        # create a test engagement to fetch by ID
        create_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": f"E2E test_engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"E2E Integration Test Engagement Desc-"
                f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        engagement_id = create_response.json()["id"]
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)

        # get the engagement by id for further validation
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), dict)
        self.assertEqual(engagement_id, fetch_response.json()["id"])

    @record_test_result(
        HttpMethod.PUT, Endpoints.ENGAGEMENTS.PUT_UPDATE_ENGAGEMENT
    )
    def test_update_engagement(self):
        """Test updating an engagement."""

        engagement_name = (
            f"E2E test_engagements Integration Test-{int(time() * 1000)}"
        )
        engagement_desc = (
            f"E2E Integration Test Engagement Desc-{int(time() * 1000)}"
        )

        # create a test engagement to update it
        create_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": engagement_name,
                "description": engagement_desc,
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        engagement_id = create_response.json()["id"]
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)

        # test engagement name and description as created
        self.assertEqual(engagement_name, create_response.json()["name"])
        self.assertEqual(
            engagement_desc, create_response.json()["description"]
        )

        updated_engagement_name = (
            f"E2E test_engagements Integration Test-{int(time() * 1000)}"
        )
        updated_engagement_desc = (
            f"E2E Integration Test Engagement Desc-{int(time() * 1000)}"
        )

        update_response = requests.put(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}",
            json={
                "name": updated_engagement_name,
                "description": updated_engagement_desc,
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, update_response.status_code)
        self.assertIsInstance(update_response.json(), dict)
        self.assertEqual(engagement_id, update_response.json()["id"])
        self.assertEqual(
            updated_engagement_name, update_response.json()["name"]
        )
        self.assertEqual(
            updated_engagement_desc, update_response.json()["description"]
        )

    @record_test_result(
        HttpMethod.DELETE, Endpoints.ENGAGEMENTS.DELETE_ENGAGEMENT
    )
    def test_delete_engagement(self):
        """Test deleting an engagement."""

        # create a test engagement to delete it
        create_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": f"E2E test_engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"E2E Integration Test Engagement Desc-"
                f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        engagement_id = create_response.json()["id"]
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)

        delete_response = requests.delete(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.NO_CONTENT, delete_response.status_code)

        # get the engagement by id to validate if engagement is deleted
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.NOT_FOUND, fetch_response.status_code)

    @record_test_result(
        HttpMethod.POST, Endpoints.ENGAGEMENTS.POST_ADD_AUDIENCE_TO_ENGAGEMENT
    )
    def test_add_audience_to_an_engagement(self):
        """Test adding an audience to an engagement."""

        # create a test engagement to add an audience to it
        create_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": f"E2E test_engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"E2E Integration Test Engagement Desc-"
                f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        engagement_id = create_response.json()["id"]
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)
        self.assertEqual(len(create_response.json()["audiences"]), 1)

        # get the last audience from get all audiences to add to an engagement
        audience_id_to_add = requests.get(
            f"{pytest.API_URL}/audiences",
            headers=pytest.HEADERS,
        ).json()["audiences"][-1]["id"]

        add_audience_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}/audiences",
            json={
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                    {
                        "id": audience_id_to_add,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.CREATED, add_audience_response.status_code)
        self.assertIsInstance(add_audience_response.json(), dict)

        # get the engagement by id for further validation
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), dict)
        self.assertEqual(engagement_id, fetch_response.json()["id"])
        self.assertEqual(len(fetch_response.json()["audiences"]), 2)

    @record_test_result(
        HttpMethod.DELETE,
        Endpoints.ENGAGEMENTS.DELETE_AUDIENCE_FROM_ENGAGEMENT,
    )
    def test_delete_audience_from_an_engagement(self):
        """Test deleting an audience from an engagement."""

        # get the last audience from get all audiences to add and delete to and
        # from an engagement
        audience_id_to_delete = requests.get(
            f"{pytest.API_URL}/audiences",
            headers=pytest.HEADERS,
        ).json()["audiences"][-1]["id"]

        # create a test engagement to add an audience to it
        create_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": f"E2E test_engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"E2E Integration Test Engagement Desc-"
                f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                    {
                        "id": audience_id_to_delete,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        engagement_id = create_response.json()["id"]
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)
        self.assertEqual(len(create_response.json()["audiences"]), 2)

        delete_audience_response = requests.delete(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}/audiences",
            json={
                "audience_ids": [audience_id_to_delete],
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(
            HTTPStatus.NO_CONTENT, delete_audience_response.status_code
        )

        # get the engagement by id for further validation
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), dict)
        self.assertEqual(engagement_id, fetch_response.json()["id"])
        self.assertEqual(len(fetch_response.json()["audiences"]), 1)

    @record_test_result(
        HttpMethod.POST,
        Endpoints.ENGAGEMENTS.POST_ADD_DESTINATION_ENGAGEMENT_AUDIENCE,
    )
    def test_add_destination_to_an_engagement_audience(self):
        """Test adding a destination to an engagement audience."""

        # create a test engagement with an audience to add a destination to it
        create_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": f"E2E test_engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"E2E Integration Test Engagement Desc-"
                f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        engagement_id = create_response.json()["id"]
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)
        self.assertEqual(len(create_response.json()["audiences"]), 1)
        self.assertEqual(
            len(create_response.json()["audiences"][0]["destinations"]), 1
        )

        # get the last destination from get all destination to add to an
        # engagement audience
        destination_id_to_add = requests.get(
            f"{pytest.API_URL}/destinations",
            headers=pytest.HEADERS,
        ).json()[-1]["id"]

        add_destination_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}"
            f"/audience/{self.audience_id}/destinations",
            json={"id": destination_id_to_add},
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, add_destination_response.status_code)
        self.assertIsInstance(add_destination_response.json(), dict)
        self.assertEqual(engagement_id, add_destination_response.json()["id"])
        self.assertEqual(len(add_destination_response.json()["audiences"]), 1)
        self.assertEqual(
            len(
                add_destination_response.json()["audiences"][0]["destinations"]
            ),
            2,
        )

    @record_test_result(
        HttpMethod.DELETE,
        Endpoints.ENGAGEMENTS.DELETE_DESTINATION_ENGAGEMENT_AUDIENCE,
    )
    def test_delete_destination_from_an_engagement_audience(self):
        """Test deleting a destination to an engagement audience."""

        # get the last destination from get all destination to add to an
        # engagement audience
        destination_id_to_delete = requests.get(
            f"{pytest.API_URL}/destinations",
            headers=pytest.HEADERS,
        ).json()[-1]["id"]

        # create a test engagement with an audience to add a destination to it
        create_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": f"E2E test_engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"E2E Integration Test Engagement Desc-"
                f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                            {
                                "id": destination_id_to_delete,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        engagement_id = create_response.json()["id"]
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)
        self.assertEqual(len(create_response.json()["audiences"]), 1)
        self.assertEqual(
            len(create_response.json()["audiences"][0]["destinations"]), 2
        )

        delete_destination_response = requests.delete(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}"
            f"/audience/{self.audience_id}/destinations",
            json={"id": destination_id_to_delete},
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(
            HTTPStatus.NO_CONTENT, delete_destination_response.status_code
        )

        # get the engagement by id for further validation
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertIsInstance(fetch_response.json(), dict)
        self.assertEqual(engagement_id, fetch_response.json()["id"])
        self.assertEqual(len(fetch_response.json()["audiences"]), 1)
        self.assertEqual(
            len(fetch_response.json()["audiences"][0]["destinations"]), 1
        )

    @record_test_result(
        HttpMethod.GET, Endpoints.ENGAGEMENTS.GET_EMAIL_PERFORMANCE_METRICS
    )
    def test_get_engagement_email_performance_metrics(self):
        """Test get engagement email performance metrics."""

        # create a test engagement
        create_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": f"E2E test_engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"E2E Integration Test Engagement Desc-"
                f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        engagement_id = create_response.json()["id"]
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)

        # get the engagement email performance metrics for further validation
        get_email_metrics_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}"
            f"/audience-performance/email",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, get_email_metrics_response.status_code)
        self.assertIsInstance(get_email_metrics_response.json(), dict)
        self.assertTrue(
            get_email_metrics_response.json()["audience_performance"]
        )

    @record_test_result(
        HttpMethod.GET,
        Endpoints.ENGAGEMENTS.GET_DOWNLOAD_EMAIL_PERFORMANCE_METRICS,
    )
    def test_download_engagement_email_performance_metrics(self):
        """Test download engagement email performance metrics."""

        # create a test engagement
        create_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": f"E2E test_engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"E2E Integration Test Engagement Desc-"
                f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        engagement_id = create_response.json()["id"]
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)

        # get the engagement email performance metrics for further validation
        download_email_metrics_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}"
            f"/audience-performance/download",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(
            HTTPStatus.OK, download_email_metrics_response.status_code
        )
        self.assertEqual(
            "application/zip",
            download_email_metrics_response.headers["content-type"],
        )

    @record_test_result(HttpMethod.GET, Endpoints.ENGAGEMENTS.GET_ENGAGEMENT)
    def test_get_engagement_display_ads_performance_metrics(self):
        """Test get engagement display ads performance metrics."""

        # create a test engagement
        create_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            json={
                "name": f"E2E test_engagements Integration Test-"
                f"{int(time() * 1000)}",
                "description": f"E2E Integration Test Engagement Desc-"
                f"{int(time() * 1000)}",
                "audiences": [
                    {
                        "id": self.audience_id,
                        "destinations": [
                            {
                                "id": self.destination_id,
                            },
                        ],
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        engagement_id = create_response.json()["id"]
        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertIsInstance(create_response.json(), dict)

        # get the engagement email performance metrics for further validation
        get_display_ads_metrics_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}"
            f"/audience-performance/display-ads",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(
            HTTPStatus.OK, get_display_ads_metrics_response.status_code
        )
        self.assertIsInstance(get_display_ads_metrics_response.json(), dict)
        self.assertTrue(
            get_display_ads_metrics_response.json()["audience_performance"]
        )

    def get_engagement_audience_facebook_destination_id(
        self,
    ) -> Union[dict, None]:
        """Get the engagement id from the get engagements response and the
        corresponding audience_id and destination_id of destination type
        facebook that are nested within the response and return it as a dict
        object.

        Returns:
            Union[dict, None]: engagement_id, and corresponding audience_id,
                destination_id(of type facebook).
        """

        response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)
        self.assertIn("total_records", response.json())
        self.assertIn(self.ENGAGEMENTS, response.json())
        self.assertIsInstance(response.json()[self.ENGAGEMENTS], list)

        for engagement in response.json()[self.ENGAGEMENTS]:
            for audience in engagement["audiences"]:
                for destination in audience["destinations"]:
                    # ensure a successful delivery exists for the audience in
                    # the destination
                    if (not destination["latest_delivery"]) or (
                        destination["latest_delivery"]["status"]
                        in ["Not Delivered", "Error"]
                    ):
                        continue
                    # ensure the destination exists
                    get_destination = requests.get(
                        f'{pytest.API_URL}/destinations/{destination["id"]}',
                        headers=pytest.HEADERS,
                    )
                    if (get_destination.status_code == 404) or (
                        get_destination.json()["name"] != "Facebook"
                    ):
                        continue
                    # ensure that the audience is not a lookalike audience since
                    # campaign mappings endpoints require regular audience
                    get_audience = requests.get(
                        f'{pytest.API_URL}/audiences/{audience["id"]}',
                        headers=pytest.HEADERS,
                    )
                    get_audience_response = get_audience.json()
                    if (
                        get_audience.status_code == 200
                        and get_audience_response
                    ):
                        if (
                            "is_lookalike" in get_audience_response
                            and get_audience_response["is_lookalike"]
                        ):
                            continue
                        return {
                            "engagement_id": engagement["id"],
                            "audience_id": audience["id"],
                            "destination_id": destination["id"],
                        }

        return None

    @record_test_result(
        HttpMethod.GET, Endpoints.CAMPAIGN.GET_CAMPAIGN_MAPPINGS
    )
    def test_get_campaign_mappings_to_attach_to_audience(self):
        """Test get campaign mappings."""

        request_query_params_value = (
            self.get_engagement_audience_facebook_destination_id()
        )

        if request_query_params_value:
            get_campaign_mappings_response = requests.get(
                f"{pytest.API_URL}/{self.ENGAGEMENTS}/"
                f'{request_query_params_value["engagement_id"]}/audience/'
                f'{request_query_params_value["audience_id"]}/destination/'
                f'{request_query_params_value["destination_id"]}/campaign-mappings',
                headers=pytest.HEADERS,
            )

            # test success
            self.assertEqual(
                HTTPStatus.OK, get_campaign_mappings_response.status_code
            )
            self.assertIsInstance(get_campaign_mappings_response.json(), dict)

    @record_test_result(HttpMethod.GET, Endpoints.CAMPAIGN.GET_CAMPAIGNS)
    def test_get_campaigns(self):
        """Test get campaigns."""

        request_query_params_value = (
            self.get_engagement_audience_facebook_destination_id()
        )

        if request_query_params_value:
            get_campaigns_response = requests.get(
                f"{pytest.API_URL}/{self.ENGAGEMENTS}/"
                f'{request_query_params_value["engagement_id"]}/audience/'
                f'{request_query_params_value["audience_id"]}/destination/'
                f'{request_query_params_value["destination_id"]}/campaigns',
                headers=pytest.HEADERS,
            )

            # test success
            self.assertEqual(HTTPStatus.OK, get_campaigns_response.status_code)
            self.assertIsInstance(get_campaigns_response.json(), list)
