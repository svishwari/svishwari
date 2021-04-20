# pylint: disable=no-self-use
"""
Models for the destinations API
"""
from typing import Union
from bson import ObjectId
from huxunifylib.database import (
    delivery_platform_management as destination_management,
    delete_util as db_delete_utils,
    constants as db_constants,
)
import huxunify.api.constants as constants
from huxunify.api.data_connectors.aws import parameter_store


class DestinationModel:
    """
    destinations model class
    """

    def get_destination_by_id(self, destination_id: str) -> Union[dict, None]:
        """Finds a destination in the delivery platform table.

        Args:
            destination_id (str): id of the destination

        Returns:
            dict: The destination in the database
        """

        try:
            destination = destination_management.get_delivery_platform(
                None,  # TODO : use mongo connector library to get mongo db client,
                ObjectId(destination_id),
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
                database=None,  # TODO : use mongo connector library to get mongo db client,
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
            # TODO - implement mongo connector when ORCH-94 and HUS-262 are ready
            destination_management.set_authentication_details(
                database=None,
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
            return destination_management.update_delivery_platform(
                database=None,  # TODO : use mongo connector library to get mongo db client,
                delivery_platform_id=ObjectId(destination_id),
                name=body[constants.DESTINATION_NAME],
                delivery_platform_type=body[constants.DESTINATION_TYPE],
                authentication_details=authentication_params,
            )

        except Exception as exc:
            raise Exception(f"Something went wrong. Details {exc}") from exc
        return None

    def delete_destination_by_id(self, destination_id: str) -> Union[dict, None]:
        """Finds a destination in the delivery platform table.

        Args:
            destination_id (str): id of the destination

        Returns:
            dict: The destination in the database
        """
        return db_delete_utils.delete_delivery_platform(
            database=None,  # TODO : use mongo connector library to get mongo db client
            delivery_platform_id=ObjectId(destination_id),
        )
