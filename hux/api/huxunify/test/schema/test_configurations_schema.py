"""Purpose of this file is to test the configurations schemas."""
from unittest import TestCase
from datetime import datetime
from bson import ObjectId

from huxunifylib.database import constants as db_c
from huxunify.api.schema.configurations import ConfigurationsSchema
from huxunify.api.schema.orchestration import is_audience_lookalikeable
from huxunify.api import constants as api_c


class ConfigurationsSchemaTest(TestCase):
    """Test Configurations Schema Classes."""

    def test_notification_schema(self):
        """Test NotificationSchema."""

        doc = dict(
            _id=str(ObjectId()),
            name="Test configuration",
            type="module",
            status=db_c.STATUS_PENDING,
            description="Configuration.",
            enabled=True,
        )

        res = ConfigurationsSchema().dump(doc)

        self.assertEqual(
            res["name"], doc[db_c.NAME]
        )
