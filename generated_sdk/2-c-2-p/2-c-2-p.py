import requests
from typing import Optional
from dataclasses import asdict
from types import (
    MerchantValidationApplePay,
    PaymentBaseRequest,
    CardInstallmentPlanInfoRequest,
    PaymentExchangeRateConverterRequest,
    PayloadRequest,
    PaymentLoyaltyPointInfoRequest,
    PaymentRequestV43,
    PaymentNotificationRequest,
    PaymentOptionDetailsRequest,
    TransactionStatusRequest,
)


class TwoC2PClient:
    def __init__(self, api_key: str, base_url: str = "https://sandbox-pgw.2c2p.com"):
        self.api_key = api_key
        self.base_url = base_url

    def _make_authenticated_request(
        self, method: str, url: str, data: Optional[dict] = None
    ) -> requests.Response:
        """
        Make an authenticated request to the API.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        return requests.request(method, url, json=data, headers=headers)

    def applepay_validate_merchant(
        self, data: MerchantValidationApplePay
    ) -> requests.Response:
        """
        Validate Apple Pay merchant.
        """
        url = f"{self.base_url}/payment/4.3/applepay/merchantvalidation"
        return self._make_authenticated_request("POST", url, asdict(data))

    def cache_clean_cache(self) -> requests.Response:
        """
        Clean the cache.
        """
        url = f"{self.base_url}/payment/4.3/cache/cleancache"
        return self._make_authenticated_request("POST", url)

    def cancel_transaction(self, data: PaymentBaseRequest) -> requests.Response:
        """
        Cancel a transaction.
        """
        url = f"{self.base_url}/payment/4.3/canceltransaction"
        return self._make_authenticated_request("POST", url, asdict(data))

    def card_installment_plan_info_create(
        self, data: CardInstallmentPlanInfoRequest
    ) -> requests.Response:
        """
        Create card installment plan info.
        """
        url = f"{self.base_url}/payment/4.3/cardinstallmentplaninfo"
        return self._make_authenticated_request("POST", url, asdict(data))

    def card_token_info_get_card_token_info(
        self, data: PaymentBaseRequest
    ) -> requests.Response:
        """
        Get card token info.
        """
        url = f"{self.base_url}/payment/4.3/cardtokeninfo"
        return self._make_authenticated_request("POST", url, asdict(data))

    def exchange_rate_get_rate(
        self, data: PaymentExchangeRateConverterRequest
    ) -> requests.Response:
        """
        Get exchange rate.
        """
        url = f"{self.base_url}/payment/4.3/exchangerate"
        return self._make_authenticated_request("POST", url, asdict(data))

    def exchange_rate_request_endpoint(self, data: PayloadRequest) -> requests.Response:
        """
        Request exchange rate endpoint.
        """
        url = f"{self.base_url}/payment/4.3/exchangerate/secure"
        return self._make_authenticated_request("POST", url, asdict(data))

    def exchange_rate_apm_mcc(self, data: PaymentBaseRequest) -> requests.Response:
        """
        Get exchange rate for APM MCC.
        """
        url = f"{self.base_url}/payment/4.3/exchangerate/apmmccexchangerate"
        return self._make_authenticated_request("POST", url, asdict(data))

    def initialization_request_creation(self) -> requests.Response:
        """
        Create initialization request.
        """
        url = f"{self.base_url}/payment/4.3/initialization"
        return self._make_authenticated_request("POST", url)

    def loyalty_point_info_post_loyalty_point_info(
        self, data: PaymentLoyaltyPointInfoRequest
    ) -> requests.Response:
        """
        Post loyalty point info.
        """
        url = f"{self.base_url}/payment/4.3/loyaltypointinfo"
        return self._make_authenticated_request("POST", url, asdict(data))

    def payment_create_payment(self, data: PaymentRequestV43) -> requests.Response:
        """
        Create a payment.
        """
        url = f"{self.base_url}/payment/4.3/payment"
        return self._make_authenticated_request("POST", url, asdict(data))

    def payment_inquiry_post_payment_details(
        self, data: PayloadRequest
    ) -> requests.Response:
        """
        Post payment details for inquiry.
        """
        url = f"{self.base_url}/payment/4.3/paymentinquiry"
        return self._make_authenticated_request("POST", url, asdict(data))

    def payment_instruction_submit_instruction(
        self, data: PayloadRequest
    ) -> requests.Response:
        """
        Submit payment instruction.
        """
        url = f"{self.base_url}/payment/4.3/paymentinstruction"
        return self._make_authenticated_request("POST", url, asdict(data))

    def payment_notification_process_notification(
        self, data: PaymentNotificationRequest
    ) -> requests.Response:
        """
        Process payment notification.
        """
        url = f"{self.base_url}/payment/4.3/paymentnotification"
        return self._make_authenticated_request("POST", url, asdict(data))

    def payment_option_create_payment_option(
        self, data: PaymentBaseRequest
    ) -> requests.Response:
        """
        Create a payment option.
        """
        url = f"{self.base_url}/payment/4.3/paymentoption"
        return self._make_authenticated_request("POST", url, asdict(data))

    def payment_option_details_post_option_details(
        self, data: PaymentOptionDetailsRequest
    ) -> requests.Response:
        """
        Post payment option details.
        """
        url = f"{self.base_url}/payment/4.3/paymentoptiondetails"
        return self._make_authenticated_request("POST", url, asdict(data))

    def payment_simulate_execute_payment_simulation(
        self, data: PayloadRequest
    ) -> requests.Response:
        """
        Execute payment simulation.
        """
        url = f"{self.base_url}/payment/4.3/paymentsimulate"
        return self._make_authenticated_request("POST", url, asdict(data))

    def payment_token_generate_token(self, data: PayloadRequest) -> requests.Response:
        """
        Generate a payment token.
        """
        url = f"{self.base_url}/payment/4.3/paymenttoken"
        return self._make_authenticated_request("POST", url, asdict(data))

    def redirect_back_end_post_payment_redirect(self) -> requests.Response:
        """
        Post payment redirect for back end.
        """
        url = f"{self.base_url}/payment/4.3/redirectbackend"
        return self._make_authenticated_request("POST", url)

    def redirect_front_end_post_payment_redirect(self) -> requests.Response:
        """
        Post payment redirect for front end.
        """
        url = f"{self.base_url}/payment/4.3/redirectfrontend"
        return self._make_authenticated_request("POST", url)

    def transaction_status_update_transaction_status(
        self, data: TransactionStatusRequest
    ) -> requests.Response:
        """
        Update transaction status.
        """
        url = f"{self.base_url}/payment/4.3/transactionstatus"
        return self._make_authenticated_request("POST", url, asdict(data))

    def user_preference_save_user_preference(
        self, data: PaymentBaseRequest
    ) -> requests.Response:
        """
        Save user preference.
        """
        url = f"{self.base_url}/payment/4.3/userpreference"
        return self._make_authenticated_request("POST", url, asdict(data))
