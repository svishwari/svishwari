"""This module is for exceptions raised from Integrated APIs."""


class IntegratedAPIEndpointException(Exception):
    """Exception due to Integration APIs like CDP/Tecton."""

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


class FailedDeliveryPlatformDependencyError(IntegratedAPIEndpointException):
    """Exception for dependency failure for delivery platform APIs."""

    exception_message = (
        "Failed to establish connection to delivery platform <{}>, "
        "returned status code <{}>."
    )


class EmptyAPIResponseError(IntegratedAPIEndpointException):
    """Exception for empty response from integrated APIs."""

    exception_message = (
        "Integrated API <{}> failure, returned status code "
        "<{}>. Failed obtaining dependent data"
    )


class FailedSSMDependencyError(IntegratedAPIEndpointException):
    """Exception for dependency failure for AWS SSM parameter store."""

    exception_message = "Raised <{}> error, returned status code <{}>."
