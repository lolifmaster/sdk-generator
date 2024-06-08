import requests
from typing import Optional, List, Dict, Any


class ApaleoInventorySDK:
    def __init__(self, access_token: str, base_url: str = "https://api.apaleo.com"):
        """Initializes the SDK with the access token and base URL."""
        self.access_token = access_token
        self.base_url = base_url

    def _make_authenticated_request(
        self, method: str, url: str, **kwargs
    ) -> requests.Response:
        """Makes an authenticated request to the specified URL."""
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        headers["Content-Type"] = "application/json"
        if "idempotency_key" in kwargs:
            headers["Idempotency-Key"] = kwargs["idempotency_key"]
        kwargs["headers"] = headers
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def get_properties_list(
        self,
        status: Optional[List[str]] = None,
        include_archived: Optional[bool] = None,
        countryCode: Optional[List[str]] = None,
        pageNumber: Optional[int] = 1,
        pageSize: Optional[int] = None,
        expand: Optional[List[str]] = None,
    ) -> requests.Response:
        """Gets a list of properties."""
        url = f"{self.base_url}/inventory/v1/properties"
        params = {
            "status": status,
            "includeArchived": include_archived,
            "countryCode": countryCode,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "expand": expand,
        }
        return self._make_authenticated_request("GET", url, params=params)

    # Implement the rest of the methods following the same pattern as above, addressing the feedback points
