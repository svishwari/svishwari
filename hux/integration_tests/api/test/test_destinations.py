"""Purpose of this file is to integration test for destinations."""
from unittest import TestCase
from http import HTTPStatus
import pytest
import requests
from prometheus_metrics import record_test_result, HttpMethod, Endpoints


class TestDestinations(TestCase):
    """Test Destinations."""

    DESTINATIONS = "destinations"
    COLLECTION = "delivery_platforms"
    DELIVERY_PLATFORM_SFMC = "sfmc"

    @record_test_result(
        HttpMethod.GET, Endpoints.DESTINATIONS.GET_ALL_DESTINATIONS
    )
    def test_get_destinations(self):
        """Test get all destinations."""

        response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)

    @record_test_result(HttpMethod.GET, Endpoints.DESTINATIONS.GET_DESTINATION)
    def test_get_destination(self):
        """Test get destination."""

        get_all_response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, get_all_response.status_code)
        self.assertIsInstance(get_all_response.json(), list)

        destination = get_all_response.json()[0]

        get_individual_destination_response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}/{destination['id']}",
            headers=pytest.HEADERS,
        )

        # test success
        self.assertEqual(
            HTTPStatus.OK, get_individual_destination_response.status_code
        )
        self.assertIsInstance(get_individual_destination_response.json(), dict)

    @record_test_result(
        HttpMethod.GET, Endpoints.DESTINATIONS.GET_DESTINATION_CONSTANTS
    )
    def test_get_destination_constants(self):
        """Test get destination constants."""

        response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}/constants",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertIsInstance(response.json(), dict)

    @record_test_result(
        HttpMethod.GET, Endpoints.DESTINATIONS.GET_DESTINATION_DATA_EXTENSIONS
    )
    def test_get_destination_data_extension(self):
        """Test get destination data extensions."""

        get_all_response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}",
            headers=pytest.HEADERS,
        )
        self.assertEqual(HTTPStatus.OK, get_all_response.status_code)
        self.assertIsInstance(get_all_response.json(), list)

        destinations = get_all_response.json()
        sfmc_destination = [
            destination
            for destination in destinations
            if destination["type"] == self.DELIVERY_PLATFORM_SFMC
        ][0]

        get_dest_data_ext = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}/{sfmc_destination['id']}/"
            f"data-extensions",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, get_dest_data_ext.status_code)
        self.assertIsInstance(get_dest_data_ext.json(), list)
        self.assertGreaterEqual(len(get_dest_data_ext.json()), 1)

    @record_test_result(
        HttpMethod.PATCH, Endpoints.DESTINATIONS.PATCH_UPDATE_DESTINATION
    )
    def test_update_destination(self):
        """Test update destination."""

        get_all_response = requests.get(
            f"{pytest.API_URL}/{self.DESTINATIONS}",
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, get_all_response.status_code)
        self.assertIsInstance(get_all_response.json(), list)

        destination = get_all_response.json()[0]

        update_response = requests.patch(
            f"{pytest.API_URL}/{self.DESTINATIONS}/{destination['id']}",
            json={"enabled": destination["is_enabled"]},
            headers=pytest.HEADERS,
        )

        self.assertEqual(HTTPStatus.OK, update_response.status_code)
        self.assertIsInstance(update_response.json(), dict)

    # TODO: Commenting out since this test ends up creating too many tickets on
    #  JIRA as part of /request endpoint as it becomes tedious process to
    #  delete them manually at a later time
    # def test_request_and_delete_a_destination(self):
    #     """Test request of new destination followed by deleting it."""
    #
    #     create_destination_response = requests.post(
    #         f"{pytest.API_URL}/{self.DESTINATIONS}/request",
    #         json={
    #             "contact_email": getenv("OKTA_TEST_USER_NAME"),
    #             "client_request": "false",
    #             "client_account": "false",
    #             "name": f"E2E test_destinations Integration Test-"
    #             f"{int(time() * 1000)}",
    #         },
    #         headers=pytest.HEADERS,
    #     )
    #
    #     created_destination_id = create_destination_response.json()["id"]
    #
    #     # add the crud object to pytest for cleaning after
    #     pytest.CRUD_OBJECTS += [Crud(self.COLLECTION, created_destination_id)]
    #
    #     # test success
    #     self.assertEqual(
    #         HTTPStatus.OK, create_destination_response.status_code
    #     )
    #     self.assertIsInstance(create_destination_response.json(), dict)
    #
    #     delete_destination_response = requests.delete(
    #         f"{pytest.API_URL}/{self.DESTINATIONS}/{created_destination_id}",
    #         headers=pytest.HEADERS,
    #     )
    #
    #     # test success
    #     self.assertEqual(
    #         HTTPStatus.NO_CONTENT, delete_destination_response.status_code
    #     )
