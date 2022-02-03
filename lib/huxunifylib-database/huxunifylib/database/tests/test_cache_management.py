"""Purpose of this file is for storing the tests of cache_management.py"""
import unittest
from unittest import mock

import mongomock
import pymongo.errors
from hypothesis import given, strategies as st

from huxunifylib.database.cache_management import (
    create_cache_entry,
    get_cache_entry,
)
from huxunifylib.database.client import DatabaseClient
import huxunifylib.database.constants as db_c


class TestCacheManagement(unittest.TestCase):
    """Test Cache Management Module"""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self) -> None:
        # Connect
        self.database = DatabaseClient(host="localhost", port=27017).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

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

        # Ensure works in Azure Setting.
        create_cache_entry(
            self.database,
            cache_key,
            cache_value,
            platform=db_c.AZURE_COSMOS_DB,
        )
        get_cache = get_cache_entry(self.database, cache_key)
        self.assertTrue(get_cache)

        self.assertRaises(
            pymongo.errors.OperationFailure,
            create_cache_entry(self.database, "asdfb", cache_value),
        )

        mock.patch.stopall()
