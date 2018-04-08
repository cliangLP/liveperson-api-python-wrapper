"""
An unofficial native Python wrapper for the LivePerson Agent Metrics API.

Documentation:
https://developers.liveperson.com/data-messaging-agent-metrics-overview.html

The LiveEngage Messaging Agent Metrics API provides information about the current state of messaging agents in the
contact center. This API exposes different metrics for an overview of the agents’ behavior and performance including:
current status, number of open conversations, agent’s skills, load etc.

Usage Example:
1. Choose User Service Login or OAuth1 Authentication.

    # For User Service Login
    > from lp_api_wrapper import UserLogin
    > auth = UserLogin(account_id='1234', username='YOURUSERNAME', password='YOURPASSWORD')

    # For OAuth1 Authentication
    > from lp_api_wrapper import OAuthLogin
    > auth = OAuthLogin(account_id='1234', app_key='K', app_secret='S', access_token='T', access_token_secret='TS')

2. Import AgentMetrics and get data from connection
    > from lp_api_wrapper import AgentMetrics
    > am_conn = AgentMetrics(auth=auth)
    > data = am_conn.summary()
"""

import requests
from ..util import (LoginService, UserLogin, OAuthLogin)
from typing import List, Optional, Union


class AgentMetrics(LoginService):
    def __init__(self, auth: Union[UserLogin, OAuthLogin]) -> None:
        super().__init__(auth=auth)
        self.am_domain = self.get_domain(service_name='msgHist')

    def agent_status(self, status: Optional[List[str]] = None, agent_ids: Optional[List[str]] = None,
                     skill_ids: Optional[List[str]] = None, agent_group_ids: Optional[List[str]] = None) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data-messaging-interactions-methods-agent-status.html

        Returns the current state of logged in agents that are handling messaging conversations with all its
        related data, including status, number of open conversations, load, skills etc.

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
        Documentation:
        https://developers.liveperson.com/data-messaging-interactions-methods-summary.html

        Returns a summary on the current state of the contact center. This includes number of agents in the different
        logged in statuses, weighted average of the agents’ load etc.

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
