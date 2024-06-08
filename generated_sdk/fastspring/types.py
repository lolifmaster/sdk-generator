from typing import TypedDict, List, Literal, Optional
from decimal import Decimal


class ContactRequest(TypedDict, total=False):
    company: str
    email: str
    first: str
    last: str
    phone: str


class CreateOneAccount(TypedDict):
    contact: ContactRequest


class AddcouponcodestoacouponRequest(TypedDict):
    codes: List[str]


class UpdateasingleeventRequest(TypedDict):
    processed: bool


class Display(TypedDict):
    en: str


class Instructions(TypedDict):
    en: str
    es: str


class Fulfillment(TypedDict):
    instructions: Instructions


class Attributes2(TypedDict):
    key1: str
    key2: str


class Price(TypedDict):
    USD: Decimal
    EUR: Decimal


class DiscountReason(TypedDict):
    en: str


class Pricing1(TypedDict):
    trial: int
    interval: str
    intervalLength: int
    quantityBehavior: str
    quantityDefault: int
    paymentCollected: bool
    paidTrial: bool
    trialPrice: Price
    price: Price
    quantityDiscounts: Dict[str, Decimal]
    discountReason: DiscountReason
    discountDuration: int


class Product(TypedDict, total=False):
    product: str
    display: Display
    fulfillment: Fulfillment
    image: str
    format: str
    sku: str
    attributes: Attributes2
    pricing: Pricing1


class CreateoneormorenewproductsRequest(TypedDict):
    products: List[Product]


class Item2(TypedDict):
    product: str
    quantity: int


class CreateasessionwithoutoverridinganydefaultvaluesRequest(TypedDict):
    account: str
    items: List[Item2]


class Subscription(TypedDict):
    subscription: str
    product: str
    quantity: int
    taxExemptId: Optional[str]


class ChangetheproductforanactivesubscriptionRequest(TypedDict):
    subscriptions: List[Subscription]


class SubscriptionAddon(TypedDict):
    product: str
    quantity: int
    pricing: Price


class EstimateSubscriptionRequest(TypedDict):
    subscription: str
    product: str
    quantity: int
    pricing: Price
    addons: List[SubscriptionAddon]


class Subscription6(TypedDict):
    subscription: str
    deactivation: str


class UncancelasubscriptionpriortodeactivationRequest(TypedDict):
    subscriptions: List[Subscription6]


class PauseSubscriptionRequest(TypedDict, total=False):
    pausePeriodCount: int


class TagRequest(TypedDict, total=False):
    key: str
    value: str


class ItemRequest(TypedDict, total=False):
    product: str
    unitListPrice: Decimal
    quantity: int


class AddressRequest(TypedDict, total=False):
    addressLine1: str
    addressLine2: str
    city: str
    country: str
    postalCode: str
    region: str


class UpdateQuoteRequest(TypedDict, total=False):
    tags: List[TagRequest]
    coupon: str
    currency: str
    expirationDateDays: int
    fulfillmentTerm: str
    items: List[ItemRequest]
    name: str
    notes: str
    netTermsDays: int
    recipientAddress: AddressRequest
    recipient: ContactRequest
    status: Literal["OPEN", "CANCELED", "AWAITING_PAYMENT", "COMPLETED", "EXPIRED"]
    taxId: str
    source: str
    sourceIP: str
    invoiceId: str


class QuotesUpdateQuoteByIdRequest(TypedDict):
    updateQuoteRequest: UpdateQuoteRequest


class CreateQuoteRequest(TypedDict, total=False):
    tags: List[TagRequest]
    coupon: str
    currency: str
    expirationDateDays: int
    fulfillmentTerm: str
    items: List[ItemRequest]
    name: str
    notes: str
    netTermsDays: int
    recipientAddress: AddressRequest
    recipient: ContactRequest
    taxId: str
    source: str
    sourceIP: str


class WebhooksUpdateWebhookKeySecretRequest(TypedDict):
    url: str
    hmacSecret: str


class FilterSubscriptionReportRequest(TypedDict, total=False):
    startDate: str
    endDate: str
    countryISO: List[str]
    productNames: List[str]
    productPaths: List[str]
    syncDate: str


class GenerateSubscriptionReportRequest(TypedDict, total=False):
    filter: FilterSubscriptionReportRequest
    reportColumns: List[str]
    groupBy: List[str]
    pageCount: int
    pageNumber: int
    async: bool
    notificationEmails: List[str]


class FilterRevenueReportRequest(TypedDict, total=False):
    startDate: str
    endDate: str
    countryISO: List[str]
    productNames: List[str]
    productPaths: List[str]
    syncDate: str


class GenerateRevenueReportRequest(TypedDict, total=False):
    filter: FilterRevenueReportRequest
    reportColumns: List[str]
    groupBy: List[str]
    pageCount: int
    pageNumber: int
    async: bool
    notificationEmails: List[str]
