"""This module is for exceptions raised from Custom errors in Unified APIs."""


class UnifiedExceptions(Exception):
    """Custom Unified API Exception.

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


class InputParamsValidationError(UnifiedExceptions):
    """Exception due to incompatible type of data in input parameters."""

    exception_message = "Value <{}> is not a valid <{}> value"
