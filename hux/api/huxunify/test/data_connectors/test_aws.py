"""Purpose of this file is to house all aws unit tests."""
import string
from unittest import TestCase, mock

import tempfile

import boto3
from botocore.exceptions import ClientError
from bson import ObjectId
from hypothesis import given, strategies as st, settings
from moto import mock_s3, mock_ssm, mock_events

from huxunify.api.config import get_config
from huxunify.api.data_connectors.aws import (
    upload_file,
    download_file,
    check_aws_ssm,
    check_aws_batch,
    check_aws_s3,
    check_aws_events,
    get_auth_from_parameter_store,
    set_cloud_watch_rule,
    put_rule_targets_aws_batch,
    check_aws_connection,
    CloudWatchState,
    toggle_cloud_watch_rule,
)
from huxunify.api import constants as api_c

# pylint: disable=too-many-public-methods
class AWSTest(TestCase):
    """Test AWS Methods."""

    def setUp(self) -> None:
        """Setup tests."""

        self.config = get_config()
        self.s3_client = boto3.client(
            api_c.AWS_S3_NAME,
            region_name="us-east-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )

    def tearDown(self) -> None:
        """Destroys resources after each test."""
        mock.patch.stopall()

    def test_check_aws_connection_failure(self) -> None:
        """Test check aws connection raises exception."""
        input_dict = {
            "client_method": "TestMethod",
            "extra_params": {},
            "client": "dummy_client",
        }

        mock.patch(
            "huxunify.api.data_connectors.aws.get_aws_client",
            side_effect=Exception(),
        )
        status, _ = check_aws_connection(**input_dict)
        self.assertFalse(status)

    @mock_ssm()
    def test_check_aws_connection_success(self) -> None:
        """Test check aws connection success."""
        input_dict = {
            "client_method": "get_parameter",
            "extra_params": {"Name": "unified_host_alias"},
            "client": "ssm",
        }

        aws_client = boto3.client(
            api_c.AWS_SSM_NAME,
            region_name="us-east-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )

        aws_client.put_parameter(
            Name="unified_host_alias",
            Value="fake_host_alias",
            Type="SecureString",
            Overwrite=True,
        )

        mock.patch(
            "huxunify.api.data_connectors.aws.get_aws_client",
            return_value=aws_client,
        ).start()

        status, message = check_aws_connection(**input_dict)
        self.assertTrue(status)
        self.assertEqual(f"{api_c.AWS_SSM_NAME} available.", message)

    def test_check_aws_ssm(self) -> None:
        """Test AWS SSM health check function"""
        mock.patch(
            "huxunify.api.data_connectors.aws.check_aws_connection",
            return_value=(True, "AWS SSM Connected."),
        ).start()

        status, message = check_aws_ssm()
        self.assertTrue(status)
        self.assertEqual("AWS SSM Connected.", message)

    def test_check_aws_batch(self) -> None:
        """Test AWS Batch health check function"""
        mock.patch(
            "huxunify.api.data_connectors.aws.check_aws_connection",
            return_value=(True, "AWS Batch Connected."),
        ).start()

        status, message = check_aws_batch()
        self.assertTrue(status)
        self.assertEqual("AWS Batch Connected.", message)

    def test_check_aws_s3(self) -> None:
        """Test AWS S3 health check function"""
        mock.patch(
            "huxunify.api.data_connectors.aws.check_aws_connection",
            return_value=(True, "AWS S3 Connected."),
        ).start()

        status, message = check_aws_s3()
        self.assertTrue(status)
        self.assertEqual("AWS S3 Connected.", message)

    def test_check_aws_events(self) -> None:
        """Test AWS Events health check function"""
        mock.patch(
            "huxunify.api.data_connectors.aws.check_aws_connection",
            return_value=(True, "AWS Events Connected."),
        ).start()

        status, message = check_aws_events()
        self.assertTrue(status)
        self.assertEqual("AWS Events Connected.", message)

    def test_get_auth_from_param_store_key_error(self) -> None:
        """Test get auth from param store key error."""
        destination_type = "Unknown"
        auth_dict = {}

        with self.assertRaises(KeyError):
            get_auth_from_parameter_store(auth_dict, destination_type)

    def test_set_cloudwatch_rule_invalid_state(self) -> None:
        """Test set cloudwatch rule with invalid state."""
        rule = {
            "rule_name": "TestRule",
            "schedule_expression": "",
            "role_arn": "dummy_arn",
            "description": "cloud watch rule",
            "state": api_c.STATUS_INACTIVE,
        }

        with self.assertRaises(ValueError):
            set_cloud_watch_rule(**rule)

    def test_set_cloudwatch_rule_invalid_name(self) -> None:
        """Test set cloudwatch rule with invalid name."""
        rule = {
            "rule_name": "Test Rule",
            "schedule_expression": "",
            "role_arn": "dummy_arn",
            "description": "cloud watch rule",
            "state": api_c.ENABLED,
        }

        with self.assertRaises(ValueError):
            set_cloud_watch_rule(**rule)

    def test_set_cloudwatch_rule_exception(self) -> None:
        """Test set cloudwatch rule raises exception."""
        rule = {
            "rule_name": "TestRule",
            "schedule_expression": "",
            "role_arn": "dummy_arn",
            "description": "cloud watch rule",
            "state": api_c.ENABLED,
        }

        mock.patch(
            "huxunify.api.data_connectors.aws.get_aws_client",
            side_effect=Exception(),
        )
        self.assertIsNone(set_cloud_watch_rule(**rule))

    def test_put_rule_targets_aws_batch(self) -> None:
        """Test put rule targets aws batch raises exception."""
        rule = {
            "rule_name": "TestRule",
            "batch_params": {},
            "delivery_job_id": ObjectId(),
            "role_arn": "dummy_arn",
            "job_queue": "TestQueue",
        }

        mock.patch(
            "huxunify.api.data_connectors.aws.get_aws_client",
            side_effect=Exception(),
        )
        self.assertIsNone(put_rule_targets_aws_batch(**rule))

    @mock_s3
    @given(
        user_name=st.text(alphabet=string.ascii_letters),
        file_type=st.text(alphabet=string.ascii_letters),
    )
    @settings(deadline=600)
    def test_upload_file(self, user_name: str, file_type: str):
        """Test upload of file to mocked S3 dataset bucket.

        Args:
            user_name (str): Value for User name.
            file_type (str): Type of File.
        """

        if not user_name:
            return

        if not file_type:
            return

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            self.s3_client.create_bucket(Bucket=self.config.S3_DATASET_BUCKET)

            self.assertTrue(
                upload_file(
                    temp_file.name,
                    self.config.S3_DATASET_BUCKET,
                    user_name=user_name,
                    file_type=file_type,
                )
            )

    @mock_s3
    @given(
        user_name=st.text(alphabet=string.ascii_letters),
        file_type=st.text(alphabet=string.ascii_letters),
    )
    @settings(deadline=600)
    def test_upload_file_with_object_name(
        self, user_name: str, file_type: str
    ):
        """Test upload of file to mocked S3 dataset bucket with specified object_name.

        Args:
            user_name (str): Value for User name.
            file_type (str): Type of File.
        """

        if not user_name:
            return

        if not file_type:
            return

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            self.s3_client.create_bucket(Bucket=self.config.S3_DATASET_BUCKET)

            self.assertTrue(
                upload_file(
                    temp_file.name,
                    self.config.S3_DATASET_BUCKET,
                    object_name="Test Object",
                    user_name=user_name,
                    file_type=file_type,
                )
            )

    @mock_s3
    @given(
        user_name=st.text(alphabet=string.ascii_letters),
        file_type=st.text(alphabet=string.ascii_letters),
    )
    @settings(deadline=600)
    def test_upload_file_exception(self, user_name: str, file_type: str):
        """Test upload of file to mocked S3 dataset bucket exception.

        Args:
            user_name (str): Value for User name.
            file_type (str): Type of File.
        """

        if not user_name:
            return

        if not file_type:
            return

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            self.s3_client.create_bucket(Bucket=self.config.S3_DATASET_BUCKET)

            mock.patch(
                "huxunify.api.data_connectors.aws.get_aws_client",
                side_effect=ClientError({}, "upload"),
            ).start()

            self.assertFalse(
                upload_file(
                    temp_file.name,
                    self.config.S3_DATASET_BUCKET,
                    user_name=user_name,
                    file_type=file_type,
                )
            )

    @mock_s3
    def test_download_file(self):
        """Test download of file to mocked S3 dataset bucket."""

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            self.s3_client.create_bucket(Bucket=self.config.S3_DATASET_BUCKET)
            self.s3_client.put_object(
                Bucket=self.config.S3_DATASET_BUCKET,
                Key=temp_file.name,
                Body="",
            )

            self.assertTrue(
                download_file(self.config.S3_DATASET_BUCKET, temp_file.name)
            )

    @mock_s3
    def test_download_file_failure(self):
        """Test download of file to mocked S3 dataset bucket failure."""

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            self.s3_client.create_bucket(Bucket=self.config.S3_DATASET_BUCKET)
            self.s3_client.put_object(
                Bucket=self.config.S3_DATASET_BUCKET,
                Key=temp_file.name,
                Body="",
            )

            mock.patch(
                "huxunify.api.data_connectors.aws.get_aws_client",
                side_effect=ClientError({}, "download"),
            ).start()
            self.assertFalse(
                download_file(self.config.S3_DATASET_BUCKET, temp_file.name)
            )

    @mock_events()
    def test_toggle_cloud_watch_rule_success(self):
        """Test toggling cloudwatch rule."""
        input_dict = {
            "rule_name": "test_rule",
            "state": CloudWatchState.DISABLE,
            "ignore_existence": True,
        }

        events_client = boto3.client(
            api_c.AWS_EVENTS_NAME,
            region_name="us-east-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )

        events_client.put_rule(
            Name=input_dict["rule_name"],
            ScheduleExpression="cron(15 0 * * ? *)",
            State="ENABLE",
            Description="testing cloudwatch rules",
            RoleArn="fake_arn",
        )

        mock.patch(
            "huxunify.api.data_connectors.aws.get_aws_client",
            return_value=events_client,
        ).start()

        self.assertTrue(toggle_cloud_watch_rule(**input_dict))

    @mock_events()
    def test_toggle_cloud_watch_rule_resource_not_found(self):
        """Test toggling cloudwatch rule resulting in resource not found error."""
        input_dict = {
            "rule_name": "test_rule",
            "state": CloudWatchState.DISABLE,
            "ignore_existence": True,
        }

        events_client = boto3.client(
            api_c.AWS_EVENTS_NAME,
            region_name="us-east-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )

        mock.patch(
            "huxunify.api.data_connectors.aws.get_aws_client",
            return_value=events_client,
        ).start()

        self.assertFalse(toggle_cloud_watch_rule(**input_dict))

    @mock_events()
    def test_toggle_cloud_watch_rule_resource_not_found_raise_error(self):
        """Test toggling cloudwatch rule resulting in resource not found
        error which raises error."""
        input_dict = {
            "rule_name": "test_rule",
            "state": CloudWatchState.DISABLE,
            "ignore_existence": False,
        }

        events_client = boto3.client(
            api_c.AWS_EVENTS_NAME,
            region_name="us-east-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )

        mock.patch(
            "huxunify.api.data_connectors.aws.get_aws_client",
            return_value=events_client,
        ).start()

        with self.assertRaises(ClientError):
            toggle_cloud_watch_rule(**input_dict)

    @mock_events()
    def test_toggle_cloud_watch_rule_exception(self):
        """Test toggling cloudwatch rule exception."""
        input_dict = {
            "rule_name": "test_rule",
            "state": CloudWatchState.DISABLE,
            "ignore_existence": False,
        }

        mock.patch(
            "huxunify.api.data_connectors.aws.get_aws_client",
            side_effect=Exception(),
        ).start()

        self.assertFalse(toggle_cloud_watch_rule(**input_dict))
