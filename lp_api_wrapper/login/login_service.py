"""
The LoginService class allows other Python LiveEngage API Wrapper classes to login via the Login Service API or using
OAuth1 authentication with app_key, app_secret, access_token, and access_token secret values.

For more information and details, please reference the Login Service API:
https://developers.liveperson.com/login-getting-started.html

:author: Anthony Jones
:email: ajones (at) liveperson (dot) com
"""

import requests
from requests_oauthlib import OAuth1
from lp_api_wrapper.domain.domain_service import DomainService


class LoginService(DomainService):
    def __init__(self, account_id, user_info: dict = None, oauth_info: dict = None):
        super().__init__(account_id=account_id)
        self.login_domain = self.get_domain(service_name='agentVep')
        self.bearer = None
        self.csrf = None
        self.oauth = None

        if user_info:
            try:
                self.user_login(user_info['username'], user_info['password'])
                self.user_info = user_info
            except KeyError:
                print("For user login, try: {'username': 'YOUR_USERNAME', 'password': 'YOUR_PASSWORD'}")

        if oauth_info:
            try:
                self.oauth_login(oauth_info['app_key'], oauth_info['app_secret'], oauth_info['access_token'],
                                 oauth_info['access_token_secret'])
                self.oauth_info = oauth_info
            except KeyError:
                print("For user login, try: {'app_key': 'APPKEY', 'app_secret': 'APPSECRET', 'access_token': "
                      "'ACCESSTOKEN', 'access_token_secret': 'ACCESSTOKENSECRET'}")

        if user_info is None and oauth_info is None:
            raise ValueError('Please login with either user or oauth credentials.')

    def oauth_login(self, app_key: str, app_secret: str, access_token: str, access_token_secret: str):
        """
        Allows OAuth1 authentication from the requests_oauthlib library.

        For more information:
        http://requests-oauthlib.readthedocs.io/en/latest/oauth1_workflow.html

        :param app_key:
        :param app_secret:
        :param access_token:
        :param access_token_secret:
        """
        # Set bearer and csrf tokens to None
        self.bearer = None
        self.csrf = None

        # Establish OAuth1 Credentials
        self.oauth = OAuth1(
            client_key=app_key,
            client_secret=app_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret
        )

    def user_login(self, username: str, password: str):
        """
        Uses the LoginServiceAPI to generate a bearer token via LPA username and password credentials.

        For more information and details, please reference:
        https://developers.liveperson.com/agent-user-login.html

        :param username: LPA username
        :param password: LPA password
        """
        self.oauth = None

        r = requests.post(
            url='https://{}/api/account/{}/login?v=1.3'.format(self.get_login_domain(), self.account_id),
            json={
                'username': username,
                'password': password
            },
            headers={
                'content-type': 'application/json',
                'accept': 'application/json'
            }
        )

        if r.status_code == requests.codes.ok:
            self.bearer = r.json()['bearer']
            self.csrf = r.json()['csrf']
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def refresh(self):
        """
        Refreshes bearer token that is issued from the Login Service API

        For more information and details, please reference:
        https://developers.liveperson.com/agent-refresh.html
        """
        r = requests.post(
            url='https://{}/api/account/{}/refresh'.format(self.get_login_domain(), self.account_id),
            json={
                'csfr': self.csrf
            },
            headers={
                'content-type': 'application/json',
                'accept': 'application/json'
            }
        )

        if r.status_code == requests.codes.ok:
            print('Bearer token has been refreshed!')
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def logout(self):
        """
        Logs out of current user session from the login service API.  Bearer token will be expired once logged out.

        For more information and details, please reference:
        https://developers.liveperson.com/agent-logout.html
        """
        r = requests.post(
            url='https://{}/api/account/{}/logout'.format(self.get_login_domain(), self.account_id),
            json={
                'csfr': self.csrf
            },
            headers={
                'content-type': 'application/json',
                'accept': 'application/json'
            }
        )

        if r.status_code == requests.codes.ok:
            print('User has been logged out!')
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()

    def authorize(self, headers: dict):
        """

        :param headers:
        :return:
        """
        auth_args = {'headers': headers}
        if self.bearer:
            auth_args['headers']['authorization'] = 'Bearer {}'.format(self.bearer)
        elif self.oauth:
            auth_args['auth'] = self.oauth
        return auth_args
