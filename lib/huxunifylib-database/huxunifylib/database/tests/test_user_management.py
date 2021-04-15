"""Database client user management tests."""

import unittest
import mongomock
from bson import ObjectId

import huxunifylib.database.db_exceptions
import huxunifylib.database.user_management as um
import huxunifylib.database.constants as c

from huxunifylib.database.client import DatabaseClient


class TestDataManagement(unittest.TestCase):
    """Test data management module."""

    def setUp(self) -> None:
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # Connect
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        # data source to be created
        self.sample_user = {
            c.OKTA_ID: "00ub0oNGTSWTBKOLGLNR",
            c.S_TYPE_EMAIL: "joe@deloitte.com",
            c.USER_ORGANIZATION: "deloitte",
            c.USER_DISPLAY_NAME: "joe smith",
            c.USER_ROLE: c.USER_ROLE_ADMIN,
            c.USER_PROFILE_PHOTO: "https://s3/unififed/3.png",
            c.USER_SUBSCRIPTION: [],
        }

        # set a user document
        self.user_doc = um.set_user(
            database=self.database,
            okta_id=self.sample_user[c.OKTA_ID],
            email_address=self.sample_user[c.S_TYPE_EMAIL],
            role=self.sample_user[c.USER_ROLE],
            organization=self.sample_user[c.USER_ORGANIZATION],
            subscriptions=self.sample_user[c.USER_SUBSCRIPTION],
            display_name=self.sample_user[c.USER_DISPLAY_NAME],
            profile_photo=self.sample_user[c.USER_PROFILE_PHOTO],
        )

    def test_set_user(self) -> None:
        """Test set_user routine

        Returns:
            Response: None
        """

        # set a user document, use a duplicate okta id
        user_doc = um.set_user(
            database=self.database,
            okta_id="hf7hr43f7hfr7h7",
            email_address="dave@deloitte.com",
            role=self.sample_user[c.USER_ROLE],
            organization=self.sample_user[c.USER_ORGANIZATION],
            subscriptions=self.sample_user[c.USER_SUBSCRIPTION],
            display_name=self.sample_user[c.USER_DISPLAY_NAME],
            profile_photo=self.sample_user[c.USER_PROFILE_PHOTO],
        )

        self.assertTrue(user_doc is not None)

    def test_duplicate_set_user(self) -> None:
        """Test duplicate set_user routine based on okta id

        Returns:
            Response: None
        """

        # set a user document, use a different okta id and email
        _ = um.set_user(
            database=self.database,
            okta_id="hf7hr43f7hfr7h7",
            email_address="dave@deloitte.com",
            role=self.sample_user[c.USER_ROLE],
            organization=self.sample_user[c.USER_ORGANIZATION],
            subscriptions=self.sample_user[c.USER_SUBSCRIPTION],
            display_name=self.sample_user[c.USER_DISPLAY_NAME],
            profile_photo=self.sample_user[c.USER_PROFILE_PHOTO],
        )

        with self.assertRaises(
            huxunifylib.database.db_exceptions.DuplicateName
        ):
            _ = um.set_user(
                database=self.database,
                okta_id="hf7hr43f7hfr7h7",
                email_address="joesmith@deloitte.com",
                role=self.sample_user[c.USER_ROLE],
                organization=self.sample_user[c.USER_ORGANIZATION],
                subscriptions=self.sample_user[c.USER_SUBSCRIPTION],
                display_name=self.sample_user[c.USER_DISPLAY_NAME],
                profile_photo=self.sample_user[c.USER_PROFILE_PHOTO],
            )

    def test_get_user(self) -> None:
        """Test get_user routine.

        Returns:
            Response: None
        """

        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        self.assertTrue(user_doc is not None)
        self.assertEqual(
            user_doc[c.USER_DISPLAY_NAME], self.user_doc[c.USER_DISPLAY_NAME]
        )

    def test_get_users(self) -> None:
        """Test get_all_users routine.

        Returns:
            Response: None
        """

        user_docs = um.get_all_users(database=self.database)

        self.assertIsNotNone(user_docs)

    def test_delete_user(self) -> None:
        """Test delete_data_source routine.

        Returns:
            Response: None
        """

        # create a user first
        user_doc = um.set_user(
            database=self.database,
            okta_id="hgf7hf8hdfgh7",
            email_address="russellw@deloitte.com",
            role=self.sample_user[c.USER_ROLE],
            organization=self.sample_user[c.USER_ORGANIZATION],
            subscriptions=self.sample_user[c.USER_SUBSCRIPTION],
            display_name=self.sample_user[c.USER_DISPLAY_NAME],
            profile_photo=self.sample_user[c.USER_PROFILE_PHOTO],
        )
        # validate user was created
        self.assertTrue(c.ID in user_doc)

        # remove the user
        success_flag = um.delete_user(self.database, user_doc[c.ID])
        self.assertTrue(success_flag)

        # ensure user does not exist anymore
        user_doc = um.get_user(self.database, user_doc[c.ID])
        self.assertIsNone(user_doc)

    def test_add_favorite(self) -> None:
        """Test function for adding manage_user_favorite routine.

        Returns:
            Response: None
        """

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        # test each component
        for component in c.FAVORITE_COMPONENTS:
            # generate source of truth
            component_id = ObjectId()

            # add favorite component
            update_doc = um.manage_user_favorites(
                self.database, user_doc[c.ID], component, component_id
            )

            # test non empty list first
            self.assertTrue(update_doc[c.USER_FAVORITES][component])

            # test to ensure the ID we added exists
            self.assertTrue(
                component_id in update_doc[c.USER_FAVORITES][component]
            )

    def test_delete_favorite(self) -> None:
        """Test function for deleting manage_user_favorite

        Returns:
            Response: None
        """

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        # test all the components
        for component in c.FAVORITE_COMPONENTS:
            # generate source of truth
            component_id = ObjectId()

            # add favorite component
            _ = um.manage_user_favorites(
                self.database, user_doc[c.ID], component, component_id
            )

            # now remove the favorite
            removed_doc = um.manage_user_favorites(
                self.database,
                user_doc[c.ID],
                component,
                component_id,
                delete_flag=True,
            )

            # test empty list first
            self.assertFalse(removed_doc[c.USER_FAVORITES][component])

    def test_duplicate_add_favorite(self) -> None:
        """Test function for duplicate adding manage_user_favorites routine.

        Returns:
            Response: None
        """

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        # test all the components
        for component in c.FAVORITE_COMPONENTS:
            # generate source of truth
            component_id = ObjectId()

            # add favorite component x2
            for _ in range(2):
                _ = um.manage_user_favorites(
                    self.database, user_doc[c.ID], component, component_id
                )

            # get user doc
            update_doc = um.get_user(self.database, user_doc[c.OKTA_ID])

            # test non empty list first
            self.assertTrue(update_doc[c.USER_FAVORITES][component])

            # test to ensure the ID we added exists
            self.assertTrue(
                component_id in update_doc[c.USER_FAVORITES][component]
            )

            # test to ensure the ID we added exists, only once!
            self.assertEqual(
                update_doc[c.USER_FAVORITES][component].count(component_id), 1
            )

    def test_set_dashboard_config(self) -> None:
        """Test function for manage_user_dashboard_config routine.

        Returns:
            Response: None
        """

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        # simulate a dashboard config
        pinned_key = "pin_key_perf_insights"
        pinned_value = True

        # set the config setting for a user
        updated_doc = um.manage_user_dashboard_config(
            self.database, user_doc[c.ID], pinned_key, pinned_value
        )

        # test pinned value key exists
        self.assertIn(pinned_key, updated_doc[c.USER_DASHBOARD_CONFIGURATION])

        # test pinned value is set correctly
        self.assertEqual(
            updated_doc[c.USER_DASHBOARD_CONFIGURATION][pinned_key],
            pinned_value,
        )

    def test_unset_dashboard_config(self) -> None:
        """Test delete_flag for manage_user_dashboard_config routine.

        Returns:
            Response: None
        """

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        # simulate a dashboard config
        pinned_key = "pin_customer_insights"
        pinned_value = True

        # set the config setting for a user first
        user_doc = um.manage_user_dashboard_config(
            self.database, user_doc[c.ID], pinned_key, pinned_value
        )

        # test pinned value key exists
        self.assertIn(pinned_key, user_doc[c.USER_DASHBOARD_CONFIGURATION])

        # test pinned value is set correctly
        self.assertEqual(
            user_doc[c.USER_DASHBOARD_CONFIGURATION][pinned_key],
            pinned_value,
        )

        # delete the config setting for a user
        updated_doc = um.manage_user_dashboard_config(
            self.database, user_doc[c.ID], pinned_key, None, delete_flag=True
        )

        # test pinned value key does not exist
        self.assertNotIn(
            pinned_key, updated_doc[c.USER_DASHBOARD_CONFIGURATION]
        )
