"""
Purpose of this file is to house all tests related to orchestration
"""

from http import HTTPStatus
from unittest import TestCase, mock
from bson import ObjectId
import mongomock
import requests_mock
from requests_mock import Mocker

from huxunifylib.database import constants as db_c, data_management
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
)
from huxunifylib.database.engagement_management import (
    set_engagement,
    get_engagements_by_audience,
)
from huxunifylib.database.orchestration_management import (
    create_audience,
    get_audience,
)
from huxunifylib.database.client import DatabaseClient
from huxunifylib.connectors.aws_batch_connector import AWSBatchConnector

from huxunify.app import create_app
from huxunify.api import constants as api_c
from huxunify.api.config import get_config
from huxunify.api.data_connectors.aws import parameter_store


BASE_URL = "/api/v1"
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
VALID_USER_RESPONSE = {
    api_c.OKTA_ID_SUB: "8548bfh8d",
    api_c.EMAIL: "davesmith@fake.com",
    api_c.NAME: "dave smith",
}
BATCH_RESPONSE = {"ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value}}


class OrchestrationRouteTest(TestCase):
    """Orchestration Route tests"""

    # pylint: disable=too-many-instance-attributes
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
        self.user_info_call = f"{self.config.OKTA_ISSUER}/oauth2/v1/userinfo"
        self.audience_api_endpoint = "/api/v1{}".format(
            api_c.AUDIENCE_ENDPOINT
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

        # mock get_db_client() for the userinfo utils.
        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        self.addCleanup(mock.patch.stopall)

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
        self.user_name = "Joe Smithers"

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
                api_c.USER_NAME: self.user_name,
                api_c.DESTINATION_IDS: [
                    {db_c.OBJECT_ID: d[db_c.ID]} for d in self.destinations
                ],
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
                api_c.USER_NAME: self.user_name,
            },
        ]

        self.audiences = []
        for audience in audiences:
            self.audiences.append(create_audience(self.database, **audience))

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
                api_c.USER_NAME: self.user_name,
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
                api_c.USER_NAME: self.user_name,
            },
        ]

        self.engagement_ids = []
        for engagement in engagements:
            engagement_id = set_engagement(self.database, **engagement)
            self.engagement_ids.append(str(engagement_id))

        # setup the flask test client
        self.test_client = create_app().test_client()

        self.introspect_call = "{}/oauth2/v1/introspect?client_id={}".format(
            self.config.OKTA_ISSUER, self.config.OKTA_CLIENT_ID
        )

    @requests_mock.Mocker()
    @mock.patch.object(parameter_store, "get_store_value")
    @mock.patch.object(
        AWSBatchConnector, "register_job", return_value=BATCH_RESPONSE
    )
    @mock.patch.object(
        AWSBatchConnector, "submit_job", return_value=BATCH_RESPONSE
    )
    def test_deliver_audience_for_all_engagements_valid_audience_id(
        self, request_mocker: Mocker, *_: None
    ):
        """
        Test delivery of audience for all engagements
        with valid audience id

        Args:
            request_mocker (Mocker): Request mocker object.
            *_ (None): Omit all extra keyword args the mock patches send.

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
        Test delivery of audience for all engagements
        with invalid audience id

        Args:
            request_mocker (Mocker): Request mocker object.

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
    def test_deliver_audience_for_all_engagements_non_existent_audience(
        self, request_mocker: Mocker
    ):
        """
        Test delivery of audience for all engagements
        with non-existent audience id

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """
        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        audience_id = ObjectId()

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
    def test_get_audience_rules_success(self, request_mocker: Mocker):
        """Test the get audience rules route
        Args:
            request_mocker (Mocker): Request mocker object.
        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)

        data_management.set_constant(
            self.database,
            db_c.AUDIENCE_FILTER_CONSTANTS,
            {
                "text_operators": {
                    "contains": "Contains",
                    "does_not_contain": "Does not contain",
                    "does_not_equal": "Does not equal",
                    "equals": "Equals",
                }
            },
        )

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/rules",
            headers={"Authorization": TEST_AUTH_TOKEN},
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn("rule_attributes", response.json)
        self.assertIn("text_operators", response.json)

    @requests_mock.Mocker()
    def test_create_audience_with_destination(self, request_mocker: Mocker):
        """Test create audience with destination.

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        request_mocker.get(self.user_info_call, json=VALID_USER_RESPONSE)

        audience_post = {
            db_c.AUDIENCE_NAME: "Test Audience Create",
            api_c.AUDIENCE_FILTERS: [
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
            api_c.DESTINATIONS: [
                {api_c.ID: str(d[db_c.ID])} for d in self.destinations
            ],
        }

        response = self.test_client.post(
            self.audience_api_endpoint,
            json=audience_post,
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(
            audience_post[api_c.AUDIENCE_NAME],
            response.json[api_c.AUDIENCE_NAME],
        )

        # validate audience in db
        audience_doc = get_audience(
            self.database, ObjectId(response.json[db_c.OBJECT_ID])
        )
        self.assertListEqual(
            audience_doc[db_c.DESTINATIONS],
            [{api_c.ID: d[db_c.ID]} for d in self.destinations],
        )

    @requests_mock.Mocker()
    def test_create_audience_with_no_destinations_no_engagements(
        self, request_mocker: Mocker
    ):
        """Test create audience with no destinations or engagements

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        request_mocker.get(self.user_info_call, json=VALID_USER_RESPONSE)

        audience_post = {
            db_c.AUDIENCE_NAME: "Test Audience Create",
            api_c.AUDIENCE_FILTERS: [
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
        }

        response = self.test_client.post(
            self.audience_api_endpoint,
            json=audience_post,
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(
            audience_post[api_c.AUDIENCE_NAME],
            response.json[api_c.AUDIENCE_NAME],
        )

        # validate audience in db
        audience_doc = get_audience(
            self.database, ObjectId(response.json[db_c.OBJECT_ID])
        )
        # test empty list
        self.assertFalse(
            audience_doc[db_c.DESTINATIONS],
        )

        self.assertFalse(
            get_engagements_by_audience(self.database, audience_doc[db_c.ID])
        )

    @requests_mock.Mocker()
    def test_create_audience_with_engagements(self, request_mocker: Mocker):
        """Test create audience with engagements.

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        request_mocker.get(self.user_info_call, json=VALID_USER_RESPONSE)

        audience_post = {
            db_c.AUDIENCE_NAME: "Test Audience Engagements",
            api_c.AUDIENCE_FILTERS: [
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
            api_c.DESTINATIONS: [
                {db_c.OBJECT_ID: str(d[db_c.ID])} for d in self.destinations
            ],
            api_c.AUDIENCE_ENGAGEMENTS: self.engagement_ids,
        }

        response = self.test_client.post(
            self.audience_api_endpoint,
            json=audience_post,
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )
        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(
            audience_post[api_c.AUDIENCE_NAME],
            response.json[api_c.AUDIENCE_NAME],
        )

        # validate audience in db
        audience_doc = get_audience(
            self.database, ObjectId(response.json[db_c.OBJECT_ID])
        )
        # test destinations
        self.assertListEqual(
            audience_doc[db_c.DESTINATIONS],
            [{api_c.ID: d[db_c.ID]} for d in self.destinations],
        )

        expected_audience = {
            db_c.OBJECT_ID: audience_doc[db_c.ID],
            db_c.DESTINATIONS: [
                {db_c.OBJECT_ID: [d[db_c.ID] for d in self.destinations][0]}
            ],
        }

        # validate the audience is attached to the engagement
        engagements = get_engagements_by_audience(
            self.database, audience_doc[db_c.ID]
        )
        for engagement in engagements:
            # get the attached audience and nested destinations
            engagement_audiences = [
                x[db_c.OBJECT_ID] for x in engagement[db_c.AUDIENCES]
            ]
            engagement_audience = engagement[db_c.AUDIENCES][
                engagement_audiences.index(audience_doc[db_c.ID])
            ]

            self.assertDictEqual(engagement_audience, expected_audience)

    @requests_mock.Mocker()
    def test_create_audience_with_no_engagement(self, request_mocker: Mocker):
        """Test create audience without engagement ids.

        Args:
            request_mocker (Mocker): Request mocker object.

        Returns:

        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        request_mocker.get(self.user_info_call, json=VALID_USER_RESPONSE)

        audience_post = {
            db_c.AUDIENCE_NAME: "Test Audience Create",
            api_c.AUDIENCE_FILTERS: [
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
            api_c.DESTINATIONS: [
                {api_c.ID: str(d[db_c.ID])} for d in self.destinations
            ],
        }

        response = self.test_client.post(
            self.audience_api_endpoint,
            json=audience_post,
            headers={
                "Authorization": TEST_AUTH_TOKEN,
                "Content-Type": "application/json",
            },
        )
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

    @requests_mock.Mocker()
    def test_get_audience(self, request_mocker: Mocker):
        """Test get audience.
        Args:
            request_mocker (Mocker): Request mocker object.
        Returns:
        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        request_mocker.get(self.user_info_call, json=VALID_USER_RESPONSE)

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{self.audiences[0][db_c.ID]}",
            headers={
                "Authorization": TEST_AUTH_TOKEN,
            },
        )
        audience = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            ObjectId(audience[db_c.OBJECT_ID]), self.audiences[0][db_c.ID]
        )
        self.assertEqual(audience[db_c.CREATED_BY], self.user_name)

    @requests_mock.Mocker()
    def test_get_audiences(self, request_mocker: Mocker):
        """Test get audiences.
        Args:
            request_mocker (Mocker): Request mocker object.
        Returns:
        """

        request_mocker.post(self.introspect_call, json=VALID_RESPONSE)
        request_mocker.get(self.user_info_call, json=VALID_USER_RESPONSE)

        response = self.test_client.get(
            f"{self.audience_api_endpoint}",
            headers={
                "Authorization": TEST_AUTH_TOKEN,
            },
        )
        audiences = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(audiences)

        audience_ids = [ObjectId(x[db_c.ID]) for x in self.audiences]
        return_ids = [ObjectId(x[db_c.OBJECT_ID]) for x in audiences]

        self.assertListEqual(audience_ids, return_ids)
        for audience in audiences:
            self.assertEqual(audience[db_c.CREATED_BY], self.user_name)
