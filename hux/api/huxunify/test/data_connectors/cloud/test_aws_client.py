"""Purpose of this module is to host all AWSClient tests."""
from unittest import TestCase, mock

import boto3
from moto import mock_ssm, mock_s3, mock_batch

from huxunify.api.config import get_config
from huxunify.api.data_connectors.cloud.cloud_client import CloudClient


class AWSClientTests(TestCase):
    """Test AWSClient methods."""

    def setUp(self) -> None:
        """setup for test methods"""
        config = get_config()
        config.CLOUD_PROVIDER = "aws"
        config.AWS_REGION = "us-east-1"

        self.aws_client = CloudClient()
        self.ssm_client = boto3.client("ssm")
        self.s3_client = boto3.client("s3")

    def tearDown(self) -> None:
        """Destroys resources after each test."""
        mock.patch.stopall()

    @mock_ssm
    def test_get_secret(self):
        """Test get secret."""
        secret_key = "some_secret"
        secret_val = "MY SECRET"
        self.ssm_client.put_parameter(
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

    def test_upload_file(self):
        """Test upload file."""
        # TODO HUS-2615
        pass

    def test_download_file(self):
        """Test download file."""
        # TODO HUS-2615
        pass

    @mock_batch
    def test_health_check_batch_service(self):
        """Test health check for batch service."""
        status = self.aws_client.health_check_batch_service()
        self.assertTrue(status[0])
        self.assertEqual("S3 storage available.", status[1])

    @mock_s3
    def test_health_check_storage_service(self):
        """Test health check for storage service."""
        status = self.aws_client.health_check_storage_service()
        self.assertTrue(status[0])
        self.assertEqual("AWS S3 storage available.", status[1])
