"""Purpose of this file is to test the configuration schemas."""
from unittest import TestCase
from bson import ObjectId

from huxunifylib.database import constants as db_c
from huxunify.api.schema.configurations import ConfigurationsSchema


class ConfigurationsSchemaTest(TestCase):
    """Test Configurations Schema Classes."""

    def test_configurations_schema(self):
        """Test ConfigurationsSchema."""

        doc = dict(
            _id=str(ObjectId()),
            name="Test configuration",
            type="module",
            status=db_c.STATUS_PENDING,
            description="Configuration.",
            enabled=True,
        )

        res = ConfigurationsSchema().dump(doc)

        self.assertEqual(res[db_c.NAME], doc[db_c.NAME])
