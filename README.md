# Unofficial LivePerson API Python Wrapper
lp_api_wrapper is a native Python library to interface with LivePerson's APIs to gather data.

The following APIs are supported:
* Messaging Interactions API
* Engagement History API

## Requirements
* Python 3.5+, requests, requests_oauthlib
```bash
$ pip install requests requests_oauthlib
```

## Import lp_api_wrapper
```python
# For the Messaging Interactions API
from lp_api_wrapper import MessagingInteractions

# For the Engagement History API
from lp_api_wrapper import EngagementHistory

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
Get data using the Messaging Interaction's conversations method.
```python
body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
mi_conn = MessagingInteractions(account_id='123456789', user_info=user_info)
data = mi_conn.conversations(body)
```

## Engagement History API
Get data using the Engagement History's engagements method.
```python
body = {'start': {'from': 1491004800000, 'to': 1491091199000}}
eh_conn = EngagementHistory(account_id='123456789', user_info=user_info)
data = eh_conn.engagements(body)
```

