import requests
from urllib.parse import urljoin
from types import *


class FoodkitClientSDKException(Exception):
    pass


class FoodkitClientSDK:
    BASE_URL = "https://dev.foodkit.io/api"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _make_authenticated_request(
        self, method: str, path: str, **kwargs
    ) -> requests.Response:
        """Makes an authenticated request to the API."""
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        kwargs["headers"] = headers

        response = requests.request(method, urljoin(self.BASE_URL, path), **kwargs)

        if not 200 <= response.status_code < 300:
            raise FoodkitClientSDKException(
                f"Request failed with status {response.status_code}"
            )

        return response

    def register_customer(
        self, customer: CustomersRegisterCustomerRequest
    ) -> requests.Response:
        """Registers a new customer."""
        return self._make_authenticated_request(
            "POST", "/v1/storefront/customers", json=customer
        )

    def update_customer_details(
        self, customer: CustomersUpdateDetailsRequest
    ) -> requests.Response:
        """Updates customer details."""
        return self._make_authenticated_request(
            "PATCH", "/v1/storefront/customers/me", json=customer
        )

    def get_customer_details(self) -> requests.Response:
        """Gets customer details."""
        return self._make_authenticated_request("GET", "/v1/storefront/customers/me")

    def get_customer_addresses(self) -> requests.Response:
        """Gets customer addresses."""
        return self._make_authenticated_request(
            "GET", "/v2/storefront/customers/me/addresses"
        )

    def get_brand_context(self) -> requests.Response:
        """Gets brand context."""
        return self._make_authenticated_request("GET", "/v3/storefront/brands")

    def get_customer_orders(self) -> requests.Response:
        """Gets customer orders."""
        return self._make_authenticated_request(
            "GET", "/v3/storefront/customers/me/orders"
        )

    def get_promotions(self, vendor: int) -> requests.Response:
        """Gets promotions."""
        return self._make_authenticated_request(
            "GET", f"/v3/storefront/vendors/{vendor}/promotions"
        )

    def track_order_status(
        self, brand: int, customer: int, id: int
    ) -> requests.Response:
        """Tracks order status."""
        return self._make_authenticated_request(
            "GET",
            f"/v4/storefront/customers/brands/{brand}/customers/{customer}/orders/{id}/track",
        )

    def get_customer_tax_ids(self, brand: int, customer: int) -> requests.Response:
        """Gets customer tax IDs."""
        return self._make_authenticated_request(
            "GET",
            f"/v4/storefront/customers/brands/{brand}/customers/{customer}/tax-ids",
        )

    def store_customer_tax_id(
        self, brand: int, customer: int, tax_id: CustomersStoreTaxIdRequest
    ) -> requests.Response:
        """Stores customer tax ID."""
        return self._make_authenticated_request(
            "POST",
            f"/v4/storefront/customers/brands/{brand}/customers/{customer}/tax-ids",
            json=tax_id,
        )

    def submit_contact_form(
        self, tenant: int, customer: int, form: BranchesSubmitContactFormRequest
    ) -> requests.Response:
        """Submits contact form."""
        return self._make_authenticated_request(
            "POST",
            f"/v5/storefront/customers/tenants/{tenant}/customers/{customer}/contact-form",
            json=form,
        )

    def create_upsell_recommendations(
        self,
        brand: int,
        branch: int,
        products: MarketingCreateUpsellRecommendationsRequest,
    ) -> requests.Response:
        """Creates upsell recommendations."""
        return self._make_authenticated_request(
            "POST",
            f"/v5/storefront/inventory/brands/{brand}/branches/{branch}/upsells",
            json=products,
        )

    def create_order(
        self, tenant: str, order: OrdersCreateOrderRequest
    ) -> requests.Response:
        """Creates order."""
        return self._make_authenticated_request(
            "POST", f"/v5/storefront/tenants/{tenant}/orders", json=order
        )

    def get_quotation(
        self, tenant: str, quote: OrdersGetQuotationRequest
    ) -> requests.Response:
        """Gets quotation."""
        return self._make_authenticated_request(
            "POST", f"/v5/storefront/tenants/{tenant}/quotes", json=quote
        )

    def opt_in_service_area_email(
        self, tenant: int, email: CustomersOptInServiceAreaEmailRequest
    ) -> requests.Response:
        """Opts in service area email."""
        return self._make_authenticated_request(
            "POST", f"/v5/storefront/tenants/{tenant}/service-area-email", json=email
        )

    def store_gdpr_preferences(
        self,
        tenant: int,
        customer: int,
        preferences: CustomersStoreGdprPreferencesRequest,
    ) -> requests.Response:
        """Stores GDPR preferences."""
        return self._make_authenticated_request(
            "POST",
            f"/v6/storefront/customers/tenants/{tenant}/customers/{customer}/gdpr-preferences",
            json=preferences,
        )

    def generate_intercom_hmac(
        self, tenant: int, customer: int, channel: CustomersGenerateIntercomHmacRequest
    ) -> requests.Response:
        """Generates Intercom HMAC."""
        return self._make_authenticated_request(
            "POST",
            f"/v6/storefront/customers/tenants/{tenant}/customers/{customer}/intercom-hmacs",
            json=channel,
        )

    def get_punchcard_for_customer(
        self, tenant: int, customer: int
    ) -> requests.Response:
        """Gets punchcard for customer."""
        return self._make_authenticated_request(
            "GET",
            f"/v6/storefront/loyalty/tenants/{tenant}/customers/{customer}/punch-card",
        )

    def get_punchcard_for_guest(self, tenant: int) -> requests.Response:
        """Gets punchcard for guest."""
        return self._make_authenticated_request(
            "GET", f"/v6/storefront/loyalty/tenants/{tenant}/punch-card"
        )

    def get_referral_codes_for_customer(
        self, tenant: int, customer: int
    ) -> requests.Response:
        """Gets referral codes for customer."""
        return self._make_authenticated_request(
            "GET", f"/v6/storefront/referrals/tenants/{tenant}/customers/{customer}"
        )

    def list_delivery_zones(
        self, tenant: int, latitude: float, longitude: float
    ) -> requests.Response:
        """Lists delivery zones."""
        return self._make_authenticated_request(
            "GET",
            f"/v6/storefront/tenants/{tenant}/delivery-zones",
            params={"latitude": latitude, "longitude": longitude},
        )
