"""
This example shows how to create a CSV MI transcripts flat file from the lp_api_wrapper library.
"""

from lp_api_wrapper import MessagingInteractions
from datetime import datetime, timedelta
import pandas as pd

# LPA Username & Password (Or use OAUTH1.  Check README.md for more info)
user_info = {'username': 'YOURUSERNAME', 'password': 'YOURPASSWORD'}

# Create MI Connections
mi_conn = MessagingInteractions(account_id='1234', user_info=user_info)

# Creates Epoch Time from 1 day ago. (If your volume is low, or none. Consider increasing days)
start_from = int((datetime.now() - timedelta(days=1)).timestamp() * 1000)

# Creates Epoch Time right now.
start_to = int(datetime.now().timestamp() * 1000)

# Conversations from date range created above
body = {'start': {'from': start_from, 'to': start_to}}

# Get data! (Only 1 offset) Great for testing...
data = mi_conn.conversations(body=body)

# For all data in date range use 'all_conversations' (May take a while...)
# data = mi_conn.all_conversations(body=body)

# Grab Conversational History Records from data.
convo_records = data['conversationHistoryRecords']

# Extract conversation level data
transcripts = []
for record in convo_records:
    for message in record['messageRecords']:
        try:
            transcript = dict(account_id=record['info']['brandId'])
            transcript['conversation_id'] = record['info']['conversationId']
            transcript['device'] = record['info']['device']
            transcript['text'] = message['messageData']['msg']['text']
            transcript['message_id'] = message['messageId']
            transcript['participant_id'] = message['participantId']
            transcript['sent_by'] = message['sentBy']
            transcript['seq'] = message['seq']
            transcript['source'] = message['source']
            transcript['time'] = message['time']
            transcript['epoch_time'] = message['timeL']
            transcripts.append(transcript)
        except KeyError:
            # Skip over record if any record doesn't exist.
            continue

# Only necessary if to move columns in a specific position
cols = [
    'account_id',
    'conversation_id',
    'message_id',
    'participant_id',
    'sent_by',
    'device',
    'source',
    'time',
    'epoch_time',
    'seq',
    'text'
]

# Convert into Pandas DataFrame
df = pd.DataFrame(transcripts)[cols]

# Export into CSV with no index column
df.to_csv(path_or_buf='transcripts.csv', index=False)

# Now you have a Transcripts Flat File!
