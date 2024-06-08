import requests
from typing import Dict, Any, Optional
from types import *


class SDK:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    def _make_authenticated_request(
        self, method: str, url: str, **kwargs
    ) -> requests.Response:
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.token}"
        kwargs["headers"] = headers
        return requests.request(method, url, **kwargs)

    def activity_get_api_requests(
        self, limit: int = 50, offset: int = 0
    ) -> requests.Response:
        """Fetch API requests with pagination."""
        url = f"{self.base_url}/activity"
        params = {"limit": limit, "offset": offset}
        return self._make_authenticated_request("GET", url, params=params)

    def vaults_list_all(self, filter: Optional[str] = None) -> requests.Response:
        """List all vaults with optional filtering."""
        url = f"{self.base_url}/vaults"
        params = {"filter": filter} if filter else {}
        return self._make_authenticated_request("GET", url, params=params)

    def vaults_get_details(self, vault_uuid: str) -> requests.Response:
        """Get details of a specific vault."""
        url = f"{self.base_url}/vaults/{vault_uuid}"
        return self._make_authenticated_request("GET", url)

    def items_get_all(
        self, vault_uuid: str, filter: Optional[str] = None
    ) -> requests.Response:
        """Get all items in a vault with optional filtering."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items"
        params = {"filter": filter} if filter else {}
        return self._make_authenticated_request("GET", url, params=params)

    def items_create_new_item(
        self, vault_uuid: str, item: FullItem
    ) -> requests.Response:
        """Create a new item in a vault."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items"
        return self._make_authenticated_request("POST", url, json=item)

    def items_get_details_by_id(
        self, vault_uuid: str, item_uuid: str
    ) -> requests.Response:
        """Get details of a specific item by its ID."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}"
        return self._make_authenticated_request("GET", url)

    def items_update_item_details(
        self, vault_uuid: str, item_uuid: str, item: FullItem
    ) -> requests.Response:
        """Update details of a specific item."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}"
        return self._make_authenticated_request("PUT", url, json=item)

    def items_delete_item_by_id(
        self, vault_uuid: str, item_uuid: str
    ) -> requests.Response:
        """Delete a specific item by its ID."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}"
        return self._make_authenticated_request("DELETE", url)

    def items_update_subset_attributes(
        self, vault_uuid: str, item_uuid: str, patch: Patch
    ) -> requests.Response:
        """Update subset attributes of a specific item."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}"
        return self._make_authenticated_request("PATCH", url, json=patch)

    def files_get_all_files_inside_item(
        self, vault_uuid: str, item_uuid: str, inline_files: Optional[bool] = None
    ) -> requests.Response:
        """Fetch all files inside an item."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}/files"
        params = {"inline_files": inline_files} if inline_files is not None else {}
        return self._make_authenticated_request("GET", url, params=params)

    def files_get_file_details(
        self,
        vault_uuid: str,
        item_uuid: str,
        file_uuid: str,
        inline_files: Optional[bool] = None,
    ) -> requests.Response:
        """Fetch file details."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}/files/{file_uuid}"
        params = {"inline_files": inline_files} if inline_files is not None else {}
        return self._make_authenticated_request("GET", url, params=params)

    def files_get_content(
        self, vault_uuid: str, item_uuid: str, file_uuid: str
    ) -> requests.Response:
        """Fetch file content."""
        url = f"{self.base_url}/vaults/{vault_uuid}/items/{item_uuid}/files/{file_uuid}/content"
        return self._make_authenticated_request("GET", url)

    def health_check_liveness(self) -> requests.Response:
        """Check liveness of the server."""
        url = f"{self.base_url}/heartbeat"
        return requests.get(url)

    def health_server_state_check(self) -> requests.Response:
        """Check the server's health state."""
        url = f"{self.base_url}/health"
        return requests.get(url)

    def metrics_query_server_metrics(self) -> requests.Response:
        """Query server metrics."""
        url = f"{self.base_url}/metrics"
        return requests.get(url)
