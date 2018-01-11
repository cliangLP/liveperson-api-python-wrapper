"""
DomainService allows other LivePerson API wrapper classes to get the required domain for the selected API.

The different service names can be found in the relevant documentation for the API you're looking to use. They can be
found in each document's Overview page. Service names are case sensitive. Please make sure to input serviceName as it is provided in each document's overview.

Reference:
https://developers.liveperson.com/agent-domain-domain-api.html
"""

import requests

__author__ = 'Anthony Jones'
__email__ = 'ajones@liveperson.com'


class DomainService:
    def __init__(self, account_id: str) -> None:
        self.account_id = account_id

    def get_domain(self, service_name: str) -> str:
        """
        Retrieves an api domain name associated with its service name and account location.

        :param service_name: Name of service that is being accessed.
        :return: Domain associated with service and account id.
        """

        # Retrieve Domain URL
        url = 'http://api.liveperson.net/api/account/{}/service/{}/baseURI.json?version=1.0'

        # Generate request
        r = requests.get(url=url.format(self.account_id, service_name))

        # Check request status
        if r.status_code == requests.codes.ok:
            return r.json()['baseURI']
        else:
            print('Error: {}'.format(r.json()))
            r.raise_for_status()
