from typing import TypedDict, Optional, List, Union
from uuid import UUID


class BrowserDetails(TypedDict, total=False):
    version: Optional[str]
    deviceType: Optional[str]
    name: Optional[str]
    os: Optional[str]


class MerchantValidationApplePay(TypedDict):
    validationUrl: Optional[str]
    paymentToken: str
    locale: Optional[str]
    clientID: UUID
    browserDetails: BrowserDetails


class PaymentBaseRequest(TypedDict):
    paymentToken: str
    locale: Optional[str]
    clientID: UUID
    browserDetails: BrowserDetails


class CardInstallmentPlanInfoRequest(TypedDict):
    cardNo: Optional[str]
    bankCode: Optional[str]
    paymentToken: str
    locale: Optional[str]
    clientID: UUID
    browserDetails: BrowserDetails


class PaymentExchangeRateConverterRequest(TypedDict):
    bin: Optional[str]
    paymentToken: str
    locale: Optional[str]
    clientID: UUID
    browserDetails: BrowserDetails


class PayloadRequest(TypedDict, total=False):
    payload: Optional[str]


class PaymentLoyaltyPointInfoRequest(TypedDict):
    providerID: Optional[str]
    profileID: Optional[str]
    referenceID: Optional[str]
    cardNo: Optional[str]
    expiryMonth: Optional[str]
    expiryYear: Optional[str]
    paymentToken: str
    locale: Optional[str]
    clientID: UUID
    browserDetails: BrowserDetails


class LoyaltyRewards(TypedDict, total=False):
    id: Optional[str]
    Quantity: float


class LoyaltyDetails(TypedDict, total=False):
    providerID: Optional[str]
    accountNo: Optional[str]
    accountAuthData: Optional[str]
    queryReferenceSpecified: bool
    externalMerchantId: Optional[str]
    redeemAmount: float
    rewards: Optional[List[LoyaltyRewards]]


class PaymentParamsDataRequestV43(TypedDict, total=False):
    accountTokenization: bool
    customerToken: Optional[str]
    name: Optional[str]
    email: Optional[str]
    mobileNo: Optional[str]
    accountNo: Optional[str]
    securePayToken: Optional[str]
    cardBank: Optional[str]
    cardCountry: Optional[str]
    installmentPeriod: int
    payLaterPeriod: Optional[int]
    interestType: Optional[str]
    securityCode: Optional[str]
    qrType: Optional[str]
    fxRateID: Optional[str]
    billingAddress1: Optional[str]
    billingAddress2: Optional[str]
    billingAddress3: Optional[str]
    billingCity: Optional[str]
    billingState: Optional[str]
    billingPostalCode: Optional[str]
    billingCountryCode: Optional[str]
    paymentExpiry: Optional[str]
    cardNo: Optional[str]
    expiryMonth: Optional[str]
    expiryYear: Optional[str]
    pin: Optional[str]
    loyaltyPoints: Optional[List[LoyaltyDetails]]
    customerNote: Optional[str]
    userAgent: Optional[str]


class PaymentOptionDetailsPaymentCode(TypedDict, total=False):
    channelCode: Optional[str]
    agentCode: Optional[str]
    agentChannelCode: Optional[str]


class PaymentParamsRequestV43(TypedDict):
    data: PaymentParamsDataRequestV43
    code: PaymentOptionDetailsPaymentCode


class PaymentRequestV43(TypedDict):
    payment: PaymentParamsRequestV43
    responseReturnUrl: Optional[str]
    clientIP: Optional[str]
    paymentToken: str
    locale: Optional[str]
    clientID: UUID
    browserDetails: BrowserDetails


class PaymentNotificationRequest(TypedDict):
    plateform: Optional[str]
    recipientID: Optional[str]
    recipientName: Optional[str]
    paymentToken: str
    locale: Optional[str]
    clientID: UUID
    browserDetails: BrowserDetails


class PaymentOptionDetailsRequest(TypedDict):
    categoryCode: str
    groupCode: str
    paymentToken: str
    locale: Optional[str]
    clientID: UUID
    browserDetails: BrowserDetails


class TransactionStatusRequest(TypedDict):
    additionalInfo: bool
    paymentToken: str
    locale: Optional[str]
    clientID: UUID
    browserDetails: BrowserDetails
