import requests
from types import CreatePartnerAccountRequest, UpdatePartnerAccountRequest
from requests import Response


class BillingAPIClient:
    def __init__(self, api_key: str):
        self.base_url = "https://billing.b5test.eu"
        self.api_key = api_key

    def _make_authenticated_request(self, method: str, url: str, **kwargs) -> Response:
        headers = kwargs.setdefault("headers", {})
        headers.setdefault("Authorization", f"Bearer {self.api_key}")
        return requests.request(method, url, **kwargs)

    def begin_provisioning_process(self, data: CreatePartnerAccountRequest) -> Response:
        """
        Initiates the provisioning process for a partner account.
        """
        url = f"{self.base_url}/api/v1/partners/accounts"
        response = self._make_authenticated_request("POST", url, json=data)
        return response

    def get_account_by_uid(self, customer_account_uid: str) -> Response:
        """
        Retrieves account information by UID.
        """
        url = f"{self.base_url}/api/v1/partners/accounts/{customer_account_uid}"
        response = self._make_authenticated_request("GET", url)
        return response

    def remove_account_from_partnership(self, customer_account_uid: str) -> Response:
        """
        Removes an account from a partnership.
        """
        url = f"{self.base_url}/api/v1/partners/accounts/{customer_account_uid}"
        response = self._make_authenticated_request("DELETE", url)
        return response

    def update_account_ends_at_by_uid(
        self, customer_account_uid: str, data: UpdatePartnerAccountRequest
    ) -> Response:
        """
        Updates the 'ends at' field of an account by UID.
        """
        url = f"{self.base_url}/api/v1/partners/accounts/{customer_account_uid}"
        response = self._make_authenticated_request("PATCH", url, json=data)
        return response
