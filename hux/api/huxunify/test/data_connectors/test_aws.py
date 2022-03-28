"""Purpose of this file is to house all aws unit tests."""
from unittest import TestCase, mock
import boto3
from huxunify.api.config import get_config
from huxunify.api.data_connectors.aws import (
    get_auth_from_parameter_store,
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
