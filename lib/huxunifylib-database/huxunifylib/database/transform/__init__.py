"""Transform utilities."""

from functools import wraps
import hashlib
import pandas as pd


def hashed(func):
    """Hashing decorator.
    Args:
        func (func): function to be hashed.

    Returns:
        func: hashing wrapper decorator
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Hashing function.
        Args:
            args (tuple): function arguments.
            kwargs (dict): function keyword arguments.

        Returns:
            hex: hashed value
        """
        result = func(*args, **kwargs)
        if result is not None:
            return hashlib.sha256(result.encode("utf-8")).hexdigest()
        return None

    return wrapper


def bypass_if_any_empty(func):
    """Decorator for bypassing empty fields.

    Args:
        func (func): function with bypass of empty fields.

    Returns:
        func: bypass empty fields wrapper decorator.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Bypass empty fields in given arguments.
        Args:
            args (tuple): function arguments.
            kwargs (dict): function keyword arguments.

        Returns:
            func: decorated function result.
        """

        for arg_val in list(args) + list(kwargs.values()):
            if arg_val is pd.NA or arg_val is None or pd.isna(arg_val):
                return None

        return func(*args, **kwargs)

    return wrapper
