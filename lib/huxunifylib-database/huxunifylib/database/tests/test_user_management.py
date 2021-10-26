"""Database client user management tests."""

import unittest
import mongomock
from hypothesis import given, strategies as st

import huxunifylib.database.user_management as um
import huxunifylib.database.orchestration_management as am
import huxunifylib.database.engagement_management as em
import huxunifylib.database.constants as c

from huxunifylib.database.client import DatabaseClient
from huxunifylib.database.db_exceptions import (
    DuplicateName,
    DuplicateFieldType,
)


class TestUserManagement(unittest.TestCase):
    """Test user management module."""

    def setUp(self) -> None:
        # init mongo patch initially
        mongo_patch = mongomock.patch(servers=(("localhost", 27017),))
        mongo_patch.start()

        # Connect
        self.database = DatabaseClient(
            "localhost", 27017, None, None
        ).connect()

        self.database.drop_database(c.DATA_MANAGEMENT_DATABASE)

        # user to be created
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

        self.audience = am.create_audience(self.database, "Test Audience", [])

        # setting id to set engagement
        self.audience[c.OBJECT_ID] = self.audience[c.ID]

        self.engagement_id = em.set_engagement(
            self.database,
            "Engagement",
            "Engagement Description",
            [self.audience],
            "user1",
        )
        self.component_ids = {
            c.ENGAGEMENTS: self.engagement_id,
            c.AUDIENCES: self.audience[c.OBJECT_ID],
        }

    def test_set_user(self) -> None:
        """Test set_user routine."""

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

        self.assertIsNotNone(user_doc)

    def test_duplicate_set_user(self) -> None:
        """Test duplicate set_user routine based on okta id."""

        # set a user document, use a different okta id and email
        um.set_user(
            database=self.database,
            okta_id="hf7hr43f7hfr7h7",
            email_address="dave@deloitte.com",
            role=self.sample_user[c.USER_ROLE],
            organization=self.sample_user[c.USER_ORGANIZATION],
            subscriptions=self.sample_user[c.USER_SUBSCRIPTION],
            display_name=self.sample_user[c.USER_DISPLAY_NAME],
            profile_photo=self.sample_user[c.USER_PROFILE_PHOTO],
        )

        with self.assertRaises(DuplicateName):
            um.set_user(
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
        """Test get_user routine."""

        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        self.assertIsNotNone(user_doc)
        self.assertEqual(
            user_doc[c.USER_DISPLAY_NAME], self.user_doc[c.USER_DISPLAY_NAME]
        )

    def test_get_users(self) -> None:
        """Test get_all_users routine."""

        user_docs = um.get_all_users(database=self.database)

        self.assertIsNotNone(user_docs)

    @given(login_count=st.integers(min_value=0, max_value=9))
    def test_update_user_success(self, login_count: int) -> None:
        """Test update_user routine success.

        Args:
            login_count (int): login_count value to be updated in the user
                record.
        """

        # set update_doc dict to update the user_doc
        update_doc = {c.USER_LOGIN_COUNT: login_count + 1}
        user_doc = um.update_user(
            self.database, self.user_doc[c.OKTA_ID], update_doc
        )

        self.assertIsNotNone(user_doc)
        self.assertIn(c.USER_LOGIN_COUNT, user_doc)
        self.assertEqual(login_count + 1, user_doc[c.USER_LOGIN_COUNT])

    def test_update_user_failure_disallowed_field(self) -> None:
        """Test update_user routine failure with disallowed field."""

        # set update_doc dict to update the user_doc
        update_doc = {c.OKTA_ID: "jd63bsfd884bdsff7348"}

        with self.assertRaises(DuplicateFieldType):
            um.update_user(self.database, self.user_doc[c.OKTA_ID], update_doc)

    def test_delete_user(self) -> None:
        """Test delete_user routine."""

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
        success_flag = um.delete_user(self.database, user_doc[c.OKTA_ID])
        self.assertTrue(success_flag)

        # ensure user does not exist anymore
        user_doc = um.get_user(self.database, user_doc[c.OKTA_ID])
        self.assertIsNone(user_doc)

    def test_add_favorite(self) -> None:
        """Test function for adding manage_user_favorites routine."""

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        # test each component
        for component in c.FAVORITE_COMPONENTS:
            component_id = self.component_ids[component]

            # add favorite component
            update_doc = um.manage_user_favorites(
                self.database, user_doc[c.OKTA_ID], component, component_id
            )

            # test non empty list first
            self.assertTrue(update_doc[c.USER_FAVORITES][component])

            # test to ensure the ID we added exists
            self.assertTrue(
                component_id in update_doc[c.USER_FAVORITES][component]
            )

    def test_delete_favorite(self) -> None:
        """Test function for deleting via manage_user_favorites routine"""

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        # test all the components
        for component in c.FAVORITE_COMPONENTS:
            component_id = self.component_ids[component]

            # add favorite component
            um.manage_user_favorites(
                self.database, user_doc[c.OKTA_ID], component, component_id
            )

            # now remove the favorite
            removed_doc = um.manage_user_favorites(
                self.database,
                user_doc[c.OKTA_ID],
                component,
                component_id,
                delete_flag=True,
            )

            # test empty list first
            self.assertFalse(removed_doc[c.USER_FAVORITES][component])

    def test_duplicate_add_favorite(self) -> None:
        """Test function for duplicate adding manage_user_favorites routine."""

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        # test all the components
        for component in c.FAVORITE_COMPONENTS:
            component_id = self.component_ids[component]

            # add favorite component x2
            for _ in range(2):
                um.manage_user_favorites(
                    self.database, user_doc[c.OKTA_ID], component, component_id
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
        """Test function for manage_user_dashboard_config routine."""

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        # simulate a dashboard config
        pinned_key = "pin_key_perf_insights"
        pinned_value = True

        # set the config setting for a user
        updated_doc = um.manage_user_dashboard_config(
            self.database, user_doc[c.OKTA_ID], pinned_key, pinned_value
        )

        # test pinned value key exists
        self.assertIn(pinned_key, updated_doc[c.USER_DASHBOARD_CONFIGURATION])

        # test pinned value is set correctly
        self.assertEqual(
            updated_doc[c.USER_DASHBOARD_CONFIGURATION][pinned_key],
            pinned_value,
        )

    def test_unset_dashboard_config(self) -> None:
        """Test delete_flag for manage_user_dashboard_config routine."""

        # first get user before we modify
        user_doc = um.get_user(self.database, self.user_doc[c.OKTA_ID])

        # simulate a dashboard config
        pinned_key = "pin_customer_insights"
        pinned_value = True

        # set the config setting for a user first
        user_doc = um.manage_user_dashboard_config(
            self.database, user_doc[c.OKTA_ID], pinned_key, pinned_value
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
            self.database,
            user_doc[c.OKTA_ID],
            pinned_key,
            None,
            delete_flag=True,
        )

        # test pinned value key does not exist
        self.assertNotIn(
            pinned_key, updated_doc[c.USER_DASHBOARD_CONFIGURATION]
        )
