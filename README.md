# Unofficial LivePerson API Python Wrapper
lp_api_wrapper is a native Python library to interface with LivePerson's APIs to gather data.

The following APIs are supported:
* Messaging Interactions API
* Engagement History API
* Agent Metrics API

## Requirements
* Python 3.5+
* requests
* requests_oauthlib
```bash
$ pip install requests requests_oauthlib
```

## Installation
```bash
$ pip install git+https://github.com/ajoneslp/liveperson-api-python-wrapper
```

## Import lp_api_wrapper
```python
# For the Messaging Interactions API
from lp_api_wrapper import MessagingInteractions

# For the Engagement History API
from lp_api_wrapper import EngagementHistory

# For Agent Metrics API
from lp_api_wrapper import AgentMetrics
```

## Login/Authentication
Each class in lp_api_wrapper accepts user login or oauth1 authentication.

Using the Messaging Interactions API as an example, we can show login/authentication.

Login with LPA User Login
```python
user_info = {'username': 'LPA-USERNAME', 'password': 'LPA-PASSWORD'}
conn = MessagingInteractions(account_id='123456789', user_info=user_info)
```

Or, login using oauth1 authentication
```python
oauth = {'app_key': 'APPKEY', 'app_secret':'APPSECRET', 'access_token':'ATOKEN', 'access_token_secret':'ATSECRET'}
conn = MessagingInteractions(account_id='123456789', oauth_info=oauth)
```

## Messaging Interactions API

```python
# Create MI Connection.
mi_conn = MessagingInteractions(account_id='123456789', user_info=user_info)
```

#### 1. Conversations

Get data using the Messaging Interaction's conversations method.

Resources:
https://developers.liveperson.com/data-messaging-interactions-conversations.html
```python
body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
data = mi_conn.conversations(body)
```

#### 2. Get conversation by conversation id

Resources:
https://developers.liveperson.com/data-messaging-interactions-get-conversation-by-conversation-id.html
```python
data = mi_conn.get_conversation_by_conversation_id(conversation_id='1234abc')
```

#### 3. Get conversation by consumer id

Resources:
https://developers.liveperson.com/data-messaging-interactions-get-conversations-by-consumer-id.html
```python
data = mi_conn.get_conversations_by_consumer_id(consumer_id='1234abc')
```

## Engagement History API

```python
# Create EH Connection.
mi_conn = EngagementHistory(account_id='123456789', user_info=user_info)
```

Get data using the Engagement History's engagements method.

Resources:
https://developers.liveperson.com/data-engagement-history-overview.html
```python
body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
data = eh_conn.engagements(body)
```

## Agent Metrics API

```python
# Create EH Connection.
am_conn = AgentMetrics(account_id='123456789', user_info=user_info)
```

#### 1. Agent Status

Resources:
https://developers.liveperson.com/data-messaging-interactions-methods-agent-status.html
```python
# Example body
body = {'skillIds': ['1234', '5678']}
data = am_conn.engagements(body)
```


#### 2. Summary

Resources:
https://developers.liveperson.com/data-messaging-interactions-methods-summary.html
```python
data = am_conn.summary()
```
