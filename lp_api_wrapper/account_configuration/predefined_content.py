import requests
from lp_api_wrapper.util.login_service import LoginService, UserLogin, OAuthLogin
from typing import Optional, Union

__author__ = 'Anthony Jones'
__email__ = 'ajones@liveperson.com'


class PredefinedContent(LoginService):
    def __init__(self, auth: Union[UserLogin, OAuthLogin]) -> None:
        super().__init__(auth=auth)
        self.pdc_domain = self.get_domain(service_name='accountConfigReadWrite')

    def get_predefined_content_items(self, version: float = 2.0, include_deleted: Optional[bool] = None,
                                     sanitize_data: Optional[bool] = None, lang: Optional[str] = None,
                                     select: Optional[str] = None, group_by: Optional[str] = None,
                                     skill_ids: Optional[str] = None, ids: Optional[str] = None):

        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Agent Status URL
        url = 'https://{}/api/account/{}/configuration/engagement-window/canned-responses'

        # Generate request
        r = requests.get(
            url=url.format(self.pdc_domain, self.account_id),
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
