"""
A Python wrapper for the LiveEngage Messaging Interactions API
https://developers.liveperson.com/data-messaging-interactions-overview.html

The MessagingInteractions class can login using LPA credentials via the Login Service API or can be authenticated
with an app_key, app_secret, access_token, and access_token_secret for an OAuth1 login.

1. Import MessagingInteractions

>>> from lp_api_wrapper import MessagingInteractions

2. Create Messaging Interaction API connection

# For User Authentication
>>> user_info = {'username': 'LPA-USERNAME', 'password': 'LPA-PASSWORD'}
>>> mi_conn = MessagingInteractions(account_id='123456789', user_info=user_info)

... OR

# For Oauth Authentication
>>> oauth = {'app_key': 'APPKEY', 'app_secret':'APPSECRET', 'access_token':'ATOKEN', 'access_token_secret':'ATSECRET'}
>>> mi_conn = MessagingInteractions(account_id='123456789', oauth_info=oauth)

3. Get data from connection

# Data from single offset request
>>> body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
>>> data = mi_conn.conversations(body)


:author: Anthony Jones
:email: ajones (at) liveperson (dot) com
"""

import concurrent.futures
import requests
from lp_api_wrapper import LoginService
from typing import List


class MessagingInteractions(LoginService):
    def __init__(self, account_id, user_info=None, oauth_info=None):
        super().__init__(account_id=account_id, user_info=user_info, oauth_info=oauth_info)
        self.mi_domain = self.get_domain(service_name='msgHist')

    def conversations(self, body: dict, offset: int = 0, limit: int = 100, sort: str = None):

        """
        * The method 'conversation' will return only 1 offset of a request. To return all conversations records within
        the start range, please use the method 'all_conversations'. It is useful to use this method first to test your
        request before using 'all_conversations'.

        Python wrapper for LiveEngage Messaging Interactions API: Conversations

        For further details and examples, please refer to the API documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-conversations.html

        :param body: REQUIRED Enter body parameters that are the same as the API documentation.
        :param offset: Specifies from which record to retrieve the chat. Default is 0.
        :param limit: Max amount of conversations to be received in the response.  Default and max is 100.
        :param sort: Sort the results in a predefined order.
        :return: Dictionary of the json data_api from the request.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        url = 'https://{}/messaging_history/api/account/{}/conversations/search?'

        r = requests.post(
            url=url.format(self.mi_domain, self.account_id),
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

    def all_conversations(self, body: dict, offset: int = 0, limit: int = 100, sort: str = None,
                          max_concurrent_requests: int = 5):

        """
        * The method all_conversations will return ALL conversation records within the start time range.  Please use 
        the conversations method to verify that the original request works.
        
        Python wrapper for LiveEngage Messaging Interactions API: Conversations for All Records

        For further details and examples, please refer to the API documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-conversations.html

        :param start_from: REQUIRED Conversation's start time range. Epoch time in milliseconds.
        :param start_to: REQUIRED Conversation's start time range. Epoch time in milliseconds.
        :param offset: Specifies from which record to retrieve the chat. Default is 0.
        :param limit: Max amount of conversations to be received in the response.  Default and max is 100.
        :param sort: Sort the results in a predefined order.
        :param body: Enter body parameters that are the same as the API documentation.
        :param max_concurrent_requests: Maximum concurrent requests
        :return: List of all conversationHistoryRecords within the start time range.
        """

        if 25 < max_concurrent_requests < 1:
            raise ValueError('Please choose between 1 and 25.')

        count = self.conversations(body=body, offset=offset, limit=limit, sort=sort)['_metadata']['count']
        if count == 0:
            raise ValueError('There are 0 records for this request.')

        def all_records(b, o, l, s):
            if self.bearer:
                api_data = []
                for attempt in range(1, 3):
                    try:
                        c = self.conversations(body=b, offset=o, limit=l, sort=s)
                        api_data = c['conversationHistoryRecords']
                    except requests.HTTPError:
                        print('Ugh. This Bearer Token is bad. Grabbing new one [Attempt {}, Offset {}]'.format(
                            attempt, o))
                        self.user_login(self.user_info['username'], self.user_info['password'])
                        print('Got a shiny new bearer token! Account is logged in.')
                        continue
                    break
                return api_data
            else:
                c = self.conversations(body=b, offset=o, limit=l, sort=s)
                return c['conversationHistoryRecords']

        conversation_records = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_requests) as executor:
            future_requests = {
                executor.submit(all_records, body, offset, limit, sort):
                    offset for offset in range(0, count, 100)
            }

            for future in concurrent.futures.as_completed(future_requests):
                print('>>> Request for offset {} finished.'.format(future_requests[future]))
                data = future.result()
                conversation_records.extend(data)

        return conversation_records

    def get_conversation_by_conversation_id(self, conversation_id: str):
        """
        Python wrapper for LiveEngage Messaging Interactions API: Conversations

        For further details and examples, please refer to the API documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-get-conversation-by-conversation-id.html

        :param conversation_id: ID of the conversation to search.
        :return: Dictionary with same structure as the returned JSON value from the API.
        """
        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        url = 'https://{}/messaging_history/api/account/{}/conversations/conversation/search'

        r = requests.post(
            url=url.format(self.mi_domain, self.account_id),
            json={'conversationId': conversation_id},
            **auth_args
        )

        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def get_conversations_by_consumer_id(self, consumer_id: str, status: List[str] = None):
        """
        Python wrapper for LiveEngage Messaging Interactions API: Conversations

        For further details and examples, please refer to the API documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-get-conversations-by-consumer-id.html

        :param consumer_id: ID of the consumer to search.
        :param status: Latest status of the conversation. Valid values: OPEN, CLOSE
        :return: Dictionary with same structure as the returned JSON value from the API.
        """
        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        url = 'https://{}/messaging_history/api/account/{}/conversations/consumer/search'

        r = requests.post(
            url=url.format(self.mi_domain, self.account_id),
            json={'consumer': consumer_id, 'status': status},
            **auth_args
        )

        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()
