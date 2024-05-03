
import os
import requests
from types import FullItem, Patch

class ClientSDK:
    def __init__(self):
        self.base_url = "http://localhost:8080/v1"
        self.api_key = os.getenv('API_KEY')

    def _make_authenticated_request(self, method, url, **kwargs):
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.api_key}'
        kwargs['headers'] = headers

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise Exception("The request timed out")
        except requests.exceptions.TooManyRedirects:
            raise Exception("The request exceeded the configured number of maximum redirections")
        except requests.exceptions.RequestException as e:
            raise Exception(str(e))
        return response

    def get_api_requests(self, limit: int = 50, offset: int = 0):
        """Retrieve a list of API Requests that have been made."""
        url = f"{self.base_url}/activity"
        params = {'limit': limit, 'offset': offset}
        return self._make_authenticated_request('GET', url, params=params)

    def get_all_files_inside_item(self, vault_uuid: str, item_uuid: str, inline_files: bool = False):
        """Get all the files inside an Item."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}/files"
        params = {'inline_files': inline_files}
        return self._make_authenticated_request('GET', url, params=params)

    def get_file_details(self, vault_uuid: str, item_uuid: str, file_uuid: str, inline_files: bool = False):
        """Get the details of a File."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}/files/{file_uuid}"
        params = {'inline_files': inline_files}
        return self._make_authenticated_request('GET', url, params=params)

    def get_content(self, vault_uuid: str, item_uuid: str, file_uuid: str):
        """Get the content of a File."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}/files/{file_uuid}/content"
        return self._make_authenticated_request('GET', url)

    def check_liveness(self):
        """Ping the server for liveness."""
        url = f"{self.base_url}/heartbeat"
        return self._make_authenticated_request('GET', url)

    def server_state_check(self):
        """Get state of the server and its dependencies."""
        url = f"{self.base_url}/health"
        return self._make_authenticated_request('GET', url)

    def get_all_items(self, vault_uuid: str, filter_str: str = None):
        """Get all items for inside a Vault."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items"
        params = {'filter': filter_str} if filter_str else {}
        return self._make_authenticated_request('GET', url, params=params)

    def create_new_item(self, vault_uuid: str, item: FullItem):
        """Create a new Item."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items"
        return self._make_authenticated_request('POST', url, json=item)

    def get_details_by_id(self, vault_uuid: str, item_uuid: str):
        """Get the details of an Item."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}"
        return self._make_authenticated_request('GET', url)

    def update_item_details(self, vault_uuid: str, item_uuid: str, item: FullItem):
        """Update an Item."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}"
        return self._make_authenticated_request('PUT', url, json=item)

    def delete_item_by_id(self, vault_uuid: str, item_uuid: str):
        """Delete an Item."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}"
        return self._make_authenticated_request('DELETE', url)

    def update_subset_attributes(self, vault_uuid: str, item_uuid: str, patch: Patch):
        """Update a subset of Item attributes."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}"
        return self._make_authenticated_request('PATCH', url, json=patch)

    def query_server_metrics(self):
        """Query server for exposed Prometheus metrics."""
        url = f"{self.base_url}/metrics"
        return self._make_authenticated_request('GET', url)

    def list_all_vaults(self, filter_str: str = None):
        """Get all Vaults."""
        url = f"{self.base_url}/vaults"
        params = {'filter': filter_str} if filter_str else {}
        return self._make_authenticated_request('GET', url, params=params)

    def get_vault_details(self, vault_uuid: str):
        """Get Vault details and metadata."""
        url = f"{self.base_url}/vaults/{vault_uuid}"
        return self._make_authenticated_request('GET', url)
