"""Purpose of this module is to host all AzureClient tests."""
from unittest import TestCase, mock

from huxunify.api.config import get_config
from huxunify.api.data_connectors.cloud.cloud_client import CloudClient


class AzureClientTests(TestCase):
    """Test AzureClient methods."""

    def setUp(self) -> None:
        """setup for test methods"""
        config = get_config()
        config.CLOUD_PROVIDER = "azure"

        self.azure_client = CloudClient()

    def tearDown(self) -> None:
        """Destroys resources after each test."""
        mock.patch.stopall()

    def test_get_secret(self):
        """Test get secret."""
        pass

    def test_get_secret_failure(self):
        """Test get secret failure."""
        pass

    def test_set_secret(self):
        """Test set secret."""
        pass

    def test_set_secret_failure(self):
        """Test set secret failure."""
        pass

    def test_upload_file(self):
        """Test upload file."""
        # TODO HUS-2615
        pass

    def test_download_file(self):
        """Test download file."""
        # TODO HUS-2615
        pass

    def test_health_check_batch_service(self):
        """Test health check for batch service."""
        # TODO HUS-2614
        pass

    def test_health_check_batch_service_failure(self):
        """Test health check batch service when service is down."""
        # TODO HUS-2614
        pass

    def test_health_check_storage_service(self):
        """Test health check for storage service."""
        # TODO HUS-2614
        pass

    def test_health_check_storage_service_failure(self):
        """Test health check for storage service when service is down."""
        # TODO HUS-2614
        pass

    def test_health_check_secret_storage(self):
        """Test health check for secret storage."""
        # TODO HUS-2614
        pass

    def test_health_check_secret_storage_failure(self):
        """Test health check for secret storage when service is down."""
        # TODO HUS-2614
        pass