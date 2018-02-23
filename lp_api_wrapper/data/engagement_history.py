"""
An unofficial native Python wrapper for the LivePerson Engagement History API

Documentation:
https://developers.liveperson.com/data-engagement-history-methods.html

Brands can now search, filter and keep copies of chat transcripts and related data, for example surveys, to later
integrate and further analyze their data with third-party tools (DWH, CRM systems, etc.). 99.5 % of chat transcript data
is available within 5 minutes. All other chat transcript data (including metadata like Engagement Attributes) is
available for up to 2 hours after a chat has ended, and is stored for 13 months.

Usage Example:
1. Choose User Service Login or OAuth1 Authentication.

    # For User Service Login
    > from lp_api_wrapper import UserLogin
    > auth = UserLogin(account_id='1234', username='YOURUSERNAME', password='YOURPASSWORD')

    # For OAuth1 Authentication
    > from lp_api_wrapper import OAuthLogin
    > auth = OAuthLogin(account_id='1234', app_key='K', app_secret='S', access_token='T', access_token_secret='TS')

2. Import EngagementHistory and get data from connection

    > from lp_api_wrapper import EngagementHistory
    > eh_conn = EngagementHistory(auth=auth)
    > body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
    > data = eh_conn.engagements(body)
"""

import concurrent.futures
import requests
from lp_api_wrapper.util.login_service import LoginService, UserLogin, OAuthLogin
from typing import List, Optional, Union


class EngagementHistory(LoginService):
    def __init__(self, auth: Union[UserLogin, OAuthLogin]) -> None:
        super().__init__(auth=auth)
        self.eh_domain = self.get_domain(service_name='engHistDomain')

    def engagements(self, body: dict, offset: int = 0, limit: int = 100, sort: Optional[str] = None) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data_api-engagement-history-methods.html

        Note:
        WILL RETURN 1 OFFSET OF DATA.  For the complete data set of the date range, use the method 'all_engagements'.

        This method returns engagements with all their metadata and related transcripts, based on a given filter,
        for example, time range, skill/s, keywords, etc.

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

    def all_engagements(self, body: dict, offset: int = 0, limit: int = 100, sort: Optional[str] = None,
                        max_concurrent_requests: int = 5, debug: bool = False) -> Union[List, List[dict]]:
        """
        Documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-conversations.html

        Note:
        WILL RETURN ALL OFFSETS OF DATA.  Please use the method 'conversations' for testing.

        This method returns engagements with all their metadata and related transcripts, based on a given filter,
        for example, time range, skill/s, keywords, etc.

        :param offset: Specifies from which record to retrieve the chat. Default is 0.
        :param limit: Max amount of conversations to be received in the response.  Default and max is 100.
        :param sort: Sort the results in a predefined order.
        :param body: Enter body parameters that are the same as the API documentation.
        :param max_concurrent_requests: Maximum concurrent requests.
        :param debug: Shows status of requests.
        :return: List of all interactionHistoryRecords within the start time range.
        """

        count = self.engagements(body, offset, limit, sort)['_metadata']['count']
        # Returns an empty list
        if count == 0:
            return []

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
                        self.user_login(username=self.auth.username, password=self.auth.password)
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
                if debug:
                    print('Record Count: {}, Offset: {} finished.'.format(count, future_requests[future]))
                # Add data to results.
                interaction_history_records.extend(future.result())

        return interaction_history_records
