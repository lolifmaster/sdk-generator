from typing import TypedDict, Union, List, Literal, Optional

CurrencyTag = Literal["crypto", "erc20", "ethereum", "fiat"]
CurrencyCode = str
ClientValue = int
InputAmount = str


class PlaceOrderRequestInputCommon(TypedDict, total=False):
    amount: InputAmount
    currency: CurrencyCode


CountryCode = str


class Owner(TypedDict, total=False):
    address: str
    address_complement: str
    city: str
    country: CountryCode
    name: str
    state: str
    zip: str


class PlaceOrderRequestInputBankAccount(TypedDict, total=False):
    iban: str
    owner: Owner
    type: Literal["bank_account"]


class PlaceOrderRequestInputBityAccount(TypedDict, total=False):
    type: Literal["bity_account"]


class PlaceOrderRequestInputCryptoAddress(TypedDict, total=False):
    crypto_address: str
    type: Literal["crypto_address"]


class PlaceOrderRequestInputOnlineInstantPayment(TypedDict, total=False):
    type: Literal["online_instant_payment"]


PlaceOrderRequestInput = Union[
    PlaceOrderRequestInputBankAccount,
    PlaceOrderRequestInputBityAccount,
    PlaceOrderRequestInputCryptoAddress,
    PlaceOrderRequestInputOnlineInstantPayment,
]

OutputAmount = str


class PlaceOrderRequestOutputCommon(TypedDict, total=False):
    amount: OutputAmount
    currency: CurrencyCode


class PostalAddressLegacy(TypedDict, total=False):
    address: str
    address_complement: str
    city: str
    country: CountryCode
    state: str
    zip: str


class PostalAddressStructured(TypedDict, total=False):
    building_name: str
    building_number: str
    country: CountryCode
    country_subdivision: str
    department: str
    district_name: str
    floor: str
    post_box: str
    post_code: str
    room: str
    street_name: str
    subdepartment: str
    town_location_name: str
    town_name: str


PostalAddress = Union[PostalAddressLegacy, PostalAddressStructured]

QrReference = str
StructuredCreditorReference = str


class PlaceOrderRequestOutputBankAccount(TypedDict, total=False):
    bic_swift: str
    iban: str
    owner: PostalAddress
    qr_reference: QrReference
    reference: str
    structured_creditor_reference: StructuredCreditorReference
    type: Literal["bank_account"]
    ultimate_debtor: PostalAddress


class PlaceOrderRequestOutputBityAccount(TypedDict, total=False):
    type: Literal["bity_account"]


class PlaceOrderRequestOutputCryptoAddress(TypedDict, total=False):
    crypto_address: str
    type: Literal["crypto_address"]


PlaceOrderRequestOutput = Union[
    PlaceOrderRequestOutputBankAccount,
    PlaceOrderRequestOutputBityAccount,
    PlaceOrderRequestOutputCryptoAddress,
]


class PartnerFee(TypedDict, total=False):
    factor: Union[float, str]


class PlaceOrderRequest(TypedDict, total=False):
    client_value: ClientValue
    contact_person: dict
    input: PlaceOrderRequestInput
    output: PlaceOrderRequestOutput
    partner_fee: PartnerFee


class AmountEstimateRequestCommon(TypedDict, total=False):
    fix_invalid_amount: bool
    partner_fee: PartnerFee


OrderInputType = Literal[
    "bank_account", "bity_account", "crypto_address", "online_instant_payment"
]


class AmountEstimateRequestInputCommon(TypedDict, total=False):
    currency: CurrencyCode
    type: OrderInputType


OrderOutputType = Literal["bank_account", "bity_account", "crypto_address"]


class AmountEstimateRequestOutputCommon(TypedDict, total=False):
    currency: CurrencyCode
    type: OrderOutputType


class InputAmountEstimateRequestOutput(TypedDict, total=False):
    amount: OutputAmount


class InputAmountEstimateRequest(TypedDict, total=False):
    input: AmountEstimateRequestInputCommon
    output: InputAmountEstimateRequestOutput


class OutputAmountEstimateRequestInput(TypedDict, total=False):
    amount: InputAmount


class OutputAmountEstimateRequest(TypedDict, total=False):
    input: OutputAmountEstimateRequestInput
    output: AmountEstimateRequestOutputCommon


AmountEstimateRequest = Union[InputAmountEstimateRequest, OutputAmountEstimateRequest]


class OrdersPerformMultipleEstimationsRequest(TypedDict, total=False):
    items: List[AmountEstimateRequest]
