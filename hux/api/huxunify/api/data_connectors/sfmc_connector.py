"""SFMC Connector functionality.
TODO : Move this to common library that can support adperf and other use cases
"""

import requests
import logging
import hux.api.huxunify.api.constants as constants


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

        params = {
            "grant_type": "client_credentials",
            "client_id": self.auth_details[constants.SFMC_CLIENT_ID],
            "client_secret": self.auth_details[constants.SFMC_CLIENT_SECRET],
            "account_id": self.auth_details[constants.SFMC_ACCOUNT_ID],
        }
        response = requests.post(
            self.auth_details[constants.SFMC_AUTH_BASE_URI], params=params
        )

        if response.status_code == 200:
            success_flag = True
        else:
            success_flag = False
            logging.error("Failed to authenticate SFMC!")

        return success_flag

    def check_connection(self) -> bool:
        """A function to check connection to SFMC.
        Returns:
            bool: A flag indicating a successful connection.
        """

        success_flag = self.authenticate()
        return success_flag
