"""This module is for exceptions raised from Custom errors in Unified APIs."""


class UnifiedException(Exception):
    """Custom Unified API Exception."""

    exception_message = ""

    def __init__(self, *args, **kwargs):
        custom_message = kwargs.get("message")

        if custom_message:
            super().__init__(custom_message)
        else:
            super().__init__(
                self.exception_message.format(*args)
                if args
                else self.exception_message
            )


class InputParamsValidationError(UnifiedException):
    """Exception due validation failure of input parameters."""

    exception_message = "'{}' is not a valid {} value"
