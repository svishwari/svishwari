"""Purpose of this file is to house all cloud connector unit tests."""
from unittest import TestCase, mock

from huxunify.api.data_connectors.cloud.cloud_client import CloudClient
from huxunify.api.data_connectors.cloud import AzureClient, AWSClient
from huxunify.api.config import get_config


class CloudClientTests(TestCase):
    """Test Cloud Client Methods."""

    def test_no_provider_mapping(self) -> None:
        """Test when no provider is mapped."""
        self.assertIsInstance(CloudClient(), CloudClient)

    def test_aws_provider_mapping(self) -> None:
        """Test when aws provider is set."""
        config = get_config()
        config.CLOUD_PROVIDER = "aws"

        with mock.patch("huxunify.api.config.get_config", return_value=config):
            self.assertIsInstance(CloudClient(), AWSClient)

    def test_azure_provider_mapping(self) -> None:
        """Test when azure provider is set."""
        config = get_config()
        config.CLOUD_PROVIDER = "azure"

        with mock.patch("huxunify.api.config.get_config", return_value=config):
            self.assertIsInstance(CloudClient(), AzureClient)
