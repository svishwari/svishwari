"""Purpose of this file is to house all the courier tests."""
import asyncio
from http import HTTPStatus
from unittest import TestCase, mock
import mongomock
from bson import ObjectId
from hypothesis import given, strategies as st
import requests_mock

import huxunifylib.database.constants as db_c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
    get_delivery_job_status,
    get_delivery_platform,
    set_connection_status,
    get_delivery_jobs_using_metadata,
)
from huxunifylib.database.engagement_audience_management import (
    set_engagement_audience_schedule,
)
from huxunifylib.database.notification_management import get_notifications
from huxunifylib.database.engagement_management import (
    get_engagement,
    set_engagement,
)
from huxunifylib.database.orchestration_management import create_audience
from huxunifylib.connectors import AWSBatchConnector
from huxunifylib.util.general.const import (
    FacebookCredentials,
    SFMCCredentials,
)
from huxunifylib.util.audience_router.const import AudienceRouterConfig
from huxunify.api.data_connectors.cloud.cloud_client import CloudClient
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.aws import (
    get_auth_from_parameter_store,
)
from huxunify.api.data_connectors.courier import (
    map_destination_credentials_to_dict,
    get_okta_test_user_creds,
    get_destination_config,
    get_audience_destination_pairs,
    deliver_audience_to_destination,
    BaseDestinationBatchJob,
    AWSDestinationBatchJob,
    AzureDestinationBatchJob,
)
from huxunify.api.data_connectors.scheduler import run_scheduled_deliveries
from huxunify.api.config import get_config
from huxunify.test import constants as t_c


# pylint: disable=too-many-public-methods
class CourierTest(TestCase):
    """Test Courier methods."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):
        """Setup method for unit tests."""

        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        # Set delivery platform
        self.auth_details_facebook = {
            "facebook_access_token": "path1",
            "facebook_app_secret": "path2",
            "facebook_app_id": "path3",
            "facebook_ad_account_id": "path4",
        }

        # create the list of destinations
        destinations = []
        for destination in [
            (db_c.DELIVERY_PLATFORM_FACEBOOK, self.auth_details_facebook)
        ]:
            # TODO - remove when we remove delivery-platform types
            destination_doc = set_delivery_platform(
                self.database,
                destination[0],
                destination[0],
                destination[1],
            )

            # ensure doc was created
            self.assertIsNotNone(destination_doc)

            # set status
            destination_doc = set_connection_status(
                self.database, destination_doc[db_c.ID], db_c.STATUS_SUCCEEDED
            )
            self.assertEqual(
                db_c.STATUS_SUCCEEDED,
                destination_doc[db_c.DELIVERY_PLATFORM_STATUS],
            )

            destinations.append(destination_doc)

        self.destination_ids = [d[db_c.ID] for d in destinations]

        # create first audience
        self.audience_one = create_audience(
            self.database,
            "audience one",
            [],
            t_c.TEST_USER_NAME,
            self.destination_ids,
        )
        self.assertIsNotNone(self.audience_one)

        # create second audience
        self.audience_two = create_audience(
            self.database,
            "audience two",
            [],
            t_c.TEST_USER_NAME,
            self.destination_ids,
        )
        self.assertIsNotNone(self.audience_two)

        # define a sample engagement, with prepopulated engagements
        engagement_doc = {
            db_c.AUDIENCE_NAME: "Chihuly Garden and Glass",
            db_c.NOTIFICATION_FIELD_DESCRIPTION: "Former fun forest amusement park.",
            db_c.AUDIENCES: [
                {
                    db_c.OBJECT_ID: self.audience_one[db_c.ID],
                    db_c.DESTINATIONS: [
                        {db_c.OBJECT_ID: x}
                        for x in self.audience_one[db_c.DESTINATIONS]
                    ],
                },
                {
                    db_c.OBJECT_ID: self.audience_two[db_c.ID],
                    db_c.DESTINATIONS: [
                        {db_c.OBJECT_ID: x}
                        for x in self.audience_two[db_c.DESTINATIONS]
                    ],
                },
            ],
            db_c.CREATED_BY: t_c.TEST_USER_NAME,
        }

        # insert engagement doc in the collection
        engagement_id = set_engagement(
            self.database,
            engagement_doc[db_c.AUDIENCE_NAME],
            engagement_doc[db_c.NOTIFICATION_FIELD_DESCRIPTION],
            engagement_doc[db_c.AUDIENCES],
            engagement_doc[db_c.CREATED_BY],
        )

        self.test_user = t_c.TEST_USER_NAME

        self.assertIsInstance(engagement_id, ObjectId)
        self.engagement = get_engagement(self.database, engagement_id)
        self.assertTrue(self.engagement)

        self.addCleanup(mock.patch.stopall)

    def test_map_destination_credentials_facebook(self):
        """Test mapping of destination credentials for submitting to AWS Batch."""

        # setup destination object with synthetic credentials.
        sample_auth = "sample_auth"
        destination = {
            api_c.DESTINATION_ID: ObjectId(),
            api_c.DESTINATION_NAME: db_c.DELIVERY_PLATFORM_FACEBOOK,
            api_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FACEBOOK,
            api_c.AUTHENTICATION_DETAILS: {
                api_c.FACEBOOK_ACCESS_TOKEN: sample_auth,
                api_c.FACEBOOK_APP_SECRET: sample_auth,
                api_c.FACEBOOK_APP_ID: sample_auth,
                api_c.FACEBOOK_AD_ACCOUNT_ID: sample_auth,
            },
        }

        env_dict, secret_dict = map_destination_credentials_to_dict(
            destination
        )

        # ensure mapping.
        auth = destination[api_c.AUTHENTICATION_DETAILS]
        self.assertDictEqual(
            env_dict,
            {
                FacebookCredentials.FACEBOOK_APP_ID.name: auth[
                    api_c.FACEBOOK_APP_ID
                ],
                FacebookCredentials.FACEBOOK_AD_ACCOUNT_ID.name: auth[
                    api_c.FACEBOOK_AD_ACCOUNT_ID
                ],
            },
        )
        self.assertEqual(
            secret_dict,
            {
                FacebookCredentials.FACEBOOK_ACCESS_TOKEN.name: auth[
                    api_c.FACEBOOK_ACCESS_TOKEN
                ],
                FacebookCredentials.FACEBOOK_APP_SECRET.name: auth[
                    api_c.FACEBOOK_APP_SECRET
                ],
            },
        )

    def test_map_destination_credentials_sfmc(self):
        """Test mapping of destination credentials for submitting to AWS Batch."""

        # setup destination object with synthetic credentials.
        sample_auth = "sample_auth"
        destination = {
            api_c.DESTINATION_ID: ObjectId(),
            api_c.DESTINATION_NAME: db_c.DELIVERY_PLATFORM_SFMC,
            api_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFMC,
            api_c.AUTHENTICATION_DETAILS: {
                api_c.SFMC_CLIENT_ID: sample_auth,
                api_c.SFMC_AUTH_BASE_URI: sample_auth,
                api_c.SFMC_ACCOUNT_ID: sample_auth,
                api_c.SFMC_CLIENT_SECRET: sample_auth,
                api_c.SFMC_SOAP_BASE_URI: sample_auth,
                api_c.SFMC_REST_BASE_URI: sample_auth,
            },
        }

        env_dict, secret_dict = map_destination_credentials_to_dict(
            destination
        )

        # ensure mapping.
        auth = destination[api_c.AUTHENTICATION_DETAILS]
        self.assertDictEqual(
            env_dict,
            {
                SFMCCredentials.SFMC_CLIENT_ID.name: auth[
                    api_c.SFMC_CLIENT_ID
                ],
                SFMCCredentials.SFMC_AUTH_URL.name: auth[
                    api_c.SFMC_AUTH_BASE_URI
                ],
                SFMCCredentials.SFMC_ACCOUNT_ID.name: auth[
                    api_c.SFMC_ACCOUNT_ID
                ],
                SFMCCredentials.SFMC_SOAP_ENDPOINT.name: auth[
                    api_c.SFMC_SOAP_BASE_URI
                ],
                SFMCCredentials.SFMC_URL.name: auth[api_c.SFMC_REST_BASE_URI],
            },
        )
        self.assertDictEqual(
            secret_dict,
            {
                SFMCCredentials.SFMC_CLIENT_SECRET.name: auth[
                    api_c.SFMC_CLIENT_SECRET
                ]
            },
        )

    def test_get_pairs(self):
        """Test get audience/destination pairs valid destination."""

        delivery_route = get_audience_destination_pairs(
            self.engagement[db_c.AUDIENCES]
        )

        self.assertTrue(delivery_route)
        self.assertEqual(len(delivery_route), 2)

    def test_get_pairs_invalid_dest(self):
        """Test get audience/destination pairs invalid destination."""

        # take the first engagement audience and set an invalid audience destination
        invalid_engagement = self.engagement[db_c.AUDIENCES]
        invalid_engagement[0][api_c.DESTINATIONS] = "invalid_data"

        # now test getting the delivery route, which should yield one destination pair.
        delivery_route = get_audience_destination_pairs(invalid_engagement)

        self.assertTrue(delivery_route)

        # test for a list length of one. the invalid data is removed from the return.
        self.assertEqual(len(delivery_route), 1)

    def test_get_okta_test_user_creds(self):
        """Test get_okta_test_user_creds"""

        # get config
        config = get_config()

        # get okta credentials
        self.assertTupleEqual(
            get_okta_test_user_creds(config),
            (
                {
                    api_c.OKTA_ISSUER: config.OKTA_ISSUER,
                    api_c.OKTA_CLIENT_ID: config.OKTA_CLIENT_ID,
                },
                {
                    api_c.OKTA_TEST_USER_NAME: api_c.UNIFIED_OKTA_TEST_USER_NAME,
                    api_c.OKTA_TEST_USER_PW: api_c.UNIFIED_OKTA_TEST_USER_PW,
                    api_c.OKTA_REDIRECT_URI: api_c.UNIFIED_OKTA_REDIRECT_URI,
                },
            ),
        )

    def test_get_delivery_route_audience(self):
        """Test get delivery route with specific audience."""

        engagement = self.engagement.copy()
        engagement[db_c.AUDIENCES] = [engagement[db_c.AUDIENCES][0]]

        delivery_route = get_audience_destination_pairs(
            engagement[db_c.AUDIENCES]
        )

        self.assertTrue(delivery_route)

        expected_route = [
            [
                self.audience_one[db_c.ID],
                {db_c.OBJECT_ID: self.audience_one[db_c.DESTINATIONS][0]},
            ]
        ]

        self.assertListEqual(expected_route, delivery_route)

    def test_destination_batch_init(self):
        """Test destination batch init."""

        delivery_route = get_audience_destination_pairs(
            self.engagement[db_c.AUDIENCES]
        )
        self.assertTrue(delivery_route)

        request_mocker = requests_mock.Mocker()
        request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        request_mocker.start()

        for pair in delivery_route:
            batch_destination = get_destination_config(
                self.database,
                *pair,
                self.engagement[db_c.ID],
                username=self.test_user,
            )

            self.assertIsNotNone(batch_destination.aws_envs)
            self.assertIsNotNone(batch_destination.aws_secrets)
            self.assertIsNotNone(batch_destination.audience_delivery_job_id)
            self.assertEqual(self.database, batch_destination.database)

            # validate the audience delivery job id exists
            audience_delivery_status = get_delivery_job_status(
                self.database, batch_destination.audience_delivery_job_id
            )
            self.assertEqual(
                audience_delivery_status, db_c.AUDIENCE_STATUS_DELIVERING
            )

    def test_destination_register_job(self):
        """Test destination batch register job."""

        delivery_route = get_audience_destination_pairs(
            self.engagement[db_c.AUDIENCES]
        )
        self.assertTrue(delivery_route)

        # walk the delivery route
        for pair in delivery_route:
            batch_destination = get_destination_config(
                self.database,
                *pair,
                self.engagement[db_c.ID],
                username=self.test_user,
            )

            batch_destination.aws_envs[
                AudienceRouterConfig.BATCH_SIZE.name
            ] = 1000
            batch_destination.aws_envs[api_c.AUDIENCE_ROUTER_STUB_TEST] = 1
            self.assertIsNotNone(batch_destination)

            # Register job
            return_value = {
                "ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value}
            }
            with mock.patch.object(
                AWSBatchConnector,
                "register_job",
                return_value=return_value,
            ):
                batch_destination.register()

            self.assertEqual(
                batch_destination.result, db_c.AUDIENCE_STATUS_DELIVERING
            )

    def test_destination_submit_job(self):
        """Test destination batch submit job."""

        delivery_route = get_audience_destination_pairs(
            self.engagement[db_c.AUDIENCES]
        )
        self.assertTrue(delivery_route)

        # walk the delivery route
        for pair in delivery_route:
            batch_destination = get_destination_config(
                self.database,
                *pair,
                self.engagement[db_c.ID],
                username=self.test_user,
            )

            # Register job
            return_value = {
                "ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value}
            }
            with mock.patch.object(
                AWSBatchConnector,
                "register_job",
                return_value=return_value,
            ):
                batch_destination.register()
            self.assertEqual(
                batch_destination.result, db_c.AUDIENCE_STATUS_DELIVERING
            )

            with mock.patch.object(
                AWSBatchConnector, "submit_job", return_value=return_value
            ):
                batch_destination.submit()

            self.assertEqual(batch_destination.result, api_c.STATUS_DELIVERING)

    @given(
        st.dictionaries(
            keys=st.one_of(st.text(), st.floats()),
            values=st.one_of(st.text(), st.floats()),
        )
    )
    def test_bad_map_destination_credentials_to_dict(self, bad_dict: dict):
        """Test mapping destination credentials with bad data.

        Args:
            bad_dict (dict): hypothesis dict of random data.
        """

        with self.assertRaises(KeyError):
            map_destination_credentials_to_dict(bad_dict)

    @given(
        st.lists(
            st.dictionaries(
                keys=st.one_of(st.text(), st.floats()),
                values=st.one_of(st.text(), st.floats()),
            )
        )
    )
    def test_bad_get_audience_destination_pairs(self, bad_list: list):
        """Test getting audience destinations with bad data.

        Args:
            bad_list (list): hypothesis list of random data.
        """

        with self.assertRaises(TypeError):
            get_audience_destination_pairs(bad_list)

    def test_get_auth_from_parameter_store(self):
        """Test function get_auth_from_parameter_store."""
        config = get_config()
        config.CLOUD_PROVIDER = "aws"

        # use audience once
        for destination_id in self.audience_one[db_c.DESTINATIONS]:
            # get destination
            destination = get_delivery_platform(self.database, destination_id)

            # setup mocks for each secret
            simulated_secret = (
                f"simulated_secret_{destination[db_c.DELIVERY_PLATFORM_TYPE]}"
            )
            for _ in api_c.DESTINATION_SECRETS[
                destination[db_c.DELIVERY_PLATFORM_TYPE]
            ]:
                for subclass in CloudClient.__subclasses__():
                    mock.patch.object(
                        subclass,
                        "get_secret",
                        return_value=simulated_secret,
                    ).start()

            # run the function
            auth = get_auth_from_parameter_store(
                destination[db_c.DELIVERY_PLATFORM_AUTH],
                destination[db_c.DELIVERY_PLATFORM_TYPE],
            )

            # test that the secrets were set to the simulated secret
            for secret in api_c.DESTINATION_SECRETS[
                destination[db_c.DELIVERY_PLATFORM_TYPE]
            ][api_c.AWS_SSM_NAME]:
                self.assertEqual(auth[secret.upper()], simulated_secret)

    def test_run_scheduled_delivery(self):
        """Test run scheduled delivery for an audience in an engagement."""

        # define a sample engagement to simulate the scheduled delivery
        engagement_doc = {
            db_c.AUDIENCE_NAME: "Seattle Space Needle",
            db_c.NOTIFICATION_FIELD_DESCRIPTION: "Fun.",
            db_c.AUDIENCES: [
                {
                    db_c.OBJECT_ID: self.audience_two[db_c.ID],
                    db_c.DESTINATIONS: [
                        {
                            db_c.OBJECT_ID: x,
                            api_c.DELIVERY_SCHEDULE: {
                                api_c.PERIODICIY: "Daily",
                                api_c.EVERY: 0,
                                api_c.HOUR: 0,
                                api_c.MINUTE: 0,
                                api_c.PERIOD: "PM",
                            },
                        }
                        for x in self.audience_two[db_c.DESTINATIONS]
                    ],
                },
            ],
            db_c.CREATED_BY: t_c.TEST_USER_NAME,
        }

        # insert engagement doc in the collection
        engagement_id = set_engagement(
            self.database,
            engagement_doc[db_c.AUDIENCE_NAME],
            engagement_doc[db_c.NOTIFICATION_FIELD_DESCRIPTION],
            engagement_doc[db_c.AUDIENCES],
            engagement_doc[db_c.CREATED_BY],
        )

        delivery_schedule = {
            api_c.SCHEDULE: {
                api_c.PERIODICIY: api_c.DAILY,
                api_c.EVERY: 0,
                api_c.HOUR: 0,
                api_c.MINUTE: 0,
                api_c.PERIOD: api_c.PM,
            },
            api_c.START_DATE: "2022-03-02T00:00:00.000Z",
        }

        set_engagement_audience_schedule(
            self.database,
            engagement_id,
            self.audience_two[db_c.ID],
            delivery_schedule,
            t_c.TEST_USER_NAME,
        )

        # mock AWS batch connector register job function
        mock.patch.object(
            AWSBatchConnector, "register_job", return_value=t_c.BATCH_RESPONSE
        ).start()

        # mock AWS batch connector submit job function
        mock.patch.object(
            AWSBatchConnector, "submit_job", return_value=t_c.BATCH_RESPONSE
        ).start()

        # manually set the delivery schedule of the engagement
        run_scheduled_deliveries(self.database)

        # validate delivery job created
        delivery_jobs = get_delivery_jobs_using_metadata(
            self.database, engagement_id
        )
        self.assertTrue(delivery_jobs)
        self.assertEqual(1, len(delivery_jobs))
        self.assertEqual(
            db_c.AUDIENCE_STATUS_DELIVERING, delivery_jobs[0][db_c.STATUS]
        )

        # validate notification created
        notifications = get_notifications(
            self.database,
            {
                db_c.NOTIFICATION_FIELD_USERNAME: engagement_doc[
                    db_c.CREATED_BY
                ]
            },
        )
        self.assertEqual(1, notifications["total_records"])

    def test_deliver_audience_to_destination(self):
        """Test delivering an audience to a destination without any
        engagement."""

        # mock AWS batch connector register job function
        mock.patch.object(
            AWSBatchConnector, "register_job", return_value=t_c.BATCH_RESPONSE
        ).start()

        # mock AWS batch connector submit job function
        mock.patch.object(
            AWSBatchConnector, "submit_job", return_value=t_c.BATCH_RESPONSE
        ).start()

        # manually deliver audience to a destination without any engagement
        asyncio.run(
            deliver_audience_to_destination(
                database=self.database,
                audience_id=self.audience_one[db_c.ID],
                destination_id=self.destination_ids[0],
                user_name="Delivery Test User",
            )
        )

        # validate delivery job created
        delivery_jobs = get_delivery_jobs_using_metadata(
            database=self.database,
            audience_id=self.audience_one[db_c.ID],
            delivery_platform_id=self.destination_ids[0],
        )
        self.assertTrue(delivery_jobs)
        self.assertEqual(1, len(delivery_jobs))
        self.assertEqual(
            db_c.AUDIENCE_STATUS_DELIVERING, delivery_jobs[0][db_c.STATUS]
        )

        # validate notification created
        notifications = get_notifications(
            self.database,
            {db_c.NOTIFICATION_FIELD_USERNAME: "Delivery Test User"},
        )
        self.assertEqual(1, notifications["total_records"])

    def test_aws_destination_batch_job(self):
        """Test destination batch job inheritance when provider is aws."""
        config = get_config(api_c.TEST_MODE)

        config.CLOUD_PROVIDER = "aws"

        mock.patch(
            "huxunify.api.config.get_config",
            return_value=config,
        ).start()

        audience_delivery_job_id = ObjectId()
        destination_batch_job = BaseDestinationBatchJob(
            database=self.database,
            audience_delivery_job_id=audience_delivery_job_id,
            secrets_dict={},
            env_dict={},
            destination_type="test",
        )

        self.assertIsInstance(destination_batch_job, AWSDestinationBatchJob)
        self.assertEqual(
            audience_delivery_job_id,
            destination_batch_job.audience_delivery_job_id,
        )

    def test_azure_destination_batch_job(self):
        """Test destination batch job inheritance when provider is azure."""

        config = get_config(api_c.TEST_MODE)

        config.CLOUD_PROVIDER = "azure"

        mock.patch(
            "huxunify.api.config.get_config",
            return_value=config,
        ).start()

        audience_delivery_job_id = ObjectId()
        destination_batch_job = BaseDestinationBatchJob(
            database=self.database,
            audience_delivery_job_id=audience_delivery_job_id,
            secrets_dict={},
            env_dict={},
            destination_type="test",
        )

        self.assertIsInstance(destination_batch_job, AzureDestinationBatchJob)
        self.assertEqual(
            audience_delivery_job_id,
            destination_batch_job.audience_delivery_job_id,
        )
