import requests
from lp_api_wrapper.util.login_service import LoginService, UserLogin, OAuthLogin
from typing import Optional, Union, Any


class PredefinedCategories(LoginService):
    def __init__(self, auth: Union[UserLogin, OAuthLogin]) -> None:
        super().__init__(auth=auth)
        self.pdc_domain = self.get_domain(service_name='accountConfigReadWrite')

    def categories_list(self, version: float = 2.0, select: Any = None, include_deleted: Optional[bool] = None) -> dict:
        # Establish Authorization
        auth_args = self.authorize(headers={'content-type': 'application/json'})

        # Agent Status URL
        url = 'https://{}/api/account/{}/configuration/le-categories/categories'

        # Generate request
        r = requests.get(
            url=url.format(self.pdc_domain, self.account_id),
            params={'v': version, 'select': select, 'include_deleted': include_deleted},
            **auth_args
        )

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()
