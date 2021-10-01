"""
Purpose of this file is to house all the delivery api tests
"""

from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
import mongomock
from bson import ObjectId

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
)
from huxunifylib.database.engagement_management import set_engagement
from huxunifylib.database.orchestration_management import create_audience
from huxunifylib.database.user_management import set_user
from huxunifylib.connectors import AWSBatchConnector
import huxunify.test.constants as t_c
import huxunify.api.constants as api_c
from huxunify.app import create_app
from huxunify.api.data_connectors.aws import parameter_store


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class TestDeliveryRoutes(TestCase):
    """Test Delivery Endpoints"""

    # pylint: disable=unused-variable
    def setUp(self) -> None:
        """
        Setup resources before each test

        Args:

        Returns:
        """

        # mock request for introspect call
        request_mocker = requests_mock.Mocker()
        request_mocker.post(t_c.INTROSPECT_CALL, json=t_c.VALID_RESPONSE)
        request_mocker.start()

        self.app = create_app().test_client()

        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        # mock get db client from utils
        mock.patch(
            "huxunify.api.route.utils.get_db_client",
            return_value=self.database,
        ).start()

        # mock get db client from decorators
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

        # mock get db client from delivery
        mock.patch(
            "huxunify.api.route.delivery.get_db_client",
            return_value=self.database,
        ).start()

        # mock parameter store
        mock.patch.object(parameter_store, "get_store_value").start()

        # mock AWS batch connector register job function
        mock.patch.object(
            AWSBatchConnector, "register_job", return_value=t_c.BATCH_RESPONSE
        ).start()

        # mock AWS batch connector submit job function
        mock.patch.object(
            AWSBatchConnector, "submit_job", return_value=t_c.BATCH_RESPONSE
        ).start()

        self.addCleanup(mock.patch.stopall)

        # setup test data
        # write a user to the database
        self.user_name = "felix hernandez"
        set_user(
            self.database,
            "fake",
            "felix_hernandez@fake.com",
            display_name=self.user_name,
        )

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

        self.audiences = [
            create_audience(self.database, **x) for x in audiences
        ]

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

        self.engagement_ids = [
            str(set_engagement(self.database, **x)) for x in engagements
        ]

    def test_deliver_audience_for_an_engagement_valid_ids(self):
        """
        Test delivery of an audience for an engagement
        with valid ids

        Args:

        Returns:

        """
        audience_id = self.audiences[1][db_c.ID]
        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/{api_c.DELIVER}"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_deliver_audience_for_an_engagement_invalid_audience_id(self):
        """
        Test delivery of an audience for an engagement
        with invalid audience id

        Args:

        Returns:

        """
        audience_id = t_c.INVALID_ID
        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/{api_c.DELIVER}"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(audience_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_deliver_audience_for_an_engagement_invalid_engagement_id(self):
        """
        Test delivery of an audience for an engagement
        with invalid engagement id

        Args:

        Returns:

        """
        audience_id = self.audiences[0][db_c.ID]
        engagement_id = t_c.INVALID_ID

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/deliver"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(engagement_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_deliver_audience_for_an_engagement_non_existent_engagement(self):
        """
        Test delivery of an audience for an engagement
        with non-existent engagement id

        Args:

        Returns:

        """
        audience_id = self.audiences[0][db_c.ID]
        engagement_id = ObjectId()

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/deliver"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.ENGAGEMENT_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_deliver_destination_for_engagement_audience_valid_ids(self):
        """
        Test delivery of a destination for an audience in engagement
        with valid ids

        Args:

        Returns:

        """
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

    def test_deliver_destination_for_non_existent_engagement(self):
        """
        Test delivery of a destination for a non-existent engagement

        Args:

        Returns:

        """
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

        valid_response = {"message": api_c.ENGAGEMENT_NOT_FOUND}

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json, valid_response)

    def test_deliver_destination_for_unattached_audience(self):
        """
        Test delivery of a destination for an unattached audience

        Args:

        Returns:

        """
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
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {
            "message": "Audience is not attached to the engagement."
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_deliver_destination_for_unattached_destination(self):
        """
        Test delivery of a destination for an unattached destination

        Args:

        Returns:

        """
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
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {
            "message": "Destination is not attached to the engagement audience."
        }

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_deliver_audience_for_all_engagements_valid_audience_id(self):
        """
        Test delivery of audience for all engagements
        with valid audience id

        Args:

        Returns:

        """
        audience_id = self.audiences[0][db_c.ID]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}/{api_c.AUDIENCES}/{audience_id}/{api_c.DELIVER}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {
            "message": f"Successfully created delivery job(s) for audience ID {audience_id}"
        }

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_deliver_audience_for_all_engagements_invalid_audience_id(self):
        """
        Test delivery of audience for all engagements
        with invalid audience id

        Args:

        Returns:

        """
        audience_id = t_c.INVALID_ID

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}/{api_c.AUDIENCES}/{audience_id}/{api_c.DELIVER}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(audience_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_deliver_audience_for_all_engagements_non_existent_audience(self):
        """
        Test delivery of audience for all engagements
        with non-existent audience id

        Args:

        Returns:

        """
        audience_id = ObjectId()

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}/{api_c.AUDIENCES}/{audience_id}/deliver",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": "Audience does not exist."}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_deliver_audience_for_engagement(self):
        """
        Test delivery of audience for a valid engagement id

        Args:

        Returns:

        """

        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/{api_c.DELIVER}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_engagement_delivery_history(self):
        """
        Test get delivery history API with valid id

        Args:

        Returns:

        """

        engagement_id = self.engagement_ids[0]
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_engagement_delivery_history_destination_filter(self):
        """
        Test get engagement delivery history API with destination filter

        Args:

        Returns:

        """

        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        params = {api_c.DESTINATIONS: str(destination_id)}
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            data=params,
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_audience_delivery_history_destination_filter(self):
        """
        Test get audience delivery history API with destination filter

        Args:

        Returns:

        """

        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        params = {api_c.DESTINATIONS: str(destination_id)}
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            data=params,
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_audience_delivery_history_engagement_filter(self):
        """Test get delivery history API with engagement ids as params.

        Args:

        Returns:
        """
        audience_id = self.audiences[0][db_c.ID]

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
            f"{api_c.DELIVERY_HISTORY}?{api_c.ENGAGEMENT_TAG}="
            f"{','.join(self.engagement_ids)}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_engagement_delivery_history_by_id_non_existent_id(self):
        """
        Test get delivery history API with non-existent id

        Args:

        Returns:

        """

        engagement_id = str(ObjectId())

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.ENGAGEMENT_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_engagement_delivery_history_audience_filter(self):
        """Test get delivery history API with audience ids as params.

        Args:

        Returns:
        """
        engagement_id = self.engagement_ids[0]
        audience_ids = [str(audience[db_c.ID]) for audience in self.audiences]

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVERY_HISTORY}?{api_c.AUDIENCES}="
            f"{','.join(audience_ids)}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_audience_delivery_history_invalid_id(self):
        """
        Test get delivery history API with valid id

        Args:

        Returns:

        """

        audience_id = t_c.INVALID_ID

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(audience_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_get_audience_delivery_history_by_id_non_existent_id(self):
        """
        Test get delivery history API with non-existent id

        Args:

        Returns:

        """

        engagement_id = str(ObjectId())

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.ENGAGEMENT_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)
