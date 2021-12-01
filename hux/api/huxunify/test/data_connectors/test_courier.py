"""Purpose of this file is to house all the courier tests."""
from http import HTTPStatus
from unittest import TestCase, mock
import mongomock
from bson import ObjectId
from hypothesis import given, strategies as st
import requests_mock
import boto3
from botocore.stub import Stubber

import huxunifylib.database.constants as db_c
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
    toggle_cloud_watch_rule,
    CloudWatchState,
)
from huxunify.api.data_connectors.courier import (
    map_destination_credentials_to_dict,
    get_okta_test_user_creds,
    get_destination_config,
    get_audience_destination_pairs,
    toggle_event_driven_routers,
)
from huxunify.api.config import get_config
from huxunify.test import constants as t_c


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

        destination_ids = [d[db_c.ID] for d in destinations]

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
            db_c.CREATED_BY: ObjectId(),
        }

        # insert engagement doc in the collection
        engagement_id = set_engagement(
            self.database,
            engagement_doc[db_c.AUDIENCE_NAME],
            engagement_doc[db_c.NOTIFICATION_FIELD_DESCRIPTION],
            engagement_doc[db_c.AUDIENCES],
            engagement_doc[db_c.CREATED_BY],
        )

        self.assertIsInstance(engagement_id, ObjectId)
        self.engagement = get_engagement(self.database, engagement_id)
        self.assertTrue(self.engagement)

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
            with mock.patch.object(
                parameter_store,
                "get_store_value",
                return_value="demo_store_value",
            ):
                batch_destination = get_destination_config(
                    self.database, self.engagement[db_c.ID], *pair
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
            with mock.patch.object(
                parameter_store,
                "get_store_value",
                return_value="demo_store_value",
            ):
                batch_destination = get_destination_config(
                    self.database, self.engagement[db_c.ID], *pair
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
            with mock.patch.object(
                parameter_store,
                "get_store_value",
                return_value="demo_store_value",
            ):
                batch_destination = get_destination_config(
                    self.database, self.engagement[db_c.ID], *pair
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
                mock.patch.object(
                    parameter_store,
                    "get_store_value",
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

    @mock.patch("huxunify.api.data_connectors.aws.get_aws_client")
    def test_create_cloud_watch_rule(self, mock_boto_client: mock.MagicMock):
        """Test function create_cloud_watch_rule

        Args:
            mock_boto_client (mock.MagicMock): mock boto client.
        """

        # use audience once
        for destination_id in self.audience_one[db_c.DESTINATIONS]:

            # get destination
            destination = get_delivery_platform(self.database, destination_id)

            # create the rule name
            cw_name = f"{self.engagement[db_c.ID]}-{destination[db_c.DELIVERY_PLATFORM_TYPE]}"

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
        """

        # use audience once
        for destination_id in self.audience_one[db_c.DESTINATIONS]:
            # get destination
            destination = get_delivery_platform(self.database, destination_id)

            # create the rule name
            cw_name = f"{self.engagement[db_c.ID]}-{destination[db_c.DELIVERY_PLATFORM_TYPE]}"

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
        """

        # get destination
        destination = get_delivery_platform(
            self.database, self.audience_one[db_c.DESTINATIONS][0]
        )

        # create the rule name
        cw_name = f"{self.engagement[db_c.ID]}-{destination[db_c.DELIVERY_PLATFORM_TYPE]}"

        batch_params = {
            "JobDefinition": "sample_job_def",
            "JobName": "sample_job_name",
        }

        sample_delivery_job_id = ObjectId()

        # put params
        put_targets_params = {
            "Rule": cw_name,
            "Targets": [
                {
                    api_c.AWS_TARGET_ID: str(sample_delivery_job_id),
                    api_c.AWS_TARGET_ARN: "fake_job_queue",
                    api_c.AWS_TARGET_ROLE_ARN: "fake_role_arn",
                    api_c.AWS_TARGET_BATCH_PARAMS: batch_params,
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
            cw_name,
            batch_params,
            sample_delivery_job_id,
            "fake_role_arn",
            "fake_job_queue",
        )

        # test mocked client result
        self.assertEqual(result, 0)

    @mock.patch("huxunify.api.data_connectors.aws.get_aws_client")
    def test_put_targets_failure(self, mock_boto_client: mock.MagicMock):
        """Test function put_targets failure.

        Args:
            mock_boto_client (mock.MagicMock): mock boto client.
        """

        # get destination
        destination = get_delivery_platform(
            self.database, self.audience_one[db_c.DESTINATIONS][0]
        )

        # create the rule name
        cw_name = f"{self.engagement[db_c.ID]}-{destination[db_c.DELIVERY_PLATFORM_TYPE]}"

        batch_params = {
            "JobDefinition": "sample_job_def",
            "JobName": "sample_job_name",
        }

        sample_delivery_job_id = ObjectId()

        # put params
        put_targets_params = {
            "Rule": cw_name,
            "Targets": [
                {
                    api_c.AWS_TARGET_ID: str(sample_delivery_job_id),
                    api_c.AWS_TARGET_ARN: "fake_job_queue",
                    api_c.AWS_TARGET_ROLE_ARN: "fake_role_arn",
                    api_c.AWS_TARGET_BATCH_PARAMS: batch_params,
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
            cw_name,
            batch_params,
            sample_delivery_job_id,
            "fake_role_arn",
            "fake_job_queue",
        )

        # test mocked client result
        self.assertIsNone(result)

    @mock.patch("huxunify.api.data_connectors.aws.get_aws_client")
    def test_toggle_cloud_watch_rule(self, mock_boto_client: mock.MagicMock):
        """Test function toggle_cloud_watch_rule

        Args:
            mock_boto_client (mock.MagicMock): mock boto client.
        """

        rule_params = {"Name": "fake-rule"}
        rule_response = {
            "ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value},
        }

        # simulate the event return rule
        client = boto3.client(api_c.AWS_EVENTS_NAME, get_config().AWS_REGION)

        stub_client = Stubber(client)
        stub_client.add_response(
            CloudWatchState.ENABLE.value, rule_response, rule_params
        )
        stub_client.activate()
        mock_boto_client.return_value = client

        self.assertTrue(
            toggle_cloud_watch_rule(
                rule_params["Name"], CloudWatchState.ENABLE
            )
        )

    @mock.patch("huxunify.api.data_connectors.aws.get_aws_client")
    def test_toggle_cloud_watch_rule_disable(
        self, mock_boto_client: mock.MagicMock
    ):
        """Test function toggle_cloud_watch_rule disabled.

        Args:
            mock_boto_client (mock.MagicMock): mock boto client.
        """

        rule_params = {"Name": "fake-rule"}
        rule_response = {
            "ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value},
        }

        # simulate the event return rule
        client = boto3.client(api_c.AWS_EVENTS_NAME, get_config().AWS_REGION)

        stub_client = Stubber(client)
        stub_client.add_response(
            CloudWatchState.DISABLE.value, rule_response, rule_params
        )
        stub_client.activate()
        mock_boto_client.return_value = client

        self.assertTrue(
            toggle_cloud_watch_rule(
                rule_params["Name"], CloudWatchState.DISABLE
            )
        )

    @mock.patch("huxunify.api.data_connectors.aws.get_aws_client")
    def test_toggle_event_driven_routers(
        self, mock_boto_client: mock.MagicMock
    ):
        """Test function toggle_event_driven_routers.

        Args:
            mock_boto_client (mock.MagicMock): mock boto client.
        """

        rule_params = {"Name": "fake-rule"}
        rule_response = {
            "ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value},
        }

        # simulate the event return rule
        client = boto3.client(api_c.AWS_EVENTS_NAME, get_config().AWS_REGION)

        stub_client = Stubber(client)
        stub_client.add_response(
            CloudWatchState.ENABLE.value, rule_response, rule_params
        )
        stub_client.activate()
        mock_boto_client.return_value = client

        self.assertIsNone(toggle_event_driven_routers(self.database))
