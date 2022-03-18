"""Purpose of this file is to house all aws unit tests."""
from unittest import TestCase, mock

import boto3
from moto import mock_ssm

from huxunify.api.config import get_config
from huxunify.api.data_connectors.aws import (
    check_aws_ssm,
    check_aws_batch,
    check_aws_s3,
    check_aws_events,
    get_auth_from_parameter_store,
    check_aws_connection,
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
