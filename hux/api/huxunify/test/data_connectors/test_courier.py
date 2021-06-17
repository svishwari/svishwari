"""
purpose of this file is to house all the courier tests.
"""
from http import HTTPStatus
from unittest import TestCase, mock
import mongomock
from bson import ObjectId
from hypothesis import given, strategies as st

import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
    get_delivery_job_status,
    set_connection_status,
)
from huxunifylib.database.engagement_management import (
    get_engagement,
    set_engagement,
)
from huxunifylib.database.orchestration_management import create_audience
from huxunifylib.connectors.aws_batch_connector import AWSBatchConnector
from huxunifylib.util.general.const import (
    FacebookCredentials,
    SFMCCredentials,
)
from huxunifylib.util.audience_router.const import AudienceRouterConfig
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.aws import parameter_store
from huxunify.api.data_connectors.courier import (
    map_destination_credentials_to_dict,
    get_destination_config,
    get_audience_destination_pairs,
)


class CourierTest(TestCase):
    """
    Test Courier
    """

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):
        """Setup method for unit tests.

        Args:

        Returns:

        """
        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        # Set delivery platform
        self.auth_details_facebook = {
            "facebook_access_token": "path1",
            "facebook_app_secret": "path2",
            "facebook_app_id": "path3",
            "facebook_ad_account_id": "path4",
        }

        # create the list of destinations
        destinations = []
        for destination in [(api_c.FACEBOOK_NAME, self.auth_details_facebook)]:
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
                self.database, destination_doc[c.ID], c.STATUS_SUCCEEDED
            )
            self.assertEqual(
                c.STATUS_SUCCEEDED, destination_doc[c.DELIVERY_PLATFORM_STATUS]
            )

            destinations.append(destination_doc)

        destination_ids = [d[c.ID] for d in destinations]

        # create first audience
        self.audience_one = create_audience(
            self.database, "audience one", [], destination_ids
        )
        self.assertIsNotNone(self.audience_one)

        # create second audience
        self.audience_two = create_audience(
            self.database, "audience two", [], destination_ids
        )
        self.assertIsNotNone(self.audience_two)

        # define a sample engagement, with prepopulated engagements
        engagement_doc = {
            c.AUDIENCE_NAME: "Chihuly Garden and Glass",
            c.NOTIFICATION_FIELD_DESCRIPTION: "Former fun forest amusement park.",
            c.AUDIENCES: [
                {
                    c.OBJECT_ID: self.audience_one[c.ID],
                    c.DESTINATIONS: [
                        {c.OBJECT_ID: x}
                        for x in self.audience_one[c.DESTINATIONS]
                    ],
                },
                {
                    c.OBJECT_ID: self.audience_two[c.ID],
                    c.DESTINATIONS: [
                        {c.OBJECT_ID: x}
                        for x in self.audience_two[c.DESTINATIONS]
                    ],
                },
            ],
            c.CREATED_BY: ObjectId(),
        }

        # insert engagement doc in the collection
        engagement_id = set_engagement(
            self.database,
            engagement_doc[c.AUDIENCE_NAME],
            engagement_doc[c.NOTIFICATION_FIELD_DESCRIPTION],
            engagement_doc[c.AUDIENCES],
            engagement_doc[c.CREATED_BY],
        )

        self.assertIsInstance(engagement_id, ObjectId)
        self.engagement = get_engagement(self.database, engagement_id)
        self.assertTrue(self.engagement)

    def test_map_destination_credentials_facebook(self):
        """Test mapping of destination credentials for submitting to AWS Batch.

        Args:

        Returns:

        """

        # setup destination object with synthetic credentials.
        sample_auth = "sample_auth"
        destination = {
            api_c.DESTINATION_ID: ObjectId(),
            api_c.DESTINATION_NAME: "Facebook",
            api_c.DELIVERY_PLATFORM_TYPE: "Facebook",
            api_c.AUTHENTICATION_DETAILS: {
                api_c.FACEBOOK_ACCESS_TOKEN: sample_auth,
                api_c.FACEBOOK_APP_SECRET: sample_auth,
                api_c.FACEBOOK_APP_ID: sample_auth,
                api_c.FACEBOOK_AD_ACCOUNT_ID: sample_auth,
            },
        }

        with mock.patch.object(
            parameter_store,
            "get_store_value",
            return_value="sample_auth",
        ):
            env_dict, _ = map_destination_credentials_to_dict(destination)

        # ensure mapping.
        auth = destination[api_c.AUTHENTICATION_DETAILS]
        # TODO HUS-582 work with ORCH so we dont' have to send creds in env_dict
        self.assertDictEqual(
            env_dict,
            {
                FacebookCredentials.FACEBOOK_APP_ID.name: auth[
                    api_c.FACEBOOK_APP_ID
                ],
                FacebookCredentials.FACEBOOK_AD_ACCOUNT_ID.name: auth[
                    api_c.FACEBOOK_AD_ACCOUNT_ID
                ],
                FacebookCredentials.FACEBOOK_ACCESS_TOKEN.name: auth[
                    api_c.FACEBOOK_ACCESS_TOKEN
                ],
                FacebookCredentials.FACEBOOK_APP_SECRET.name: auth[
                    api_c.FACEBOOK_APP_SECRET
                ],
            },
        )

    def test_map_destination_credentials_sfmc(self):
        """Test mapping of destination credentials for submitting to AWS Batch.

        Args:

        Returns:

        """

        # setup destination object with synthetic credentials.
        sample_auth = "sample_auth"
        destination = {
            api_c.DESTINATION_ID: ObjectId(),
            api_c.DESTINATION_NAME: "SFMC",
            api_c.DELIVERY_PLATFORM_TYPE: "SFMC",
            api_c.AUTHENTICATION_DETAILS: {
                api_c.SFMC_CLIENT_ID: sample_auth,
                api_c.SFMC_AUTH_BASE_URI: sample_auth,
                api_c.SFMC_ACCOUNT_ID: sample_auth,
                api_c.SFMC_CLIENT_SECRET: sample_auth,
                api_c.SFMC_SOAP_BASE_URI: sample_auth,
                api_c.SFMC_REST_BASE_URI: sample_auth,
            },
        }

        with mock.patch.object(
            parameter_store,
            "get_store_value",
            return_value="sample_auth",
        ):
            env_dict, secret_dict = map_destination_credentials_to_dict(
                destination
            )

        # ensure mapping.
        auth = destination[api_c.AUTHENTICATION_DETAILS]
        # TODO HUS-582 work with ORCH so we dont' have to send creds in env_dict
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
        """Test get audience/destination pairs

        Args:

        Returns:

        """

        delivery_route = get_audience_destination_pairs(
            self.engagement[c.AUDIENCES]
        )

        self.assertTrue(delivery_route)
        self.assertEqual(len(delivery_route), 2)

    def test_get_delivery_route_audience(self):
        """Test get delivery route with specific audience

        Args:

        Returns:

        """

        engagement = self.engagement.copy()
        engagement[c.AUDIENCES] = [engagement[c.AUDIENCES][0]]

        delivery_route = get_audience_destination_pairs(
            engagement[c.AUDIENCES]
        )

        self.assertTrue(delivery_route)

        expected_route = [
            [self.audience_one[c.ID], self.audience_one[c.DESTINATIONS][0]]
        ]

        self.assertListEqual(expected_route, delivery_route)

    def test_destination_batch_init(self):
        """Test destination batch init

        Args:

        Returns:

        """
        delivery_route = get_audience_destination_pairs(
            self.engagement[c.AUDIENCES]
        )
        self.assertTrue(delivery_route)

        for pair in delivery_route:
            with mock.patch.object(
                parameter_store,
                "get_store_value",
                return_value="demo_store_value",
            ):
                batch_destination = get_destination_config(
                    self.database, *pair
                )
            self.assertIsNotNone(batch_destination.aws_envs)
            self.assertIsNotNone(batch_destination.aws_secrets)
            self.assertIsNotNone(batch_destination.audience_delivery_job_id)
            self.assertEqual(self.database, batch_destination.database)

            # validate the audience delivery job id exists
            audience_delivery_status = get_delivery_job_status(
                self.database, batch_destination.audience_delivery_job_id
            )
            self.assertEqual(audience_delivery_status, c.STATUS_PENDING)

    def test_destination_register_job(self):
        """Test destination batch register job

        Args:

        Returns:

        """
        delivery_route = get_audience_destination_pairs(
            self.engagement[c.AUDIENCES]
        )
        self.assertTrue(delivery_route)

        # walk the delivery route
        for pair in delivery_route:
            with mock.patch.object(
                parameter_store,
                "get_store_value",
                return_value="demo_store_value",
            ):
                batch_destination = get_destination_config(
                    self.database, *pair
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

            self.assertEqual(batch_destination.result, c.STATUS_PENDING)

    def test_destination_submit_job(self):
        """Test destination batch submit job

        Args:

        Returns:

        """
        delivery_route = get_audience_destination_pairs(
            self.engagement[c.AUDIENCES]
        )
        self.assertTrue(delivery_route)

        # walk the delivery route
        for pair in delivery_route:
            with mock.patch.object(
                parameter_store,
                "get_store_value",
                return_value="demo_store_value",
            ):
                batch_destination = get_destination_config(
                    self.database, *pair
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
            self.assertEqual(batch_destination.result, c.STATUS_PENDING)

            with mock.patch.object(
                AWSBatchConnector, "submit_job", return_value=return_value
            ):
                batch_destination.submit()

            self.assertEqual(batch_destination.result, c.STATUS_IN_PROGRESS)

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

        Returns:

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
            bad_list (dict): hypothesis list of random data.

        Returns:

        """
        with self.assertRaises(TypeError):
            get_audience_destination_pairs(bad_list)
