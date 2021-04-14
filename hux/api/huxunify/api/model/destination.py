# pylint: disable=no-self-use
"""
Models for the destinations API
"""
from bson import ObjectId
from typing import Union, List
from hux.api.huxunify.api import utils as util
from lib.huxunifylib.huxunifylib.database import (
    delivery_platform_management as destination_management,
    utils as db_utils,
)
from lib.huxunifylib.huxunifylib.database import constants as db_constants
import hux.api.huxunify.api.constants as constants
from hux.api.huxunify.api.data_connectors.mongo_client import get_mongo_client
from hux.api.huxunify.api.data_connectors.aws import parameter_store


class DestinationModel:
    """
    destinations model class
    """

    def get_destinations(self) -> List[dict]:
        """Reads the destination / delivery platform table.

        Returns:
            list(dict): The list of destinations / delivery platforms.
        """

        try:
            all_destinations = destination_management.get_all_delivery_platforms(
                get_mongo_client()
            )
            return all_destinations

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

    def get_destination_by_id(self, destination_id: str) -> Union[dict, None]:
        """Finds a destination in the delivery platform table.

        Args:
            destination_id (str): id of the destination

        Returns:
            dict: The destination in the database
        """

        try:
            destination = destination_management.get_delivery_platform(
                get_mongo_client(), ObjectId(destination_id)
            )
            return destination

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

    def create_destination(self, body: dict) -> Union[str, None]:
        """Creates a destination in  delivery platform table.

        Args:
            body (str): destination object

        Returns:
            int: The destination id in the database
        """

        try:
            # create destination
            destination_id = destination_management.set_delivery_platform(
                database=get_mongo_client(),
                delivery_platform_type=body[constants.DESTINATION_TYPE],
                name=body[constants.DESTINATION_NAME],
                authentication_details=None,
            )[db_constants.ID]

            # store the secrets in AWS parameter store
            authentication_parameters = (
                parameter_store.set_destination_authentication_secrets(
                    authentication_details=body[constants.AUTHENTICATION_DETAILS],
                    is_updated=False,
                    destination_id=str(destination_id),
                    destination_name=body[constants.DESTINATION_NAME],
                )
            )

            # store the secrets paths in database
            destination_management.set_authentication_details(
                database=get_mongo_client(),
                delivery_platform_id=destination_id,
                authentication_details=authentication_parameters,
            )

            return destination_id

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

    def update_destination(
        self, destination_id: str, body: dict, authentication_params: dict
    ) -> Union[dict, None]:
        """Creates a destination in  delivery platform table.

        Args:
            destination_id: destination id
            body: destination object to be updated
            authentication_params: Auth params

        Returns:
            int: The destination id in the database
        """

        try:
            # update the platform
            destination_management.update_delivery_platform(
                database=get_mongo_client(),
                delivery_platform_id=ObjectId(destination_id),
                name=body[constants.DESTINATION_NAME],
                delivery_platform_type=body[constants.DESTINATION_TYPE],
                authentication_details=authentication_params,
            )

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc

    def delete_destination_by_id(self, destination_id: str) -> Union[dict, None]:
        """Finds a destination in the delivery platform table.

        Args:
            destination_id (str): id of the destination

        Returns:
            dict: The destination in the database
        """
        return db_utils.delete_delivery_platform(
            database=get_mongo_client(),
            delivery_platform_id=ObjectId(destination_id),
        )

    def get_destination_constants(self) -> List[dict]:
        """Return auth constants.

        Returns:
            int: The destination id in the database
        """

        auth_details = {
            db_constants.DELIVERY_PLATFORM_FACEBOOK: {
                constants.FACEBOOK_AD_ACCOUNT_ID: "Ad Account ID",
                constants.FACEBOOK_APP_ID: "Facebook App ID",
                constants.FACEBOOK_APP_SECRET: "App Secret",
                constants.FACEBOOK_ACCESS_TOKEN: "Access Token",
            },
            db_constants.DELIVERY_PLATFORM_SFMC: {
                constants.SFMC_CLIENT_ID: "Client ID",
                constants.SFMC_ACCOUNT_ID: "Account ID",
                constants.SFMC_CLIENT_SECRET: "Client Secret",
                constants.SFMC_AUTH_BASE_URI: "Auth Base URI",
                constants.SFMC_REST_BASE_URI: "REST Base URI",
                constants.SFMC_SOAP_BASE_URI: "SOAP Base URI",
            },
        }

        return auth_details
