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

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_new_client_ssl_path(self):
        """Test that a new MongoClient object can be initialized."""

        # details based on a local MongoDB configuration
        host = "localhost"
        port = 27017
        username = ""
        password = ""
        ssl_path = "test.pem"

        # set up the database client
        client = DatabaseClient(host, port, username, password, ssl_path)

        # verify the setup
        self.assertIsNotNone(client)
        self.assertEqual(client.host, host)
        self.assertEqual(client.port, port)
        self.assertEqual(client.ssl_cert_path, ssl_path)

    @mongomock.patch(servers=(("localhost", 27017),))
    def test_new_client_ssl_flag(self):
        """Test that a new MongoClient object can be initialized."""

        # details based on a local MongoDB configuration
        host = "localhost"
        port = 27017
        username = ""
        password = ""
        ssl_flag = True

        # set up the database client
        client = DatabaseClient(
            host=host,
            port=port,
            username=username,
            password=password,
            ssl_flag=ssl_flag,
        )

        # verify the setup
        self.assertIsNotNone(client)
        self.assertEqual(client.host, host)
        self.assertEqual(client.port, port)
        self.assertEqual(client.ssl_flag, ssl_flag)
