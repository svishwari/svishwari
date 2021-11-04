"""Purpose of this file is for holding methods to query and push data to JIRA
"""
from jira import JIRA, JIRAError
from huxunify.api import constants as api_c
from huxunify.api.config import get_config


class JiraConnection:
    """JIRA Connection class"""

    def __init__(self):
        """Initialize Jira Connection"""
        config = get_config()

        # get JIRA client
        self.jira_client = JIRA(
            server=config.JIRA_SERVER,
            options={
                "headers": {
                    **JIRA.DEFAULT_OPTIONS["headers"],
                    api_c.AUTHORIZATION: f"Bearer {config.JIRA_API_KEY}",
                }
            },
        )
        self.project_key = config.JIRA_PROJECT_KEY

    def check_jira_connection(self) -> bool:
        """Check JIRA connections status

        Returns:
            bool: True/False specifying if connection to JIRA is established

        """
        try:
            return self.get_project_details() is not None
        except JIRAError:
            return False

    def get_project_details(self) -> dict:
        """Fetch details of a JIRA project

        Args:

        Returns:
            dict: Dictionary of project details
        """
        project = self.jira_client.project(self.project_key)

        return dict(id=project.id, name=project.name, key=project.key)

    def create_jira_issue(
        self, issue_type: dict, summary: str, description: str
    ):
        """Create a new issue in JIRA

        Args:
            issue_type (str): Type of issue
            summary (str): Summary of issue
            description (str): Description of issue

        Returns:
            dict: Object of new issue created
        """
        issue_dict = {
            "project": {api_c.ID: self.get_project_details().get(api_c.ID)},
            "components": [{api_c.NAME: self.project_key}],
            "issuetype": {api_c.NAME: issue_type},
            "summary": summary,
            "description": description,
        }
        new_issue = self.jira_client.create_issue(fields=issue_dict)

        return {
            api_c.ID: new_issue.id,
            api_c.KEY: new_issue.key,
            api_c.TYPE: new_issue.fields.issuetype,
            api_c.SUMMARY: new_issue.fields.summary,
            api_c.DESCRIPTION: new_issue.fields.description,
        }
