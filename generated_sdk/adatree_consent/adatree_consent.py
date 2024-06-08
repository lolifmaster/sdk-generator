import requests
import json
from types import CreateConsent, ConsentUpdateViaDashboardRequest, Authorization
from typing import List


class CDRInsightsClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://cdr-insights-prod.api.adatree.com.au",
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def _make_authenticated_request(self, method: str, url: str, **kwargs):
        return requests.request(method, url, headers=self.headers, **kwargs)

    def get_all_consents(
        self,
        consumer_id: str = None,
        status: str = None,
        access_frequency: str = None,
        post_usage_action: str = None,
        direct_marketing_allowed: bool = None,
        use_cases: List[str] = None,
        data_holder_brand_id: str = None,
        oldest_created: str = None,
        newest_created: str = None,
        oldest_revoked: str = None,
        newest_revoked: str = None,
        oldest_sharing_end_date: str = None,
        newest_sharing_end_date: str = None,
        external_id: str = None,
    ):
        """
        Retrieve all consents based on the provided query parameters.
        """
        params = {
            "consumerId": consumer_id,
            "status": status,
            "accessFrequency": access_frequency,
            "postUsageAction": post_usage_action,
            "directMarketingAllowed": direct_marketing_allowed,
            "useCases": use_cases,
            "dataHolderBrandId": data_holder_brand_id,
            "oldestCreated": oldest_created,
            "newestCreated": newest_created,
            "oldestRevoked": oldest_revoked,
            "newestRevoked": newest_revoked,
            "oldestSharingEndDate": oldest_sharing_end_date,
            "newestSharingEndDate": newest_sharing_end_date,
            "externalId": external_id,
        }
        url = f"{self.base_url}/consents"
        response = self._make_authenticated_request("GET", url, params=params)
        return response

    def create_consent(self, consent_data: CreateConsent):
        """
        Create a new consent.
        """
        url = f"{self.base_url}/consents"
        response = self._make_authenticated_request(
            "POST", url, data=json.dumps(consent_data)
        )
        return response

    def get_consent(self, consent_id: str):
        """
        Retrieve a specific consent by its ID.
        """
        url = f"{self.base_url}/consents/{consent_id}"
        response = self._make_authenticated_request("GET", url)
        return response

    def update_consent_via_dashboard(
        self, consent_id: str, consent_update_data: ConsentUpdateViaDashboardRequest
    ):
        """
        Update a consent via the dashboard.
        """
        url = f"{self.base_url}/consents/{consent_id}"
        response = self._make_authenticated_request(
            "PATCH", url, data=json.dumps(consent_update_data)
        )
        return response

    def revoke_consent(self, consent_id: str):
        """
        Revoke a consent by its ID.
        """
        url = f"{self.base_url}/consents/{consent_id}"
        response = self._make_authenticated_request("DELETE", url)
        return response

    def get_authorization_redirect_url(
        self, consent_id: str, state: str = None, redirect_uri: str = None
    ):
        """
        Get the authorization redirect URL for a consent.
        """
        params = {"state": state, "redirectUri": redirect_uri}
        url = f"{self.base_url}/consents/{consent_id}/authorization"
        response = self._make_authenticated_request("GET", url, params=params)
        return response

    def get_consent_events(
        self,
        oldest: str = None,
        newest: str = None,
        consent_id: str = None,
        page: int = None,
        page_size: int = None,
    ):
        """
        Retrieve consent events based on the provided query parameters.
        """
        params = {
            "oldest": oldest,
            "newest": newest,
            "consentId": consent_id,
            "page": page,
            "pageSize": page_size,
        }
        url = f"{self.base_url}/consents/events"
        response = self._make_authenticated_request("GET", url, params=params)
        return response

    def get_data_holders(self, software_product_id: str):
        """
        Retrieve data holders for a specific software product ID.
        """
        url = f"{self.base_url}/software-products/{software_product_id}/data-holders"
        response = self._make_authenticated_request("GET", url)
        return response

    def create_tokens(self, authorization_data: Authorization):
        """
        Create tokens for a specific authorization.
        """
        url = f"{self.base_url}/tokens"
        response = self._make_authenticated_request(
            "POST", url, data=json.dumps(authorization_data)
        )
        return response

    def get_use_cases(self, combine_scopes: bool = None):
        """
        Get use-cases based on the provided query parameters.
        """
        params = {"combineScopes": combine_scopes}
        url = f"{self.base_url}/use-cases"
        response = self._make_authenticated_request("GET", url, params=params)
        return response
