"""Facebook Connector functionality."""

import logging
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError
import hux.api.huxunify.api.constants as constants


class FacebookConnector:
    """Facebook connector."""

    def __init__(
        self,
        auth_details: dict,
    ):
        """Initialize, connect to facebook.
        Args:
            auth_details (dict): Authentication details.
        """

        self.auth_details = auth_details
        self.authenticate()
        self.delivery_platform_audience = None

    def authenticate(self) -> bool:
        """Authenticates Facebook connector.
        Returns:
            bool: A true/false flag indicating successful authentication.
        """

        ret_value = FacebookAdsApi.init(
            self.auth_details[constants.FACEBOOK_APP_ID],
            self.auth_details[constants.FACEBOOK_APP_SECRET],
            self.auth_details[constants.FACEBOOK_ACCESS_TOKEN],
        )

        if ret_value is None:
            logging.error("Failed to authenticate Facebook!")
            raise Exception("Failed to connect to Facebook")

        success_flag = ret_value is not None

        return success_flag

    def check_connection(self) -> bool:
        """A function to check connection to Facebook.
        Returns:
            bool: A flag indicating a successful connection.
        """

        success_flag = False

        # Set authentication details
        success_flag = self.authenticate()

        # If successful try to get a list of existing custom audiences
        if success_flag:
            ad_account_id = str(self.auth_details[constants.FACEBOOK_AD_ACCOUNT_ID])

            try:
                ret_val = AdAccount(ad_account_id).get_custom_audiences()
                if ret_val is not None:
                    success_flag = True
            except FacebookRequestError as exc:
                success_flag = False
                logging.error(exc)

        if success_flag:
            logging.info("Connection to Facebook was successful!")
        else:
            logging.error("Connection to Facebook failed!")

        return success_flag
