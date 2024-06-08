import requests
from urllib.parse import urljoin
from types import *


class BlueSnapClient:
    def __init__(
        self, api_key: str, base_url: str = "https://sandbox.bluesnap.com/services/2"
    ):
        self.api_key = api_key
        self.base_url = base_url

    def _make_authenticated_request(
        self, method: str, url: str, data=None, params=None
    ):
        """Make an authenticated request using the provided method, url, data, and params."""
        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.request(
            method, url, headers=headers, json=data, params=params
        )
        response.raise_for_status()
        return response

    def authorization_create_transaction(
        self, data: AuthorizationCreateTransactionRequest
    ):
        """Create an authorization transaction."""
        url = urljoin(self.base_url, "transactions")
        return self._make_authenticated_request("POST", url, data=data)

    def reversal_auth_transaction(self, data: ReversalAuthTransactionRequest):
        """Reverse an authorization transaction."""
        url = urljoin(self.base_url, "transactions")
        return self._make_authenticated_request("PUT", url, data=data)

    def transaction_get_by_id(self, transaction_id: str):
        """Get a transaction by its ID."""
        url = urljoin(self.base_url, f"transactions/{transaction_id}")
        return self._make_authenticated_request("GET", url)

    def transaction_create_sofort_transaction(
        self, data: TransactionCreateSofortTransactionRequest
    ):
        """Create a Sofort transaction."""
        url = urljoin(self.base_url, "alt-transactions")
        return self._make_authenticated_request("POST", url, data=data)

    def transaction_update_paypal_transaction(
        self, data: TransactionUpdatePaypalTransactionRequest
    ):
        """Update a PayPal transaction."""
        url = urljoin(self.base_url, "alt-transactions")
        return self._make_authenticated_request("PUT", url, data=data)

    def transaction_get_sepa_dd(self, transaction_id: str):
        """Get a SEPA Direct Debit transaction."""
        url = urljoin(self.base_url, f"alt-transactions/{transaction_id}")
        return self._make_authenticated_request("GET", url)

    def transaction_get_sofort_transaction(self, order_id: int):
        """Get a Sofort transaction by order ID."""
        url = urljoin(self.base_url, "alt-transactions/resolve")
        params = {"orderId": order_id}
        return self._make_authenticated_request("GET", url, params=params)

    def agreement_create_debit_for_aus_can(
        self,
        region: str,
        debit_type: str,
        planid: str = None,
        overriderecurringchargeamount: str = None,
    ):
        """Create a debit agreement for Australia or Canada."""
        url = urljoin(self.base_url, f"agreements/debit/{region}/{debit_type}")
        params = {
            "planid": planid,
            "overriderecurringchargeamount": overriderecurringchargeamount,
        }
        return self._make_authenticated_request("POST", url, params=params)

    def agreement_get_debit(self, agreement_id: str = None):
        """Get a debit agreement by its ID."""
        url = urljoin(
            self.base_url,
            f"agreements/{agreement_id}" if agreement_id else "agreements",
        )
        return self._make_authenticated_request("GET", url)

    def transaction_get_pre_notification_debit_agreement(
        self, transaction_id: str = None
    ):
        """Get a pre-notification debit agreement by its transaction ID."""
        url = urljoin(
            self.base_url,
            f"agreements/prenotification/{transaction_id}"
            if transaction_id
            else "agreements/prenotification",
        )
        return self._make_authenticated_request("GET", url)

    def transaction_get_paypal_transaction(self, order_id: str):
        """Get a PayPal transaction by order ID."""
        url = urljoin(self.base_url, f"alt-transactions/resolve/{order_id}")
        return self._make_authenticated_request("GET", url)

    def transaction_create_batch_transaction(
        self, data: TransactionCreateBatchTransactionRequest
    ):
        """Create a batch transaction."""
        url = urljoin(self.base_url, "batch-transactions")
        return self._make_authenticated_request("POST", url, data=data)

    def transaction_initiate_refund(
        self, transaction_id: str, data: TransactionInitiateRefundRequest
    ):
        """Initiate a refund for a transaction."""
        url = urljoin(self.base_url, f"transactions/refund/{transaction_id}")
        return self._make_authenticated_request("POST", url, data=data)

    def transaction_cancel_pending_refund(self, transaction_id: str):
        """Cancel a pending refund for a transaction."""
        url = urljoin(self.base_url, f"transactions/pending-refund/{transaction_id}")
        return self._make_authenticated_request("DELETE", url)

    def shopper_create_vaulted_shopper(self, data: ShopperCreateVaultedShopperRequest):
        """Create a vaulted shopper."""
        url = urljoin(self.base_url, "vaulted-shoppers")
        return self._make_authenticated_request("POST", url, data=data)

    def shopper_update_vaulted_shopper(
        self, vaulted_shopper_id: str, data: ShopperUpdateVaultedShopperRequest
    ):
        """Update a vaulted shopper."""
        url = urljoin(self.base_url, f"vaulted-shoppers/{vaulted_shopper_id}")
        return self._make_authenticated_request("PUT", url, data=data)

    def shopper_get(self, vaulted_shopper_id: str):
        """Get a vaulted shopper by its ID."""
        url = urljoin(self.base_url, f"vaulted-shoppers/{vaulted_shopper_id}")
        return self._make_authenticated_request("GET", url)

    def shopper_delete_vaulted_shopper(self, vaulted_shopper_id: str):
        """Delete a vaulted shopper."""
        url = urljoin(self.base_url, f"vaulted-shoppers/{vaulted_shopper_id}")
        return self._make_authenticated_request("DELETE", url)

    def plan_create_recurring_plan(self, data: PlanCreateRecurringPlanRequest):
        """Create a recurring plan."""
        url = urljoin(self.base_url, "recurring/plans")
        return self._make_authenticated_request("POST", url, data=data)

    def plan_update_recurring_plan(
        self, plan_id: int, data: PlanUpdateRecurringPlanRequest
    ):
        """Update a recurring plan."""
        url = urljoin(self.base_url, f"recurring/plans/{plan_id}")
        return self._make_authenticated_request("PUT", url, data=data)

    def plan_get_specific(self, plan_id: int):
        """Get a specific recurring plan."""
        url = urljoin(self.base_url, f"recurring/plans/{plan_id}")
        return self._make_authenticated_request("GET", url)

    def plan_get_all(
        self,
        pagesize: str = None,
        after: str = None,
        gettotal: bool = None,
        fulldescription: bool = None,
    ):
        """Get all recurring plans."""
        url = urljoin(self.base_url, "recurring/plansparameters")
        params = {
            "pagesize": pagesize,
            "after": after,
            "gettotal": gettotal,
            "fulldescription": fulldescription,
        }
        return self._make_authenticated_request("GET", url, params=params)

    def subscription_create_new(self, data: SubscriptionCreateNewRequest):
        """Create a new subscription."""
        url = urljoin(self.base_url, "recurring/subscriptions")
        return self._make_authenticated_request("POST", url, data=data)

    def subscription_update_subscription(
        self, subscription_id: int, data: SubscriptionUpdateSubscriptionRequest
    ):
        """Update a subscription."""
        url = urljoin(self.base_url, f"recurring/subscriptions/{subscription_id}")
        return self._make_authenticated_request("PUT", url, data=data)

    def subscription_get_specific(self, subscription_id: int):
        """Get a specific subscription."""
        url = urljoin(self.base_url, f"recurring/subscriptions/{subscription_id}")
        return self._make_authenticated_request("GET", url)

    def subscription_create_merchant_managed_subscription(
        self, data: SubscriptionCreateMerchantManagedSubscriptionRequest
    ):
        """Create a merchant-managed subscription."""
        url = urljoin(self.base_url, "recurring/ondemand")
        return self._make_authenticated_request("POST", url, data=data)

    def subscription_create_merchant_managed_charge(
        self, subscription_id: int, data: SubscriptionCreateMerchantManagedChargeRequest
    ):
        """Create a merchant-managed charge."""
        url = urljoin(self.base_url, f"recurring/ondemand/{subscription_id}")
        return self._make_authenticated_request("POST", url, data=data)

    def subscription_get_switch_charge_amount(
        self, subscription_id: int, newplanid: str = None, newquantity: str = None
    ):
        """Get the switch charge amount for a subscription."""
        url = urljoin(
            self.base_url,
            f"recurring/subscriptions/{subscription_id}/switch-charge-amount",
        )
        params = {"newplanid": newplanid, "newquantity": newquantity}
        return self._make_authenticated_request("GET", url, params=params)

    def transaction_approve_merchant_transaction(
        self, transactionid: str = None, approvetransaction: bool = None
    ):
        """Approve a merchant transaction."""
        url = urljoin(self.base_url, "transactions/approval")
        params = {
            "transactionid": transactionid,
            "approvetransaction": approvetransaction,
        }
        return self._make_authenticated_request("PUT", url, params=params)

    def vendor_create(self, data: VendorCreateRequest):
        """Create a vendor."""
        url = urljoin(self.base_url, "vendors")
        return self._make_authenticated_request("POST", url, data=data)

    def vendor_update_vendor(self, vendor_id: int, data: VendorUpdateVendorRequest):
        """Update a vendor."""
        url = urljoin(self.base_url, f"vendors/{vendor_id}")
        return self._make_authenticated_request("PUT", url, data=data)

    def vendor_get_vendor(self, vendor_id: int):
        """Get a vendor by its ID."""
        url = urljoin(self.base_url, f"vendors/{vendor_id}")
        return self._make_authenticated_request("GET", url)
