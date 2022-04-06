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

        for engagement in engagements:
            for audience in engagement["audiences"]:
                self.engagement_id = engagement["id"]
                self.audience_id = audience["id"]
                break
            else:
                continue
            break

        # fetch facebook's destination_id
        destinations = requests.get(
            f"{pytest.API_URL}/destinations",
            headers=pytest.HEADERS,
        ).json()
        self.destination_id = next(
            (
                destination["id"]
                for destination in destinations
                if destination["name"] == "Facebook"
            ),
            None,
        )

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
                        "id": self.destination_id,
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
            f"deliver?destinations={self.destination_id}&"
            f"audiences={self.audience_id}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    def test_update_delivery_schedule_for_audience_in_engagement(self):
        """Test updating delivery schedule for an audience in engagement and
        reset it."""

        # request to set delivery schedule of an audience in engagement
        response = requests.post(
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
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

        # request to reset delivery schedule of an audience in engagement
        response = requests.post(
            f"{pytest.API_URL}/{self.ENGAGEMENTS}/{self.engagement_id}/"
            f"audience/{self.audience_id}/schedule",
            json={},
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

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
