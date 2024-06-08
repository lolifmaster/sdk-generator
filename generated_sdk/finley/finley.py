import requests
from types import *
from typing import Any


class FinleyCMSException(Exception):
    """Exception raised for errors in the FinleyCMS SDK."""


class FinleyCMSClient:
    def __init__(self, base_url: str, api_key: str):
        """Initializes the FinleyCMSClient with the given base URL and API key."""
        self.base_url = base_url
        self.api_key = api_key

    def _make_authenticated_request(
        self, method: str, path: str, **kwargs: Any
    ) -> requests.Response:
        """Makes an authenticated request to the FinleyCMS API."""
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        kwargs["headers"] = headers
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, **kwargs)
        if response.status_code >= 400:
            raise FinleyCMSException(
                f"Request failed with status {response.status_code}"
            )
        return response

    def get_borrowing_base_report_by_id(
        self, creditFacilityId: str, borrowingBaseReportId: str
    ) -> requests.Response:
        """Gets a borrowing base report by its ID."""
        path = f"/credit-facilities/{creditFacilityId}/borrowing-base-reports/{borrowingBaseReportId}"
        return self._make_authenticated_request("GET", path)

    def get_borrowing_base_reports(self, creditFacilityId: str) -> requests.Response:
        """Gets all borrowing base reports for a given credit facility."""
        path = f"/credit-facilities/{creditFacilityId}/borrowing-base-reports"
        return self._make_authenticated_request("GET", path)

    def get_credit_facility_by_id(self, creditFacilityId: str) -> requests.Response:
        """Gets a credit facility by its ID."""
        path = f"/credit-facilities/{creditFacilityId}"
        return self._make_authenticated_request("GET", path)

    def get_credit_facilities(self) -> requests.Response:
        """Gets all credit facilities."""
        path = "/credit-facilities"
        return self._make_authenticated_request("GET", path)

    def get_expenses_fees_report(
        self, creditFacilityId: str, startDate: str = None, endDate: str = None
    ) -> requests.Response:
        """Gets an expenses/fees report for a given credit facility and date range."""
        path = f"/credit-facilities/{creditFacilityId}/expenses-fees"
        params = {}
        if startDate:
            params["startDate"] = startDate
        if endDate:
            params["endDate"] = endDate
        return self._make_authenticated_request("GET", path, params=params)

    def get_funding_request_by_id(
        self, creditFacilityId: str, fundingRequestId: str
    ) -> requests.Response:
        """Gets a funding request by its ID."""
        path = (
            f"/credit-facilities/{creditFacilityId}/funding-requests/{fundingRequestId}"
        )
        return self._make_authenticated_request("GET", path)

    def get_funding_requests(
        self,
        creditFacilityId: str,
        borrowingBaseReportId: str = None,
        status: str = None,
    ) -> requests.Response:
        """Gets all funding requests for a given credit facility, borrowing base report, and status."""
        path = f"/credit-facilities/{creditFacilityId}/funding-requests"
        params = {}
        if borrowingBaseReportId:
            params["borrowingBaseReportId"] = borrowingBaseReportId
        if status:
            params["status"] = status
        return self._make_authenticated_request("GET", path, params=params)

    def create_funding_request(
        self, creditFacilityId: str, body: FundingRequestSubmissionRequestBody
    ) -> requests.Response:
        """Creates a new funding request."""
        path = f"/credit-facilities/{creditFacilityId}/funding-requests"
        return self._make_authenticated_request("POST", path, json=body)

    def get_component_by_id(
        self,
        creditFacilityId: str,
        fundingRequestId: str,
        fundingRequestComponentId: str,
    ) -> requests.Response:
        """Gets a funding request component by its ID."""
        path = f"/credit-facilities/{creditFacilityId}/funding-requests/{fundingRequestId}/components/{fundingRequestComponentId}"
        return self._make_authenticated_request("GET", path)

    def get_components_by_request_id(
        self, creditFacilityId: str, fundingRequestId: str
    ) -> requests.Response:
        """Gets all components for a given funding request."""
        path = f"/credit-facilities/{creditFacilityId}/funding-requests/{fundingRequestId}/components"
        return self._make_authenticated_request("GET", path)

    def settle_component(
        self,
        creditFacilityId: str,
        fundingRequestId: str,
        fundingRequestComponentId: str,
        body: SettleRequestBody,
    ) -> requests.Response:
        """Settles a funding request component."""
        path = f"/credit-facilities/{creditFacilityId}/funding-requests/{fundingRequestId}/components/{fundingRequestComponentId}/settle"
        return self._make_authenticated_request("PUT", path, json=body)

    def submit_funding_request(
        self,
        creditFacilityId: str,
        fundingRequestId: str,
        body: FundingRequestSubmissionRequestBody,
    ) -> requests.Response:
        """Submits a funding request."""
        path = f"/credit-facilities/{creditFacilityId}/funding-requests/{fundingRequestId}/submit"
        return self._make_authenticated_request("PUT", path, json=body)
