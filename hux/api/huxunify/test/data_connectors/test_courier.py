"""
purpose of this file is to house all the courier tests.
"""
from http import HTTPStatus
from unittest import TestCase, mock
import mongomock
from bson import ObjectId
from hypothesis import given, strategies as st
import requests_mock
import boto3
from botocore.stub import Stubber

import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.delivery_platform_management import (
    set_delivery_platform,
    get_delivery_job_status,
    get_delivery_platform,
    set_connection_status,
)
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
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.aws import (
    parameter_store,
    get_auth_from_parameter_store,
    set_cloud_watch_rule,
    put_rule_targets_aws_batch,
)
from huxunify.api.data_connectors.courier import (
    map_destination_credentials_to_dict,
    get_destination_config,
    get_audience_destination_pairs,
)
from huxunify.api.config import get_config
from huxunify.test import constants as t_c


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
        for destination in [
            (c.DELIVERY_PLATFORM_FACEBOOK, self.auth_details_facebook)
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
            api_c.DESTINATION_NAME: c.DELIVERY_PLATFORM_FACEBOOK,
            api_c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_FACEBOOK,
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
        """Test mapping of destination credentials for submitting to AWS Batch.

        Args:

        Returns:

        """

        # setup destination object with synthetic credentials.
        sample_auth = "sample_auth"
        destination = {
            api_c.DESTINATION_ID: ObjectId(),
            api_c.DESTINATION_NAME: c.DELIVERY_PLATFORM_SFMC,
            api_c.DELIVERY_PLATFORM_TYPE: c.DELIVERY_PLATFORM_SFMC,
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

    def test_get_pairs_invalid_dest(self):
        """Test get audience/destination pairs

        Args:

        Returns:

        """

        # take the first engagement audience and set an invalid audience destination
        invalid_engagement = self.engagement[c.AUDIENCES]
        invalid_engagement[0][api_c.DESTINATIONS] = "invalid_data"

        # now test getting the delivery route, which should yield one destination pair.
        delivery_route = get_audience_destination_pairs(invalid_engagement)

        self.assertTrue(delivery_route)

        # test for a list length of one. the invalid data is removed from the return.
        self.assertEqual(len(delivery_route), 1)

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
            [
                self.audience_one[c.ID],
                {c.OBJECT_ID: self.audience_one[c.DESTINATIONS][0]},
            ]
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

        request_mocker = requests_mock.Mocker()
        request_mocker.post(
            f"{t_c.TEST_CONFIG.CDP_SERVICE}/customer-profiles/insights",
            json=t_c.CUSTOMER_INSIGHT_RESPONSE,
        )
        request_mocker.start()

        for pair in delivery_route:
            with mock.patch.object(
                parameter_store,
                "get_store_value",
                return_value="demo_store_value",
            ):
                batch_destination = get_destination_config(
                    self.database, self.engagement[c.ID], *pair
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
                    self.database, self.engagement[c.ID], *pair
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
                batch_destination.register(self.engagement)

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
                    self.database, self.engagement[c.ID], *pair
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
                batch_destination.register(self.engagement)
            self.assertEqual(batch_destination.result, c.STATUS_PENDING)

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

    def test_get_auth_from_parameter_store(self):
        """Test function get_auth_from_parameter_store

        Args:

        Returns:

        """

        # use audience once
        for destination_id in self.audience_one[c.DESTINATIONS]:
            # get destination
            destination = get_delivery_platform(self.database, destination_id)

            # setup mocks for each secret
            simulated_secret = (
                f"simulated_secret_{destination[c.DELIVERY_PLATFORM_TYPE]}"
            )
            for _ in api_c.DESTINATION_SECRETS[
                destination[c.DELIVERY_PLATFORM_TYPE]
            ]:
                mock.patch.object(
                    parameter_store,
                    "get_store_value",
                    return_value=simulated_secret,
                ).start()

            # run the function
            auth = get_auth_from_parameter_store(
                destination[c.DELIVERY_PLATFORM_AUTH],
                destination[c.DELIVERY_PLATFORM_TYPE],
            )

            # test that the secrets were set to the simulated secret
            for secret in api_c.DESTINATION_SECRETS[
                destination[c.DELIVERY_PLATFORM_TYPE]
            ][api_c.AWS_SSM_NAME]:
                self.assertEqual(auth[secret.upper()], simulated_secret)

    @mock.patch("huxunify.api.data_connectors.aws.get_aws_client")
    def test_create_cloud_watch_rule(self, mock_boto_client: mock.MagicMock):
        """Test function create_cloud_watch_rule
        Args:
            mock_boto_client (mock.MagicMock): mock boto client.
        Returns:
        """

        # use audience once
        for destination_id in self.audience_one[c.DESTINATIONS]:

            # get destination
            destination = get_delivery_platform(self.database, destination_id)

            # create the rule name
            cw_name = f"{self.engagement[c.ID]}-{destination[c.DELIVERY_PLATFORM_TYPE]}"

            # put params
            put_rule_params = {
                "Name": cw_name,
                "ScheduleExpression": "cron(15 0 * * ? *)",
                "Description": "",
                "State": api_c.ENABLED.upper(),
                "RoleArn": "fake_arn",
            }

            put_rule_response = {
                "RuleArn": "test-result-rulearn",
                "ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value},
            }

            # simulate the event return rule
            client = boto3.client(
                api_c.AWS_EVENTS_NAME, get_config().AWS_REGION
            )
            stub_client = Stubber(client)
            stub_client.add_response(
                "put_rule", put_rule_response, put_rule_params
            )
            stub_client.activate()

            mock_boto_client.return_value = client

            result = set_cloud_watch_rule(
                cw_name, "cron(15 0 * * ? *)", "fake_arn"
            )

            # test mocked client result
            self.assertEqual(result, put_rule_response["RuleArn"])

    @mock.patch("huxunify.api.data_connectors.aws.get_aws_client")
    def test_create_cloud_watch_rule_fail(
        self, mock_boto_client: mock.MagicMock
    ):
        """Test function create_cloud_watch_rule failure.
        Args:
            mock_boto_client (mock.MagicMock): mock boto client.
        Returns:
        """

        # use audience once
        for destination_id in self.audience_one[c.DESTINATIONS]:
            # get destination
            destination = get_delivery_platform(self.database, destination_id)

            # create the rule name
            cw_name = f"{self.engagement[c.ID]}-{destination[c.DELIVERY_PLATFORM_TYPE]}"

            # put params
            put_rule_params = {
                "Name": cw_name,
                "ScheduleExpression": "cron(15 0 * * ? *)",
                "Description": "",
                "State": api_c.ENABLED.upper(),
                "RoleArn": "fake_arn",
            }

            put_rule_response = {
                "RuleArn": "test-result-rulearn",
                "ResponseMetadata": {
                    "HTTPStatusCode": HTTPStatus.BAD_REQUEST.value
                },
            }

            # simulate the event return rule
            client = boto3.client(
                api_c.AWS_EVENTS_NAME, get_config().AWS_REGION
            )
            stub_client = Stubber(client)
            stub_client.add_response(
                "put_rule", put_rule_response, put_rule_params
            )
            stub_client.activate()

            mock_boto_client.return_value = client

            result = set_cloud_watch_rule(
                cw_name, "cron(15 0 * * ? *)", "fake_arn"
            )

            # test mocked client result
            self.assertIsNone(result)

    @mock.patch("huxunify.api.data_connectors.aws.get_aws_client")
    def test_put_targets(self, mock_boto_client: mock.MagicMock):
        """Test function put_targets.
        Args:
            mock_boto_client (mock.MagicMock): mock boto client.
        Returns:
        """

        # get destination
        destination = get_delivery_platform(
            self.database, self.audience_one[c.DESTINATIONS][0]
        )

        # create the rule name
        cw_name = (
            f"{self.engagement[c.ID]}-{destination[c.DELIVERY_PLATFORM_TYPE]}"
        )

        batch_params = {
            "JobDefinition": "sample_job_def",
            "JobName": "sample_job_name",
        }

        # put params
        put_targets_params = {
            "Rule": cw_name,
            "Targets": [
                {
                    "Id": cw_name,
                    "Arn": "fake_arn",
                    "RoleArn": "fake_role_arn",
                    "BatchParameters": batch_params,
                }
            ],
        }

        put_targets_response = {
            "FailedEntryCount": 0,
            "FailedEntries": [
                {
                    "TargetId": cw_name,
                    "ErrorCode": "test-pass",
                    "ErrorMessage": "",
                },
            ],
            "ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value},
        }

        # simulate the event return rule
        client = boto3.client(api_c.AWS_EVENTS_NAME, get_config().AWS_REGION)
        stub_client = Stubber(client)
        stub_client.add_response(
            "put_targets", put_targets_response, put_targets_params
        )
        stub_client.activate()

        mock_boto_client.return_value = client

        result = put_rule_targets_aws_batch(
            cw_name, batch_params, "fake_arn", "fake_role_arn"
        )

        # test mocked client result
        self.assertEqual(result, 0)

    @mock.patch("huxunify.api.data_connectors.aws.get_aws_client")
    def test_put_targets_failure(self, mock_boto_client: mock.MagicMock):
        """Test function put_targets failure.
        Args:
            mock_boto_client (mock.MagicMock): mock boto client.
        Returns:
        """

        # get destination
        destination = get_delivery_platform(
            self.database, self.audience_one[c.DESTINATIONS][0]
        )

        # create the rule name
        cw_name = (
            f"{self.engagement[c.ID]}-{destination[c.DELIVERY_PLATFORM_TYPE]}"
        )

        batch_params = {
            "JobDefinition": "sample_job_def",
            "JobName": "sample_job_name",
        }

        # put params
        put_targets_params = {
            "Rule": cw_name,
            "Targets": [
                {
                    "Id": cw_name,
                    "Arn": "fake_arn",
                    "RoleArn": "fake_role_arn",
                    "BatchParameters": batch_params,
                }
            ],
        }

        put_targets_response = {
            "FailedEntryCount": 1,
            "FailedEntries": [
                {
                    "TargetId": cw_name,
                    "ErrorCode": "test-pass",
                    "ErrorMessage": "",
                },
            ],
            "ResponseMetadata": {
                "HTTPStatusCode": HTTPStatus.BAD_REQUEST.value
            },
        }

        # simulate the event return rule
        client = boto3.client(api_c.AWS_EVENTS_NAME, get_config().AWS_REGION)
        stub_client = Stubber(client)
        stub_client.add_response(
            "put_targets", put_targets_response, put_targets_params
        )
        stub_client.activate()

        mock_boto_client.return_value = client

        result = put_rule_targets_aws_batch(
            cw_name, batch_params, "fake_arn", "fake_role_arn"
        )

        # test mocked client result
        self.assertIsNone(result)
