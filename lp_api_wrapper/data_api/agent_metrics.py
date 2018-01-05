"""
An unofficial native Python wrapper for the LivePerson Agent Metrics API.

Reference:
https://developers.liveperson.com/data-messaging-agent-metrics-overview.html

The LiveEngage Messaging Agent Metrics API provides information about the current state of messaging agents in the
contact center. This API exposes different metrics for an overview of the agents’ behavior and performance including:
current status, number of open conversations, agent’s skills, load etc.

Usage Example:
1. Import AgentMetrics

    > from lp_api_wrapper import AgentMetrics

2. Choose User Service Login or OAuth1 Authentication.

    # For User Service Login
    > user_info = {'username': 'LPA-USERNAME', 'password': 'LPA-PASSWORD'}
    > am_conn = AgentMetrics(account_id='123456789', user_info=user_info)

    # For OAuth1 Authentication
    > oauth = {'app_key': 'APPKEY', 'app_secret':'APPSECRET', 'access_token':'ATOKEN', 'access_token_secret':'ATSECRET'}
    > am_conn = AgentMetrics(account_id='123456789', oauth_info=oauth)

3. Get data from connection

    > data = am_conn.summary()
"""

import requests
from lp_api_wrapper.login.login_service import LoginService
from typing import List, Optional

__author__ = 'Anthony Jones'
__email__ = 'ajones@liveperson.com'


class AgentMetrics(LoginService):
    def __init__(self, account_id: str, user_info: Optional[dict] = None, oauth_info: Optional[dict] = None) -> None:
        super().__init__(account_id=account_id, user_info=user_info, oauth_info=oauth_info)
        self.am_domain = self.get_domain(service_name='msgHist')

    def agent_status(self, status: Optional[List[str]] = None, agent_ids: Optional[List[str]] = None,
                     skill_ids: Optional[List[str]] = None, agent_group_ids: Optional[List[str]] = None) -> dict:
        """
        Returns the current state of logged in agents that are handling messaging conversations with all its
        related data, including status, number of open conversations, load, skills etc.

        Reference:
        https://developers.liveperson.com/data-messaging-interactions-methods-agent-status.html

        :param status: List of Agent’s statuses to be filtered
        :param agent_ids: List of agent ids - when provided, data will be returned for the specified agents who are in
         logged in state. If not provided, data on all logged in agents will be returned.
        :param skill_ids: List of skill ids - when provided, data will be returned for the agents with the specified
         skills who are in logged in state.
        :param agent_group_ids: List of agent group ids - when provided, data will be returned for the agents that are
         member of the specified agent groups who are in logged in state.
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Agent Status URL
        url = 'https://{}/messaging_history/api/account/{}/agent-view/status'

        # Generate request
        r = requests.post(
            url=url.format(self.am_domain, self.account_id),
            json={'status': status, 'agentIds': agent_ids, 'skillIds': skill_ids, 'agentGroupIds': agent_group_ids},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def summary(self, status: Optional[List[str]] = None, agent_ids: Optional[List[str]] = None,
                skill_ids: Optional[List[str]] = None, agent_group_ids: Optional[List[str]] = None) -> dict:
        """
        Returns a summary on the current state of the contact center. This includes number of agents in the different
        logged in statuses, weighted average of the agents’ load etc.

        Reference:
        https://developers.liveperson.com/data-messaging-interactions-methods-summary.html

        :param status: List of Agent's statuses to be filtered
        :param agent_ids: List of agent ids - when provided, data will be returned for the specified agents who are in
         logged in state. If not provided, data on all logged in agents will be returned.
        :param skill_ids: List of skill ids - when provided, data will be returned for the agents with the specified
         skills who are in logged in state.
        :param agent_group_ids: List of agent group ids - when provided, data will be returned for the agents that are
         member of the specified agent groups who are in logged in state.
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Summary URL
        url = 'https://{}/messaging_history/api/account/{}/agent-view/summary?'

        # Generate request
        r = requests.post(
            url=url.format(self.am_domain, self.account_id),
            json={'status': status, 'agentIds': agent_ids, 'skillIds': skill_ids, 'agentGroupIds': agent_group_ids},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()
