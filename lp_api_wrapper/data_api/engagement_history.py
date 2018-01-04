"""
A Python wrapper for the LiveEngage Engagement History API
https://developers.liveperson.com/data-engagement-history-methods.html

The EngagementHistory class can login using LPA credentials via the Login Service API or can be authenticated
with an app_key, app_secret, access_token, and access_token_secret for an OAuth1 login.

1. Create Engagement History API connection

# For User Authentication
>>> user_info = {'username': 'LPA-USERNAME', 'password': 'LPA-PASSWORD'}
>>> eh_conn = EngagementHistory(account_id='123456789', user_info=user_info)

... OR

# For Oauth Authentication
>>> oauth = {'app_key': 'APPKEY', 'app_secret':'APPSECRET', 'access_token':'ATOKEN', 'access_token_secret':'ATSECRET'}
>>> eh_conn = EngagementHistory(account_id='123456789', oauth_info=oauth)

2. Get data from connection

# Data from single offset request
>>> body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
>>> data = eh_conn.engagements(body)

:author: Anthony Jones
:email: ajones (at) liveperson (dot) com
"""

import concurrent.futures
import requests
from lp_api_wrapper.login.login_service import LoginService


class EngagementHistory(LoginService):
    def __init__(self, account_id, user_info=None, oauth_info=None):
        super().__init__(account_id=account_id, user_info=user_info, oauth_info=oauth_info)
        self.eh_domain = self.get_domain(service_name='engHistDomain')

    def engagements(self, body: dict, offset: int = 0, limit: int = 100, sort: str = None):
        """
        * The method 'engagements' will return only 1 offset of a request. To return all engagement records within
        the start range, please use the method 'all_engagements'. It is useful to use this method first to test your
        request before using 'all_conversations'.

        Python wrapper for the LiveEngage Engagement History API: Retreive Engagement List by Criteria

        For further details and examples, please refer to the API documentation:
        https://developers.liveperson.com/data_api-engagement-history-methods.html

        :param body: REQUIRED Enter body parameters that are the same as the API documentation.
        :param offset: Specifies from which record to retrieve the chat. Default is 0.
        :param limit: Max amount of conversations to be received in the response.  Default and max is 100.
        :param sort: Sort the results in a predefined order.
        :return: Dictionary of the json data_api from the request.
        """

        url = 'https://{}/interaction_history/api/account/{}/interactions/search?'

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        r = requests.post(
            url=url.format(self.eh_domain, self.account_id),
            params={'offset': offset, 'limit': limit, 'sort': sort},
            json=body,
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def all_engagements(self, body: dict, offset: int = 0, limit: int = 100, sort: str = None,
                        max_concurrent_requests: int = 5):

        """
        * The method all_engagements will return ALL engagement history records within the start time range. Please use
        the method 'engagements' to verify that the original request works.

        Python wrapper for LiveEngage Engagement History API: Conversations for All Records

        For further details and examples, please refer to the API documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-conversations.html

        :param offset: Specifies from which record to retrieve the chat. Default is 0.
        :param limit: Max amount of conversations to be received in the response.  Default and max is 100.
        :param sort: Sort the results in a predefined order.
        :param body: Enter body parameters that are the same as the API documentation.
        :param max_concurrent_requests: Maximum concurrent requests
        :return: List of all interactionHistoryRecords within the start time range.
        """

        if 25 < max_concurrent_requests < 1:
            raise ValueError('Please choose between 1 and 25.')

        count = self.engagements(body, offset, limit, sort)['_metadata']['count']
        if count == 0:
            raise ValueError('There are 0 records for this request.')

        def all_records(o, l, s, b):
            if self.bearer:
                api_data = []
                for attempt in range(1, 3):
                    try:
                        c = self.engagements(body=b, offset=o, limit=l, sort=s)
                        api_data = c['interactionHistoryRecords']
                    except requests.HTTPError:
                        print('Ugh. This Bearer Token is bad. Grabbing new one [Attempt {}, Offset {}]'.format(
                            attempt, o))
                        self.user_login(self.user_info['username'], self.user_info['password'])
                        print('Got a shiny new bearer token! Account is logged in.')
                        continue
                    break
                return api_data
            else:
                c = self.engagements(body=b, offset=o, limit=l, sort=s)
                return c['interactionHistoryRecords']

        interaction_history_records = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_requests) as executor:
            future_requests = {
                executor.submit(all_records, offset, limit, sort, body):
                    offset for offset in range(0, count, 100)
            }

            for future in concurrent.futures.as_completed(future_requests):
                print('>>> Request for offset {} finished.'.format(future_requests[future]))
                data = future.result()
                interaction_history_records.extend(data)

        return interaction_history_records
