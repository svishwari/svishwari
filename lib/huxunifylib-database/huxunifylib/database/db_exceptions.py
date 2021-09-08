"""This module is for database exceptions."""


class HuxAdvException(Exception):
    """Exception for Hux Advertising Performance purposes."""

    exception_message = ""

    def __init__(self, *args):
        """Initialize the exception class."""
        super().__init__(
            self.exception_message.format(*args)
            if args
            else self.exception_message
        )


class DuplicateName(HuxAdvException):
    """Exception for duplicate names."""

    exception_message = (
        "The name <{}> already exists. The creation/update failed."
    )


class InvalidName(HuxAdvException):
    """Exception for invalid names."""

    exception_message = "The specified name <{}> is invalid."


class DataSourceLocked(HuxAdvException):
    """Exception for when data source is already associated with an ingestion job."""

    exception_message = (
        "Data source with ID <{}> is associated to an ingestion job "
        "and cannot be updated!"
    )


class NoUpdatesSpecified(HuxAdvException):
    """Exception for when no update is specified in an update function."""

    exception_message = "Nothing was passed to update <{}>!"


class InvalidID(HuxAdvException):
    """Exception for when an entity does not exist in database."""

    exception_message = "The ID <{}> does not exist in the database!"


class UnknownDeliveryPlatformType(HuxAdvException):
    """Exception for when a delivery platform type is unknown."""

    exception_message = "Unknown delivery platform type <{}>!"


class NoDeliveryPlatformConnection(HuxAdvException):
    """Exception for when a delivery platform has not established connection."""

    exception_message = (
        "Delivery platform with ID <{}> has not established "
        "a successful connection!"
    )


class IncorrectFilterValue(HuxAdvException):
    """Exception for incorrect audience filter values."""

    exception_message = (
        "Incorrect filter value of type <{}> for filter of type <{}>!"
    )


class DefaultAudienceLocked(HuxAdvException):
    """Exception for updating default audiences."""

    exception_message = (
        "Audience <{}> cannot be updated as it is a default audience!"
    )


class DuplicateDataSourceFieldType(HuxAdvException):
    """Exception for duplicate data source field type."""

    exception_message = "Data source with duplicate <{}> cannot be created!"


class DuplicateFieldType(HuxAdvException):
    """Exception for duplicate field type."""

    exception_message = "Invalid Input Field(s) <{}>!"


class InvalidNotificationType(HuxAdvException):
    """Exception for invalid notification type."""

    exception_message = "Invalid Notification type <{}>!"


class InvalidValueException(HuxAdvException):
    """Exception for invalid value provided."""

    exception_message = "Invalid value provided: <{}>!"


class InsufficientDataException(HuxAdvException):
    """Exception for insufficient values provided."""

    exception_message = "Insufficient data to fetch <{}>!"
