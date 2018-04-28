"""
This example shows how to view all Data Access Agent Activity by account.
"""

from datetime import datetime, timedelta
from lp_api_wrapper import UserLogin, DataAccess

# Set up account authentication.
auth = UserLogin(account_id='1234', username='USERNAME', password='PASSWORD')

# Connect to Engagement History API.
da_conn = DataAccess(auth=auth)

# Set up body with defined time frame.
start_time = int((datetime.now() - timedelta(days=.1)).timestamp() * 1000)
end_time = int(datetime.now().timestamp() * 1000)


# Retrieve all interaction history records in time frame
da_web_session_records = da_conn.web_session(start_time, end_time)

print(da_web_session_records)