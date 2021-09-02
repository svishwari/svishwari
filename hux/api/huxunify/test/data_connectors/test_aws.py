"""
Purpose of this file is to house all aws unit tests
"""
import string
from unittest import TestCase

import tempfile

import boto3
from hypothesis import given, strategies as st, settings
from moto import mock_s3

from huxunify.api.config import get_config
from huxunify.api.data_connectors.aws import (
    upload_file,
    download_file,
)
from huxunify.api import constants as api_c


class AWSTest(TestCase):
    """
    Test AWS Methods
    """

    def setUp(self) -> None:
        """Setup tests

        Returns:

        """
        self.config = get_config()
        self.s3_client = boto3.client(
            api_c.S3,
            region_name="us-east-1",
            aws_access_key_id="fake_access_key",
            aws_secret_access_key="fake_secret_key",
        )

    @mock_s3
    @given(
        user_name=st.text(alphabet=string.ascii_letters),
        file_type=st.text(alphabet=string.ascii_letters),
    )
    @settings(deadline=600)
    def test_upload_file(self, user_name, file_type):
        """

        Returns:

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
    def test_download_file(self):
        """

        Returns:

        """

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
