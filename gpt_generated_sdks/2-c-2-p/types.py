from typing import TypedDict, Optional, List, NotRequired
from typing_extensions import NotRequired


class BrowserDetails(TypedDict, total=False):
    version: Optional[str]
    deviceType: Optional[str]
    name: Optional[str]
    os: Optional[str]


class MerchantValidationApplePay(TypedDict):
    paymentToken: str
    validationUrl: NotRequired[Optional[str]]
    locale: NotRequired[Optional[str]]
    clientID: str
    browserDetails: NotRequired[BrowserDetails]


class PaymentBaseRequest(TypedDict):
    paymentToken: str
    locale: NotRequired[Optional[str]]
    clientID: str
    browserDetails: NotRequired[BrowserDetails]


class CardInstallmentPlanInfoRequest(TypedDict):
    paymentToken: str
    cardNo: NotRequired[Optional[str]]
    bankCode: NotRequired[Optional[str]]
    locale: NotRequired[Optional[str]]
    clientID: str
    browserDetails: NotRequired[BrowserDetails]


class PaymentExchangeRateConverterRequest(TypedDict):
    paymentToken: str
    bin: NotRequired[Optional[str]]
    locale: NotRequired[Optional[str]]
    clientID: str
    browserDetails: NotRequired[BrowserDetails]


class PayloadRequest(TypedDict, total=False):
    payload: Optional[str]


class PaymentLoyaltyPointInfoRequest(TypedDict):
    paymentToken: str
    providerID: NotRequired[Optional[str]]
    profileID: NotRequired[Optional[str]]
    referenceID: NotRequired[Optional[str]]
    cardNo: NotRequired[Optional[str]]
    expiryMonth: NotRequired[Optional[str]]
    expiryYear: NotRequired[Optional[str]]
    locale: NotRequired[Optional[str]]
    clientID: str
    browserDetails: NotRequired[BrowserDetails]


class LoyaltyRewards(TypedDict):
    id: NotRequired[Optional[str]]
    Quantity: float


class LoyaltyDetails(TypedDict):
    providerID: NotRequired[Optional[str]]
    accountNo: NotRequired[Optional[str]]
    accountAuthData: NotRequired[Optional[str]]
    queryReferenceSpecified: NotRequired[bool]
    externalMerchantId: NotRequired[Optional[str]]
    redeemAmount: float
    rewards: NotRequired[Optional[List[LoyaltyRewards]]]


class PaymentParamsDataRequestV43(TypedDict):
    accountTokenization: bool
    customerToken: NotRequired[Optional[str]]
    name: NotRequired[Optional[str]]
    email: NotRequired[Optional[str]]
    mobileNo: NotRequired[Optional[str]]
    accountNo: NotRequired[Optional[str]]
    securePayToken: NotRequired[Optional[str]]
    cardBank: NotRequired[Optional[str]]
    cardCountry: NotRequired[Optional[str]]
    installmentPeriod: int
    payLaterPeriod: NotRequired[Optional[int]]
    interestType: NotRequired[Optional[str]]
    securityCode: NotRequired[Optional[str]]
    qrType: NotRequired[Optional[str]]
    fxRateID: NotRequired[Optional[str]]
    billingAddress1: NotRequired[Optional[str]]
    billingAddress2: NotRequired[Optional[str]]
    billingAddress3: NotRequired[Optional[str]]
    billingCity: NotRequired[Optional[str]]
    billingState: NotRequired[Optional[str]]
    billingPostalCode: NotRequired[Optional[str]]
    billingCountryCode: NotRequired[Optional[str]]
    paymentExpiry: NotRequired[Optional[str]]
    cardNo: NotRequired[Optional[str]]
    expiryMonth: NotRequired[Optional[str]]
    expiryYear: NotRequired[Optional[str]]
    pin: NotRequired[Optional[str]]
    loyaltyPoints: NotRequired[Optional[List[LoyaltyDetails]]]
    customerNote: NotRequired[Optional[str]]
    userAgent: NotRequired[Optional[str]]


class PaymentOptionDetailsPaymentCode(TypedDict, total=False):
    channelCode: Optional[str]
    agentCode: Optional[str]
    agentChannelCode: Optional[str]


class PaymentParamsRequestV43(TypedDict):
    data: PaymentParamsDataRequestV43
    code: NotRequired[PaymentOptionDetailsPaymentCode]


class PaymentRequestV43(TypedDict):
    paymentToken: str
    payment: PaymentParamsRequestV43
    responseReturnUrl: NotRequired[Optional[str]]
    clientIP: NotRequired[Optional[str]]
    locale: NotRequired[Optional[str]]
    clientID: str
    browserDetails: NotRequired[BrowserDetails]


class PaymentNotificationRequest(TypedDict):
    paymentToken: str
    plateform: NotRequired[Optional[str]]
    recipientID: NotRequired[Optional[str]]
    recipientName: NotRequired[Optional[str]]
    locale: NotRequired[Optional[str]]
    clientID: str
    browserDetails: NotRequired[BrowserDetails]


class PaymentOptionDetailsRequest(TypedDict):
    categoryCode: str
    groupCode: str
    paymentToken: str
    locale: NotRequired[Optional[str]]
    clientID: str
    browserDetails: NotRequired[BrowserDetails]


class TransactionStatusRequest(TypedDict):
    paymentToken: str
    additionalInfo: bool
    locale: NotRequired[Optional[str]]
    clientID: str
    browserDetails: NotRequired[BrowserDetails]
