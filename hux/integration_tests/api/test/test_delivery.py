"""Purpose of this file is to integration test for delivery."""
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests


class TestDelivery(TestCase):
    """Test Delivery."""

    ENGAGEMENTS = "engagements"
    AUDIENCES = "audiences"
    COLLECTION = "delivery_jobs"

    def setUp(self) -> None:
        """Setup resources before each test."""

        # get an engagement and an audience associated to it
        engagements = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}",
            headers=pytest.HEADERS,
        ).json()

        self.engagement_id = None
        self.audience_id = None
        self.facebook_destination_id = None

        for engagement in engagements:
            for audience in engagement["audiences"]:
                for destination in audience["destinations"]:
                    # ensure the destination exists
                    get_destination = requests.get(
                        f'{pytest.API_URL}/destinations/{destination["id"]}',
                        headers=pytest.HEADERS,
                    )
                    if get_destination.status_code == 404:
                        continue
                    # fetch only facebook's destination_id
                    if get_destination.json()["name"] != "Facebook":
                        continue
                    # ensure that the audience is not a lookalike audience
                    # since delivery requires regular audience
                    get_audience = requests.get(
                        f'{pytest.API_URL}/audiences/{audience["id"]}',
                        headers=pytest.HEADERS,
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

    def test_get_engagement_delivery_history(self):
        """Test get engagement delivery history."""

        response = requests.get(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{self.engagement_id}/"
            f"delivery-history",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    def test_get_audience_delivery_history(self):
        """Test get audience delivery history."""

        response = requests.get(
            f"{pytest.API_URL}/{self.AUDIENCES}/{self.audience_id}/"
            f"delivery-history",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)

    def test_deliver_audience_to_destination(self):
        """Test deliver audience to a destination."""

        # request to deliver audience to a destination
        response = requests.post(
            f"{pytest.API_URL}/{self.AUDIENCES}/{self.audience_id}/deliver",
            json={
                "destinations": [
                    {
                        "id": self.facebook_destination_id,
                    },
                ],
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_deliver_audience_in_engagement(self):
        """Test deliver audience that is part of an engagement."""

        # request to deliver an audience from an engagement to a destination
        response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{self.engagement_id}/"
            f"deliver?destinations={self.facebook_destination_id}&"
            f"audiences={self.audience_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_deliver_engagement_audience_to_destination(self):
        """Test deliver an engagement audience to a destination."""

        # request to deliver an audience from an engagement to a destination
        response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{self.engagement_id}/"
            f"audience/{self.audience_id}/destination/"
            f"{self.facebook_destination_id}/deliver",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_update_delivery_schedule_for_audience_in_engagement(self):
        """Test updating delivery schedule for an audience in engagement and
        reset it."""

        # request to set delivery schedule of an audience in engagement
        set_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{self.engagement_id}/"
            f"audience/{self.audience_id}/schedule",
            json={
                "schedule": {
                    "periodicity": "Daily",
                    "every": 1,
                    "hour": 12,
                    "minute": 15,
                    "period": "AM",
                },
                "start_date": "2022-03-02T00:00:00.000Z",
                "end_date": "2022-04-02T00:00:00.000Z",
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, set_response.status_code)
        self.assertIsInstance(set_response.json(), dict)

        # request to reset delivery schedule of an audience in engagement
        reset_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{self.engagement_id}/"
            f"audience/{self.audience_id}/schedule",
            json={},
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, reset_response.status_code)
        self.assertIsInstance(reset_response.json(), dict)

    def test_deliver_audience_in_an_engagement(self):
        """Test deliver audience in an engagement to the destinations attached
        to it."""

        # request to deliver audience in an engagement to the destinations
        # attached
        response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{self.engagement_id}/"
            f"audience/{self.audience_id}/deliver",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_update_and_delete_destination_delivery_schedule_in_engagement_audience(
        self,
    ):
        """Test updating and followed by deleting delivery schedule for a
        destination in an engagement audience."""

        # request to set delivery schedule of a destination in engagement
        # audience
        post_response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{self.engagement_id}/"
            f"audience/{self.audience_id}/destination/"
            f"{self.facebook_destination_id}/schedule",
            json={
                "periodicity": "Daily",
                "every": 21,
                "hour": 11,
                "minute": 15,
                "period": "PM",
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, post_response.status_code)
        self.assertIsInstance(post_response.json(), dict)

        # request to reset delivery schedule of a destination in engagement
        # audience
        delete_response = requests.delete(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{self.engagement_id}/"
            f"audience/{self.audience_id}/destination/"
            f"{self.facebook_destination_id}/schedule",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, delete_response.status_code)
        self.assertIsInstance(delete_response.json(), dict)
