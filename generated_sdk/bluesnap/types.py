from typing import TypedDict, List, Literal, Union
from typing_extensions import Annotated


class CardHolderInfo(TypedDict):
    firstName: str
    lastName: str
    zip: str


class CreditCard(TypedDict):
    expirationYear: int
    securityCode: int
    expirationMonth: str
    cardNumber: str


class AuthorizationCreateTransactionRequest(TypedDict):
    amount: float
    softDescriptor: str
    cardHolderInfo: CardHolderInfo
    currency: str
    creditCard: CreditCard
    cardTransactionType: Literal["AUTH_ONLY"]


class ReversalAuthTransactionRequest(TypedDict):
    cardTransactionType: Literal["AUTH_REVERSAL"]
    transactionId: int


class EcpTransaction(TypedDict):
    routingNumber: str
    accountType: str
    accountNumber: int


class PayerInfo(TypedDict):
    zip: str
    firstName: str
    lastName: str
    phone: str
    country: str


class BecsDirectDebitTransaction(TypedDict):
    bsbNumber: str
    accountNumber: str
    accountName: str
    financialInstitution: str
    branchName: str
    agreementId: int


class IdealTransaction(TypedDict):
    returnUrl: str


class LocalBankTransferTransaction(TypedDict):
    pass


class PaypalTransaction(TypedDict):
    cancelUrl: str
    returnUrl: str
    transactionType: str


class AcssDirectDebitTransaction(TypedDict):
    routingNumber: str
    accountNumber: str
    accountType: str
    agreementId: int


class SepaDirectDebitTransaction(TypedDict):
    iban: str


class TransactionCreateSofortTransactionRequest(TypedDict):
    ecpTransaction: EcpTransaction
    amount: float
    payerInfo: PayerInfo
    softDescriptor: str
    currency: str
    authorizedByShopper: bool
    becsDirectDebitTransaction: BecsDirectDebitTransaction
    idealTransaction: IdealTransaction
    localBankTransferTransaction: LocalBankTransferTransaction
    paypalTransaction: PaypalTransaction
    acssDirectDebitTransaction: AcssDirectDebitTransaction
    sepaDirectDebitTransaction: SepaDirectDebitTransaction


class TransactionUpdatePaypalTransactionRequest(TypedDict):
    amount: float
    currency: str
    paypalTransaction: PaypalTransaction


class CardTransaction(TypedDict):
    cardTransactionType: str
    merchantTransactionId: str
    amount: str
    currency: str
    cardHolderInfo: CardHolderInfo
    creditCard: CreditCard


class BatchTransaction(TypedDict):
    batchId: str
    callbackUrl: str
    cardTransaction: List[CardTransaction]


class TransactionCreateBatchTransactionRequest(TypedDict):
    batchTransaction: BatchTransaction


class TransactionInitiateRefundRequest(TypedDict):
    reason: str
    cancelSubscriptions: bool
    transactionMetaData: Annotated[dict, NotRequired]


class CreditCardInfo(TypedDict):
    creditCard: CreditCard


class PaymentSources(TypedDict):
    creditCardInfo: List[CreditCardInfo]


class ShopperCreateVaultedShopperRequest(TypedDict):
    paymentSources: PaymentSources
    firstName: str
    lastName: str


class ShopperUpdateVaultedShopperRequest(TypedDict):
    paymentSources: PaymentSources
    firstName: str
    lastName: str


class PlanCreateRecurringPlanRequest(TypedDict):
    chargeFrequency: str
    gracePeriodDays: int
    trialPeriodDays: int
    initialChargeAmount: int
    name: str
    currency: str
    maxNumberOfCharges: int
    recurringChargeAmount: float
    chargeOnPlanSwitch: bool


class PlanUpdateRecurringPlanRequest(TypedDict):
    chargeFrequency: str
    trialPeriodDays: str
    initialChargeAmount: str
    name: str
    currency: str
    recurringChargeAmount: str


class SubscriptionCreateNewRequest(TypedDict):
    payerInfo: PayerInfo
    paymentSource: PaymentSources
    planId: int


class SubscriptionUpdateSubscriptionRequest(TypedDict):
    planId: str


class SubscriptionCreateMerchantManagedSubscriptionRequest(TypedDict):
    amount: float
    currency: str
    payerInfo: PayerInfo
    paymentSource: PaymentSources


class SubscriptionCreateMerchantManagedChargeRequest(TypedDict):
    amount: float
    currency: str
    merchantTransactionId: str
    taxReference: str


class VendorCreateRequest(TypedDict):
    email: str
    firstName: str
    lastName: str
    phone: str
    address: str
    city: str
    country: str
    state: str
    zip: str
    defaultPayoutCurrency: str
    ipnUrl: str
    vendorPrincipal: PayerInfo
    vendorAgreement: Annotated[dict, NotRequired]
    payoutInfo: Annotated[dict, NotRequired]


class VendorUpdateVendorRequest(TypedDict):
    email: str
    name: str
    firstName: str
    lastName: str
    address: str
    city: str
    zip: str
    country: str
    phone: str
    state: str
    taxId: int
    vendorUrl: str
    ipnUrl: str
    defaultPayoutCurrency: str
    vendorPrincipal: PayerInfo
    payoutInfo: List[Annotated[dict, NotRequired]]
    vendorAgreement: Annotated[dict, NotRequired]
