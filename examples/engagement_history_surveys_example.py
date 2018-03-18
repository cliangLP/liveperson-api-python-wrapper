"""
This example shows how to view all Engagement History Surveys by account.
"""

import pandas as pd
from collections import OrderedDict
from datetime import datetime, timedelta
from lp_api_wrapper import UserLogin, EngagementHistory


# Set up account authentication.
auth = UserLogin(account_id='1234', username='YOURUSERNAME', password='YOURPASSWORD')

# Connect to Engagement History API.
eh_conn = EngagementHistory(auth=auth)

# Set up body with defined time frame.
start_from = int((datetime.now() - timedelta(days=.1)).timestamp() * 1000)
start_to = int(datetime.now().timestamp() * 1000)
body = {'start': {'from': start_from, 'to': start_to}}

# Retrieve all interaction history records in time frame.
interaction_history_records = eh_conn.all_engagements(body, debug=True)

# Extract all survey data from interaction history records.
survey_data = []
for ihr in interaction_history_records:
    if 'surveys' in ihr:
        for survey_type, surveys in ihr['surveys'].items():
            survey_records = []
            for survey in surveys:
                survey_record = dict(
                    # Experiment by adding additional info parameters.
                    accountId=ihr['info']['accountId'],
                    engagementID=ihr['info']['engagementId'],
                    agentId=ihr['info']['agentId'],
                    surveyType=survey_type
                )
                survey_record.update(survey)
                survey_records.append(OrderedDict(survey_record))
            survey_data.extend(survey_records)

# Convert to a Pandas DF
survey_df = pd.DataFrame(survey_data)

print(survey_df.head())
