"""
A Python wrapper for the LiveEngage Agent Metrics API
https://developers.liveperson.com/data-messaging-agent-metrics-overview.html

The AgentMetrics class can login using LPA credentials via the Login Service API or can be authenticated
with an app_key, app_secret, access_token, and access_token_secret for an OAuth1 login.

1. Import AgentMetrics

>>> from lp_api_wrapper import AgentMetrics

2. Create Agent Metrics API connection

# For User Authentication
>>> user_info = {'username': 'LPA-USERNAME', 'password': 'LPA-PASSWORD'}
>>> am_conn = AgentMetrics(account_id='123456789', user_info=user_info)

... OR

# For Oauth Authentication
>>> oauth = {'app_key': 'APPKEY', 'app_secret':'APPSECRET', 'access_token':'ATOKEN', 'access_token_secret':'ATSECRET'}
>>> am_conn = AgentMetrics(account_id='123456789', oauth_info=oauth)

3. Get data from connection

# Data from single offset request
>>> data = am_conn.summary()


:author: Anthony Jones
:email: ajones (at) liveperson (dot) com
"""

import requests
from lp_api_wrapper.login.login_service import LoginService


class AgentMetrics(LoginService):
    def __init__(self, account_id, user_info=None, oauth_info=None):
        super().__init__(account_id=account_id, user_info=user_info, oauth_info=oauth_info)
        self.am_domain = self.get_domain(service_name='msgHist')

    def agent_status(self, body):
        """

        :param body:
        :return:
        """
        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        url = 'https://{}/messaging_history/api/account/{}/agent-view/status'

        r = requests.post(
            url=url.format(self.am_domain, self.account_id),
            json=body,
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def summary(self, url_parameters: dict = None):
        """

        :param url_parameters:
        :return:
        """
        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        url = 'https://{}/messaging_history/api/account/{}/agent-view/summary'

        r = requests.post(
            url=url.format(self.am_domain, self.account_id),
            params=url_parameters,
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()
