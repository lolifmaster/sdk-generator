import requests
import json
from typing import Optional, Dict, Any


class CDRInsightsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://cdr-insights-prod.api.adatree.com.au"

    def _make_authenticated_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.request(
                method, url, headers=headers, params=params, data=json.dumps(data)
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise CustomException(f"Error making request: {e}")
        return response

    def get_cdr_arrangement_accounts(
        self, cdr_arrangement_id: str
    ) -> requests.Response:
        """Get accounts under a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/accounts"
        return self._make_authenticated_request("GET", url)

    def get_filtered_balances(self, cdr_arrangement_id: str) -> requests.Response:
        """Get filtered balances for a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/accounts/balances"
        return self._make_authenticated_request("GET", url)

    def obtain_single_account_balance(
        self, cdr_arrangement_id: str, account_id: str
    ) -> requests.Response:
        """Get balance for a single account under a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/accounts/{account_id}/balance"
        return self._make_authenticated_request("GET", url)

    def obtain_account_detail(
        self, cdr_arrangement_id: str, account_id: str
    ) -> requests.Response:
        """Get account details for a single account under a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/accounts/{account_id}"
        return self._make_authenticated_request("GET", url)

    def get_transactions_for_account(
        self, cdr_arrangement_id: str, account_id: str
    ) -> requests.Response:
        """Get transactions for a single account under a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/accounts/{account_id}/transactions"
        return self._make_authenticated_request("GET", url)

    def get_transaction_detail(
        self, cdr_arrangement_id: str, account_id: str, transaction_id: str
    ) -> requests.Response:
        """Get transaction details for a single transaction under a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/accounts/{account_id}/transactions/{transaction_id}"
        return self._make_authenticated_request("GET", url)

    def get_direct_debits_for_account(
        self, cdr_arrangement_id: str, account_id: str
    ) -> requests.Response:
        """Get direct debits for a single account under a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/accounts/{account_id}/direct-debits"
        return self._make_authenticated_request("GET", url)

    def get_bulk_direct_debits(self, cdr_arrangement_id: str) -> requests.Response:
        """Get bulk direct debits for a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/accounts/direct-debits"
        return self._make_authenticated_request("GET", url)

    def get_scheduled_payments_for_account(
        self, cdr_arrangement_id: str, account_id: str
    ) -> requests.Response:
        """Get scheduled payments for a single account under a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/accounts/{account_id}/payments/scheduled"
        return self._make_authenticated_request("GET", url)

    def get_scheduled_payments_bulk(self, cdr_arrangement_id: str) -> requests.Response:
        """Get bulk scheduled payments for a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/payments/scheduled"
        return self._make_authenticated_request("GET", url)

    def get_payees(self, cdr_arrangement_id: str) -> requests.Response:
        """Get payees for a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/payees"
        return self._make_authenticated_request("GET", url)

    def get_payee_detail(
        self, cdr_arrangement_id: str, payee_id: str
    ) -> requests.Response:
        """Get payee details for a single payee under a CDR arrangement ID."""
        url = f"{self.base_url}/adr/banking/arrangements/{cdr_arrangement_id}/payees/{payee_id}"
        return self._make_authenticated_request("GET", url)

    def get_user_info_by_arrangement_id(
        self, cdr_arrangement_id: str
    ) -> requests.Response:
        """Get user information for a CDR arrangement ID."""
        url = f"{self.base_url}/adr/common/arrangements/{cdr_arrangement_id}/userinfo"
        return self._make_authenticated_request("GET", url)

    def get_customer_info(self, cdr_arrangement_id: str) -> requests.Response:
        """Get customer information for a CDR arrangement ID."""
        url = f"{self.base_url}/adr/common/arrangements/{cdr_arrangement_id}/customer"
        return self._make_authenticated_request("GET", url)

    def obtain_detailed_customer_info(
        self, cdr_arrangement_id: str
    ) -> requests.Response:
        """Get detailed customer information for a CDR arrangement ID."""
        url = f"{self.base_url}/adr/common/arrangements/{cdr_arrangement_id}/customer/detail"
        return self._make_authenticated_request("GET", url)

    def get_status(self) -> requests.Response:
        """Get API status."""
        url = f"{self.base_url}/adr/discovery/status"
        return self._make_authenticated_request("GET", url)

    def get_outages(self) -> requests.Response:
        """Get API outages."""
        url = f"{self.base_url}/adr/discovery/outages"
        return self._make_authenticated_request("GET", url)


class CustomException(Exception):
    pass
