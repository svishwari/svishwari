"""Purpose of this file is for storing the tests of cache_management.py"""
import unittest

import mongomock
from huxunifylib.database.cache_management import (
    create_cache_entry,
    get_cache_entry,
)
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.constants as c
from hypothesis import given, strategies as st


class TestCacheManagement(unittest.TestCase):
    """Test Cache Management Module"""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self) -> None:
        # Connect
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

    @mongomock.patch(servers=(("localhost", 27017),))
    @given(cache_key=st.text(min_size=1), cache_value=st.text(min_size=1))
    def test_create_cache_entry(self, cache_key: str, cache_value: str):
        """Test for cache entry

        Args:
            cache_key (str): name of the cache key.
            cache_value (str): name of the cache key value.
        """

        create_cache_entry(self.database, cache_key, cache_value)
        get_cache = get_cache_entry(self.database, cache_key)
        self.assertTrue(get_cache)
