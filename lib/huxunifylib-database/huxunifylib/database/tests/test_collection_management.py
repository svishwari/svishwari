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
                "name": "Tecton model 2",
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
                "name": "Tecton model 3",
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
            query_filter={db_c.ID: configurations[db_c.DOCUMENTS][0][db_c.ID]},
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
                "name": "Tecton model 2",
                "status": "Requested",
            },
        )

        self.assertIsNotNone(new_doc)

        self.assertTrue(
            dmg.delete_document(
                database=self.database,
                collection=db_c.CONFIGURATIONS_COLLECTION,
                query_filter={db_c.ID: new_doc[db_c.ID]},
                hard_delete=False,
            )
        )

        configuration = dmg.get_document(
            self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            query_filter={db_c.ID: new_doc[db_c.ID]},
        )
        self.assertIsNone(configuration)

        updated_doc = dmg.get_document(
            self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            query_filter={db_c.ID: new_doc[db_c.ID]},
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
                "name": "Tecton model 2",
                "status": "Requested",
            },
        )

        self.assertIsNotNone(configuration)

        self.assertTrue(
            dmg.delete_document(
                database=self.database,
                collection=db_c.CONFIGURATIONS_COLLECTION,
                query_filter={db_c.ID: configuration[db_c.ID]},
            )
        )

        configuration = dmg.get_document(
            self.database,
            collection=db_c.CONFIGURATIONS_COLLECTION,
            query_filter={db_c.ID: configuration[db_c.ID]},
        )
        self.assertIsNone(configuration)


class ModelsCollectionManagementTest(TestCase):
    """Test model collection management."""

    @mongomock.patch(servers=(("localhost", 27017),))
    def setUp(self):
        """Setup resources before each test."""

        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(db_c.DATA_MANAGEMENT_DATABASE)

        models = [
            {
                db_c.NAME: "Tecton model 1",
                db_c.TYPE: "Classification",
                db_c.CATEGORY: "Email",
                db_c.MODEL_DESCRIPTION: "Test model 1",
                db_c.MODEL_ID: "f6cedc82-5473-11ec-985a-b07d64f17254",
                db_c.STATUS: db_c.PENDING,
                db_c.ENABLED: True,
                db_c.ADDED: False,
            },
            {
                db_c.NAME: "Tecton model 2",
                db_c.TYPE: "Regression",
                db_c.CATEGORY: "Trust",
                db_c.MODEL_DESCRIPTION: "Test model 2",
                db_c.MODEL_ID: "1f7cf6b8-5474-11ec-ae92-b07d64f17254",
                db_c.STATUS: db_c.PENDING,
                db_c.ENABLED: True,
                db_c.ADDED: False,
            },
        ]

        self.models = [
            dmg.create_document(
                database=self.database,
                collection=db_c.MODELS_COLLECTION,
                new_doc=model,
                username="test_user",
            )
            for model in models
        ]

    def test_create_model_document(self):
        """Test creating a configuration document."""

        model_doc = {
            db_c.NAME: "Tecton model create",
            db_c.TYPE: "Test",
            db_c.CATEGORY: "Functionality Testing",
            db_c.MODEL_DESCRIPTION: "Test model creation",
            db_c.MODEL_ID: "7e1c9178-5474-11ec-a506-b07d64f17254",
            db_c.STATUS: db_c.PENDING,
            db_c.ENABLED: False,
            db_c.ADDED: False,
        }

        model = dmg.create_document(
            database=self.database,
            collection=db_c.MODELS_COLLECTION,
            new_doc=model_doc,
        )

        self.assertIsNotNone(model)
        self.assertEqual("unknown", model[db_c.CREATED_BY])
        self.assertEqual(model_doc[db_c.MODEL_ID], model[db_c.MODEL_ID])

        model_doc = {
            db_c.NAME: "Tecton model create 2",
            db_c.TYPE: "Test",
            db_c.CATEGORY: "Functionality Testing 2",
            db_c.MODEL_DESCRIPTION: "Test model creation",
            db_c.MODEL_ID: "05df00b4-5476-11ec-8374-b07d64f17254",
            db_c.STATUS: db_c.PENDING,
            db_c.ENABLED: False,
            db_c.ADDED: False,
        }
        model = dmg.create_document(
            database=self.database,
            collection=db_c.MODELS_COLLECTION,
            new_doc=model_doc,
            username="test_user",
        )

        self.assertIsNotNone(model)
        self.assertEqual("test_user", model[db_c.CREATED_BY])
        self.assertEqual(model_doc[db_c.MODEL_ID], model[db_c.MODEL_ID])

    def test_update_model_document(self):
        """Test update document"""
        update_doc = {
            db_c.TYPE: "Classification",
            db_c.NAME: "Updated tecton model",
            db_c.STATUS: db_c.ACTIVE,
            db_c.ENABLED: True,
        }
        updated_doc = update_document(
            self.database,
            collection=db_c.MODELS_COLLECTION,
            document_id=self.models[0][db_c.ID],
            update_doc=update_doc,
        )
        self.assertTrue(updated_doc)
        self.assertEqual(updated_doc[db_c.STATUS], update_doc[db_c.STATUS])

    def test_get_all_model_documents(self):
        """Test get all models via batch."""

        models = dmg.get_documents(
            database=self.database,
            collection=db_c.MODELS_COLLECTION,
        )

        self.assertEqual(len(self.models), len(models[db_c.DOCUMENTS]))

        for model in models[db_c.DOCUMENTS]:
            self.assertIn(
                model[db_c.TYPE],
                [x[db_c.TYPE] for x in self.models],
            )
            self.assertIn(
                model[db_c.NAME],
                [x[db_c.NAME] for x in self.models],
            )
            self.assertIn(
                model[db_c.ID],
                [x[db_c.ID] for x in self.models],
            )

        self.assertEqual(len(self.models), models["total_records"])

    def test_get_model_document(self):
        """Test to get model."""
        models = dmg.get_documents(
            self.database,
            collection=db_c.MODELS_COLLECTION,
        )
        model = dmg.get_document(
            self.database,
            collection=db_c.MODELS_COLLECTION,
            query_filter={db_c.ID: models[db_c.DOCUMENTS][0][db_c.ID]},
        )
        self.assertTrue(model)
        self.assertFalse(model[db_c.DELETED])
        self.assertEqual(
            models[db_c.DOCUMENTS][0][db_c.TYPE],
            model[db_c.TYPE],
        )

        model = dmg.get_document(
            self.database,
            collection=db_c.MODELS_COLLECTION,
            query_filter={
                db_c.MODEL_ID: models[db_c.DOCUMENTS][1][db_c.MODEL_ID]
            },
        )
        self.assertTrue(model)
        self.assertFalse(model[db_c.DELETED])
        self.assertEqual(
            models[db_c.DOCUMENTS][1][db_c.TYPE],
            model[db_c.TYPE],
        )

    def test_soft_delete_model(self):
        """Test deleting a model"""
        self.assertTrue(
            dmg.delete_document(
                database=self.database,
                collection=db_c.MODELS_COLLECTION,
                query_filter={db_c.ID: self.models[0][db_c.ID]},
                hard_delete=False,
            )
        )

        model = dmg.get_document(
            self.database,
            collection=db_c.MODELS_COLLECTION,
            query_filter={db_c.ID: self.models[0][db_c.ID]},
        )
        self.assertIsNone(model)

        updated_doc = dmg.get_document(
            self.database,
            collection=db_c.MODELS_COLLECTION,
            query_filter={db_c.ID: self.models[0][db_c.ID]},
            include_deleted=True,
        )
        self.assertTrue(updated_doc[db_c.DELETED])

    def test_hard_delete_model(self):
        """Test deleting a model"""

        self.assertTrue(
            dmg.delete_document(
                database=self.database,
                collection=db_c.MODELS_COLLECTION,
                query_filter={db_c.ID: self.models[1][db_c.ID]},
            )
        )

        model = dmg.get_document(
            self.database,
            collection=db_c.MODELS_COLLECTION,
            query_filter={db_c.ID: self.models[1][db_c.ID]},
        )
        self.assertIsNone(model)
