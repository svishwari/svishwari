# pylint: disable=too-many-lines
"""Purpose of this file is to house all the delivery API tests."""
from datetime import datetime
from unittest import mock
from http import HTTPStatus
from bson import ObjectId

import huxunifylib.database.constants as db_c
from huxunify.test.route.route_test_util.route_test_case import RouteTestCase
from huxunifylib.database.collection_management import get_document
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
    get_delivery_platform,
    set_delivery_job,
    set_delivery_job_status,
    set_connection_status,
)
from huxunifylib.database.engagement_management import (
    set_engagement,
    get_engagement,
)
from huxunifylib.database.orchestration_management import (
    create_audience,
    append_destination_to_standalone_audience,
)
from huxunifylib.database.user_management import set_user, delete_user
from huxunifylib.connectors import AWSBatchConnector
import huxunify.test.constants as t_c
import huxunify.api.constants as api_c


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class TestDeliveryRoutes(RouteTestCase):
    """Test Delivery Endpoints."""

    # pylint: disable=unused-variable
    def setUp(self) -> None:
        """Setup resources before each test."""

        super().setUp()

        # mock get db client from delivery
        mock.patch(
            "huxunify.api.route.delivery.get_db_client",
            return_value=self.database,
        ).start()

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
        self.user_name = t_c.VALID_USER_RESPONSE[api_c.NAME]
        set_user(
            self.database,
            okta_id=t_c.VALID_USER_RESPONSE[api_c.OKTA_ID_SUB],
            email_address=t_c.VALID_USER_RESPONSE[api_c.EMAIL],
            display_name=self.user_name,
            role=t_c.VALID_USER_RESPONSE[api_c.ROLE],
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
            {
                db_c.DELIVERY_PLATFORM_NAME: "SendGrid by Twilio",
                db_c.DELIVERY_PLATFORM_TYPE: "sendgrid",
                db_c.STATUS: db_c.STATUS_SUCCEEDED,
                db_c.ENABLED: True,
                db_c.ADDED: True,
                db_c.DELIVERY_PLATFORM_AUTH: {
                    api_c.SENDGRID_AUTH_TOKEN: "auth1",
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
                api_c.USER_NAME: self.user_name,
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
                api_c.USER_NAME: self.user_name,
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
                            {db_c.OBJECT_ID: self.destinations[0][db_c.ID]}
                        ],
                    },
                    {
                        db_c.OBJECT_ID: self.audiences[1][db_c.ID],
                        api_c.DESTINATIONS_TAG: [
                            {db_c.OBJECT_ID: self.destinations[0][db_c.ID]}
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

        delivery_jobs = [
            {
                api_c.AUDIENCE_ID: self.audiences[1][db_c.ID],
                db_c.DELIVERY_PLATFORM_ID: self.destinations[1][db_c.ID],
                db_c.DELIVERY_PLATFORM_GENERIC_CAMPAIGNS: [],
                db_c.USERNAME: self.user_name,
                api_c.ENGAGEMENT_ID: ObjectId(self.engagement_ids[0]),
                # db_c.DELETED: False
            }
        ]
        self.delivery_jobs = [
            set_delivery_job(self.database, **job) for job in delivery_jobs
        ]
        set_delivery_job_status(
            self.database,
            self.delivery_jobs[0][db_c.ID],
            db_c.STATUS_DELIVERED,
        )

    def test_deliver_audience_for_an_engagement_valid_ids(self):
        """Test delivery of an audience for an engagement with valid IDs."""

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
        """Test delivery of an audience for an engagement with invalid
        audience ID."""

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
        """Test delivery of an audience for an engagementcwith invalid
        engagement ID."""

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
        """Test delivery of an audience for an engagement with non-existent
        engagement ID."""

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
        """Test delivery of a destination for an audience in engagement with
        valid IDs."""

        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        # mock get db client from decorators
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

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

    def test_replace_audience_deliver(self):
        """Test audience with replace_audience flag"""

        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        # mock get db client from decorators
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/"
                f"{api_c.DESTINATION}/{destination_id}/"
                f"{api_c.DELIVER}?{db_c.REPLACE_AUDIENCE}=true"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        engagement_doc = get_document(
            database=self.database,
            collection=db_c.ENGAGEMENTS_COLLECTION,
            query_filter={},
        )
        for audience in engagement_doc[db_c.AUDIENCES]:
            for destination in audience[db_c.DESTINATIONS]:
                if (
                    destination[api_c.ID] == destination_id
                    and audience[api_c.ID] == audience_id
                ):
                    self.assertTrue(
                        destination.get(db_c.REPLACE_AUDIENCE, False)
                    )

    def test_deliver_all_destination_for_engagement_audience_valid_ids(self):
        """Test delivery of a destination for all audiences in an engagement
        with valid IDs."""

        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        # mock get db client from decorators
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{db_c.ZERO_OBJECT_ID}/"
                f"{api_c.DESTINATION}/{destination_id}/"
                f"{api_c.DELIVER}"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_delivery_destination_with_a_bad_connection(self):
        """Test delivery of a destination with a bad connection."""

        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        # get the delivery platform, set failed status and patch it.
        destination = get_delivery_platform(self.database, destination_id)
        destination[db_c.DELIVERY_PLATFORM_STATUS] = db_c.STATUS_FAILED

        # temporarily patch the response to simulate a failed status.
        patch = mock.patch(
            "huxunify.api.data_connectors.courier.get_delivery_platform",
            return_value=destination,
        )
        patch.start()

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

        patch.stop()
        self.assertEqual(HTTPStatus.FAILED_DEPENDENCY, response.status_code)

    def test_deliver_destination_for_non_existent_engagement(self):
        """Test delivery of a destination for a non-existent engagement."""

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
        """Test delivery of a destination for an unattached audience."""

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
        """Test delivery of a destination for an unattached destination."""

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

    def test_deliver_audience_for_all_engagements_invalid_audience_id(self):
        """Test delivery of audience for all engagements with invalid
        audience ID."""

        audience_id = t_c.INVALID_ID

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}/{api_c.AUDIENCES}/{audience_id}/{api_c.DELIVER}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.BSON_INVALID_ID(audience_id)}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_deliver_audience_for_all_engagements_non_existent_audience(self):
        """Test delivery of audience for all engagements with non-existent
        audience ID."""

        audience_id = ObjectId()

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}/{api_c.AUDIENCES}/{audience_id}/deliver",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": "Audience does not exist."}

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_deliver_audience_for_engagement(self):
        """Test delivery of audience for a valid engagement ID."""

        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/{api_c.DELIVER}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_deliver_audience_for_engagement_with_destinations(self):
        """Test delivery of audience for a valid engagement ID."""

        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVER}?{api_c.DESTINATIONS}=60b9601a6021710aa146df30",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_engagement_delivery_history(self):
        """Test get delivery history API with valid ID."""

        engagement_id = self.engagement_ids[0]
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_engagement_delivery_history_destination_filter(self):
        """Test get engagement delivery history API with destination filter."""

        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        params = {api_c.DESTINATIONS: str(destination_id)}
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            query_string=params,
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_audience_delivery_history_destination_filter(self):
        """Test get audience delivery history API with destination filter."""

        audience_id = self.audiences[0][db_c.ID]
        destination_id = self.destinations[0][db_c.ID]

        params = {api_c.DESTINATIONS: str(destination_id)}
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            query_string=params,
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
            f"{api_c.DELIVERY_HISTORY}?{api_c.ENGAGEMENT}="
            f"{self.engagement_ids[0]}&{api_c.ENGAGEMENT}="
            f"{self.engagement_ids[1]}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_engagement_delivery_history_by_id_non_existent_id(self):
        """Test get delivery history API with non-existent ID."""

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
            f"{api_c.DELIVERY_HISTORY}?{api_c.AUDIENCE}={audience_ids[0]}&"
            f"{api_c.AUDIENCE}={audience_ids[1]}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_get_audience_delivery_history_invalid_id(self):
        """Test get delivery history API with valid ID."""

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
        """Test get delivery history API with non-existent ID."""

        engagement_id = str(ObjectId())

        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )

        valid_response = {"message": api_c.ENGAGEMENT_NOT_FOUND}

        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(valid_response, response.json)

    def test_set_delivery_schedule(self):
        """Test setting a delivery schedule for an engaged audience destination"""

        self.request_mocker.stop()
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.start()

        delivery_schedule = {
            api_c.PERIODICIY: "Daily",
            api_c.EVERY: 2,
            api_c.HOUR: 11,
            api_c.MINUTE: 15,
            api_c.PERIOD: "PM",
        }

        self.assertEqual(
            HTTPStatus.OK,
            self.app.post(
                (
                    f"{t_c.BASE_ENDPOINT}"
                    f"{api_c.ENGAGEMENT_ENDPOINT}/{self.engagement_ids[0]}/"
                    f"{api_c.AUDIENCE}/{self.audiences[0][db_c.ID]}/"
                    f"{api_c.DESTINATION}/{self.destinations[0][db_c.ID]}/"
                    f"{api_c.SCHEDULE}"
                ),
                json=delivery_schedule,
                headers=t_c.STANDARD_HEADERS,
            ).status_code,
        )

        # validate the schedule was actually set.
        engagement = get_engagement(
            self.database, ObjectId(self.engagement_ids[0])
        )
        self.assertIn(db_c.AUDIENCES, engagement)

        # take the first audience
        audience = engagement.get(db_c.AUDIENCES)[0]
        self.assertIn(db_c.DESTINATIONS, audience)

        # take the first destination
        destination = audience.get(db_c.DESTINATIONS)[0]
        self.assertIn(db_c.ENGAGEMENT_DELIVERY_SCHEDULE, destination)
        self.assertDictEqual(
            destination[db_c.ENGAGEMENT_DELIVERY_SCHEDULE], delivery_schedule
        )

    def test_delete_delivery_schedule(self):
        """Test setting a delivery schedule for an engaged audience
        destination."""

        self.request_mocker.stop()
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.start()

        response = self.app.delete(
            (
                f"{t_c.BASE_ENDPOINT}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{self.engagement_ids[0]}/"
                f"{api_c.AUDIENCE}/{self.audiences[0][db_c.ID]}/"
                f"{api_c.DESTINATION}/{self.destinations[0][db_c.ID]}/"
                f"{api_c.SCHEDULE}"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(
            HTTPStatus.OK,
            response.status_code,
        )

        # validate the schedule was actually unset.
        engagement = get_engagement(
            self.database, ObjectId(self.engagement_ids[0])
        )
        self.assertIn(db_c.AUDIENCES, engagement)
        self.assertTrue(
            not any(
                d.get(db_c.ENGAGEMENT_DELIVERY_SCHEDULE)
                for x in engagement[db_c.AUDIENCES]
                for d in x[db_c.DESTINATIONS]
            )
        )

    def test_deliver_standalone_audience_to_a_destination(self):
        """Test delivery of standalone audience to a destination attached to
        audience."""

        # mock AWS batch connector register job function
        mock.patch.object(
            AWSBatchConnector, "register_job", return_value=t_c.BATCH_RESPONSE
        ).start()

        # mock AWS batch connector submit job function
        mock.patch.object(
            AWSBatchConnector, "submit_job", return_value=t_c.BATCH_RESPONSE
        ).start()

        standalone_audience = create_audience(
            self.database,
            "standalone test audience",
            [],
            t_c.TEST_USER_NAME,
            [],
        )

        sfmc_destination = set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_SFMC,
            db_c.DELIVERY_PLATFORM_SFMC,
        )
        sfmc_destination = set_connection_status(
            self.database, sfmc_destination[db_c.ID], db_c.STATUS_SUCCEEDED
        )

        aud_destination = {
            db_c.OBJECT_ID: sfmc_destination[db_c.ID],
            db_c.DELIVERY_PLATFORM_CONFIG: {
                db_c.DATA_EXTENSION_NAME: "SFMC Date Extension"
            },
            db_c.DATA_ADDED: datetime.utcnow(),
        }

        standalone_audience = append_destination_to_standalone_audience(
            database=self.database,
            audience_id=standalone_audience[db_c.ID],
            destination=aud_destination,
            user_name=t_c.TEST_USER_NAME,
        )

        audience_id = standalone_audience[db_c.ID]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
            f"{api_c.DELIVER}",
            json={
                api_c.DESTINATIONS: [
                    {db_c.OBJECT_ID: str(sfmc_destination[db_c.ID])}
                ]
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
        self.assertEqual(
            {
                api_c.MESSAGE: f"Successfully created delivery job(s) for "
                f"audience ID {audience_id}"
            },
            response.json,
        )

    def test_deliver_standalone_audience_to_a_destination_not_attached(self):
        """Test delivery of standalone audience to a destination not attached
        to audience."""

        # mock AWS batch connector register job function
        mock.patch.object(
            AWSBatchConnector, "register_job", return_value=t_c.BATCH_RESPONSE
        ).start()

        # mock AWS batch connector submit job function
        mock.patch.object(
            AWSBatchConnector, "submit_job", return_value=t_c.BATCH_RESPONSE
        ).start()

        standalone_audience = create_audience(
            self.database,
            "standalone test audience",
            [],
            t_c.TEST_USER_NAME,
            [],
        )

        sfmc_destination = set_delivery_platform(
            self.database,
            db_c.DELIVERY_PLATFORM_SFMC,
            db_c.DELIVERY_PLATFORM_SFMC,
        )
        sfmc_destination = set_connection_status(
            self.database, sfmc_destination[db_c.ID], db_c.STATUS_SUCCEEDED
        )

        aud_destination = {
            db_c.OBJECT_ID: sfmc_destination[db_c.ID],
            db_c.DELIVERY_PLATFORM_CONFIG: {
                db_c.DATA_EXTENSION_NAME: "SFMC Date Extension"
            },
            db_c.DATA_ADDED: datetime.utcnow(),
        }

        standalone_audience = append_destination_to_standalone_audience(
            database=self.database,
            audience_id=standalone_audience[db_c.ID],
            destination=aud_destination,
            user_name=t_c.TEST_USER_NAME,
        )

        audience_id = standalone_audience[db_c.ID]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.AUDIENCE_ENDPOINT}/{audience_id}/"
            f"{api_c.DELIVER}",
            json={
                api_c.DESTINATIONS: [
                    {db_c.OBJECT_ID: str(self.destinations[0][db_c.ID])}
                ]
            },
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            {
                api_c.MESSAGE: f"Destination ID {str(self.destinations[0][db_c.ID])} "
                f"to be delivered not attached to audience "
                f"ID {audience_id}."
            },
            response.json,
        )

    def test_set_delivery_schedule_for_all_destinations(self):
        """Test setting a delivery schedule for all engaged destination(s)"""

        self.request_mocker.stop()
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.start()

        delivery_schedule = {
            api_c.PERIODICIY: "Daily",
            api_c.EVERY: 2,
            api_c.HOUR: 11,
            api_c.MINUTE: 15,
            api_c.PERIOD: "PM",
        }

        self.assertEqual(
            HTTPStatus.OK,
            self.app.post(
                (
                    f"{t_c.BASE_ENDPOINT}"
                    f"{api_c.ENGAGEMENT_ENDPOINT}/{self.engagement_ids[0]}/"
                    f"{api_c.AUDIENCE}/{db_c.ZERO_OBJECT_ID}/"
                    f"{api_c.DESTINATION}/{self.destinations[0][db_c.ID]}/"
                    f"{api_c.SCHEDULE}"
                ),
                json=delivery_schedule,
                headers=t_c.STANDARD_HEADERS,
            ).status_code,
        )

        # validate the schedule was actually set.
        engagement = get_engagement(
            self.database, ObjectId(self.engagement_ids[0])
        )
        self.assertIn(db_c.AUDIENCES, engagement)

        destinations = [
            d for a in engagement[db_c.AUDIENCES] for d in a[db_c.DESTINATIONS]
        ]

        # check length of destinations
        self.assertEqual(2, len(destinations))

        # process each destination and validate
        for destination in destinations:
            self.assertIn(db_c.ENGAGEMENT_DELIVERY_SCHEDULE, destination)
            self.assertDictEqual(
                destination[db_c.ENGAGEMENT_DELIVERY_SCHEDULE],
                delivery_schedule,
            )

    def test_delete_delivery_schedule_for_all_destinations(self):
        """Test setting a delivery schedule for all engaged
        destinations."""

        self.request_mocker.stop()
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.start()

        response = self.app.delete(
            (
                f"{t_c.BASE_ENDPOINT}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{self.engagement_ids[0]}/"
                f"{api_c.AUDIENCE}/{db_c.ZERO_OBJECT_ID}/"
                f"{api_c.DESTINATION}/{self.destinations[0][db_c.ID]}/"
                f"{api_c.SCHEDULE}"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(
            HTTPStatus.OK,
            response.status_code,
        )

        # validate the schedule was actually unset.
        engagement = get_engagement(
            self.database, ObjectId(self.engagement_ids[0])
        )
        self.assertIn(db_c.AUDIENCES, engagement)
        self.assertTrue(
            not any(
                d.get(db_c.ENGAGEMENT_DELIVERY_SCHEDULE)
                for x in engagement[db_c.AUDIENCES]
                for d in x[db_c.DESTINATIONS]
            )
        )

    def test_set_delivery_schedule_for_an_engagement_audience(self):
        """Test setting delivery schedule for an engagement audience."""

        self.request_mocker.stop()
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.start()

        delivery_schedule = {
            api_c.SCHEDULE: {
                api_c.PERIODICIY: api_c.DAILY,
                api_c.EVERY: 1,
                api_c.HOUR: 12,
                api_c.MINUTE: 15,
                api_c.PERIOD: api_c.AM,
            },
            api_c.START_DATE: "2022-03-02T00:00:00.000Z",
            api_c.END_DATE: "2022-03-04T00:00:00.000Z",
        }

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{self.engagement_ids[0]}/"
                f"{api_c.AUDIENCE}/{self.audiences[0][db_c.ID]}/"
                f"{api_c.SCHEDULE}"
            ),
            json=delivery_schedule,
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(
            {api_c.MESSAGE: "Successfully updated delivery schedule."},
            response.json,
        )

        # validate the schedule was actually set.
        engagement = get_engagement(
            self.database, ObjectId(self.engagement_ids[0])
        )
        self.assertIn(db_c.AUDIENCES, engagement)

        audiences = list(engagement[db_c.AUDIENCES])
        # check that there are two audiences in the engagement
        self.assertEqual(2, len(audiences))

        # validate that the delivery_schedule is only set for the audience that
        # is passed in the request
        for audience in audiences:
            if audience[api_c.ID] == self.audiences[0][db_c.ID]:
                self.assertIn(db_c.ENGAGEMENT_DELIVERY_SCHEDULE, audience)
            else:
                self.assertNotIn(db_c.ENGAGEMENT_DELIVERY_SCHEDULE, audience)

    def test_remove_delivery_schedule_for_an_engagement_audience(self):
        """Test removing delivery schedule for an engagement audience."""

        self.request_mocker.stop()
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.start()

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}"
                f"{api_c.ENGAGEMENT_ENDPOINT}/{self.engagement_ids[0]}/"
                f"{api_c.AUDIENCE}/{self.audiences[0][db_c.ID]}/"
                f"{api_c.SCHEDULE}?{api_c.UNSET}=True"
            ),
            json={},
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(
            {api_c.MESSAGE: "Successfully removed delivery schedule."},
            response.json,
        )

        # validate the schedule was actually unset.
        engagement = get_engagement(
            self.database, ObjectId(self.engagement_ids[0])
        )
        self.assertIn(db_c.AUDIENCES, engagement)
        self.assertFalse(
            any(
                aud.get(db_c.ENGAGEMENT_DELIVERY_SCHEDULE)
                for aud in engagement[db_c.AUDIENCES]
            )
        )

    # pylint: disable=attribute-defined-outside-init
    def test_viewer_user_permissions(self) -> None:
        """Test Viewer user access to different delivery API end points."""

        delete_user(
            self.database, t_c.VALID_INTROSPECTION_RESPONSE.get(api_c.OKTA_UID)
        )
        # write a user to the database
        self.user_name = t_c.VALID_USER_RESPONSE.get(api_c.NAME)
        self.user_doc = set_user(
            self.database,
            t_c.VALID_VIEWER_INTROSPECTION_RESPONSE.get(api_c.OKTA_UID),
            t_c.VALID_VIEWER_USER_RESPONSE.get(api_c.EMAIL),
            display_name=self.user_name,
            role=t_c.VALID_VIEWER_USER_RESPONSE[api_c.ROLE],
        )

        audience_id = self.audiences[1][db_c.ID]
        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            (
                f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
                f"{api_c.AUDIENCE}/{audience_id}/{api_c.DELIVER}"
            ),
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        # mock get db client from decorators
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

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

        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/{api_c.DELIVER}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

        engagement_id = self.engagement_ids[0]
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    # pylint: disable=attribute-defined-outside-init
    def test_editor_user_permissions(self) -> None:
        """Test Editor user access to different delivery API end points."""

        delete_user(
            self.database, t_c.VALID_INTROSPECTION_RESPONSE.get(api_c.OKTA_UID)
        )
        # write a user to the database
        self.user_name = t_c.VALID_USER_RESPONSE.get(api_c.NAME)
        self.user_doc = set_user(
            self.database,
            t_c.VALID_EDITOR_INTROSPECTION_RESPONSE.get(api_c.OKTA_UID),
            t_c.VALID_EDITOR_USER_RESPONSE.get(api_c.EMAIL),
            display_name=self.user_name,
            role=t_c.VALID_EDITOR_USER_RESPONSE[api_c.ROLE],
        )

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

        audience_id = self.audiences[0][db_c.ID]
        engagement_id = self.engagement_ids[0]
        destination_id = self.destinations[0][db_c.ID]

        # mock get db client from decorators
        mock.patch(
            "huxunify.api.route.decorators.get_db_client",
            return_value=self.database,
        ).start()

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

        engagement_id = self.engagement_ids[0]

        response = self.app.post(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/{api_c.DELIVER}",
            headers=t_c.STANDARD_HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)

        engagement_id = self.engagement_ids[0]
        response = self.app.get(
            f"{t_c.BASE_ENDPOINT}{api_c.ENGAGEMENT_ENDPOINT}/{engagement_id}/"
            f"{api_c.DELIVERY_HISTORY}",
            headers=t_c.STANDARD_HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
