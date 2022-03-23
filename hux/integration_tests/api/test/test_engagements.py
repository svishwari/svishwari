"""Purpose of this file is to integration test for engagements."""
from time import time
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests
from hux.integration_tests.api.test.conftest import Crud


class TestEngagements(TestCase):
    """Test Engagements."""

    ENGAGEMENTS = "engagements"
    COLLECTION = "engagements"

    def setUp(self) -> None:
        """Setup resources before each test."""

        self.audience_id = requests.get(
            f"{pytest.API_URL}/audiences",
            headers=pytest.HEADERS,
        ).json()[0]["id"]

        self.destination_id = requests.get(
            f"{pytest.API_URL}/destinations",
            headers=pytest.HEADERS,
        ).json()[0]["id"]

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

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertTrue(isinstance(response.json(), dict))

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, response.json()["id"])]

    def test_get_engagements(self):
        """Test get all engagements."""

        response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(isinstance(response.json(), list))
        self.assertTrue(len(response.json()) >= 1)

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

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertTrue(isinstance(create_response.json(), dict))

        engagement_id = create_response.json()["id"]

        # get the engagement by id for further validation
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertTrue(isinstance(fetch_response.json(), dict))
        self.assertEqual(engagement_id, fetch_response.json()["id"])

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

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

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertTrue(isinstance(create_response.json(), dict))

        engagement_id = create_response.json()["id"]

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
        self.assertTrue(isinstance(update_response.json(), dict))
        self.assertEqual(engagement_id, update_response.json()["id"])
        self.assertEqual(
            updated_engagement_name, update_response.json()["name"]
        )
        self.assertEqual(
            updated_engagement_desc, update_response.json()["description"]
        )

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

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

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertTrue(isinstance(create_response.json(), dict))

        engagement_id = create_response.json()["id"]

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

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

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

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertTrue(isinstance(create_response.json(), dict))
        self.assertTrue(len(create_response.json()["audiences"]) == 1)

        engagement_id = create_response.json()["id"]

        # get the last audience from get all audiences to add to an engagement
        audience_id_to_add = requests.get(
            f"{pytest.API_URL}/audiences",
            headers=pytest.HEADERS,
        ).json()[-1]["id"]

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
        self.assertTrue(isinstance(add_audience_response.json(), dict))

        # get the engagement by id for further validation
        fetch_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, fetch_response.status_code)
        self.assertTrue(isinstance(fetch_response.json(), dict))
        self.assertEqual(engagement_id, fetch_response.json()["id"])
        self.assertTrue(len(fetch_response.json()["audiences"]) == 2)

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

    def test_delete_audience_from_an_engagement(self):
        """Test deleting an audience from an engagement."""

        # get the last audience from get all audiences to add and delete to and
        # from an engagement
        audience_id_to_delete = requests.get(
            f"{pytest.API_URL}/audiences",
            headers=pytest.HEADERS,
        ).json()[-1]["id"]

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

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertTrue(isinstance(create_response.json(), dict))
        self.assertTrue(len(create_response.json()["audiences"]) == 2)

        engagement_id = create_response.json()["id"]

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
        self.assertTrue(isinstance(fetch_response.json(), dict))
        self.assertEqual(engagement_id, fetch_response.json()["id"])
        self.assertTrue(len(fetch_response.json()["audiences"]) == 1)

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

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

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertTrue(isinstance(create_response.json(), dict))
        self.assertTrue(len(create_response.json()["audiences"]) == 1)
        self.assertTrue(
            len(create_response.json()["audiences"][0]["destinations"]) == 1
        )

        engagement_id = create_response.json()["id"]

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
        self.assertTrue(isinstance(add_destination_response.json(), dict))
        self.assertEqual(engagement_id, add_destination_response.json()["id"])
        self.assertTrue(len(add_destination_response.json()["audiences"]) == 1)
        self.assertTrue(
            len(
                add_destination_response.json()["audiences"][0]["destinations"]
            )
            == 2
        )

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

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

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertTrue(isinstance(create_response.json(), dict))
        self.assertTrue(len(create_response.json()["audiences"]) == 1)
        self.assertTrue(
            len(create_response.json()["audiences"][0]["destinations"]) == 2
        )

        engagement_id = create_response.json()["id"]

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
        self.assertTrue(isinstance(fetch_response.json(), dict))
        self.assertEqual(engagement_id, fetch_response.json()["id"])
        self.assertTrue(len(fetch_response.json()["audiences"]) == 1)
        self.assertTrue(
            len(fetch_response.json()["audiences"][0]["destinations"]) == 1
        )

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

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

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertTrue(isinstance(create_response.json(), dict))

        engagement_id = create_response.json()["id"]

        # get the engagement email performance metrics for further validation
        get_email_metrics_response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{engagement_id}"
            f"/audience-performance/email",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, get_email_metrics_response.status_code)
        self.assertTrue(isinstance(get_email_metrics_response.json(), dict))
        self.assertTrue(
            get_email_metrics_response.json()["audience_performance"]
        )

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

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

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertTrue(isinstance(create_response.json(), dict))

        engagement_id = create_response.json()["id"]

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

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]

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

        # test engagement created successfully
        self.assertEqual(HTTPStatus.CREATED, create_response.status_code)
        self.assertTrue(isinstance(create_response.json(), dict))

        engagement_id = create_response.json()["id"]

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
        self.assertTrue(
            isinstance(get_display_ads_metrics_response.json(), dict)
        )
        self.assertTrue(
            get_display_ads_metrics_response.json()["audience_performance"]
        )

        # add the crud object to pytest for cleaning after
        pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, engagement_id)]
