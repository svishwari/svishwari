"""Purpose of this file is to house all aws unit tests."""
import string
from unittest import TestCase, mock

import tempfile

import boto3
from botocore.exceptions import ClientError
from hypothesis import given, strategies as st, settings
from moto import mock_s3

from huxunify.api.config import get_config
from huxunify.api.data_connectors.aws import (
    upload_file,
    download_file,
    get_auth_from_parameter_store,
    set_cloud_watch_rule,
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
