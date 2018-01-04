"""
The DomainService class allows other LiveEngage API Wrapper classes to get the required domain for the selected API.

For more information and details, please reference the Domain Service API:
https://developers.liveperson.com/agent-domain-domain-api.html

:author: Anthony Jones
:email: ajones (at) liveperson (dot) com
"""

import requests


class DomainService:
    def __init__(self, account_id: str):
        self.account_id = account_id

    def get_domain(self, service_name: str):
        """
        Retrieves an api domain name associated with its service name and account location.

        :param service_name: Name of service that is being accessed.
        :return: Domain associated with service and account id.
        """
        url = 'http://api.liveperson.net/api/account/{}/service/{}/baseURI.json?version=1.0'
        r = requests.get(url=url.format(self.account_id, service_name))

        if r.status_code == requests.codes.ok:
            return r.json()['baseURI']
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()
