import requests


class AdatreeClient:
    def __init__(self, api_key: str):
        self.base_url = "https://cdr-insights-prod.api.adatree.com.au"
        self.api_key = api_key

    def _make_authenticated_request(
        self, method: str, endpoint: str, params: dict = None, headers: dict = None
    ) -> requests.Response:
        """Makes an authenticated request to the API."""
        url = f"{self.base_url}{endpoint}"
        headers = headers or {}
        headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"
        try:
            return requests.request(method, url, params=params, headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_banking_accounts(self, params: dict = None) -> requests.Response:
        """Gets banking accounts."""
        endpoint = "/data/banking/accounts"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_banking_transactions(self, params: dict = None) -> requests.Response:
        """Gets banking transactions."""
        endpoint = "/data/banking/transactions"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_banking_payees(self, params: dict = None) -> requests.Response:
        """Gets banking payees."""
        endpoint = "/data/banking/payees"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_banking_direct_debits(self, params: dict = None) -> requests.Response:
        """Gets banking direct debits."""
        endpoint = "/data/banking/payments/direct-debits"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_scheduled_payments(self, params: dict = None) -> requests.Response:
        """Gets scheduled payments."""
        endpoint = "/data/banking/payments/scheduled"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_banking_products(self, params: dict = None) -> requests.Response:
        """Gets banking products."""
        endpoint = "/data/banking/products"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_customers(self, params: dict = None) -> requests.Response:
        """Gets customers."""
        endpoint = "/data/common/customers"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_energy_plans(self, params: dict = None) -> requests.Response:
        """Gets energy plans."""
        endpoint = "/data/energy/plans"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_energy_accounts(self, params: dict = None) -> requests.Response:
        """Gets energy accounts."""
        endpoint = "/data/energy/accounts"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_energy_invoices(self, params: dict = None) -> requests.Response:
        """Gets energy invoices."""
        endpoint = "/data/energy/invoices"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_energy_bills(self, params: dict = None) -> requests.Response:
        """Gets energy bills."""
        endpoint = "/data/energy/bills"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_electricity_service_points(self, params: dict = None) -> requests.Response:
        """Gets electricity service points."""
        endpoint = "/data/energy/electricity/servicepoints"
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_electricity_usage(self, params: dict = None) -> requests.Response:
        """Gets electricity usage."""
        endpoint = "/data/energy/electricity/usage"
        return self._make_authenticated_request("GET", endpoint, params=params)
