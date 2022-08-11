"""Purpose of this file is to integration test for trust id insights."""
from time import time
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests
from prometheus_metrics import record_test_result, HttpMethod, Endpoints
from huxunify.api import constants as api_c
from huxunifylib.database import constants as db_c

class TestTrustId(TestCase):
    """Test Trust ID."""

    TRUST_ID = "trust_id"
    SIGNAL_NAME = "capability"
    SEGMENT_FILTERS = [
        {
            "description": "Gender",
            "type": "gender",
            "values": ["Female", "Male"],
        }
    ]

    def test_trust_user_role(self):
        """Test trust ID user role."""
        get_user_response = requests.get(
            f"{pytest.API_URL}/users/profile",
            headers=pytest.HEADERS,
        )
        data = get_user_response.json()
        user_id = data.get(api_c.ID)
        user_pii_access = data.get(api_c.USER_PII_ACCESS)
        user_old_role = data.get(api_c.ROLE)

        update_user_response = requests.patch(
            f"{pytest.API_URL}/users",
            json={
                api_c.ID: user_id,
                api_c.USER_PII_ACCESS: user_pii_access,
                api_c.ROLE: db_c.USER_ROLE_TRUSTID,
            },
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, update_user_response.status_code)

        get_engagements = requests.get(
            f"{pytest.API_URL}/engagements",
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, get_engagements.status_code)

        get_audiences = requests.get(
            f"{pytest.API_URL}/engagements",
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, get_audiences.status_code)

        get_navigation_configuration = requests.get(
            f"{pytest.API_URL}/configurations/navigation",
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, get_navigation_configuration.status_code)
        for parent_config in get_navigation_configuration.json().get(api_c.SETTINGS):
            if parent_config.get(db_c.CONFIGURATION_FIELD_NAME) == "Insights":
                self.assertTrue(parent_config.get(db_c.CONFIGURATION_FIELD_ENABLED))
            else:
                self.assertFalse(parent_config.get(db_c.CONFIGURATION_FIELD_ENABLED))

            for children_config in parent_config.get(db_c.CONFIGURATION_FIELD_CHILDREN):
                if children_config.get(db_c.CONFIGURATION_FIELD_NAME) == "HX TrustID":
                    self.assertTrue(children_config.get(db_c.CONFIGURATION_FIELD_ENABLED))
                else:
                    self.assertFalse(children_config.get(db_c.CONFIGURATION_FIELD_ENABLED))

        revert_user_response = requests.patch(
            f"{pytest.API_URL}/users",
            json={
                api_c.ID: user_id,
                api_c.USER_PII_ACCESS: user_pii_access,
                api_c.ROLE: user_old_role,
            },
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, revert_user_response.status_code)

    def test_get_trust_id_user_filters(self):
        """Test get trust ID user filters."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/user_filters",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)
        for user_filter in response.json():
            self.assertIn("description", user_filter)
            self.assertIn("type", user_filter)
            self.assertIn("values", user_filter)
            self.assertIsInstance(user_filter["values"], list)

    @record_test_result(HttpMethod.GET, Endpoints.TRUST_ID.GET_ATTRIBUTES)
    def test_get_trust_id_attributes(self):
        """Test get trust ID attributes data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/attributes",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)

        for attribute in response.json():
            self.assertIn("factor_name", attribute)
            self.assertIn("attribute_score", attribute)
            self.assertIn("attribute_description", attribute)
            self.assertIn("attribute_short_description", attribute)
            self.assertIn("overall_customer_rating", attribute)
            self.assertIsInstance(attribute["overall_customer_rating"], dict)

    @record_test_result(HttpMethod.GET, Endpoints.TRUST_ID.GET_COMPARISON_DATA)
    def test_get_trust_id_comparison(self):
        """Test get trust ID comparison."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/comparison",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        comparison_data = response.json()
        self.assertIsInstance(comparison_data, list)
        self.assertGreaterEqual(len(comparison_data), 1)

        for comparison_segment_type in comparison_data:
            self.assertIn("segment_type", comparison_segment_type)
            self.assertIn("segments", comparison_segment_type)
            self.assertIsInstance(comparison_segment_type["segments"], list)
            for segment in comparison_segment_type["segments"]:
                self.assertIn("segment_name", segment)
                self.assertIn("segment_filters", segment)
                self.assertIsInstance(segment["segment_filters"], list)
                self.assertIn("attributes", segment)
                self.assertIsInstance(segment["attributes"], list)
                for attribute_data in segment["attributes"]:
                    self.assertIn("attribute_type", attribute_data)
                    self.assertIn("attribute_name", attribute_data)
                    self.assertIn("attribute_score", attribute_data)
                    self.assertIn("attribute_description", attribute_data)

    @record_test_result(HttpMethod.GET, Endpoints.TRUST_ID.GET_OVERIVEW)
    def test_get_trust_id_overview(self):
        """Test get trust ID overview data."""

        response = requests.get(
            f"{pytest.API_URL}/{self.TRUST_ID}/overview",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        overview_data = response.json()
        self.assertIsInstance(overview_data, dict)
        self.assertIn("trust_id_score", overview_data)
        self.assertIn("factors", overview_data)
        self.assertIsInstance(overview_data["factors"], list)
        for factor in overview_data["factors"]:
            self.assertIn("factor_name", factor)
            self.assertIn("factor_score", factor)
            self.assertIn("factor_description", factor)
            self.assertIn("overall_customer_rating", factor)
            self.assertIsInstance(factor["overall_customer_rating"], dict)

    @record_test_result(HttpMethod.POST, Endpoints.TRUST_ID.POST_ADD_SEGMENT)
    def test_add_and_remove_trust_id_segment(self):
        """Test adding and removing trust ID segment for a user."""
        # TODO https://jira.hux.deloitte.com/browse/HUS-3679

        segment_name = (
            f"E2E test_trust_id Integration Test-{int(time() * 1000)}"
        )

        # request to add trust ID segment to a user
        add_response = requests.post(
            f"{pytest.API_URL}/{self.TRUST_ID}/segment",
            params={"default": False},
            json={
                "segment_name": segment_name,
                "segment_filters": self.SEGMENT_FILTERS,
            },
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.CREATED, add_response.status_code)
        add_response_data = add_response.json()
        self.assertIsInstance(add_response_data, list)

        for comparison_segment_type in add_response_data:
            self.assertIn("segment_type", comparison_segment_type)
            self.assertIn("segments", comparison_segment_type)
            self.assertIsInstance(comparison_segment_type["segments"], list)
            self.assertEqual(len(comparison_segment_type["segments"]), 1)
            for segment in comparison_segment_type["segments"]:
                self.assertIn("segment_name", segment)
                self.assertEqual(segment_name, segment["segment_name"])
                self.assertIn("segment_filters", segment)
                self.assertIsInstance(segment["segment_filters"], list)
                self.assertDictContainsSubset(
                    self.SEGMENT_FILTERS[0], segment["segment_filters"][0]
                )
                self.assertIn("attributes", segment)
                self.assertIsInstance(segment["attributes"], list)
                for attribute_data in segment["attributes"]:
                    self.assertIn("attribute_type", attribute_data)
                    self.assertIn("attribute_name", attribute_data)
                    self.assertIn("attribute_score", attribute_data)
                    self.assertIn("attribute_description", attribute_data)

        # request to remove trust ID segment to a user
        remove_response = requests.delete(
            f"{pytest.API_URL}/{self.TRUST_ID}/segment?segment_name={segment_name}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, remove_response.status_code)
        remove_response_data = remove_response.json()
        self.assertIsInstance(remove_response_data, list)

        for comparison_segment_type in remove_response_data:
            self.assertIn("segment_type", comparison_segment_type)
            self.assertIn("segments", comparison_segment_type)
            self.assertIsInstance(comparison_segment_type["segments"], list)
            self.assertEqual(len(comparison_segment_type["segments"]), 1)
            for segment in comparison_segment_type["segments"]:
                self.assertIn("segment_name", segment)
                self.assertIn("segment_filters", segment)
                self.assertIsInstance(segment["segment_filters"], list)
                self.assertFalse(segment["segment_filters"])
                self.assertTrue(segment["default"])
                self.assertIn("attributes", segment)
                self.assertIsInstance(segment["attributes"], list)
                for attribute_data in segment["attributes"]:
                    self.assertIn("attribute_type", attribute_data)
                    self.assertIn("attribute_name", attribute_data)
                    self.assertIn("attribute_score", attribute_data)
                    self.assertIn("attribute_description", attribute_data)
