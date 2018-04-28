"""
An unofficial native Python wrapper for the LivePerson Data Access (BETA) API.

Documentation:
https://developers.liveperson.com/data-data-access-overview.html

The LiveEngage Data Access API provides brands with the ability to address specific Goals and KPIs while also extending
the reporting capabilities of their account by accessing their entire raw data. The data includes full information about
their agents’ activities and visitors’ journeys.

Usage Example:
1. Choose User Service Login or OAuth1 Authentication.

    # For User Service Login
    > from lp_api_wrapper import UserLogin
    > auth = UserLogin(account_id='1234', username='YOURUSERNAME', password='YOURPASSWORD')

    # For OAuth1 Authentication
    > from lp_api_wrapper import OAuthLogin
    > auth = OAuthLogin(account_id='1234', app_key='K', app_secret='S', access_token='T', access_token_secret='TS')

TODO: FIX EXAMPLE
2. Import AgentMetrics and get data from connection
    > from lp_api_wrapper import AgentMetrics
    > am_conn = AgentMetrics(auth=auth)
    > data = am_conn.summary()

"""

import requests
from ..util import (LoginService, UserLogin, OAuthLogin)
from typing import List, Optional, Union


class DataAccess(LoginService):
    def __init__(self, auth: Union[UserLogin, OAuthLogin]) -> None:
        super().__init__(auth=auth)
        # TODO: ADD other domains for UK & SY
        self.da_domain = 'va.da.liveperson.net'

    def agent_activity(self, start_time: int, end_time: int) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data-data-access-agent-activity.html

        Agent Activity retrieves the agent’s session data in .zip format files. The agent’s activity data is a list of
        sessions which occur from the agent’s login time to the agent’s logout time. This data is used to analyze agent
        efficiency and availability. Each session includes the agent’s information, such as login name, nickname, status
        changes, number of concurrent chats, etc.

        :param start_time: Start time in milliseconds, refers to the start time boundary of the range the files were
        generated. Should be used as an incremental timestamp.
        :param end_time: in milliseconds, refers to the start time boundary of the range the files were generated.
        Should be used as an incremental timestamp.
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Agent Status URL
        url = 'https://{}/data_access_le/account/{}/le/webSession?startTime={}&endTime={}'


        # Generate request, NOTE: USING GET NOT POST
        r = requests.get(
            url=url.format(self.da_domain, self.account_id, start_time, end_time),
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print(r.text)
            print(r.status_code)
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def web_session(self, start_time: int, end_time: int) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data-data-access-web-session.html

        Web session retrieves the list of files in zip format of the visitor’s web session data.

        :param start_time: Start time in milliseconds, refers to the start time boundary of the range the files were
        generated. Should be used as an incremental timestamp.
        :param end_time: in milliseconds, refers to the start time boundary of the range the files were generated.
        Should be used as an incremental timestamp.
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Agent Status URL
        url = 'https://{}/data_access_le/account/{}/le/agentActivity?startTime={}&endTime={}'

        # Generate request, NOTE: USING GET NOT POST
        r = requests.get(
            url=url.format(self.da_domain, self.account_id, start_time, end_time),
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print(r.text)
            print(r.status_code)
            print('Error: {}'.format(r.json()))
            r.raise_for_status()