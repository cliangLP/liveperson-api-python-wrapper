"""
An unofficial native Python wrapper for the LivePerson Engagement History API

Reference:
https://developers.liveperson.com/data-engagement-history-methods.html

Brands can now search, filter and keep copies of chat transcripts and related data, for example surveys, to later
integrate and further analyze their data with third-party tools (DWH, CRM systems, etc.). 99.5 % of chat transcript data
is available within 5 minutes. All other chat transcript data (including metadata like Engagement Attributes) is
available for up to 2 hours after a chat has ended, and is stored for 13 months. The Engagement History API is based
on the REST architecture style.

Usage Example:
1. Import EngagementHistory

    > from lp_api_wrapper import EngagementHistory

2. Choose User Service Login or OAuth1 Authentication.

    # For User Authentication
    > user_info = {'username': 'LPA-USERNAME', 'password': 'LPA-PASSWORD'}
    > eh_conn = EngagementHistory(account_id='123456789', user_info=user_info)

    # For Oauth Authentication
    > oauth = {'app_key': 'APPKEY', 'app_secret':'APPSECRET', 'access_token':'ATOKEN', 'access_token_secret':'ATSECRET'}
    > eh_conn = EngagementHistory(account_id='123456789', oauth_info=oauth)

2. Get data from connection

    > body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
    > data = eh_conn.engagements(body)
"""

import concurrent.futures
import requests
from lp_api_wrapper.login.login_service import LoginService
from typing import List, Optional

__author__ = 'Anthony Jones'
__email__ = 'ajones@liveperson.com'


class EngagementHistory(LoginService):
    def __init__(self, account_id: str, user_info: Optional[dict] = None, oauth_info: Optional[dict] = None) -> None:
        super().__init__(account_id=account_id, user_info=user_info, oauth_info=oauth_info)
        self.eh_domain = self.get_domain(service_name='engHistDomain')

    def engagements(self, body: dict, offset: int = 0, limit: int = 100, sort: Optional[str] = None) -> dict:
        """
        This method returns engagements with all their metadata and related transcripts, based on a given filter,
        for example, time range, skill/s, keywords, etc.

        * RETURNS 1 OFFSET OF DATA.  For the complete data set of the date range, use the method 'all_engagements'.

        Reference:
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

        # Generate request
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

    def all_engagements(self, body, offset=0, limit=100, sort=None, max_concurrent_requests=5) -> List[dict]:
        """
        This method returns engagements with all their metadata and related transcripts, based on a given filter,
        for example, time range, skill/s, keywords, etc.

        * RETURNS ALL OFFSETS OF DATA.  Please use the method 'conversations' for testing.

        Reference:
        https://developers.liveperson.com/data_api-messaging-interactions-conversations.html

        :param offset: Specifies from which record to retrieve the chat. Default is 0.
        :param limit: Max amount of conversations to be received in the response.  Default and max is 100.
        :param sort: Sort the results in a predefined order.
        :param body: Enter body parameters that are the same as the API documentation.
        :param max_concurrent_requests: Maximum concurrent requests
        :return: List of all interactionHistoryRecords within the start time range.
        """

        # Set at 25 to prevent overloading API servers.
        if max_concurrent_requests > 25:
            raise ValueError('Please do not go over 25 concurrent requests.')

        count = self.engagements(body, offset, limit, sort)['_metadata']['count']
        # Method will breaks out if there are no records.
        if count == 0:
            raise ValueError('There are 0 records for this request.')

        # Inner function to process concurrent requests.
        def get_record(b, o, l, s):
            if self.bearer:
                # If User Login is used.
                api_data = []
                for attempt in range(1, 3):
                    try:
                        api_data = self.engagements(body=b, offset=o, limit=l, sort=s)['interactionHistoryRecords']
                    except requests.HTTPError:
                        print('Reconnecting... [Attempt {}, Offset {}]'.format(attempt, o))
                        self.user_login(self.user_info['username'], self.user_info['password'])
                        print('Woot! We have connection!')
                        continue
                    break
                return api_data
            else:
                # If OAuth1 is used.
                return self.engagements(body=b, offset=o, limit=l, sort=s)['interactionHistoryRecords']

        interaction_history_records = []
        # Multi-threading to handle multiple requests at a time.
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_requests) as executor:
            future_requests = {
                executor.submit(get_record, body, offset, limit, sort): offset for offset in range(0, count, 100)
            }

            for future in concurrent.futures.as_completed(future_requests):
                print('Info: Saving data from request with offset {}.'.format(future_requests[future]))
                # Add data to results.
                interaction_history_records.extend(future.result())

        return interaction_history_records
