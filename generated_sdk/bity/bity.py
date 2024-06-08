import requests
from typing import Optional, List
from types import *


class BityClient:
    def __init__(self, api_key: str):
        self.base_url = "https://exchange.api.bity.com/v2"
        self.api_key = api_key

    def _make_authenticated_request(
        self, method: str, endpoint: str, **kwargs
    ) -> requests.Response:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}{endpoint}"
        return requests.request(method, url, headers=headers, **kwargs)

    def get_currencies(
        self, tags: Optional[List[CurrencyTag]] = None
    ) -> requests.Response:
        """Get a list of currencies."""
        endpoint = "/currencies"
        params = {}
        if tags:
            params["tags"] = tags
        return self._make_authenticated_request("GET", endpoint, params=params)

    def get_currency_by_code(self, currency_code: CurrencyCode) -> requests.Response:
        """Get currency details by code."""
        endpoint = f"/currencies/{currency_code}"
        return self._make_authenticated_request("GET", endpoint)

    def list_orders(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        status: Optional[str] = None,
    ) -> requests.Response:
        """List orders with optional filters."""
        endpoint = "/orders"
        params = {
            k: v
            for k, v in {"page": page, "page_size": page_size, "status": status}.items()
            if v is not None
        }
        return self._make_authenticated_request("GET", endpoint, params=params)

    def place_order(self, place_order_request: PlaceOrderRequest) -> requests.Response:
        """Place a new order."""
        endpoint = "/orders"
        return self._make_authenticated_request(
            "POST", endpoint, json=place_order_request
        )

    def calculate_amount_estimate(
        self, amount_estimate_request: AmountEstimateRequest
    ) -> requests.Response:
        """Calculate amount estimate for an order."""
        endpoint = "/orders/estimate"
        return self._make_authenticated_request(
            "POST", endpoint, json=amount_estimate_request
        )

    def perform_multiple_estimations(
        self,
        orders_perform_multiple_estimations_request: OrdersPerformMultipleEstimationsRequest,
    ) -> requests.Response:
        """Perform multiple estimations for orders."""
        endpoint = "/orders/estimate/multiple"
        return self._make_authenticated_request(
            "POST", endpoint, json=orders_perform_multiple_estimations_request
        )

    def get_order_details(self, order_uuid: str) -> requests.Response:
        """Get order details by UUID."""
        endpoint = f"/orders/{order_uuid}"
        return self._make_authenticated_request("GET", endpoint)

    def get_qr_bill(self, order_uuid: str) -> requests.Response:
        """Get QR bill for a bank transfer order."""
        endpoint = f"/orders/{order_uuid}/bank_transfer_qr_bill"
        return self._make_authenticated_request("GET", endpoint)

    def cancel_order(self, order_uuid: str) -> requests.Response:
        """Cancel an order by UUID."""
        endpoint = f"/orders/{order_uuid}/cancel"
        return self._make_authenticated_request("POST", endpoint)

    def duplicate_order(self, order_uuid: str) -> requests.Response:
        """Duplicate an order by UUID."""
        endpoint = f"/orders/{order_uuid}/duplicate"
        return self._make_authenticated_request("POST", endpoint)

    def execute_order(self, order_uuid: str) -> requests.Response:
        """Execute an order by UUID."""
        endpoint = f"/orders/{order_uuid}/execute"
        return self._make_authenticated_request("POST", endpoint)

    def submit_signature(self, order_uuid: str) -> requests.Response:
        """Submit a signature for an order."""
        endpoint = f"/orders/{order_uuid}/signature"
        return self._make_authenticated_request("POST", endpoint)

    def get_currency_pairs(
        self,
        input: Optional[str] = None,
        output: Optional[str] = None,
        enabled: Optional[str] = None,
    ) -> requests.Response:
        """Get currency pairs with optional filters."""
        endpoint = "/pairs"
        params = {
            k: v
            for k, v in {"input": input, "output": output, "enabled": enabled}.items()
            if v is not None
        }
        return self._make_authenticated_request("GET", endpoint, params=params)
