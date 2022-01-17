from unittest import TestCase, mock
from jira import JIRAError
from huxunify.api.data_connectors.jira import JiraConnection


class JiraConnectionTest(TestCase):
    """Tests for Jira Connection."""

    def tearDown(self) -> None:
        """Run after every class"""

        mock.patch.stopall()

    def test_jira_connection_success(self) -> None:
        """Test successful Jira Connection."""

        mock.patch(
            "huxunify.api.data_connectors.jira.JIRA",
            return_value=True,
        ).start()
        self.assertTrue(JiraConnection.check_jira_connection()[0])

    def test_jira_connection_error(self) -> None:
        """Test to cover Exceptions thrown while creating Jira instance."""

        # Observed while Unauthorized user is used.
        mock.patch(
            "huxunify.api.data_connectors.jira.JIRA",
            side_effect=JIRAError(),
        ).start()
        self.assertFalse(JiraConnection.check_jira_connection()[0])

        # Observed while wrong server URL is used.].
        mock.patch(
            "huxunify.api.data_connectors.jira.JIRA",
            side_effect=AttributeError(),
        ).start()
        self.assertFalse(JiraConnection.check_jira_connection()[0])

        mock.patch(
            "huxunify.api.data_connectors.jira.JIRA",
            side_effect=Exception(),
        ).start()
        self.assertFalse(JiraConnection.check_jira_connection()[0])


