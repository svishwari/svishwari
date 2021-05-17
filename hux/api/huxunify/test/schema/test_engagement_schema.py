# pylint: disable=no-self-use
"""
Purpose of this file is to test the engagement schemas
"""
from unittest import TestCase

from huxunify.api.schema.engagement import (
    EngagementGetSchema,
    EngagementPostSchema,
    EngagementPutSchema,
)
from huxunify.api import constants as api_c


class EngagementSchemaTest(TestCase):
    """Test Engagement Schema Classes"""

    def test_successful_engagement_get_schema(self) -> None:
        """Test Successful EngagementGetSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.ENGAGEMENT_ID: "5f5f7262997acad4bac4373b",
            api_c.ENGAGEMENT_NAME: "Engagement 1",
            api_c.ENGAGEMENT_DESCRIPTION: "Engagement 1 description",
            api_c.ENGAGEMENT_AUDIENCES: [],
            api_c.ENGAGEMENT_STATUS: api_c.ENGAGEMENT_STATUS_ACTIVE,
            api_c.ENGAGEMENT_DELIVERY_SCHEDULE: {},
            api_c.ENABLED: True,
        }

        assert EngagementGetSchema().validate(doc) == {}

    def test_successful_engagement_post_schema(self) -> None:
        """Test Successful EngagementPostSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.ENGAGEMENT_NAME: "Engagement 1",
            api_c.ENGAGEMENT_DESCRIPTION: "Engagement 1 description",
            api_c.ENGAGEMENT_AUDIENCES: [],
            api_c.ENGAGEMENT_DELIVERY_SCHEDULE: {},
        }

        assert EngagementPostSchema().validate(doc) == {}

    def test_successful_engagement_put_schema(self) -> None:
        """Test Successful EngagementPutSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.ENGAGEMENT_NAME: "Engagement 1",
            api_c.ENGAGEMENT_DESCRIPTION: "Engagement 1 description",
        }

        assert EngagementPutSchema().validate(doc) == {}

    def test_unsuccessful_engagement_get_schema_bad_name(self) -> None:
        """Test unsuccessful EngagementGetSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.ENGAGEMENT_ID: "5f5f7262997acad4bac4373b",
            api_c.ENGAGEMENT_NAME: 3,
            api_c.ENGAGEMENT_DESCRIPTION: "Engagement 1 description",
            api_c.ENGAGEMENT_AUDIENCES: [],
            api_c.ENGAGEMENT_STATUS: api_c.ENGAGEMENT_STATUS_ACTIVE,
            api_c.ENGAGEMENT_DELIVERY_SCHEDULE: {},
        }

        assert EngagementGetSchema().validate(doc) != {}

    def test_unsuccessful_engagement_get_schema_missing_audiences(
        self,
    ) -> None:
        """Test unsuccessful EngagementGetSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.ENGAGEMENT_ID: "5f5f7262997acad4bac4373b",
            api_c.ENGAGEMENT_NAME: "Engagement 1",
            api_c.ENGAGEMENT_DESCRIPTION: "Engagement 1 description",
            api_c.ENGAGEMENT_STATUS: api_c.ENGAGEMENT_STATUS_ACTIVE,
            api_c.ENGAGEMENT_DELIVERY_SCHEDULE: {},
            api_c.ENABLED: True
        }

        assert EngagementGetSchema().validate(doc) != {}

    def test_unsuccessful_engagement_post_schema_bad_name(self) -> None:
        """Test unsuccessful EngagementPostSchema Serialization

        Returns:
            Response: None

        """
        doc = {
            api_c.ENGAGEMENT_NAME: 3,
            api_c.ENGAGEMENT_DESCRIPTION: "Engagement 1 description",
            api_c.ENGAGEMENT_AUDIENCES: [],
            api_c.ENGAGEMENT_DELIVERY_SCHEDULE: {},
        }

        assert EngagementPostSchema().validate(doc) != {}

    def test_unsuccessful_engagement_put_schema_bad_field(self) -> None:
        """Test unsuccessful EngagementPutSchema Serialization

        Returns:
            Response: None

        """
        doc = {"SomeRandomField": "Some Random String"}

        assert EngagementPutSchema().validate(doc) != {}
