"""Purpose of this file is to house all the delivery API tests."""

from unittest import TestCase, mock
from http import HTTPStatus
import requests_mock
import mongomock
from bson import ObjectId
from hypothesis import given, strategies as st

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
    set_delivery_job,
    set_delivery_job_status,
)
from huxunifylib.database.engagement_management import (
    set_engagement,
    get_engagement,
)
from huxunifylib.database.orchestration_management import create_audience
from huxunifylib.database.user_management import set_user
from huxunifylib.connectors import AWSBatchConnector
import huxunify.test.constants as t_c
import huxunify.api.constants as api_c
from huxunify.app import create_app
from huxunify.api.data_connectors.aws import parameter_store


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class TestDeliveryRoutes(TestCase):
    """Test Delivery Endpoints."""

    # pylint: disable=unused-variable
    def setUp(self) -> None:
        """Setup resources before each test."""

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

        # mock get db client from delivery
        mock.patch(
            "huxunify.api.route.delivery.get_db_client",
            return_value=self.database,
        ).start()

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

    @given(
        days=st.integers(min_value=1, max_value=7),
        hours=st.integers(min_value=1, max_value=12),
        minutes=st.integers(min_value=0, max_value=45),
        meridiem=st.sampled_from(["AM", "PM"]),
    )
    def test_set_delivery_schedule_daily(
        self, days: int, hours: int, minutes: int, meridiem: str
    ):
        """Test setting daily delivery schedule(s).

        Args:
            days (int): Day of delivery.
            hours (int): Hour of delivery.
            minutes (int): Minute of delivery.
            meridiem (str): Meridiem of delivery.

        """

        self.request_mocker.stop()
        self.request_mocker.get(
            t_c.USER_INFO_CALL, json=t_c.VALID_USER_RESPONSE
        )
        self.request_mocker.start()

        delivery_schedule = {
            api_c.PERIODICIY: "Daily",
            api_c.EVERY: days,
            api_c.HOUR: hours,
            api_c.MINUTE: minutes,
            api_c.PERIOD: meridiem,
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
