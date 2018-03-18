import requests
from lp_api_wrapper.util.login_service import LoginService, UserLogin, OAuthLogin
from typing import Optional, Union


class PredefinedContent(LoginService):
    def __init__(self, auth: Union[UserLogin, OAuthLogin]) -> None:
        super().__init__(auth=auth)
        self.pdc_domain = self.get_domain(service_name='accountConfigReadWrite')

    def get_predefined_content_items(self, include_deleted: Optional[bool] = None, sanitize_data: Optional[bool] = None,
                                     lang: Optional[str] = None, select: Optional[str] = None,
                                     group_by: Optional[str] = None, skill_ids: Optional[str] = None,
                                     ids: Optional[str] = None):

        """
        Documentation:
        https://developers.liveperson.com/account-configuration-predefined-content-get-items.html

        Retrieves a list of Predefined Content items from a specific account.

        :param include_deleted: Flag indicating whether deleted entities should be returned in the response.
         Valid values: True/False. Default value: False
        :param sanitize_data: Flag indicating whether the text should be sanitized (Antisamy).
         Valid values: True/False. Default value: False
        :param lang: Languages (separated by commas) to filter the response by.
         Format: 'en-US, en-UK' ~ Default value: null
        :param select: Yoga selector expression.
         Example values: 'id, name, accountid' ~ Default value: null
        :param group_by: Property type to group the return entities by.
         Example value: 'CATEGORIES' ~ Default value: null
        :param skill_ids: Skills IDs (separated by commas) to filter the response by.
         Example values: '2,3,4' ~ Default value: null
        :param ids: Entity IDs (separated by commas) to filter the response by.
         Example values: '2,3,4' ~ Default value: null
        :return:
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Agent Status URL
        url = 'https://{}/api/account/{}/configuration/engagement-window/canned-responses'

        # Generate request
        r = requests.get(
            url=url.format(self.pdc_domain, self.account_id),
            params={
                'include_deleted': include_deleted,
                'sanitize_data': sanitize_data,
                'lang': lang,
                'select': select,
                'group_by': group_by,
                'skill_ids': skill_ids,
                'ids': ids
            },
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def get_predefined_content_by_id(self, predefined_content_id: str, version: float = 2.0,
                                     include_deleted: Optional[bool] = None, sanitize_data: Optional[bool] = None,
                                     lang: Optional[str] = None, select: Optional[str] = None,
                                     group_by: Optional[str] = None, skill_ids: Optional[str] = None,
                                     ids: Optional[str] = None):

        """
        Documentation:
        https://developers.liveperson.com/account-configuration-predefined-content-get-by-id.html

        Retrieves a list of Predefined Content items from a specific account.

        :param predefined_content_id: Account Config object’s unique ID
        :param version: API version
        :param include_deleted: Flag indicating whether deleted entities should be returned in the response.
         Valid values: True/False. Default value: False
        :param sanitize_data: Flag indicating whether the text should be sanitized (Antisamy).
         Valid values: True/False. Default value: False
        :param lang: Languages (separated by commas) to filter the response by.
         Format: 'en-US, en-UK' ~ Default value: null
        :param select: Yoga selector expression.
         Example values: 'id, name, accountid' ~ Default value: null
        :param group_by: Property type to group the return entities by.
         Example value: 'CATEGORIES' ~ Default value: null
        :param skill_ids: Skills IDs (separated by commas) to filter the response by.
         Example values: '2,3,4' ~ Default value: null
        :param ids: Entity IDs (separated by commas) to filter the response by.
         Example values: '2,3,4' ~ Default value: null
        :return:
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Agent Status URL
        url = 'https://{}/api/account/{}/configuration/engagement-window/canned-responses/{}'

        # Generate request
        r = requests.get(
            url=url.format(self.pdc_domain, self.account_id, predefined_content_id),
            params={
                'v': version,
                'include_deleted': include_deleted,
                'sanitize_data': sanitize_data,
                'lang': lang,
                'select': select,
                'group_by': group_by,
                'skill_ids': skill_ids,
                'ids': ids
            },
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def get_default_predefined_content_by_id(self, template_id: str):

        """
        Documentation:
        https://developers.liveperson.com/account-configuration-predefined-content-get-default-items-by-id.html

        Retrieves a single, default Predefined Content item by template ID from a specific account.

        :param template_id: ID of a template used to instantiate the object.
        :return:
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Agent Status URL
        url = 'https://{}//api/account/{}/configuration/defaults/engagement-window/canned-responses/{}'

        # Generate request
        r = requests.get(
            url=url.format(self.pdc_domain, self.account_id, template_id),
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def get_default_predefined_content_items(self):

        """
        Documentation:
        https://developers.liveperson.com/account-configuration-predefined-content-get-default-items.html

        Retrieves default Predefined Content items from a specific account.

        :return:
        """

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Agent Status URL
        url = 'https://{}//api/account/{}/configuration/defaults/engagement-window/canned-responses'

        # Generate request
        r = requests.get(
            url=url.format(self.pdc_domain, self.account_id),
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()


