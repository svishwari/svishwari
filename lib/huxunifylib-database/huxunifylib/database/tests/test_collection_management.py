"""Database client collection management tests."""
from unittest import TestCase

import mongomock
from huxunifylib.database.client import DatabaseClient
from huxunifylib.database import constants as db_c
from huxunifylib.database import collection_management as dmg
import huxunifylib.database.db_exceptions as de
from huxunifylib.database.collection_management import update_document


class ConfigurationCollectionManagementTest(TestCase):
    """Test configuration collection management."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):
        """Setup resources before each test."""

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        configurations = [
            {
                "type": "model",
                "name": "Tecton model 1",
                "status": "Requested",
                "enabled": True,
            },
            {
                "type": "module",
                "name": "Data Management",
                "icon": "Icon1",
                "status": "Active",
                "description": "Sample description",
                "enabled": True,
            },
        ]

        self.configurations = [
            dmg.create_document(
                database=self.database,
                collection=db_c.CONFIGURATIONS_COLLECTION,
                new_doc=configuration,
                username="test_user",
            )
            for configuration in configurations
        ]

    def test_create_configuration_document(self):
        """Test creating a configuration document."""

        configuration = dmg.create_document(
            database=self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            new_doc={
                "type": "model",
                "name": "Tecton model 1",
                "status": "Requested",
            },
        )

        self.assertIsNotNone(configuration)
        self.assertEqual("unknown", configuration[db_c.CREATED_BY])

        configuration = dmg.create_document(
            database=self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            new_doc={
                "type": "model",
                "name": "Tecton model 1",
                "status": "Requested",
            },
            username="test_user",
        )

        self.assertIsNotNone(configuration)
        self.assertEqual("test_user", configuration[db_c.CREATED_BY])

    def test_update_document(self):
        """Test update document"""
        update_doc = {
            "type": "model",
            "name": "Tecton model 1",
            "status": "Active",
            "enabled": True,
        }
        updated_doc = update_document(
            self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            document_id=self.configurations[0][db_c.ID],
            update_doc=update_doc,
        )
        self.assertTrue(updated_doc)
        self.assertEqual(updated_doc[db_c.STATUS], update_doc[db_c.STATUS])

    def test_get_documents_configuration(self):
        """Test get all configurations via batch."""

        configurations = dmg.get_documents(
            database=self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
        )

        self.assertEqual(
            len(self.configurations), len(configurations[db_c.DOCUMENTS])
        )

        for configuration in configurations[db_c.DOCUMENTS]:
            self.assertIn(
                configuration[db_c.TYPE],
                [x[db_c.TYPE] for x in self.configurations],
            )
            self.assertIn(
                configuration[db_c.NAME],
                [x[db_c.NAME] for x in self.configurations],
            )
            self.assertIn(
                configuration[db_c.ID],
                [x[db_c.ID] for x in self.configurations],
            )

        self.assertEqual(
            len(self.configurations), configurations["total_records"]
        )

    def test_get_document_configuration(self):
        """Test to get configuration."""
        configurations = dmg.get_documents(
            self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
        )
        configuration = dmg.get_document(
            self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            document_id=configurations[db_c.DOCUMENTS][0][db_c.ID],
        )
        self.assertTrue(configuration)
        self.assertFalse(configuration[db_c.DELETED])
        self.assertEqual(
            configurations[db_c.DOCUMENTS][0][db_c.TYPE],
            configuration[db_c.TYPE],
        )

    def test_get_document_collection_not_exists(self):
        """Test to get configuration."""

        with self.assertRaises(de.InvalidValueException) as context:
            dmg.get_documents(
                self.database,
                collection="invalid_collection",
            )
        self.assertIsNotNone(context.exception)

    def test_delete_document_configuration(self):
        """Test deleting a configuration"""
        new_doc = dmg.create_document(
            database=self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            new_doc={
                "type": "model",
                "name": "Tecton model 1",
                "status": "Requested",
            },
        )

        self.assertIsNotNone(new_doc)

        self.assertTrue(
            dmg.delete_document(
                database=self.database,
                collection=db_c.CONFIGURATIONS_COLLECTION,
                document_id=new_doc[db_c.ID],
                hard_delete=False,
            )
        )

        configuration = dmg.get_document(
            self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            document_id=new_doc[db_c.ID],
        )
        self.assertIsNone(configuration)

        updated_doc = dmg.get_document(
            self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            document_id=new_doc[db_c.ID],
            include_deleted=True,
        )
        self.assertTrue(updated_doc[db_c.DELETED])

    def test_hard_delete_configuration(self):
        """Test deleting a configuration"""

        configuration = dmg.create_document(
            database=self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            new_doc={
                "type": "model",
                "name": "Tecton model 1",
                "status": "Requested",
            },
        )

        self.assertIsNotNone(configuration)

        self.assertTrue(
            dmg.delete_document(
                database=self.database,
                collection=db_c.CONFIGURATIONS_COLLECTION,
                document_id=configuration[db_c.ID],
            )
        )

        configuration = dmg.get_document(
            self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            document_id=configuration[db_c.ID],
        )
        self.assertIsNone(configuration)
