"""Purpose of this module is to host all AWSClient tests."""
from unittest import TestCase, mock

import boto3
from moto import mock_ssm, mock_s3

from huxunify.api.config import get_config
from huxunify.api.data_connectors.cloud.cloud_client import CloudClient


class AWSClientTests(TestCase):
    """Test AWSClient methods."""

    def setUp(self) -> None:
        """setup for test methods"""
        self.config = get_config()
        self.config.CLOUD_PROVIDER = "aws"
        self.config.AWS_REGION = "us-east-1"
        self.config.S3_DATASET_BUCKET = "S3_data_bucket"

        self.aws_client = CloudClient()

    def tearDown(self) -> None:
        """Destroys resources after each test."""
        mock.patch.stopall()

    @mock_ssm
    def test_get_secret(self):
        """Test get secret."""
        secret_key = "some_secret"
        secret_val = "MY SECRET"
        ssm_client = boto3.client("ssm")
        ssm_client.put_parameter(
            Name=secret_key,
            Value=secret_val,
            Type="SecureString",
            Overwrite=False,
        )
        self.assertEqual(secret_val, self.aws_client.get_secret(secret_key))

    @mock_ssm
    def test_set_secret(self):
        """Test set secret."""
        secret_key = "some_secret"
        secret_val = "MY SECRET"
        self.aws_client.set_secret(secret_key, secret_val)
        self.assertEqual(secret_val, self.aws_client.get_secret(secret_key))

    @mock_s3
    def test_health_check_storage_service(self):
        """Test health check for storage service."""
        # create a mock bucket
        s3_client = boto3.client("s3")
        s3_client.create_bucket(
            ACL="public-read-write", Bucket=self.config.S3_DATASET_BUCKET
        )

        # verify that a bucket exists
        status = self.aws_client.health_check_storage_service()
        self.assertTrue(status[0])
        self.assertEqual("s3 available.", status[1])

    @mock_ssm
    def test_health_check_secret_storage(self):
        """Test health check for secret storage service."""
        # create a mock parameter
        ssm_client = boto3.client("ssm")
        ssm_client.put_parameter(
            Name="unifieddb_host_alias",
            Value="host alias",
            Type="SecureString",
            Overwrite=False,
        )

        status = self.aws_client.health_check_secret_storage()
        self.assertTrue(status[0])
        self.assertEqual("ssm available.", status[1])
