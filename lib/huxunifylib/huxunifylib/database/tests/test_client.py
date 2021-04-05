"""Database client tests."""

import unittest
import mongomock
from huxunifylib.database.client import DatabaseClient


class TestClient(unittest.TestCase):
    """Test the new MongoClient object."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_new_client(self):
        """Test that a new MongoClient object can be initialized."""

        # details based on a local MongoDB configuration
        host = "localhost"
        port = 27017
        username = ""
        password = ""

        # set up the database client
        client = DatabaseClient(host, port, username, password)

        # verify the setup
        self.assertTrue(client is not None)
        self.assertEqual(client.host, host)
        self.assertEqual(client.port, port)
