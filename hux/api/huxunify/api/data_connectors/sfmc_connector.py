"""Facebook Connector functionality."""

import logging


class SFMCConnector:
    """SFMC connector"""

    def __init__(
        self,
        auth_details: dict,
    ):
        """Initialize, connect to SFMC.
        Args:
            auth_details (dict): Authentication details.
        """

        self.auth_details = auth_details
        self.authenticate()

    def authenticate(self) -> bool:
        """Authenticates SFMC connector.
        Returns:
            bool: A true/false flag indicating successful authentication.
        """
        # This is WIP and needs to be updated
        return False

    def check_connection(self) -> bool:
        """A function to check connection to SFMC.
        Returns:
            bool: A flag indicating a successful connection.
        """

        # This is WIP and needs to be updated
        return False
