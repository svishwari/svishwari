"""
purpose of this file is to house all the courier tests.
"""
from http import HTTPStatus
from unittest import TestCase, mock
import mongomock
from bson import ObjectId

import huxunifylib.database.delivery_platform_management as dpm
import huxunifylib.database.audience_management as am
import huxunifylib.database.data_management as dm
import huxunifylib.database.constants as c
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.audience_data_management_util import (
    update_audience_doc,
)
from huxunifylib.connectors.aws_batch_connector import AWSBatchConnector
from huxunify.api import constants as api_c
from huxunify.api.data_connectors.courier import (
    Courier,
    map_destination_credentials_to_dict,
    get_destination_config,
)


class CourierTest(TestCase):
    """
    Test Courier
    """

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):
        """Setup method for unit tests.
        This setup method needs to be reduced, at time of writing it is clear
        we have a few backlog items that need to be addressed, so I have flagged
        as TODOs as relevant tickets will be created for each.

        Args:

        Returns:

        """
        # setup the mock DB client
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        # Set delivery platform
        self.auth_details_facebook = {
            "facebook_access_token": "path1",
            "facebook_app_secret": "path2",
            "facebook_app_id": "path3",
            "facebook_ad_account_id": "path4",
        }

        self.auth_details_sfmc = {
            "sfmc_client_id": "path1",
            "sfmc_client_secret": "path2",
            "sfmc_account_id": "path3",
            "sfmc_auth_base_uri": "path4",
            "sfmc_rest_base_uri": "path5",
            "sfmc_soap_base_uri": "path5",
        }

        # create the list of destinations
        destinations = []
        for destination in [
            (api_c.FACEBOOK_NAME, self.auth_details_facebook),
            (api_c.SFMC_NAME, self.auth_details_sfmc),
        ]:
            # TODO - remove when we remove delivery-platform types
            destination_doc = dpm.set_delivery_platform(
                self.database,
                destination[0],
                destination[0],
                destination[1],
            )

            # ensure doc was created
            self.assertIsNotNone(destination_doc)

            # set status
            destination_doc = dpm.set_connection_status(
                self.database, destination_doc[c.ID], c.STATUS_SUCCEEDED
            )
            self.assertEqual(
                c.STATUS_SUCCEEDED, destination_doc[c.DELIVERY_PLATFORM_STATUS]
            )

            destinations.append(destination_doc)

        # create first audience
        self.audience_one = am.create_audience(
            self.database,
            self._setup_ingestion_job("ds1")[c.ID],
            "audience one",
            [],
        )
        self.assertIsNotNone(self.audience_one)

        # create second audience
        self.audience_two = am.create_audience(
            self.database,
            self._setup_ingestion_job("ds2")[c.ID],
            "audience two",
            [],
        )
        self.assertIsNotNone(self.audience_two)

        # TODO - assign the audiences to the destinations
        # need to discuss this one, I don't know where we
        # assign this currently, we have to assign it.
        destination_ids = [d[c.ID] for d in destinations]
        update_dict = {c.DESTINATIONS: destination_ids}
        self.audience_one = update_audience_doc(
            self.database, self.audience_one[c.ID], update_dict
        )
        self.assertListEqual(
            self.audience_one[c.DESTINATIONS], destination_ids
        )

        self.audience_two = update_audience_doc(
            self.database, self.audience_two[c.ID], update_dict
        )
        self.assertListEqual(
            self.audience_two[c.DESTINATIONS], destination_ids
        )

        # TODO - set engagement object when engagements are in Database Library
        # simulate for now
        engagements = self.database[c.DATA_MANAGEMENT_DATABASE]["engagements"]

        # define a sample engagement, with prepopulated engagements
        engagement_doc = {
            c.AUDIENCE_NAME: "Chihuly Garden and Glass",
            c.NOTIFICATION_FIELD_DESCRIPTION: "Former fun forest amusement park.",
            c.AUDIENCES: [self.audience_one[c.ID], self.audience_two[c.ID]],
            c.CREATED_BY: ObjectId(),
        }
        # insert engagement doc in the collection
        self.engagement_id = engagements.insert_one(engagement_doc).inserted_id
        self.assertIsNotNone(self.engagement_id)

        engagement = engagements.find_one(self.engagement_id)
        for key, value in engagement_doc.items():
            self.assertIn(key, engagement)
            self.assertEqual(value, engagement[key])

    def _setup_ingestion_job(self, data_source_name: str) -> dict:
        """Setup ingestion jobs so we can test audience delivery

        Args:
            data_source_name (str): Name of a data source.

        Returns:
           dict: Return an ingestion job dict.
        """
        data_source_params = [
            data_source_name,
            1,
            "CSV",
            "S3",
            None,
            None,
        ]

        data_source_doc = dm.set_data_source(
            self.database, *data_source_params
        )
        ingestion_job_doc = dm.set_ingestion_job(
            self.database, data_source_doc[c.ID]
        )
        return ingestion_job_doc

    def test_map_destination_credentials(self):
        """Test mapping of destination credentials for submitting to AWS Batch.

        Args:

        Returns:

        """

        # setup destination object with synthetic credentials.
        destination = {
            api_c.DESTINATION_ID: ObjectId(),
            api_c.DESTINATION_NAME: "My destination",
            api_c.DESTINATION_TYPE: "Facebook",
            api_c.AUTHENTICATION_DETAILS: {
                api_c.FACEBOOK_ACCESS_TOKEN: "MkU3Ojgwm",
                api_c.FACEBOOK_APP_SECRET: "717bdOQqZO99",
                api_c.FACEBOOK_APP_ID: "2951925002021888",
                api_c.FACEBOOK_AD_ACCOUNT_ID: "111333777",
            },
        }

        cred_dict = map_destination_credentials_to_dict(destination)

        # ensure mapping.
        self.assertDictEqual(
            cred_dict, destination[api_c.AUTHENTICATION_DETAILS]
        )

    def test_courier_init(self):
        """Test Courier class init

        Args:

        Returns:

        """
        courier = Courier(self.engagement_id, self.database)
        self.assertIsInstance(courier, Courier)
        self.assertEqual(courier.engagement_id, self.engagement_id)
        self.assertEqual(courier.db_client, self.database)

    def test_courier_delivery_route(self):
        """Test Courier get delivery route

        Args:

        Returns:

        """
        courier = Courier(self.engagement_id, self.database)
        self.assertIsInstance(courier, Courier)

        delivery_route = courier.get_delivery_route()
        self.assertIsNotNone(delivery_route)

        expected_route = {
            self.audience_one[c.ID]: self.audience_one[c.DESTINATIONS],
            self.audience_two[c.ID]: self.audience_two[c.DESTINATIONS],
        }
        self.assertDictEqual(expected_route, delivery_route)

    def test_destination_batch_init(self):
        """Test destination batch init

        Args:

        Returns:

        """
        courier = Courier(self.engagement_id, self.database)
        self.assertIsInstance(courier, Courier)

        delivery_route = courier.get_delivery_route()
        self.assertIsNotNone(delivery_route)

        for audience_id, destination_ids in delivery_route.items():
            for destination_id in destination_ids:
                batch_destination = get_destination_config(
                    self.database, destination_id, audience_id
                )
                self.assertIsNotNone(batch_destination.aws_envs)
                self.assertIsNotNone(batch_destination.aws_secrets)
                self.assertIsNotNone(
                    batch_destination.audience_delivery_job_id
                )
                self.assertEqual(self.database, batch_destination.database)

                # validate the audience delivery job id exists
                audience_delivery_status = dpm.get_delivery_job_status(
                    self.database, batch_destination.audience_delivery_job_id
                )
                self.assertEqual(audience_delivery_status, c.STATUS_PENDING)

    def test_destination_register_job(self):
        """Test destination batch register job

        Args:

        Returns:

        """
        courier = Courier(self.engagement_id, self.database)
        self.assertIsInstance(courier, Courier)

        delivery_route = courier.get_delivery_route()
        self.assertIsNotNone(delivery_route)

        # walk the delivery route
        for audience_id, destination_ids in delivery_route.items():
            for destination_id in destination_ids:
                batch_destination = get_destination_config(
                    self.database, destination_id, audience_id
                )

                self.assertIsNotNone(batch_destination)

                # Register job
                return_value = {
                    "ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value}
                }
                with mock.patch.object(
                    AWSBatchConnector,
                    "register_job",
                    return_value=return_value,
                ):
                    batch_destination.register()

                self.assertEqual(batch_destination.result, c.STATUS_PENDING)

    def test_destination_submit_job(self):
        """Test destination batch submit job

        Args:

        Returns:

        """
        courier = Courier(self.engagement_id, self.database)
        self.assertIsInstance(courier, Courier)

        delivery_route = courier.get_delivery_route()
        self.assertIsNotNone(delivery_route)

        # walk the delivery route
        for audience_id, destination_ids in delivery_route.items():
            for destination_id in destination_ids:
                batch_destination = get_destination_config(
                    self.database, destination_id, audience_id
                )

                # Register job
                return_value = {
                    "ResponseMetadata": {"HTTPStatusCode": HTTPStatus.OK.value}
                }
                with mock.patch.object(
                    AWSBatchConnector,
                    "register_job",
                    return_value=return_value,
                ):
                    batch_destination.register()
                self.assertEqual(batch_destination.result, c.STATUS_PENDING)

                with mock.patch.object(
                    AWSBatchConnector, "submit_job", return_value=return_value
                ):
                    batch_destination.submit()

                self.assertEqual(
                    batch_destination.result, c.STATUS_IN_PROGRESS
                )
