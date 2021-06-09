"""
Purpose of this file is to house all tests related to Delivery CRUD operations
"""

import unittest
from http import HTTPStatus
from unittest import mock

import mongomock
import requests_mock
from requests_mock import Mocker
from bson import ObjectId

from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
)
from huxunifylib.database.engagement_management import (
    set_engagement,
)
from huxunifylib.database.orchestration_management import create_audience

from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.schema.destinations import DestinationGetSchema
from huxunify.api.schema.orchestration import AudienceGetSchema

from huxunify.app import create_app


BASE_URL = "/api/vi"
TEST_AUTH_TOKEN = "Bearer 12345678"
VALID_RESPONSE = {
    "active": True,
    "scope": "openid email profile",
    "username": "davesmith",
    "exp": 1234,
    "iat": 12345,
    "sub": "davesmith@fake",
    "aud": "sample_aud",
    "iss": "sample_iss",
    "jti": "sample_jti",
    "token_type": "Bearer",
    "client_id": "1234",
    "uid": "1234567",
}


class TestDeliveryOperations(unittest.TestCase):
    """
    Tests for Delivery APIs
    """

    def setUp(self) -> None:
        """
        Setup resources before each test

        Args:

        Returns:
        """
        self.config = get_config("TEST")

        self.introspect_call = (
            f"{self.config.OKTA_ISSUER}"
            f"/oauth2/v1/introspect?client_id="
            f"{self.config.OKTA_CLIENT_ID}"
        )

        self.app = create_app().test_client()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        get_db_client_mock = mock.patch(
            "huxunify.api.route.orchestration.get_db_client"
        ).start()
        get_db_client_mock.return_value = self.database
        self.addCleanup(mock.patch.stopall)

        # TODO: Add dummy audiences, destinations, engagements
        destinations = [
            {
                db_c.DELIVERY_PLATFORM_NAME: "Salesforce Marketing Cloud",
                db_c.DELIVERY_PLATFORM_TYPE: "salesforce",
                db_c.STATUS: db_c.ACTIVE,
                db_c.ENABLED: True,
                db_c.ADDED: False,
            },
            {
                db_c.DELIVERY_PLATFORM_NAME: "Facebook",
                db_c.DELIVERY_PLATFORM_TYPE: "facebook",
                db_c.STATUS: db_c.ACTIVE,
                db_c.ENABLED: True,
                db_c.ADDED: False,
            },
        ]

        self.destinations = []
        for destination in destinations:
            self.destinations.append(
                DestinationGetSchema().dump(
                    set_delivery_platform(self.database, **destination)
                )
            )

        audiences = [
            {
                db_c.AUDIENCE_NAME: "Test Audience",
                "audience_filters": [],
                api_c.DESTINATION_IDS: [
                    d[api_c.ID] for d in self.destinations
                ],
            },
            {
                db_c.AUDIENCE_NAME: "Test Audience 2",
                "audience_filters": [],
                api_c.DESTINATION_IDS: [
                    d[api_c.ID] for d in self.destinations
                ],
            },
        ]

        # TODO: Map audience key names aptly
        self.audiences = []
        for audience in audiences:
            self.audiences.append(
                AudienceGetSchema().dump(
                    create_audience(self.database, **audience)
                )
            )

        engagements = [
            {
                db_c.ENGAGEMENT_NAME: "Test Engagement 1",
                db_c.ENGAGEMENT_DESCRIPTION: "test-engagement",
                db_c.AUDIENCES: [],  # self.audiences,
                db_c.USER_ID: ObjectId(),
            },
            {
                db_c.ENGAGEMENT_NAME: "Test Engagement 2",
                db_c.ENGAGEMENT_DESCRIPTION: "test-engagement",
                db_c.AUDIENCES: [],  # self.audiences,
                db_c.USER_ID: ObjectId(),
            },
        ]

        self.engagement_ids = []
        for engagement in engagements:
            # engagement = EngagementPostSchema().dump(engagement)
            self.engagement_ids.append(
                str(set_engagement(self.database, **engagement))
            )

    @requests_mock.Mocker()
    def test_deliver_audience_for_all_engagements_valid_request(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of audience for all engagements

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        audience_id = self.audiences[0][db_c.ID]

        response = self.app.post(
            f"{BASE_URL}/{api_c.AUDIENCES}/{audience_id}/deliver",
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {
            "message": f"Successfully created delivery job(s) for audience ID {audience_id}"
        }

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_audience_for_all_engagements_invalid_audience_id(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of audience for all engagements it is a part of with invalid audience id

        Args:
            request_mocker (str): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        audience_id = "XYZ123"

        response = self.app.post(
            f"{BASE_URL}/{api_c.AUDIENCES}/{audience_id}/deliver",
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Invalid Object ID"}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_audience_for_all_engagements_valid_object_id_not_found(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of audience for all engagements it is a part of with valid Object id
        but no audience is found with the Object id

        Args:
            request_mocker (str): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        audience_id = str(ObjectId())

        response = self.app.post(
            f"{BASE_URL}/{api_c.AUDIENCES}/{audience_id}/deliver",
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Audience does not exist."}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_audience_for_an_engagement_valid_ids(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of an audience for an engagements with valid Object ids

        Args:
            request_mocker (str): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        audience_id = self.audiences[0][api_c.ID]
        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            (
                f"{BASE_URL}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/deliver"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {
            "message": (
                f"Successfully created delivery job(s) "
                f"for engagement ID {engagement_id} and "
                f"audience ID {audience_id}"
            )
        }

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_audience_for_an_engagement_invalid_audience_id(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of an audience for an engagements with invalid audience id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        audience_id = "XYZ123"
        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            (
                f"{BASE_URL}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/deliver"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Invalid Object ID"}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_audience_for_an_engagement_invalid_engagement_id(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of an audience for an engagements with invalid engagement id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        audience_id = self.audiences[0][api_c.ID]
        engagement_id = "XYZ123"

        response = self.app.post(
            (
                f"{BASE_URL}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/deliver"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Invalid Object ID"}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_audience_for_an_engagement_no_engagement(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of an audience for an engagements with invalid engagement id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        audience_id = self.audiences[0][api_c.ID]
        engagement_id = ObjectId()

        response = self.app.post(
            (
                f"{BASE_URL}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/deliver"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Engagement does not exist."}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_audience_for_an_engagement_no_audience(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of an audience for an engagements with invalid engagement id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        audience_id = ObjectId()
        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            (
                f"{BASE_URL}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/deliver"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Audience does not exist."}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_destination_for_engagement_audience_valid_ids(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of a destination for an audience in engagement

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        audience_id = self.audiences[0][api_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][api_c.ID]

        response = self.app.post(
            (
                f"{BASE_URL}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
                f"{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Audience does not exist."}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_destination_for_engagement_audience_no_engagement(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of a destination for a non-existent engagement

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        engagement_id = str(ObjectId())
        audience_id = self.audiences[0][api_c.ID]
        destination_id = self.destinations[0][api_c.ID]

        response = self.app.post(
            (
                f"{BASE_URL}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
                f"{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Engagement does not exist."}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_destination_for_non_existent_engagement(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of a destination for a non-existent engagement

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        engagement_id = str(ObjectId())
        audience_id = self.audiences[0][api_c.ID]
        destination_id = self.destinations[0][api_c.ID]

        response = self.app.post(
            (
                f"{BASE_URL}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
                f"{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Engagement does not exist."}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_destination_for_engagement_w_no_audience(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of a destination for a non-existent engagement

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        engagement_id = self.engagement_ids[1]  # No audience exists
        audience_id = self.audiences[0][api_c.ID]
        destination_id = self.destinations[0][api_c.ID]

        response = self.app.post(
            (
                f"{BASE_URL}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
                f"{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Engagement has no audiences."}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_destination_for_unattached_audience(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of a destination for a non-existent engagement

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        engagement_id = self.engagement_ids[0]
        audience_id = self.audiences[1][api_c.ID]  # Unattached
        destination_id = self.destinations[0][api_c.ID]

        response = self.app.post(
            (
                f"{BASE_URL}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
                f"{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {
            "message": "Audience is not attached to the engagement."
        }

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_invalid_destination_for_engagement_audience(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of an invalid destination for engagement audience

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        engagement_id = self.engagement_ids[0]
        audience_id = self.audiences[1][api_c.ID]  # Unattached
        destination_id = ObjectId()

        response = self.app.post(
            (
                f"{BASE_URL}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
                f"{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Destination does not exist."}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_destination_for_no_audience(self, request_mocker: Mocker):
        """
        Test delivery of an invalid destination for engagement audience

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        engagement_id = self.engagement_ids[0]
        audience_id = ObjectId()
        destination_id = self.destinations[0][api_c.ID]

        response = self.app.post(
            (
                f"{BASE_URL}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}"
                f"{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
                f"{api_c.DESTINATIONS_ENDPOINT}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )

        valid_response = {"message": "Audience does not exist."}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)
