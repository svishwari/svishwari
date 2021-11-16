# pylint: disable=too-many-lines
"""Purpose of this file is to house all tests related to orchestration."""
from http import HTTPStatus
from unittest import TestCase, mock
from bson import ObjectId
import mongomock
import requests_mock

from huxunifylib.connectors import FacebookConnector
from huxunifylib.database import constants as db_c
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
    set_delivery_job,
    set_delivery_job_status,
    create_delivery_platform_lookalike_audience,
    get_delivery_platform_lookalike_audience,
)
from huxunifylib.database.engagement_management import (
    set_engagement,
    get_engagement,
    get_engagements_by_audience,
    remove_audience_from_all_engagements,
)
from huxunifylib.database.orchestration_management import (
    create_audience,
    get_audience,
    get_audience_insights,
    delete_audience,
)

from huxunifylib.database.user_management import (
    set_user,
    manage_user_favorites,
)
from huxunifylib.database.engagement_audience_management import (
    get_all_engagement_audience_destinations,
)
from huxunifylib.database.client import DatabaseClient
from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api import constants as api_c
import huxunify.test.constants as t_c
from huxunify.app import create_app


# pylint: disable=too-many-public-methods
class OrchestrationRouteTest(TestCase):
    """Orchestration Route tests."""

    # pylint: disable=too-many-instance-attributes
    def setUp(self) -> None:
        """Setup resources before each test."""

        self.audience_api_endpoint = f"/api/v1{api_c.AUDIENCE_ENDPOINT}"

        # mock request for introspect call
        self.request_mocker = requests_mock.Mocker()
        self.request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.start()

        self.app = create_app().test_client()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock get_db_client() for the orchestration.
        mock.patch(
            "huxunify.api.route.orchestration.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() for the userinfo decorator.
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_db_client() for the utils.
        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        # mock get_store_value of parameter store
        mock.patch.object(
            parameter_store, "get_store_value", return_value="secret"
        ).start()

        self.addCleanup(mock.patch.stopall)

        destinations = [
            {
                db_c.DELIVERY_PLATFORM_NAME: "Facebook",
                db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FACEBOOK,
                db_c.STATUS: db_c.STATUS_SUCCEEDED,
                db_c.ENABLED: True,
                db_c.ADDED: True,
                db_c.IS_AD_PLATFORM: True,
                db_c.DELIVERY_PLATFORM_AUTH: {
                    api_c.FACEBOOK_ACCESS_TOKEN: "path1",
                    api_c.FACEBOOK_APP_SECRET: "path2",
                    api_c.FACEBOOK_APP_ID: "path3",
                    api_c.FACEBOOK_AD_ACCOUNT_ID: "path4",
                },
            },
            {
                db_c.DELIVERY_PLATFORM_NAME: "SFMC",
                db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFMC,
                db_c.STATUS: db_c.STATUS_SUCCEEDED,
                db_c.ENABLED: True,
                db_c.ADDED: True,
                db_c.IS_AD_PLATFORM: False,
                db_c.DELIVERY_PLATFORM_AUTH: {
                    api_c.SFMC_ACCOUNT_ID: "id12345",
                    api_c.SFMC_AUTH_BASE_URI: "base_uri",
                    api_c.SFMC_CLIENT_ID: "id12345",
                    api_c.SFMC_CLIENT_SECRET: "client_secret",
                    api_c.SFMC_SOAP_BASE_URI: "soap_base_uri",
                    api_c.SFMC_REST_BASE_URI: "rest_base_uri",
                },
            },
        ]
        self.user_name = "dave smith"
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
                                api_c.AUDIENCE_FILTER_FIELD: api_c.GENDER,
                                api_c.AUDIENCE_FILTER_TYPE: api_c.TYPE,
                                api_c.AUDIENCE_FILTER_VALUE: "male",
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
                                api_c.AUDIENCE_FILTER_FIELD: api_c.GENDER,
                                api_c.AUDIENCE_FILTER_TYPE: api_c.TYPE,
                                api_c.AUDIENCE_FILTER_VALUE: "female",
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

        self.lookalike_audience_doc = (
            create_delivery_platform_lookalike_audience(
                self.database,
                self.destinations[0][db_c.ID],
                self.audiences[0][db_c.ID],
                "Lookalike audience",
                0.01,
                "US",
                self.user_name,
                31,
            )
        )

        engagements = [
            {
                db_c.ENGAGEMENT_NAME: "Test Engagement",
                db_c.ENGAGEMENT_DESCRIPTION: "test-engagement",
                db_c.AUDIENCES: [
                    {
                        db_c.OBJECT_ID: self.audiences[0][db_c.ID],
                        api_c.DESTINATIONS: [
                            {db_c.OBJECT_ID: dest[db_c.ID]}
                            for dest in self.destinations
                        ],
                    },
                    {
                        db_c.OBJECT_ID: self.audiences[1][db_c.ID],
                        api_c.DESTINATIONS: [
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
                        api_c.DESTINATIONS: [],
                    },
                ],
                api_c.USER_NAME: self.user_name,
            },
        ]

        self.engagement_ids = []
        for engagement in engagements:
            self.engagement_ids.append(
                str(set_engagement(self.database, **engagement))
            )

        self.delivery_jobs = [
            set_delivery_job(
                self.database,
                self.audiences[0][db_c.ID],
                self.destinations[0][db_c.ID],
                [],
                ObjectId(engagement_id),
            )
            for engagement_id in self.engagement_ids
        ]

        for delivery_job in self.delivery_jobs:
            set_delivery_job_status(
                self.database,
                delivery_job[db_c.ID],
                db_c.AUDIENCE_STATUS_DELIVERING,
            )

            set_delivery_job_status(
                self.database,
                delivery_job[db_c.ID],
                db_c.AUDIENCE_STATUS_DELIVERED,
            )

        set_user(
            self.database,
            okta_id=t_c.VALID_RESPONSE.get(api_c.OKTA_UID),
            email_address=t_c.VALID_USER_RESPONSE.get(api_c.EMAIL),
            display_name="dave smith",
        )

        # Set an audience as favorite
        manage_user_favorites(
            self.database,
            okta_id=t_c.VALID_RESPONSE.get(api_c.OKTA_UID),
            component_name=api_c.AUDIENCES,
            component_id=self.audiences[0][db_c.ID],
        )

        # Set a lookalike audience as favorite
        manage_user_favorites(
            self.database,
            okta_id=t_c.VALID_RESPONSE.get(api_c.OKTA_UID),
            component_name=api_c.LOOKALIKE,
            component_id=self.lookalike_audience_doc[db_c.ID],
        )

        # setup the flask test client
        self.test_client = create_app().test_client()

    def test_get_audience_rules_success(self):
        """Test the get audience rules route success."""

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/rules", headers=t_c.STANDARD_HEADERS
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn("rule_attributes", response.json)
        self.assertIn("text_operators", response.json)

    def test_create_audience_with_destination(self):
        """Test create audience with destination."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

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
            headers=t_c.STANDARD_HEADERS,
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

    def test_create_audience_empty_user_info(self):
        """Test create audience with destination given empty user info.
        The introspect call returns a valid response but user info call
        returns an empty response.
        """

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
        # simulating userinfo endpoint to give invalid user response
        self.request_mocker.get(t_c.USER_INFO_CALL, json={})

        response = self.test_client.post(
            self.audience_api_endpoint,
            json=audience_post,
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.AUTH401_ERROR_MESSAGE}
        self.assertEqual(valid_response, response.json)
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_create_audience_no_destination_id(self) -> None:
        """Test create audience with destination given no id in destination
        object.
        """

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
                {api_c.DATA_EXTENSION_ID: str(d[db_c.ID])}
                for d in self.destinations
            ],
        }

        response = self.test_client.post(
            self.audience_api_endpoint,
            json=audience_post,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_create_audience_invalid_user_info(self):
        """Test create audience with destination given invalid user info.
        The introspect call returns a valid response but user info call
        returns an invalid response, i.e., missing some fields.
        """

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
        # simulating userinfo endpoint to give invalid user response
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.INVALID_USER_RESPONSE
        )

        response = self.test_client.post(
            self.audience_api_endpoint,
            json=audience_post,
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.AUTH401_ERROR_MESSAGE}
        self.assertEqual(valid_response, response.json)
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_create_audience_with_no_destinations_no_engagements(self):
        """Test create audience with no destinations or engagements."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

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
            headers=t_c.STANDARD_HEADERS,
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

    def test_create_audience_with_engagements(self):
        """Test create audience with engagements."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

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
            headers=t_c.STANDARD_HEADERS,
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
                {api_c.ID: d[db_c.ID]} for d in self.destinations
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

    def test_create_audience_with_no_engagement(self):
        """Test create audience without engagement IDs."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

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
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.CREATED, response.status_code)

    def test_get_audience(self):
        """Test get audience."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{self.audiences[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )
        audience = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            ObjectId(audience[db_c.OBJECT_ID]), self.audiences[0][db_c.ID]
        )
        self.assertEqual(audience[db_c.CREATED_BY], self.user_name)
        self.assertEqual(audience[api_c.LOOKALIKEABLE], api_c.STATUS_INACTIVE)
        self.assertFalse(audience[api_c.IS_LOOKALIKE])

        self.assertIn(api_c.DESTINATIONS, audience)
        self.assertEqual(len(audience[api_c.DESTINATIONS]), 2)

        # validate the facebook destination in the audience is set to "Not delivered"
        for audience in audience[api_c.AUDIENCE_ENGAGEMENTS]:
            self.assertTrue(
                all(
                    x[api_c.STATUS] == db_c.AUDIENCE_STATUS_NOT_DELIVERED
                    for x in audience[api_c.DELIVERIES]
                )
            )
            self.assertIn(db_c.DELIVERIES, audience)
            for delivery in audience[db_c.DELIVERIES]:
                self.assertIn(db_c.DELIVERY_PLATFORM_ID, delivery)

    def test_get_lookalike_audience(self):
        """Test get audience for a lookalike audience."""

        # create a lookalike audience
        lookalike_audience = create_delivery_platform_lookalike_audience(
            self.database,
            self.destinations[0][db_c.ID],
            self.audiences[0],
            "My lookalike audience 1",
            0.01,
            "US",
            self.user_name,
        )

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{lookalike_audience[db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )

        audience = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(audience)
        self.assertEqual(
            str(lookalike_audience[db_c.ID]), audience[db_c.OBJECT_ID]
        )
        self.assertEqual(lookalike_audience[api_c.NAME], audience[api_c.NAME])
        self.assertEqual(self.user_name, audience[db_c.CREATED_BY])
        self.assertTrue(audience[api_c.IS_LOOKALIKE])
        self.assertEqual(
            str(self.audiences[0][db_c.ID]), audience[t_c.SOURCE_ID]
        )
        self.assertEqual(
            self.audiences[0][api_c.NAME], audience[t_c.SOURCE_NAME]
        )
        self.assertEqual(
            self.audiences[0][api_c.SIZE], audience[t_c.SOURCE_SIZE]
        )
        self.assertListEqual(
            self.audiences[0][api_c.AUDIENCE_FILTERS],
            audience[api_c.AUDIENCE_FILTERS],
        )

    def test_get_lookalike_audience_source_audience_does_not_exist(self):
        """Test get audience for a lookalike audience where the source
        audience does not exist."""

        audience_doc = {
            db_c.AUDIENCE_NAME: "Test Source Audience 1",
            "audience_filters": [
                {
                    api_c.AUDIENCE_SECTION_AGGREGATOR: "ALL",
                    api_c.AUDIENCE_SECTION_FILTERS: [
                        {
                            api_c.AUDIENCE_FILTER_FIELD: api_c.GENDER,
                            api_c.AUDIENCE_FILTER_TYPE: api_c.TYPE,
                            api_c.AUDIENCE_FILTER_VALUE: "female",
                        }
                    ],
                }
            ],
            api_c.USER_NAME: self.user_name,
            api_c.SIZE: 100,
        }

        source_audience = create_audience(self.database, **audience_doc)

        # create a lookalike audience
        lookalike_audience = create_delivery_platform_lookalike_audience(
            self.database,
            self.destinations[0][db_c.ID],
            source_audience,
            "My lookalike audience 2",
            0.01,
            "US",
            self.user_name,
        )

        # delete the source audience from mock database
        deleted_audience = delete_audience(
            self.database, source_audience[db_c.ID]
        )
        self.assertTrue(deleted_audience)

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{lookalike_audience[db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )

        audience = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(audience)
        self.assertEqual(
            str(lookalike_audience[db_c.ID]), audience[db_c.OBJECT_ID]
        )
        self.assertEqual(lookalike_audience[api_c.NAME], audience[api_c.NAME])
        self.assertEqual(self.user_name, audience[db_c.CREATED_BY])
        self.assertTrue(audience[api_c.IS_LOOKALIKE])
        self.assertEqual(
            str(source_audience[db_c.ID]), audience[t_c.SOURCE_ID]
        )
        self.assertEqual(
            source_audience[api_c.NAME], audience[t_c.SOURCE_NAME]
        )
        self.assertEqual(
            source_audience[api_c.SIZE], audience[t_c.SOURCE_SIZE]
        )
        self.assertListEqual(
            source_audience[api_c.AUDIENCE_FILTERS],
            audience[api_c.AUDIENCE_FILTERS],
        )

    def test_get_audience_does_not_exist(self):
        """Test get audience that does not exist."""

        audience_id = ObjectId()
        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{audience_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_get_audience_invalid_id(self):
        """Test get audience with invalid ID."""

        audience_id = "asdfg13456"
        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{audience_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_get_audiences(self):
        """Test get all audiences."""

        response = self.test_client.get(
            f"{self.audience_api_endpoint}",
            headers=t_c.STANDARD_HEADERS,
        )
        audiences = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(audiences)

        audience_ids = [ObjectId(x[db_c.ID]) for x in self.audiences]
        lookalike_audience_ids = [self.lookalike_audience_doc[db_c.ID]]
        return_ids = [ObjectId(x[db_c.OBJECT_ID]) for x in audiences]

        expected_audience_destinations = (
            get_all_engagement_audience_destinations(self.database)
        )

        self.assertListEqual(audience_ids + lookalike_audience_ids, return_ids)
        for audience in audiences:
            if not audience[api_c.IS_LOOKALIKE]:
                self.assertEqual(audience[db_c.CREATED_BY], self.user_name)
                self.assertIn(db_c.AUDIENCE_FILTERS, audience)
                self.assertFalse(audience[api_c.IS_LOOKALIKE])
                self.assertTrue(audience[api_c.STATUS])
                self.assertIn(
                    audience[api_c.STATUS],
                    [
                        api_c.STATUS_NOT_DELIVERED,
                        api_c.STATUS_DELIVERING,
                        api_c.STATUS_DELIVERED,
                        api_c.STATUS_DELIVERY_PAUSED,
                        api_c.STATUS_ERROR,
                    ],
                )

                # validate that not delivered has no delivery time set.
                if audience[api_c.STATUS] == api_c.STATUS_NOT_DELIVERED:
                    self.assertIsNone(audience[api_c.AUDIENCE_LAST_DELIVERED])

                # find the matched audience destinations, should be the same.
                matched_audience = [
                    x
                    for x in expected_audience_destinations
                    if x[db_c.ID] == ObjectId(audience[api_c.ID])
                ]

                # test that the unique count of delivery destinations
                # is the same as the response.
                self.assertEqual(
                    len(audience[db_c.DESTINATIONS]),
                    len(matched_audience[0][db_c.DESTINATIONS]),
                )
            else:
                self.assertEqual(audience[db_c.CREATED_BY], self.user_name)
                self.assertTrue(audience[api_c.IS_LOOKALIKE])
                self.assertTrue(audience[api_c.STATUS])
                self.assertEqual(
                    audience[api_c.STATUS],
                    api_c.STATUS_DELIVERING,
                )

    def test_update_audience(self):
        """Test update an audience."""

        new_name = "New Test Audience"

        response = self.test_client.put(
            f"{self.audience_api_endpoint}/{self.audiences[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
            json={
                db_c.AUDIENCE_NAME: new_name,
                db_c.AUDIENCE_FILTERS: [
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
                api_c.DESTINATIONS: [],
                api_c.ENGAGEMENT_IDS: self.engagement_ids,
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(new_name, response.json[db_c.AUDIENCE_NAME])

        # test the audience was appended to engagements
        audience_engagements = get_audience_insights(
            self.database,
            self.audiences[0][db_c.ID],
        )

        self.assertListEqual(
            self.engagement_ids,
            [str(x[db_c.ID]) for x in audience_engagements],
        )

    def test_create_lookalike_audience_facebook_connection_fail(self):
        """Test create lookalike audience when facebook connection fails."""

        # setup facebook connector mock address
        mock.patch.object(
            FacebookConnector,
            "check_connection",
            return_value=False,
        ).start()

        lookalike_audience_name = "FAILED LA AUDIENCE"

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.LOOKALIKE_AUDIENCES_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json={
                api_c.AUDIENCE_ID: str(self.audiences[0][db_c.ID]),
                api_c.NAME: lookalike_audience_name,
                api_c.AUDIENCE_SIZE_PERCENTAGE: 1.5,
                api_c.ENGAGEMENT_IDS: self.engagement_ids,
            },
        )

        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_create_lookalike_audience(self):
        """Test create lookalike audience."""

        # setup facebook connector mock address
        mock.patch.object(
            FacebookConnector,
            "check_connection",
            return_value=True,
        ).start()

        mock.patch.object(
            FacebookConnector,
            "get_new_lookalike_audience",
            return_value="LA_ID_12345",
        ).start()

        lookalike_audience_name = "NEW LA AUDIENCE"

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.LOOKALIKE_AUDIENCES_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json={
                api_c.AUDIENCE_ID: str(self.audiences[0][db_c.ID]),
                api_c.NAME: lookalike_audience_name,
                api_c.AUDIENCE_SIZE_PERCENTAGE: 1.5,
                api_c.ENGAGEMENT_IDS: self.engagement_ids,
            },
        )

        new_engagement = get_engagement(
            self.database, ObjectId(self.engagement_ids[0])
        )

        self.assertEqual(HTTPStatus.ACCEPTED, response.status_code)
        self.assertEqual(lookalike_audience_name, response.json[api_c.NAME])
        lookalike_audience_id = ObjectId(response.json[api_c.ID])

        engaged_lookalike_audience = None

        for audience in new_engagement[api_c.AUDIENCES]:
            if audience[api_c.ID] == ObjectId(response.json[api_c.ID]):
                engaged_lookalike_audience = audience

        self.assertIsNotNone(engaged_lookalike_audience)

        # test getting the audience and lookalikes response
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{lookalike_audience_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        lookalike_audience = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            lookalike_audience[api_c.ID], str(lookalike_audience_id)
        )
        self.assertEqual(lookalike_audience[api_c.SIZE], 3329)
        self.assertEqual(
            lookalike_audience[t_c.SOURCE_SIZE], self.audiences[0][db_c.SIZE]
        )
        self.assertEqual(
            lookalike_audience[t_c.SOURCE_NAME], self.audiences[0][db_c.NAME]
        )
        self.assertGreaterEqual(lookalike_audience[api_c.MATCH_RATE], 0)
        self.assertEqual(
            lookalike_audience[t_c.SOURCE_ID],
            str(self.audiences[0][db_c.ID]),
        )
        self.assertTrue(lookalike_audience[api_c.IS_LOOKALIKE])

    def test_create_lookalike_audience_invalid_engagement_ids(self):
        """Test create lookalike audience with invalid engagement IDs."""

        # setup facebook connector mock address
        mock.patch.object(
            FacebookConnector,
            "check_connection",
            return_value=True,
        ).start()

        mock.patch.object(
            FacebookConnector,
            "get_new_lookalike_audience",
            return_value="LA_ID_12345",
        ).start()

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.LOOKALIKE_AUDIENCES_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json={
                api_c.AUDIENCE_ID: str(self.audiences[0][db_c.ID]),
                api_c.NAME: "NEW LA AUDIENCE",
                api_c.AUDIENCE_SIZE_PERCENTAGE: 1.5,
                api_c.ENGAGEMENT_IDS: ["bad_id1", "bad_id2"],
            },
        )

        valid_response = {"message": api_c.BSON_INVALID_ID("bad_id1")}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_create_lookalike_audience_invalid_source_audience_id(self):
        """Test create lookalike audience with invalid engagement IDs."""

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.LOOKALIKE_AUDIENCES_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json={
                api_c.AUDIENCE_ID: "bad_id1",
                api_c.NAME: "NEW LA AUDIENCE",
                api_c.AUDIENCE_SIZE_PERCENTAGE: 1.5,
                api_c.ENGAGEMENT_IDS: self.engagement_ids,
            },
        )

        valid_response = {"message": api_c.BSON_INVALID_ID("bad_id1")}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_create_lookalike_audience_source_audience_not_found(self):
        """Test create lookalike audience with invalid engagement IDs."""

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.LOOKALIKE_AUDIENCES_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json={
                api_c.AUDIENCE_ID: str(ObjectId()),
                api_c.NAME: "NEW LA AUDIENCE",
                api_c.AUDIENCE_SIZE_PERCENTAGE: 1.5,
                api_c.ENGAGEMENT_IDS: self.engagement_ids,
            },
        )

        valid_response = {"message": api_c.AUDIENCE_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_audience_by_id_validate_match_rate(self) -> None:
        """Test get audience API and validate match_rate.
        This will check for match delivery for an AD platform.
        """

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{self.audiences[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )

        audience = response.json

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            ObjectId(audience[db_c.OBJECT_ID]), self.audiences[0][db_c.ID]
        )
        self.assertEqual(audience[db_c.CREATED_BY], self.user_name)

        # Validate that the match_rate in deliveries contained within
        # engagements are greater than or equal to 0 for ad platforms.
        # None for non ad platforms.
        for engagement in audience.get(api_c.AUDIENCE_ENGAGEMENTS):
            for delivery in engagement.get(api_c.DELIVERIES):
                if delivery.get(api_c.IS_AD_PLATFORM):
                    self.assertGreaterEqual(delivery.get(api_c.MATCH_RATE), 0)
                else:
                    self.assertIsNone(delivery.get(api_c.MATCH_RATE))

    def test_get_audience_by_id_validate_match_rate_lookalike_audience(self):
        """Test validate match rate for a lookalike audience."""

        # setup facebook connector mock address
        mock.patch.object(
            FacebookConnector,
            "check_connection",
            return_value=True,
        ).start()

        mock.patch.object(
            FacebookConnector,
            "get_new_lookalike_audience",
            return_value="LA_ID_12345",
        ).start()

        response = self.test_client.post(
            f"{t_c.BASE_ENDPOINT}{api_c.LOOKALIKE_AUDIENCES_ENDPOINT}",
            headers=t_c.STANDARD_HEADERS,
            json={
                api_c.AUDIENCE_ID: str(self.audiences[0][db_c.ID]),
                api_c.NAME: "TEST LOOKALIKE LA",
                api_c.AUDIENCE_SIZE_PERCENTAGE: 1.5,
                api_c.ENGAGEMENT_IDS: self.engagement_ids,
            },
        )
        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{response.json.get(api_c.ID)}",
            headers=t_c.STANDARD_HEADERS,
        )
        audience = response.json
        # For lookalike audiences match rate will be None always.
        for engagement in audience.get(api_c.AUDIENCE_ENGAGEMENTS):
            for delivery in engagement.get(api_c.DELIVERIES):
                if delivery.get(api_c.IS_AD_PLATFORM):
                    self.assertIsNone(delivery.get(api_c.MATCH_RATE))

    def test_delete_audience(self) -> None:
        """Test delete audience API with valid ID."""

        # create multiple audiences
        audiences = []

        for i in range(4):
            audiences.append(
                create_audience(
                    self.database,
                    f"audience{i}",
                    [],
                    [],
                    self.user_name,
                    100 + i,
                )
            )

        engagements = [
            set_engagement(
                self.database,
                "ENG0",
                "Engagement 0",
                [
                    {
                        db_c.OBJECT_ID: audiences[0][db_c.ID],
                        api_c.DESTINATIONS: [],
                    },
                    {
                        db_c.OBJECT_ID: audiences[1][db_c.ID],
                        api_c.DESTINATIONS: [],
                    },
                ],
                self.user_name,
            ),
            set_engagement(
                self.database,
                "ENG1",
                "Engagement 1",
                [
                    {
                        db_c.OBJECT_ID: audiences[2][db_c.ID],
                        api_c.DESTINATIONS: [],
                    },
                    {
                        db_c.OBJECT_ID: audiences[3][db_c.ID],
                        api_c.DESTINATIONS: [],
                    },
                ],
                self.user_name,
            ),
            set_engagement(
                self.database,
                "ENG2",
                "Engagement 2",
                [
                    {
                        db_c.OBJECT_ID: audiences[0][db_c.ID],
                        api_c.DESTINATIONS: [],
                    },
                    {
                        db_c.OBJECT_ID: audiences[1][db_c.ID],
                        api_c.DESTINATIONS: [],
                    },
                    {
                        db_c.OBJECT_ID: audiences[2][db_c.ID],
                        api_c.DESTINATIONS: [],
                    },
                    {
                        db_c.OBJECT_ID: audiences[3][db_c.ID],
                        api_c.DESTINATIONS: [],
                    },
                ],
                self.user_name,
            ),
        ]

        remove_audience_from_all_engagements(
            self.database, audiences[0][db_c.ID], self.user_name
        )

        response = self.test_client.delete(
            f"{self.audience_api_endpoint}/{self.audiences[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)
        # validate audience is deleted in db
        self.assertIsNone(
            get_audience(self.database, self.audiences[0][db_c.ID])
        )

        for engagement in engagements:
            new_eng = get_engagement(self.database, engagement)
            self.assertFalse(
                list(
                    x
                    for x in new_eng[api_c.AUDIENCES]
                    if x[db_c.OBJECT_ID] == audiences[0][db_c.ID]
                )
            )

    def test_delete_lookalike_audience(self) -> None:
        """Test delete audience API for valid lookalike audience."""

        # create a lookalike audience
        lookalike_audience = create_delivery_platform_lookalike_audience(
            self.database,
            self.destinations[0][db_c.ID],
            self.audiences[0],
            "My lookalike audience 0",
            0.01,
            "US",
        )

        set_engagement(
            self.database,
            "ENG0",
            "Engagement 0",
            [
                {
                    db_c.OBJECT_ID: lookalike_audience[db_c.ID],
                    api_c.DESTINATIONS: [],
                },
            ],
            self.user_name,
        )

        response = self.test_client.delete(
            f"{self.audience_api_endpoint}/{lookalike_audience[db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NO_CONTENT, response.status_code)
        # validate lookalike audience is deleted in db
        self.assertIsNone(
            get_delivery_platform_lookalike_audience(
                self.database, lookalike_audience[db_c.ID]
            )
        )

    def test_delete_audience_where_audience_does_not_exist(self) -> None:
        """Test delete audience API with valid ID but the object does not
        exist."""

        response = self.test_client.delete(
            f"{self.audience_api_endpoint}/{str(ObjectId())}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(
            HTTPStatus.INTERNAL_SERVER_ERROR, response.status_code
        )
        self.assertEqual(
            {api_c.MESSAGE: api_c.OPERATION_FAILED}, response.json
        )

    def test_delete_audience_with_invalid_id(self) -> None:
        """Test delete audience API with invalid ID."""

        response = self.test_client.delete(
            f"{self.audience_api_endpoint}/{t_c.INVALID_ID}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(t_c.INVALID_ID)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_audience_with_not_delivered(self):
        """Test get audience empty update_time for un-delivered engagements."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{self.audiences[1][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )
        audience = response.json

        for audience_engagement in audience[api_c.AUDIENCE_ENGAGEMENTS]:
            for delivery in audience_engagement[api_c.DELIVERIES]:
                if delivery[api_c.STATUS] != db_c.STATUS_DELIVERED:
                    self.assertIsNone(delivery[db_c.UPDATE_TIME])

    def test_get_audience_not_in_favorites(self):
        """Test get audience not a favorite."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{self.audiences[1][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )
        audience = response.json
        self.assertFalse(audience.get(api_c.FAVORITE))

    def test_get_audience_in_favorites(self):
        """Test get audience which is a favorite."""

        self.request_mocker.stop()
        self.request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        self.request_mocker.start()

        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{self.audiences[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )
        audience = response.json
        self.assertTrue(audience.get(api_c.FAVORITE))

    def test_get_audiences_with_valid_filters(self):
        """Test get all audiences with valid filters."""

        response = self.test_client.get(
            f"{self.audience_api_endpoint}?{api_c.FAVORITES}=True&"
            f"{api_c.WORKED_BY}=True&{api_c.ATTRIBUTE}={api_c.GENDER}",
            headers=t_c.STANDARD_HEADERS,
        )

        audiences = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(audiences)
        self.assertEqual(2, len(audiences))
        self.assertEqual(
            str(self.audiences[0][db_c.ID]), audiences[0][api_c.ID]
        )
        self.assertEqual(
            str(self.lookalike_audience_doc[db_c.ID]), audiences[1][api_c.ID]
        )

    def test_get_lookalike_audiences_with_valid_filters(self):
        """Test get all audiences with valid filters."""

        response = self.test_client.get(
            f"{self.audience_api_endpoint}?{api_c.FAVORITES}=True&",
            headers=t_c.STANDARD_HEADERS,
        )

        audiences = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(audiences)
        self.assertEqual(2, len(audiences))
        self.assertEqual(
            str(self.audiences[0][db_c.ID]), audiences[0][api_c.ID]
        )
        self.assertEqual(
            str(self.lookalike_audience_doc[db_c.ID]), audiences[1][api_c.ID]
        )

    def test_get_worked_by_audiences_with_valid_filters(self):
        """Test get all audiences with valid filters."""

        response = self.test_client.get(
            f"{self.audience_api_endpoint}?{api_c.WORKED_BY}=True",
            headers=t_c.STANDARD_HEADERS,
        )

        audiences = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(audiences)
        self.assertEqual(3, len(audiences))
        self.assertEqual(
            str(self.audiences[0][db_c.ID]), audiences[0][api_c.ID]
        )
        self.assertEqual(audiences[0][db_c.CREATED_BY], self.user_name)
        self.assertEqual(
            str(self.lookalike_audience_doc[db_c.ID]), audiences[2][api_c.ID]
        )
