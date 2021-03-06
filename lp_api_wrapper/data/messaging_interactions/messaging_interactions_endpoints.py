"""
An unofficial native Python wrapper for the LivePerson Messaging Interactions API

Documentation:
https://developers.liveperson.com/data-messaging-interactions-overview.html

The LiveEngage Messaging Interactions API retrieves the most up to date information available about contact center
messaging interactions. This API makes it possible to search, filter and analyze data and transcripts of
open and closed conversations.

The API returns the conversation’s transcripts and all of its related metadata such as start time, end time, MCS, CSAT,
summary, participated agents, the reason the conversation was closed etc.
"""

import concurrent.futures
import requests
from ...util.login_service import (LoginService, UserLogin, OAuthLogin)
from typing import List, Optional, Union


class MessagingInteractionsEndpoints(LoginService):
    def __init__(self, auth: Union[UserLogin, OAuthLogin]) -> None:
        super().__init__(auth=auth)
        self.mi_domain = self.get_domain(service_name='msgHist')

    def conversations_endpoint(self, body: dict, url_parameters: dict) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-conversations.html

        This method retrieves conversations with all their metadata and related messages based on a predefined search
        criteria. Search criteria includes filtering by time range, agent, skill, etc.

        :param body: REQUIRED Enter body parameters that are the same as the API documentation.
        :param url_parameters: REQUIRED Enter url parameters that are the same as the API documentation.
        :return: Dictionary with same structure as the JSON data from the API.
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Conversations URL
        url = 'https://{}/messaging_history/api/account/{}/conversations/search?'

        # Generate request
        r = requests.post(
            url=url.format(self.mi_domain, self.account_id),
            params=url_parameters,
            json=body,
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def all_conversations(self, body: dict, offset: int = 0, limit: int = 100, sort: Optional[str] = None,
                          max_concurrent_requests: int = 5, debug: bool = False) -> Union[List, List[dict]]:
        """
        Method is deprecated.  Please use 'conversations' in MessagingInteractions.  Will remove this at a later date.

        Documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-conversations.html

        This method retrieves a list of conversations with all their metadata and related messages based on a
        predefined search criteria. Search criteria includes filtering by time range, agent, skill, etc.

        Note:
        WILL RETURN ALL OFFSETS OF DATA.  Please use the method 'conversations' for testing.

        :param body: Enter body parameters that are the same as the API documentation.
        :param offset: Specifies from which record to retrieve the chat. Default is 0.
        :param limit: Max amount of conversations to be received in the response.  Default and max is 100.
        :param sort: Sort the results in a predefined order.
        :param max_concurrent_requests: Maximum concurrent requests.
        :param debug: Shows status of requests.
        :return: List of all conversationHistoryRecords within the start time range.
        """

        count = self.conversations_endpoint(
            body=body, url_parameters={'offset': offset, 'limit': limit, 'sort': sort}
        )['_metadata']['count']
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
                        api_data = self.conversations_endpoint(
                            body=b, url_parameters={'offset': o, 'limit': l, 'sort': s}
                        )['conversationHistoryRecords']
                    except requests.HTTPError:
                        print('Reconnecting... [Attempt {}, Offset {}]'.format(attempt, o))
                        self.user_login(username=self.auth.username, password=self.auth.password)
                        print('Woot! We have connection!')
                        continue
                    break
                return api_data
            else:
                # If OAuth1 is used.
                return self.conversations_endpoint(
                    body=b, url_parameters={'offset': o, 'limit': l, 'sort': s}['conversationHistoryRecords']
                )

        conversation_records = []
        # Multi-threading to handle multiple requests at a time.
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent_requests) as executor:
            future_requests = {
                executor.submit(get_record, body, offset, limit, sort): offset for offset in range(0, count, 100)
            }

            for future in concurrent.futures.as_completed(future_requests):
                if debug:
                    print('Record Count: {}, Offset: {} finished.'.format(count, future_requests[future]))
                # Add data to results.
                conversation_records.extend(future.result())
        return conversation_records

    def get_conversation_by_conversation_id_endpoint(self, conversation_id: str) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-get-conversation-by-conversation-id.html

        This method retrieves a conversation according to the given conversation ID.

        :param conversation_id: ID of the conversation to search.
        :return: Dictionary with same structure as the JSON data from the API.
        """
        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Get conversation by conversation id URL
        url = 'https://{}/messaging_history/api/account/{}/conversations/conversation/search'

        # Generate request
        r = requests.post(
            url=url.format(self.mi_domain, self.account_id),
            json={'conversationId': conversation_id},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def get_conversations_by_consumer_id_endpoint(self, consumer_id: str, status: Optional[List[str]] = None) -> dict:
        """
        Documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-get-conversations-by-consumer-id.html

        This method retrieves a list of conversations that the consumer participated in.

        :param consumer_id: ID of the consumer to search.
        :param status: Latest status of the conversation. Valid values: OPEN, CLOSE
        :return: Dictionary with same structure as the JSON data from the API.
        """
        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Get conversations by consumer id URL
        url = 'https://{}/messaging_history/api/account/{}/conversations/consumer/search'

        # Generate request
        r = requests.post(
            url=url.format(self.mi_domain, self.account_id),
            json={'consumer': consumer_id, 'status': status},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()
