"""
An unofficial native Python wrapper for the LivePerson Messaging Interactions API

Documentation:
https://developers.liveperson.com/data-messaging-interactions-overview.html

The LiveEngage Messaging Interactions API retrieves the most up to date information available about contact center
messaging interactions. This API makes it possible to search, filter and analyze data and transcripts of
open and closed conversations.

The API returns the conversation’s transcripts and all of its related metadata such as start time, end time, MCS, CSAT,
summary, participated agents, the reason the conversation was closed etc.

Usage Example:
1. Choose User Service Login or OAuth1 Authentication.

    # For User Service Login
    > from lp_api_wrapper import UserLogin
    > auth = UserLogin(account_id='1234', username='YOURUSERNAME', password='YOURPASSWORD')

    # For OAuth1 Authentication
    > from lp_api_wrapper import OAuthLogin
    > auth = OAuthLogin(account_id='1234', app_key='K', app_secret='S', access_token='T', access_token_secret='TS')

2. Import MessagingInteractions and get data from connection

    > from lp_api_wrapper import MessagingInteractions
    > mi_conn = MessagingInteractions(auth=auth)
    > body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
    > data = mi_conn.conversations(body)
"""

import concurrent.futures
from ..messaging_interactions.messaging_interactions_endpoints import MessagingInteractionsEndpoints
from ..messaging_interactions.conversation_history_record import ConversationHistoryRecord
from ...util.login_service import (UserLogin, OAuthLogin)
from typing import (List, Optional, Union)


class MessagingInteractions(MessagingInteractionsEndpoints):
    def __init__(self, auth: Union[UserLogin, OAuthLogin]) -> None:
        super().__init__(auth=auth)

    def conversations(self, body: dict, max_workers: int = 10,
                      debug: bool = False) -> Union[List, List[ConversationHistoryRecord]]:

        """
        Documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-conversations.html

        This method retrieves conversations with all their metadata and related messages based on a predefined search
        criteria. Search criteria includes filtering by time range, agent, skill, etc.

        :param body: REQUIRED Enter body parameters that are the same as the API documentation.
        :param max_workers: Number of workers for requests.
        :param debug: Prints data collection process.
        :return:
        """

        initial_payload = self.conversations_endpoint(
            body=body, url_parameters={'offset': 0, 'limit': 100, 'sort': None}
        )
        count = initial_payload['_metadata']['count']

        if count == 0:
            return []

        conversation_history_records = [
            ConversationHistoryRecord(record) for record in initial_payload['conversationHistoryRecords']
        ]

        # Multi-threading to handle multiple requests at a time.
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_requests = {
                executor.submit(self.conversations_endpoint, body, {'offset': offset, 'limit': 100, 'sort': None}):
                    offset for offset in range(100, count, 100)
            }

            for future in concurrent.futures.as_completed(future_requests):
                if debug:
                    print('Record Count: {}, Offset: {} finished.'.format(count, future_requests[future]))
                # Add data to results.
                records = future.result()['conversationHistoryRecords']
                conversation_history_records.extend([ConversationHistoryRecord(record) for record in records])
        return conversation_history_records

    def get_conversation_by_conversation_id(self, conversation_id: str) -> ConversationHistoryRecord:
        """
        Documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-get-conversation-by-conversation-id.html

        This method retrieves a conversation according to the given conversation ID.

        :param conversation_id: ID of the conversation to search.
        :return: ConversationHistoryRecord
        """

        payload = self.get_conversation_by_conversation_id_endpoint(conversation_id=conversation_id)

        return ConversationHistoryRecord(payload['conversationHistoryRecords'][0])

    def get_conversations_by_consumer_id(self, consumer_id: str, status: Optional[List[str]] = None
                                         ) -> ConversationHistoryRecord:
        """
        Documentation:
        https://developers.liveperson.com/data_api-messaging-interactions-get-conversations-by-consumer-id.html

        This method retrieves a list of conversations that the consumer participated in.

        :param consumer_id: ID of the consumer to search.
        :param status: Latest status of the conversation. Valid values: OPEN, CLOSE
        :return: ConversationHistoryRecord
        """

        payload = self.get_conversations_by_consumer_id_endpoint(consumer_id=consumer_id, status=status)

        return ConversationHistoryRecord(payload['conversationHistoryRecords'][0])
