"""Purpose of this file is for interacting with aws"""

from typing import Union, Callable

from huxunifylib.util.general.logging import logger
from huxunifylib.database.cache_management import (
    get_cache_entry,
    create_cache_entry,
)

from huxunify.api.route.utils import get_db_client


class Caching:
    """Interact with Caching Service."""

    @staticmethod
    def check_and_return_cache(
        cache_key: str,
        method: Callable,
        keyword_arguments: dict,
    ) -> Union[list, dict]:
        """Checks for cache to return or creates an entry
        Args:
            cache_key(str): Cache key
            method(Callable): Method to retrieve data if there is no cache
            keyword_arguments(dict): Keyword arguments for method

        Returns:
            Union[list,dict]: Data to be retrieved

        """
        database = get_db_client()
        data = get_cache_entry(database, cache_key)

        if not data:
            logger.info("No cache data available, retrieving actual data")
            data = method(**keyword_arguments)
            create_cache_entry(
                database=database,
                cache_key=cache_key,
                cache_value=data,
            )

        return data
