import requests
from types import *


class AdatreeAPIClient:
    base_url = "https://cdr-insights-prod.api.adatree.com.au"

    def __init__(self, token: str):
        self.token = token

    def _make_authenticated_request(
        self, method: str, path: str, **kwargs
    ) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        return requests.request(method, url, headers=headers, **kwargs)

    def get_all_consents(self, **params) -> requests.Response:
        return self._make_authenticated_request("GET", "/consents", params=params)

    def create_consent(self, data: CreateConsent) -> requests.Response:
        return self._make_authenticated_request("POST", "/consents", json=data)

    def get_consent(self, consentId: str) -> requests.Response:
        return self._make_authenticated_request("GET", f"/consents/{consentId}")

    def update_consent_via_dashboard(
        self, consentId: str, data: ConsentUpdateViaDashboardRequest
    ) -> requests.Response:
        return self._make_authenticated_request(
            "PATCH", f"/consents/{consentId}", json=data
        )

    def revoke_consent(self, consentId: str) -> requests.Response:
        return self._make_authenticated_request("DELETE", f"/consents/{consentId}")

    def get_consent_authorization_redirect_url(
        self, consentId: str, **params
    ) -> requests.Response:
        return self._make_authenticated_request(
            "GET", f"/consents/{consentId}/authorization", params=params
        )

    def get_consent_events(self, **params) -> requests.Response:
        return self._make_authenticated_request(
            "GET", "/consents/events", params=params
        )

    def list_data_holders(self, softwareProductId: str) -> requests.Response:
        return self._make_authenticated_request(
            "GET", f"/software-products/{softwareProductId}/data-holders"
        )

    def create_tokens(self, data: Authorization) -> requests.Response:
        return self._make_authenticated_request("POST", "/tokens", json=data)

    def get_all_use_cases(self, **params) -> requests.Response:
        return self._make_authenticated_request("GET", "/use-cases", params=params)
