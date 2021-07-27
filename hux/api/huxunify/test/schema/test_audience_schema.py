"""
Purpose of this file is to test the audience schemas
"""
from unittest import TestCase

from huxunifylib.database import constants as db_c
from huxunify.api.schema.orchestration import is_audience_lookalikeable
from huxunify.api import constants as api_c


class EngagementSchemaTest(TestCase):
    """Test Audience Schema Classes"""

    def test_is_audience_lookalikeable_active(self) -> None:
        """Test is_audience_lookalikeable active status

        Returns:
            Response: None

        """

        audience = {
            api_c.DELIVERIES: [
                {
                    db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FACEBOOK,
                    db_c.STATUS: db_c.STATUS_SUCCEEDED,
                }
            ]
        }

        # check engagement status per weighting
        self.assertEqual(db_c.ACTIVE, is_audience_lookalikeable(audience))

    def test_is_audience_lookalikeable_inactive(self) -> None:
        """Test is_audience_lookalikeable inactive status

        Returns:
            Response: None

        """

        audience = {
            api_c.DELIVERIES: [
                {
                    db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_FACEBOOK,
                    db_c.STATUS: db_c.STATUS_FAILED,
                }
            ]
        }

        # check engagement status per weighting
        self.assertEqual(
            api_c.STATUS_INACTIVE, is_audience_lookalikeable(audience)
        )

    def test_is_audience_lookalikeable_disabled(self) -> None:
        """Test is_audience_lookalikeable disabled status

        Returns:
            Response: None

        """

        audience = {
            api_c.DELIVERIES: [
                {
                    db_c.DELIVERY_PLATFORM_TYPE: db_c.DELIVERY_PLATFORM_SFMC,
                    db_c.STATUS: db_c.STATUS_FAILED,
                }
            ]
        }

        # check engagement status per weighting
        self.assertEqual(api_c.DISABLED, is_audience_lookalikeable(audience))
