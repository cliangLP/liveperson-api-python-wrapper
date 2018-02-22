"""
An unofficial native Python wrapper for the LivePerson Messaging Operations API.

Documentation:
https://developers.liveperson.com/data-messaging-operations-overview.html

The Messaging Operations API extracts data according to the search query. The API allows agent managers to extract
information about their call center on the account, skill, and agent level. The data includes closed conversations
and their associated attributes, such as customer satisfaction, average conversation length, resolved status and so on.

Usage Example:
1. Choose User Service Login or OAuth1 Authentication.

    # For User Service Login
    > from lp_api_wrapper import UserLogin
    > auth = UserLogin(account_id='1234', username='YOURUSERNAME', password='YOURPASSWORD')

    # For OAuth1 Authentication
    > from lp_api_wrapper import OAuthLogin
    > auth = OAuthLogin(account_id='1234', app_key='K', app_secret='S', access_token='T', access_token_secret='TS')

2.  Import MessagingOperations and get data from connection

    > from lp_api_wrapper import MessagingOperations
    > mo_conn = MessagingOperations(auth=auth)
    > data = mo_conn.messaging_conversation(time_frame=1440, skill_ids='1,2' agent_ids='3,4', interval=1440)
"""

import requests
from lp_api_wrapper.util.login_service import LoginService, UserLogin, OAuthLogin
from typing import List, Optional, Union


class MessagingOperations(LoginService):
    def __init__(self, auth: Union[UserLogin, OAuthLogin]) -> None:
        super().__init__(auth=auth)
        self.am_domain = self.get_domain(service_name='leDataReporting')

    def messaging_conversation(self, time_frame: int, version: int = 1, skill_ids: Optional[str] = None,
                               agent_ids: Optional[str] = None, interval: Optional[int] = None) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data-messaging-operations-messaging-conversation.html

        Retrieves messaging conversation related metrics at the site, skill or agent level.

        :param time_frame: The time range (in minutes) by which the data can be filtered. Where: end time is the current
         time and the start time = end time - timeframe. The maximum timeframe value is 1440 minutes (24 hours).
        :param version: version of API e.g. v=1
        :param skill_ids: When provided, metrics on the response will be grouped by the requested skill/s' id/s.
         For each skill the metrics will be grouped per agent and also in total for all the skills specified.
         When neither skill nor agent ID are provided, metrics on the response will be calculated at the account level.
         If there is no data for the specified skill/s an object will be returned with an empty value for key:
         "metricsPerSkill" and "metricsTotal" key with a map including all metrics valued zero. You can provide one or
         more skill IDs.
         Example: skill_ids='4,15,3'. To retrieve all skills active for the time period use skill_ids='all'
        :param agent_ids: When provided, metrics on the response will be grouped by the requested agent/s' ID/s.
         The metrics will also be grouped in total for all specified agent/s' id/s. When neither skill nor agent ID
         are provided, metrics on the response will be calculated at the account level. If there is no data for the
         specified agent/s an object will be returned with an empty value for key: "metricsPerAgent" and "metricsTotal"
         key with a map including all metrics valued at zero. You can provide one or more skill IDs.
         Example: agent_ids='4,15,3'. To retrieve all skills active for the time period use agent_ids='all'
        :param interval: Interval size in minutes. When provided, the returned data will be aggregated by intervals of
         the requested size. The interval has to be smaller or equal to the time frame and also a divisor of the time
         frame. Example:
         time_frame=60 interval=30 (correct),
         time_frame=60 interval=61 (bad request),
         time_frame=60 interval=31 (bad request)
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Messaging Conversation URL
        url = 'https://{}/operations/api/account/{}/msgconversation'

        # Generate request
        r = requests.post(
            url=url.format(self.am_domain, self.account_id),
            json={'timeframe': time_frame, 'v': version, 'skillIds': skill_ids, 'agentIds': agent_ids,
                  'interval': interval},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def messaging_csat_distribution(self, time_frame: int, version: int = 1, skill_ids: Optional[str] = None,
                                    agent_ids: Optional[str] = None) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data-messaging-operations-messaging-csat-distribution.html

        Retrieves messaging CSAT (Customer Satisfaction) distribution related metrics at the site, skill or agent level.

        :param time_frame: The time range (in minutes) by which the data can be filtered. Where: end time is the current
         time and the start time is the end time - timeframe. The maximum timeframe value is 1440 minutes (24 hours).
        :param version: Version of API e.g. v=1
        :param skill_ids: When provided, metrics on the response will be grouped by the requested skill/s' id/s.
         For each skill the metrics will be grouped per agent and also in total for all the skills specified.
         When neither skill nor agent ID are provided, metrics on the response will be calculated at the account level.
         If there is no data for the specified skill/s an object will be returned with an empty value for key:
         "metricsPerSkill" and "metricsTotal" key with a map including all metrics valued zero.
         You can provide one or more skill IDs.
         Example: skill_ids='4,15,3'. To retrieve all skills active for the time period use skill_ids='all'
        :param agent_ids: When provided, metrics on the response will be grouped by the requested agent/s' ID/s.
         The metrics will also be grouped in total for all specified agent/s' id/s. When neither skill nor agent ID are
         provided, metrics on the response will be calculated at the account level. If there is no data for the
         specified agent/s an object will be returned with an empty value for key: "metricsPerAgent" and "metricsTotal"
         key with a map including all metrics valued at zero. You can provide one or more skill IDs.
         Example: agent_ids='4,15,3'. To retrieve all skills active for the time period use agent_ids='all'
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Messaging CSAT Distribution URL
        url = 'https://{}/operations/api/account/{}/msgcsatdistribution'

        # Generate request
        r = requests.get(
            url=url.format(self.am_domain, self.account_id),
            params={'timeframe': time_frame, 'v': version, 'skillIds': skill_ids, 'agentIds': agent_ids},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()
