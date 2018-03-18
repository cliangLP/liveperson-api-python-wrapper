"""
This example shows how to view all Predefined Content and Categories by account.
"""

from collections import OrderedDict
from lp_api_wrapper import (PredefinedContent, PredefinedCategories, UserLogin, OAuthLogin)
from typing import Union, List
import pandas as pd


def clean_text(text: str):
    return text.replace('\n', '').replace('\t', '').replace('\r', '').replace('\"', '')


class PredefinedData:
    def __init__(self, auth: Union[UserLogin, OAuthLogin]):
        self.auth = auth
        self.account_id = auth.account_id

    def predefined_categories_by_account(self) -> dict:

        pdc_conn = PredefinedCategories(self.auth)
        payload = pdc_conn.categories_list()

        predefined_categories = {}
        for pdc in payload:
            predefined_categories[pdc['id']] = clean_text(pdc['name'])

        return predefined_categories

    def predefined_content_by_account(self) -> List[dict]:

        pdc_conn = PredefinedContent(self.auth)

        return pdc_conn.get_predefined_content_items(select='accountid', sanitize_data=True)

    def predefined_data_by_account(self) -> List[OrderedDict]:

        predefined_categories = self.predefined_categories_by_account()
        predefined_content = self.predefined_content_by_account()

        predefined_data = []
        for pdc_item in predefined_content:
            try:
                for pdc_data in pdc_item['data']:
                    row = {
                        'accountid': self.account_id,
                        'predefined_content_id': int(pdc_item['id']),
                        'predefined_content_title': clean_text(pdc_data['title']),
                        'predefined_content_msg': clean_text(pdc_data['msg']),
                        'predefined_content_lang': clean_text(pdc_data['lang'])
                    }
                    if 'categoriesIds' in pdc_item:
                        row['predefined_category_ids'] = ', '.join(
                            list(map(lambda pdc: str(pdc), pdc_item['categoriesIds']))
                        )
                        row['predefined_category_names'] = ', '.join(
                            list(map(lambda pdc: predefined_categories[pdc], pdc_item['categoriesIds']))
                        )
                    else:
                        row['predefined_category_ids'] = 'NULL'
                        row['predefined_category_names'] = 'NULL'
                    predefined_data.append(OrderedDict(row))
            except KeyError as e:
                print('Error: {}'.format(e))
        return predefined_data


if __name__ == '__main__':

    # Set up authentication
    account_auth = UserLogin(account_id='1234', username='YOURUSERNAME', password='YOURPASSWORD')

    # Set up Predefined Data.
    pdd = PredefinedData(auth=account_auth)

    # Shows a dictionary of predefined categories.
    predefined_categories_by_account = pdd.predefined_categories_by_account()

    # Shows all Predefined Content of an account.
    predefined_content_by_account = pdd.predefined_content_by_account()

    # Shows all Predefined Data (Predefined Content and Predefined Categories) by account.
    predefined_data_by_account = pdd.predefined_data_by_account()

    # Convert Predefined Data into Pandas DataFrame.
    df = pd.DataFrame(predefined_data_by_account)

    print(df.head())
