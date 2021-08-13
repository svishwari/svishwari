"""
Purpose of this file is to house all tests related to orchestration
"""
from http import HTTPStatus
from unittest import TestCase, mock
from bson import ObjectId
import mongomock
import requests_mock

from huxunifylib.connectors import FacebookConnector
from huxunifylib.database import data_management, constants as db_c
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
    set_delivery_job,
    set_delivery_job_status,
)
from huxunifylib.database.engagement_management import (
    set_engagement,
    get_engagement,
    get_engagements_by_audience,
)
from huxunifylib.database.orchestration_management import (
    create_audience,
    get_audience,
)
from huxunifylib.database.client import DatabaseClient
from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api import constants as api_c
import huxunify.test.constants as t_c
from huxunify.app import create_app


class OrchestrationRouteTest(TestCase):
    """Orchestration Route tests"""

    # pylint: disable=too-many-instance-attributes
    def setUp(self) -> None:
        """
        Setup resources before each test

        Args:

        Returns:
        """

        self.audience_api_endpoint = "/api/v1{}".format(
            api_c.AUDIENCE_ENDPOINT
        )

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

        # mock get_db_client() for the userinfo utils.
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
            engagement_id = set_engagement(self.database, **engagement)
            self.engagement_ids.append(str(engagement_id))

        self.delivery_jobs = [
            set_delivery_job(
                self.database,
                self.audiences[0][db_c.ID],
                self.destinations[0][db_c.ID],
                [],
                ObjectId(self.engagement_ids[0]),
            ),
            set_delivery_job(
                self.database,
                self.audiences[0][db_c.ID],
                self.destinations[0][db_c.ID],
                [],
                ObjectId(self.engagement_ids[1]),
            ),
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

            set_delivery_job_status(
                self.database, delivery_job[db_c.ID], db_c.STATUS_SUCCEEDED
            )

        # setup the flask test client
        self.test_client = create_app().test_client()

    def test_get_audience_rules_success(self):
        """Test the get audience rules route
        Args:

        """

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
            f"{self.audience_api_endpoint}/rules", headers=t_c.STANDARD_HEADERS
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIn("rule_attributes", response.json)
        self.assertIn("text_operators", response.json)

    def test_create_audience_with_destination(self):
        """Test create audience with destination.

        Args:
        Returns:

        """

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

        Args:

        Returns:

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

    def test_create_audience_invalid_user_info(self):
        """Test create audience with destination given invalid user info.

        The introspect call returns a valid response but user info call
        returns an invalid response, i.e., missing some fields.

        Args:

        Returns:

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
        """Test create audience with no destinations or engagements

        Args:

        Returns:

        """

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
        """Test create audience with engagements.

        Args:

        Returns:

        """

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

    def test_create_audience_with_no_engagement(self):
        """Test create audience without engagement ids.

        Args:

        Returns:

        """

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
        """Test get audience.
        Args:

        Returns:
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
        self.assertEqual(audience[api_c.LOOKALIKEABLE], api_c.STATUS_INACTIVE)
        self.assertFalse(audience[api_c.IS_LOOKALIKE])

        # validate the facebook destination in the audience is set to "Not delivered"
        for audience in audience[api_c.AUDIENCE_ENGAGEMENTS]:
            self.assertTrue(
                all(
                    x[api_c.STATUS] == db_c.AUDIENCE_STATUS_NOT_DELIVERED
                    for x in audience[api_c.DELIVERIES]
                )
            )

    def test_get_audience_does_not_exist(self):
        """Test get audience that does not exist
        Args:

        Returns:
        """
        audience_id = ObjectId()
        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{audience_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)

    def test_get_audience_invalid_id(self):
        """Test get audience that does not exist
        Args:

        Returns:
        """
        audience_id = "asdfg13456"
        response = self.test_client.get(
            f"{self.audience_api_endpoint}/{audience_id}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_get_audiences(self):
        """Test get audiences.
        Args:

        Returns:
        """

        mock.patch(
            "huxunify.api.route.orchestration.get_customers_count_async",
            return_value={},
        ).start()

        response = self.test_client.get(
            f"{self.audience_api_endpoint}",
            headers=t_c.STANDARD_HEADERS,
        )
        audiences = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTrue(audiences)

        audience_ids = [ObjectId(x[db_c.ID]) for x in self.audiences]
        return_ids = [ObjectId(x[db_c.OBJECT_ID]) for x in audiences]

        self.assertListEqual(audience_ids, return_ids)
        for audience in audiences:
            self.assertEqual(audience[db_c.CREATED_BY], self.user_name)
            self.assertFalse(audience[api_c.IS_LOOKALIKE])

    def test_update_audience(self):
        """Test update an audience.
        Args:

        Returns:
        """
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
            },
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(new_name, response.json[db_c.AUDIENCE_NAME])

    def test_create_lookalike_audience(self):
        """Test create lookalike audience
        Args:

        Returns:
        """
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

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(lookalike_audience_name, response.json[api_c.NAME])

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
            f"{self.audience_api_endpoint}/{self.audiences[0][db_c.ID]}",
            headers=t_c.STANDARD_HEADERS,
        )
        audience = response.json
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(
            ObjectId(audience[db_c.OBJECT_ID]), self.audiences[0][db_c.ID]
        )
        self.assertTrue(audience[api_c.LOOKALIKE_AUDIENCES])

        # test returned audience
        lookalike_audience = audience[api_c.LOOKALIKE_AUDIENCES][0]
        self.assertEqual(
            ObjectId(lookalike_audience[db_c.OBJECT_ID]),
            engaged_lookalike_audience[db_c.OBJECT_ID],
        )
        self.assertEqual(
            lookalike_audience[db_c.NAME], lookalike_audience_name
        )

    def test_create_lookalike_audience_invalid_engagement_ids(self):
        """Test create lookalike audience with invalid engagement ids
        Args:

        Returns:
        """

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
        """Test create lookalike audience with invalid engagement ids
        Args:

        Returns:
        """

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
        """Test create lookalike audience with invalid engagement ids
        Args:

        Returns:
        """

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
