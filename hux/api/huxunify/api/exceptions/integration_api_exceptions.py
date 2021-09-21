"""This module is for exceptions raised from Integrated APIs."""
from huxunify.api import constants


class IntegratedAPIEndpointException(Exception):
    """Exception due to Integration APIs like CDP/Tecton.

    Args:
        Exception: Exception being raised.
    """

    exception_message = ""

    def __init__(self, *args):
        """Initialize the exception class."""
        super().__init__(
            self.exception_message.format(*args)
            if args
            else self.exception_message
        )


class FailedAPIDependencyError(IntegratedAPIEndpointException):
    """Exception for dependency failure from integrated APIs."""

    exception_message = (
        "Integrated API <{}> failure, returned status code "
        "<{}>. Failed obtaining dependent data"
    )


class FailedDateFilterIssue(IntegratedAPIEndpointException):
    """Exception for dependency failure from integrated APIs."""

    exception_message = constants.START_DATE_GREATER_THAN_END_DATE
