"""Database client tests."""
from unittest import TestCase, mock
import mongomock
from huxunifylib.database import constants as db_c
from pymongo import ASCENDING
import database.create_database_indexes as cdi


class TestCreateDBIndexes(TestCase):
    """Test the DB Indexes creation."""

    def setUp(self):
        """TestCase Initial Setup."""

        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # setup the mock DB client
        self.database = mongomock.MongoClient("localhost", 27017)

        self.addCleanup(mock.patch.stopall)

    def test_set_indexes(self):
        """Unit Test for set Indexes."""

        index_list = [
            (
                db_c.DATA_MANAGEMENT_DATABASE,
                db_c.CONSTANTS_COLLECTION,
                [(db_c.CONSTANT_NAME, ASCENDING)],
            ),
            (
                db_c.DATA_MANAGEMENT_DATABASE,
                db_c.INGESTION_JOBS_COLLECTION,
                [(db_c.DATA_SOURCE_ID, ASCENDING)],
            ),
        ]
        cdi.set_indexes(self.database, index_list)
        const_collection = self.database[db_c.DATA_MANAGEMENT_DATABASE][
            db_c.CONSTANTS_COLLECTION
        ]
        self.assertTrue(const_collection.index_information())

    def test_add_unique_compound_index(self):
        """Unit Test for set Indexes."""

        cdi.add_unique_compound_index(self.database)
        ing_collection = self.database[db_c.DATA_MANAGEMENT_DATABASE][
            db_c.INGESTED_DATA_COLLECTION
        ]

        self.assertTrue(list(ing_collection.list_indexes()))
