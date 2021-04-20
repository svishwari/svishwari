"""
Models for the User API
"""
from typing import Union, List

from bson import ObjectId
from huxunify.api.data_connectors.snowflake_client import SnowflakeClient
from huxunifylib.database.user_management import *


class UserModel:
    """
    user model class
    """

    def __init__(self, database: Union[SnowflakeClient, None] = None) -> None:
        self.message = "Hello user"
        if database is None:
            self.database = SnowflakeClient()
        else:
            self.database = database
        self.ctx = self.database.connect()

    def get_all_users(self) -> List[dict]:
        """A function to get all user documents.

        Args:

        Returns:
            list: List of all user documents.

        """

        data = get_all_users(self.ctx)
        return data

    def get_user(self, okta_id: str) -> dict:
        """A function to get a user.

        Args:
            okta_id (str): id derived from okta authentication.

        Returns:
            dict: MongoDB document for a user.

        """
        data = get_user(self.ctx, okta_id=okta_id)
        return data

    def update_user(self, user_id: ObjectId, update_doc: dict) -> dict:
        """A function to update a user.

        Args:
            user_id (ObjectId): MongoDB ID of a user doc.
            update_doc (dict): Dict of key values to update.

        Returns:
            dict: Updated MongoDB document for a user.

        """
        data = update_user(self.ctx, user_id=user_id, update_doc=update_doc)
        return data

    # TODO config_key should be a string ?
    def update_user_dashboard(
        self, user_id: ObjectId, config_key: str, config_value: Any
    ) -> dict:
        """A function to manage user dashboard configuration

        Args:
            user_id (ObjectId): MongoDB ID of a user doc.
            config_key (str): name of the config param.
            config_value (Any): value of the config key.

            Returns:
                dict: Updated MongoDB document for a user.

        """
        data = manage_user_dashboard_config(
            self.ctx, user_id=user_id, config_key=config_key, config_value=config_value
        )
        return data

    # TODO component name is and ObjectId or a str?
    def update_user_favorites(
        self,
        user_id: ObjectId,
        component_name: str,
        component_id: ObjectId,
        delete: bool = False,
    ) -> dict:
        """A function to add a favorite component for a user.

        Args:
            user_id (ObjectId): MongoDB ID of a user doc.
            component_name (ObjectId): name of the component (i.e campaigns, destinations, etc.).
            component_id (ObjectId): MongoDB ID of the input component

        Returns:
            dict: Updated MongoDB document for a user.

        """

        data = manage_user_favorites(
            self.ctx,
            user_id=user_id,
            component_name=component_name,
            component_id=component_id,
            delete_flag=delete,
        )
        return data
