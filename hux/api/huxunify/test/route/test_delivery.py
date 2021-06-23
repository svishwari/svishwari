"""
Purpose of this file is to house all the delivery api tests
"""

import json
from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
from flask_marshmallow import Schema
from requests_mock import Mocker
import mongomock
from bson import ObjectId
from marshmallow import ValidationError

import huxunify.test.constants as t_c
from huxunifylib.database import constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
)
from huxunifylib.database.engagement_management import (
    set_engagement,
    get_engagements,
    get_engagement,
)
from huxunifylib.database.orchestration_management import create_audience
from huxunifylib.connectors.aws_batch_connector import AWSBatchConnector
from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.app import create_app
from huxunify.api.schema.engagement import (
    DisplayAdsSummary,
    DispAdIndividualAudienceSummary,
    EmailSummary,
    EmailIndividualAudienceSummary,
    EngagementGetSchema,
)
from huxunify.api.data_connectors.aws import parameter_store

BATCH_RESPONSE = {"ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value}}


class TestDeliveryRoutes(TestCase):
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
            "huxunify.api.route.engagement.get_db_client"
        ).start()
        get_db_client_mock.return_value = self.database

        parameter_store_mock = mock.patch.object(parameter_store, "get_store_value").start()
        aws_batch_connector_register_mock = mock.patch.object(AWSBatchConnector, "register_job").start()
        aws_batch_connector_register_mock.return_value = BATCH_RESPONSE
        aws_batch_connector_submit_mock = mock.patch.object(AWSBatchConnector, "submit_job").start()
        aws_batch_connector_submit_mock.return_value = BATCH_RESPONSE

        self.addCleanup(mock.patch.stopall)

        # setup test data
        destinations = [
            {
                db_c.DELIVERY_PLATFORM_NAME: "Facebook",
                db_c.DELIVERY_PLATFORM_TYPE: "facebook",
                db_c.STATUS: db_c.STATUS_SUCCEEDED,
                db_c.ENABLED: True,
                db_c.ADDED: True,
                db_c.DELIVERY_PLATFORM_AUTH: {
                    api_c.FACEBOOK_ACCESS_TOKEN: "path1",
                    api_c.FACEBOOK_APP_SECRET: "path2",
                    api_c.FACEBOOK_APP_ID: "path3",
                    api_c.FACEBOOK_AD_ACCOUNT_ID: "path4",
                },
            },
        ]

        self.destinations = []
        for destination in destinations:
            self.destinations.append(
                set_delivery_platform(self.database, **destination)
            )

        audiences = [
            {
                db_c.AUDIENCE_NAME: "Test Audience",
                "audience_filters": [
                    {
                        api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                        api_c.AUDIENCE_SECTION_FILTERS: [
                            {
                                api_c.AUDIENCE_FILTER_FIELD: "filter_field",
                                api_c.AUDIENCE_FILTER_TYPE: "type",
                                api_c.AUDIENCE_FILTER_VALUE: "value",
                            }
                        ],
                    }
                ],
                api_c.DESTINATION_IDS: [d[db_c.ID] for d in self.destinations],
            },
            {
                db_c.AUDIENCE_NAME: "Test Audience No Destinations",
                "audience_filters": [
                    {
                        api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                        api_c.AUDIENCE_SECTION_FILTERS: [
                            {
                                api_c.AUDIENCE_FILTER_FIELD: "filter_field",
                                api_c.AUDIENCE_FILTER_TYPE: "type",
                                api_c.AUDIENCE_FILTER_VALUE: "value",
                            }
                        ],
                    }
                ],
            },
        ]

        self.audiences = []
        for audience in audiences:
            self.audiences.append(create_audience(self.database, **audience))

        user_id = ObjectId()

        engagements = [
            {
                db_c.ENGAGEMENT_NAME: "Test Engagement",
                db_c.ENGAGEMENT_DESCRIPTION: "test-engagement",
                db_c.AUDIENCES: [
                    {
                        db_c.OBJECT_ID: self.audiences[0][db_c.ID],
                        api_c.DESTINATIONS_TAG: [
                            {db_c.OBJECT_ID: dest[db_c.ID]}
                            for dest in self.destinations
                        ],
                    },
                    {
                        db_c.OBJECT_ID: self.audiences[1][db_c.ID],
                        api_c.DESTINATIONS_TAG: [
                            {db_c.OBJECT_ID: dest[db_c.ID]}
                            for dest in self.destinations
                        ],
                    },
                ],
                db_c.USER_ID: user_id,
            },
            {
                db_c.ENGAGEMENT_NAME: "Test Engagement No Destination",
                db_c.ENGAGEMENT_DESCRIPTION: "test-engagement",
                db_c.AUDIENCES: [
                    {
                        db_c.OBJECT_ID: self.audiences[1][db_c.ID],
                        api_c.DESTINATIONS_TAG: [],
                    },
                ],
                db_c.USER_ID: user_id,
            },
        ]

        self.engagement_ids = []
        for engagement in engagements:
            self.engagement_ids.append(
                str(set_engagement(self.database, **engagement))
            )

    @requests_mock.Mocker()
    @mock.patch.object(parameter_store, "get_store_value")
    @mock.patch.object(
        AWSBatchConnector, "register_job", return_value=BATCH_RESPONSE
    )
    @mock.patch.object(
        AWSBatchConnector, "submit_job", return_value=BATCH_RESPONSE
    )
    def test_deliver_audience_for_an_engagement_valid_ids(
        self, request_mocker: Mocker, *_: None
    ):
        """
        Test delivery of an audience for an engagement
        with valid ids

        Args:
            request_mocker (Mocker): Request mocker object.
            *_ (None): Omit all extra keyword args the mock patches send.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=t_c.VALID_RESPONSE)
        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/deliver"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    @requests_mock.Mocker()
    def test_deliver_audience_for_an_engagement_invalid_audience_id(
            self, request_mocker: Mocker
    ):
        """
        Test delivery of an audience for an engagement
        with invalid audience id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=t_c.VALID_RESPONSE)
        audience_id = "XYZ123"
        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/deliver"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": "Invalid Object ID"}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    @requests_mock.Mocker()
    def test_deliver_audience_for_an_engagement_invalid_engagement_id(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of an audience for an engagement
        with invalid engagement id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=t_c.VALID_RESPONSE)
        audience_id = self.audiences[0][db_c.ID]
        engagement_id = "XYZ123"

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/deliver"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": "Invalid Object ID"}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_audience_for_an_engagement_non_existent_engagement(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of an audience for an engagement
        with non-existent engagement id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=t_c.VALID_RESPONSE)
        audience_id = self.audiences[0][db_c.ID]
        engagement_id = ObjectId()

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/deliver"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": "Engagement does not exist."}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    @requests_mock.Mocker()
    @mock.patch.object(parameter_store, "get_store_value")
    @mock.patch.object(
        AWSBatchConnector, "register_job", return_value=BATCH_RESPONSE
    )
    @mock.patch.object(
        AWSBatchConnector, "submit_job", return_value=BATCH_RESPONSE
    )
    def test_deliver_destination_for_engagement_audience_valid_ids(
        self, request_mocker: Mocker, *_: None
    ):
        """
        Test delivery of a destination for an audience in engagement
        with valid ids

        Args:
            request_mocker (Mocker): Request mocker object.
            *_ (None): Omit all extra keyword args the mock patches send.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=t_c.VALID_RESPONSE)
        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

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
        request_mocker.post(self.introspect_call, json=t_c.VALID_RESPONSE)
        engagement_id = str(ObjectId())
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": "Engagement does not exist."}

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json, valid_response)

    @requests_mock.Mocker()
    def test_deliver_destination_for_unattached_audience(
            self, request_mocker: Mocker
    ):
        """
        Test delivery of a destination for an unattached audience

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=t_c.VALID_RESPONSE)
        engagement_id = self.engagement_ids[1]

        # Unattached audience id
        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers=t_c.STANDARD_HEADERS
        )

        valid_response = {
            "message": "Audience is not attached to the engagement."
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    @requests_mock.Mocker()
    def test_deliver_destination_for_unattached_destination(
            self, request_mocker: Mocker
    ):
        """
        Test delivery of a destination for an unattached destination

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=t_c.VALID_RESPONSE)
        engagement_id = self.engagement_ids[1]
        audience_id = self.audiences[1][db_c.ID]

        # Unattached destination id
        destination_id = self.destinations[0][db_c.ID]

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers=t_c.STANDARD_HEADERS
        )

        valid_response = {
            "message": "Destination is not attached to the engagement audience."
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)