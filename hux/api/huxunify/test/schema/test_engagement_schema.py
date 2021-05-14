"""
Purpose of this file is to test the engagement schemas
"""

from unittest import TestCase
import datetime
import json

from huxunify.api.schema.engagement import EngagementGetSchema
from huxunifylib.database import constants as db_c
from huxunify.api import constants as api_c


class EngagementSchemaTest(TestCase):

    def setUp(self) -> None:
        """ Setup function for engagement schema tests

        Args:

        Returns:

        """
        pass

    def test1(self) -> None:
        """

        """
        doc = {
            api_c.ENGAGEMENT_ID: "5f5f7262997acad4bac4373b",
            api_c.ENGAGEMENT_NAME: "Engagement 1",
            api_c.ENGAGEMENT_DESCRIPTION: "Engagement 1 description",
            api_c.ENGAGEMENT_AUDIENCES: [],
            api_c.ENGAGEMENT_STATUS: api_c.ENGAGEMENT_STATUS_ACTIVE,
            api_c.ENGAGEMENT_DELIVERY_SCHEDULE: {}
        }
        print(json.dumps(doc))

        val = EngagementGetSchema().validate(doc)
        val = EngagementGetSchema().load(doc)
        print(json.dumps(val))

        assert EngagementGetSchema().validate(doc) == {}
