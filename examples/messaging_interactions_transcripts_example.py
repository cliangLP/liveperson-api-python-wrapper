"""
This example shows how to create a Messaging Interactions transcripts CSV flat file from the lp_api_wrapper library.
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

# Grab Conversational History Records from data.
convo_records = data['conversationHistoryRecords']

# For all data in date range use 'all_conversations'. (Handles all offsets)
# Note: This method extracts 'conversationHistoryRecords' already.
#       Look in messaging_interactions.py for more information.
# convo_records = mi_conn.all_conversations(body=body)

# Extract conversation level data
# Look at Messaging Interactions API documentation to see the JSON data structure from conversations.
transcripts = []
for record in convo_records:
    for message in record['messageRecords']:
        try:
            transcript = {
                'account_id': record['info']['brandId'],
                'conversation_id': record['info']['conversationId'],
                'device': record['info']['device'],
                'text': message['messageData']['msg']['text'],
                'message_id': message['messageId'],
                'participant_id': message['participantId'],
                'sent_by': message['sentBy'],
                'seq': message['seq'],
                'source': message['source'],
                'time': message['time'],
                'epoch_time': message['timeL']
            }
            transcripts.append(transcript)
        except KeyError:
            # Skip over record if any record doesn't exist.
            continue

# Only necessary if you want to position your columns in your flat file, column names
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

# File path with file name.
file_path = './transcripts.csv'

# Export into CSV with no index column
df.to_csv(path_or_buf=file_path, index=False)

# Now you have a Transcripts Flat File!
