# lp_api_wrapper: Unofficial LivePerson API Python Wrapper
[![PyPI version](https://badge.fury.io/py/lp_api_wrapper.svg)](https://badge.fury.io/py/lp_api_wrapper)

![Python version](https://img.shields.io/badge/python-3.5%2C%203.6-green.svg)

lp_api_wrapper is a native Python library to interface with LivePerson's APIs to gather data.

The following APIs are supported:
* Messaging Interactions API
* Engagement History API
* Agent Metrics API
* Messaging Operations API
* Operational Realtime API


## Dependencies
* requests
* requests_oauthlib
```bash
$ pip install requests requests_oauthlib
```

## Installation
```bash
$ pip install --upgrade lp_api_wrapper
```

## Import lp_api_wrapper
```python
# For Messaging Interactions API
from lp_api_wrapper import MessagingInteractions

# For Engagement History API
from lp_api_wrapper import EngagementHistory

# For Agent Metrics API
from lp_api_wrapper import AgentMetrics

# For Messaging Operations API
from lp_api_wrapper import MessagingOperations

# For Operational Realtime API
from lp_api_wrapper import OperationalRealtime
```

## Login/Authentication
Each class in lp_api_wrapper accepts user login or oauth1 authentication.

Login with LPA User Login
```python
from lp_api_wrapper import UserLogin
auth = UserLogin(account_id='1234', username='YOURUSERNAME', password='YOURPASSWORD')
```

Or, login using OAuth1 authentication
```python
from lp_api_wrapper import OAuthLogin
auth = OAuthLogin(account_id='1234', app_key='APP_KEY', app_secret='APP_SECRET', access_token='ACCESS_TOKEN', access_token_secret='ACCESS_TOKEN_SECRET')
```

## Messaging Interactions API
Create Messaging Interactions Connection
```python
from lp_api_wrapper import MessagingInteractions
mi_conn = MessagingInteractions(auth=auth)
```

#### 1. Conversations
Reference:
https://developers.liveperson.com/data-messaging-interactions-conversations.html

Arguments:

* body: dict Note: Check reference for details.
* offset: int (OPTIONAL) Defaults to 0
* limit: int (OPTIONAL) Defaults to 100
* sort: str (OPTIONAL)

```python
body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
data = mi_conn.conversations(body)
```

#### 2. Get conversation by conversation id
Reference:
https://developers.liveperson.com/data-messaging-interactions-get-conversation-by-conversation-id.html

Arguments:

* conversation_id: str

```python
data = mi_conn.get_conversation_by_conversation_id(conversation_id='1234abc')
```

#### 3. Get conversation by consumer id
Reference:
https://developers.liveperson.com/data-messaging-interactions-get-conversations-by-consumer-id.html

Arguments:

* consumer_id: str

```python
data = mi_conn.get_conversations_by_consumer_id(consumer_id='1234abc')
```

## Engagement History API
Create Engagement History Connection.
```python
from lp_api_wrapper import EngagementHistory
mi_conn = EngagementHistory(auth=auth)
```

#### 1. Engagements
Arguments:

* body: dict (Note: Check reference for details.)
* offset: int (OPTIONAL) Defaults to 0
* limit: int (OPTIONAL) Defaults to 100
* sort: str (OPTIONAL)


Reference:
https://developers.liveperson.com/data-engagement-history-overview.html
```python
body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
data = eh_conn.engagements(body)
```

## Agent Metrics API
Create Agent Metrics Connection.
```python
# Create EH Connection.
from lp_api_wrapper import AgentMetrics
am_conn = AgentMetrics(auth=auth)
```

#### 1. Agent Status
Arguments:

* status: List[str] (OPTIONAL)
* agent_ids: List[str] (OPTIONAL)
* skill_ids: List[str] (OPTIONAL)
* agent_group_ids: List[str] (OPTIONAL)

* If all are left blank, this method will return all agents' status for the account.

Reference:
https://developers.liveperson.com/data-messaging-interactions-methods-agent-status.html
```python
# Example
data = am_conn.agent_status(skill_ids=['1234', '5678'])
```


#### 2. Summary
Arguments:

* status: List[str] (OPTIONAL)
* agent_ids: List[str] (OPTIONAL)
* skill_ids: List[str] (OPTIONAL)
* agent_group_ids: List[str] (OPTIONAL)

* If all are left blank, this method will return the status for the account.

Reference:
https://developers.liveperson.com/data-messaging-interactions-methods-summary.html
```python
data = am_conn.summary()
```


## Messaging Operations API
Create Messaging Operations Connection.
```python
from lp_api_wrapper import MessagingOperations
mo_conn = MessagingOperations(auth=auth)
```

#### 1. Messaging Operations
Arguments:

* time_frame: int
* version: int (OPTIONAL) Default is 1
* skill_ids: str (OPTIONAL)
* agent_ids: str (OPTIONAL)
* interval: int (OPTIONAL)

Reference:
https://developers.liveperson.com/data-messaging-operations-messaging-conversation.html
```python
# Example
data = mo_conn.messaging_operations(time_frame=1440)
```

#### 2. Messaging CSAT Distribution
Arguments:

* time_frame: int
* version: int (OPTIONAL) Default is 1
* skill_ids: str (OPTIONAL)
* agent_ids: str (OPTIONAL)

Reference:
https://developers.liveperson.com/data-messaging-operations-messaging-csat-distribution.html
```python
# Example
data = mo_conn.messaging_csat_distribution(time_frame=1440)
```

## Operational Realtime API
Create Operational Realtime Connection.
```python
from lp_api_wrapper import OperationalRealtime
or_conn = OperationalRealtime(auth=auth)
```

#### 1. Queue Health
Arguments:

* time_frame: int
* version: int (OPTIONAL) Default is 1
* skill_ids: str (OPTIONAL)
* interval: int (OPTIONAL)

Reference:
https://developers.liveperson.com/data-operational-realtime-queue-health.html
```python
# Example
data = or_conn.queue_health(time_frame=1440)
```

#### 2. Engagement Activity
Arguments:

* time_frame: int
* version: int (OPTIONAL) Default is 1
* skill_ids: str (OPTIONAL)
* agent_ids: str (OPTIONAL)
* interval: int (OPTIONAL)

Reference:
https://developers.liveperson.com/data-operational-realtime-engagement-activity.html
```python
# Example
data = or_conn.engagement_activity(time_frame=1440)
```

#### 3. Agent Activity
Arguments:

* time_frame: int
* version: int (OPTIONAL) Default is 1
* agent_ids: str (OPTIONAL)
* interval: int (OPTIONAL)

Reference:
https://developers.liveperson.com/data-operational-realtime-agent-activity.html
```python
# Example
data = or_conn.agent_activity(time_frame=1440)
```

#### 4. Current Queue State
Arguments:

* version: int (OPTIONAL) Default is 1
* skill_ids: str (OPTIONAL)

Reference:
https://developers.liveperson.com/data-operational-realtime-current-queue-state.html
```python
# Example
data = or_conn.current_queue_state()
```

#### 5. SLA Histogram
Arguments:

* time_frame: int
* version: int (OPTIONAL) Default is 1
* skill_ids: str (OPTIONAL)
* group_ids: str (OPTIONAL)
* histogram: int (OPTIONAL)

Reference:
https://developers.liveperson.com/data-operational-realtime-sla-histogram.html
```python
# Example
data = or_conn.sla_histogram(time_frame=1440)
```