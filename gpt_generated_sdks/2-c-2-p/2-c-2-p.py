import requests
from types import *


class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def _make_authenticated_request(self, method: str, path: str, json: dict = None):
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, headers=headers, json=json)
        return response

    def ApplePay_validateMerchant(self, data: MerchantValidationApplePay):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/applepay/merchantvalidation", json=data
        )

    def Cache_cleanCache(self):
        return self._make_authenticated_request("POST", "/payment/4.3/cache/cleancache")

    def CancelTransaction_post(self, data: PaymentBaseRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/canceltransaction", json=data
        )

    def CardInstallmentPlanInfo_create(self, data: CardInstallmentPlanInfoRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/cardinstallmentplaninfo", json=data
        )

    def CardTokenInfo_getCardTokenInfo(self, data: PaymentBaseRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/cardtokeninfo", json=data
        )

    def ExchangeRate_getRate(self, data: PaymentExchangeRateConverterRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/exchangerate", json=data
        )

    def ExchangeRate_requestEndpoint(self, data: PayloadRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/exchangerate/secure", json=data
        )

    def ExchangeRate_apmMcc(self, data: PaymentBaseRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/exchangerate/apmmccexchangerate", json=data
        )

    def Initialization_requestCreation(self):
        return self._make_authenticated_request("POST", "/payment/4.3/initialization")

    def LoyaltyPointInfo_postLoyaltyPointInfo(
        self, data: PaymentLoyaltyPointInfoRequest
    ):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/loyaltypointinfo", json=data
        )

    def Payment_createPayment(self, data: PaymentRequestV43):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/payment", json=data
        )

    def PaymentInquiry_postPaymentDetails(self, data: PayloadRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/paymentinquiry", json=data
        )

    def PaymentInstruction_submitInstruction(self, data: PayloadRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/paymentinstruction", json=data
        )

    def PaymentNotification_processNotification(self, data: PaymentNotificationRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/paymentnotification", json=data
        )

    def PaymentOption_createPaymentOption(self, data: PaymentBaseRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/paymentoption", json=data
        )

    def PaymentOptionDetails_postOptionDetails(self, data: PaymentOptionDetailsRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/paymentoptiondetails", json=data
        )

    def PaymentSimulate_executePaymentSimulation(self, data: PayloadRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/paymentsimulate", json=data
        )

    def PaymentToken_generateToken(self, data: PayloadRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/paymenttoken", json=data
        )

    def RedirectBackEnd_postPaymentRedirect(self):
        return self._make_authenticated_request("POST", "/payment/4.3/redirectbackend")

    def RedirectFrontEnd_postPaymentRedirect(self):
        return self._make_authenticated_request("POST", "/payment/4.3/redirectfrontend")

    def TransactionStatus_updateTransactionStatus(self, data: TransactionStatusRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/transactionstatus", json=data
        )

    def UserPreference_saveUserPreference(self, data: PaymentBaseRequest):
        return self._make_authenticated_request(
            "POST", "/payment/4.3/userpreference", json=data
        )
