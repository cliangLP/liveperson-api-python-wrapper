"""
An unofficial native Python wrapper for the LivePerson Operational Realtime API.

Documentation:
https://developers.liveperson.com/data-operational-realtime-overview.html

The LiveEngage Operational Real-Time API provides real-time information about contact center performance.
Using this API, Agent Managers can measure contact center performance at account level, at skill level, or even drill
down to agent level. Data is provided for the previous 24 hours, up to the last 5 minutes, with a refresh rate of 10
seconds.

Usage Example:
1. Choose User Service Login or OAuth1 Authentication.

    # For User Service Login
    > from lp_api_wrapper import UserLogin
    > auth = UserLogin(account_id='1234', username='YOURUSERNAME', password='YOURPASSWORD')

    # For OAuth1 Authentication
    > from lp_api_wrapper import OAuthLogin
    > auth = OAuthLogin(account_id='1234', app_key='K', app_secret='S', access_token='T', access_token_secret='TS')

2. Import OperationalRealtime and get data from connection

    > from lp_api_wrapper import OperationalRealtime
    > or_conn = OperationalRealtime(auth=auth)
    > data = or_conn.queue_health(time_frame=1440, skill_ids='1,2', interval=1440)
"""

import requests
from ..util import (LoginService, UserLogin, OAuthLogin)
from typing import Optional, Union


class OperationalRealtime(LoginService):
    def __init__(self, auth: Union[UserLogin, OAuthLogin]) -> None:
        super().__init__(auth=auth)
        self.am_domain = self.get_domain(service_name='leDataReporting')

    def queue_health(self, time_frame: int, version: int = 1, skill_ids: Optional[str] = None,
                     interval: Optional[int] = None) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data-operational-realtime-queue-health.html

        Retrieves queue-related metrics at the account or skill level.

        :param time_frame: The time range (in minutes) by which the data can be filtered. Where: end time is the current
         time and the start time = end time - timeframe. The maximum timeframe value is 1440 minutes (24 hours).
        :param version: version of API e.g. v=1
        :param skill_ids: When provided, metrics on the response will be grouped by the requested skills. When not
         provided, metrics on the response will be calculated at the account level. You can provide one or more
         skillIDs.
         Example: skill_ids='4,153'. To retrieve all skills active for the time period, use skill_ids='all'.
        :param interval: Interval size in minutes. When provided, the returned data will be aggregated by intervals of
         the requested size. The interval has to be smaller or equal to the time frame and also a divisor of the time
         frame.
         Example:
         time_frame=60 interval=30 (correct),
         time_frame=60 interval=61 (bad request),
         time_frame=60 interval=31 (bad request)
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Queue Health URL
        url = 'https://{}/operations/api/account/{}/queuehealth'

        # Generate request
        r = requests.get(
            url=url.format(self.am_domain, self.account_id),
            params={'timeframe': time_frame, 'v': version, 'skillIds': skill_ids, 'interval': interval},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def engagement_activity(self, time_frame: int, version: int = 1, skill_ids: Optional[str] = None,
                            agent_ids: Optional[str] = None, interval: Optional[int] = None) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data-operational-realtime-engagement-activity.html

        Retrieves engagement activity-related metrics at the account, skill, or agent level.

        :param time_frame: The time range (in minutes) in which the data can be filtered.
         Where end time = current time, and start time = end time - timeframe. The maximum timeframe value is
         1440 minutes (24 hours).
        :param version: Version of API, for example, v=1.
        :param skill_ids: When provided, metrics on the response will be grouped by the requested skill/s' id/s.
         For each skill, the metrics will be grouped per agent and also in total for all the skills specified.
         When neither skill id nor agent ID are provided, metrics on the response will be calculated at the account
         level. If there is no data for the specified skill/s, an object will be returned with an empty value for
         key: "metricsPerSkill" and "metricsTotal" key, with a map including all metrics valued zero. You can provide
         one or more skill IDs.
         Example: skill_ids='4,15,3'. To retrieve all skills active for the time period, use skill_ids='all'.
        :param agent_ids: When provided, metrics on the response will be grouped by the requested agent/s' ID/s.
         The metrics will also be grouped in total for all specified agent/s' id/s. When neither skill id nor agent ID
         are provided, metrics on the response will be calculated at the account level. If there is no data for the
         specified agent/s, an object will be returned with an empty value for key: "metricsPerAgent" and "metricsTotal"
         key, with a map including all metrics valued zero. You can provide one or more skillIDs.
         Example: agent_ids='4,15,3'. To retrieve all skills active for the time period, use agent_ids='all'.
        :param interval: Interval size in minutes (the minimum value is five minutes). When provided, the returned data
         will be aggregated by intervals of the requested size. The interval has to be smaller or equal to the time
         frame, and also a divisor of the time frame.
         Example:
         time_frame=60 interval=30 (correct)
         time_frame=60 interval=61 (bad request)
         time_frame=60 interval=31 (bad request)
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Engagement Activity URL
        url = 'https://{}/operations/api/account/{}/engactivity'

        # Generate request
        r = requests.get(
            url=url.format(self.am_domain, self.account_id),
            params={'timeframe': time_frame, 'v': version, 'agentIds': agent_ids, 'skillIds': skill_ids,
                    'interval': interval},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def agent_activity(self, time_frame: int, agent_ids: str, version: int = 1, interval: Optional[int] = None) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data-operational-realtime-agent-activity.html

        Retrieves Agent State Distribution data, which includes the following states:

        * Logged in (total of all states)
        * Online
        * Away
        * Back soon

        For each state, the following is indicated:

        * Time spent chatting
        * Time spent not chatting
        * Time spent logged in and chatting concurrently with the maximum allowed chats

        :param time_frame: The time range (in minutes) in which the data can be filtered. Where end time = current time,
         and start time = end time - timeframe.
        :param version: Version of API, for example, v=1.
        :param agent_ids: When provided, metrics on the response will be grouped by the requested agents' IDs.
         If there is no data for the specified agents, an object will be returned with an empty value for key:
         "metricsPerAgent" with a map including all metrics valued zero. To retrieve all active agents for the time
         period, use agent_ids='all'.
        :param interval: Interval size in minutes (the minimum value is five minutes). When provided, the returned data
         will be aggregated by intervals of the requested size. The interval has to be smaller or equal to the time
         frame, and also a divisor of the time frame.
         Example:
         time_frame=60 interval=30 (correct)
         time_frame=60 interval=61 (bad request)
         time_frame=60 interval=31 (bad request)
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Agent Activity URL
        url = 'https://{}/operations/api/account/{}/agentactivity'

        # Generate request
        r = requests.post(
            url=url.format(self.am_domain, self.account_id),
            json={'timeframe': time_frame, 'agentIds': agent_ids, 'v': version, 'interval': interval},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def current_queue_state(self, version: int = 1, skill_ids: Optional[str] = None) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data-operational-realtime-current-queue-state.html

        Retrieves the current queue state related metrics at the skill level:

        * Current queue size
        * Current available slots

        :param version: Version of API, for example, v=1.
        :param skill_ids: When provided, metrics on the response will be grouped by the requested skills.
        When not provided, the default will be 'skillIds=all’, and metrics on the response will be calculated by all
        skills with queue state data. You can provide one or more skill IDs.
        Example: skill_ids='4,15,3'. To retrieve all skills active for the time period use skill_ids='all'
        (same as default if not provided).
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Engagement Activity URL
        url = 'https://{}/operations/api/account/{}/queuestate'

        # Generate request
        r = requests.get(
            url=url.format(self.am_domain, self.account_id),
            params={'v': version, 'skillIds': skill_ids},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def sla_histogram(self, time_frame: int, version: int = 1, skill_ids: Optional[str] = None,
                      group_ids: Optional[str] = None, histogram: Optional[str] = None) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data-operational-realtime-sla-histogram.html

        Retrieves the distribution of visitors’ wait time in the queue, before an agent replies to their chat. The wait
        time in the histogram is accurate (no more than +/- 5 seconds). Histogram bucket sizes are specified in
        multiples of 5 seconds.

        :param time_frame: The time range (in minutes) in which the data can be filtered. Where end time = current time,
         and start time = end time - timeframe. The maximum timeframe value is 1440 minutes (24 hours).
        :param version: Version of API, for example, v=1.
        :param skill_ids: When provided, SLA will be calculated only for interactions involving agents of the specified
         skills. You can provide one or more skill IDs.
         Example: skill_ids='4,15,3'. To retrieve all skills active for the time period, use skill_ids='all'.
         If no skillIds is provided, 'all’ is assumed.
        :param group_ids: When provided, SLA will be calculated only for interactions involving agents of the specified
         groups. You can provide one or more agent group IDs.
         Example: group_ids='4,15,3'. To retrieve all agent groups active for the time period, use group_ids='all'.
         If no group_ids is provided, 'all’ is assumed.
        :param histogram: Histogram bucket ranges (in seconds). Values in the list must be multiples of 5 seconds.
         Each value is taken as the lower limit of a bucket. The value '0’ is always assumed to be part of the
         histogram. The highest value in the histogram will bucket all waiting times that are higher.
         Example: histogram='0,50,100,200,400,1000'
         If no histogram is provided, the default histogram is assumed: '0,15,30,45,60,90,120'
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # SLA Histogram URL
        url = 'https://{}/operations/api/account/{}/sla'

        # Generate request
        r = requests.get(
            url=url.format(self.am_domain, self.account_id),
            params={'timeframe': time_frame, 'v': version, 'skillIds': skill_ids, 'groupIds': group_ids,
                    'histogram': histogram},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()
