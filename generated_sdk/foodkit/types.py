from typing import TypedDict, Literal, List


class CustomersRegisterCustomerRequest(TypedDict, total=False):
    title: str
    email: str
    phone_number: str
    name: str
    first_name: str
    last_name: str
    password: str
    date_of_birth: str
    gender: Literal["male", "female"]
    accepts_terms_and_conditions: bool
    accepts_marketing_notifications: bool


class CustomersUpdateDetailsRequest(TypedDict, total=False):
    name: str
    email: str
    password: str


class CustomersStoreTaxIdRequest(TypedDict, total=False):
    customer_id: int
    tax_id: str
    company_name: str
    company_address: str
    company_district: str
    company_area: str
    company_province: str
    company_postcode: str
    company_phone: str
    is_headoffice: bool
    branch_no: str


class BranchesSubmitContactFormRequest(TypedDict, total=False):
    message: str


class Product(TypedDict, total=False):
    id: int


class MarketingCreateUpsellRecommendationsRequest(TypedDict, total=False):
    products: List[Product]


class ExtraItem(TypedDict, total=False):
    id: int
    quantity: int


class ComboItem(TypedDict, total=False):
    product_id: int
    combo_group_id: int
    extra_items: List[ExtraItem]


class ProductOrder(TypedDict, total=False):
    id: int
    quantity: int
    extra_items: List[ExtraItem]
    combo_items: List[ComboItem]
    comments: str


class Card(TypedDict, total=False):
    id: int
    card_token: str


class Address(TypedDict, total=False):
    id: int
    address1: str
    address_label: str
    building_name: str
    address2: str
    room_number: str
    floor_number: str
    directions: str
    latitude: str
    longitude: float


class OrdersCreateOrderRequest(TypedDict, total=False):
    branch_id: int
    order_type: Literal["delivery", "pickup", "room-service", "digital"]
    payment_type: Literal[
        "cod",
        "payment_link",
        "external_credit_card",
        "third_party",
        "credit_card",
        "card_on_file",
        "bank_transfer",
        "paypal_express",
        "other",
        "none",
    ]
    card: Card
    store_card_info: bool
    products: List[ProductOrder]
    latitude: str
    longitude: float
    address: Address
    is_realtime: bool
    scheduled_date: str
    scheduled_time: str
    comments: str
    customer_tax_id: int
    _3ds_callback_url: str
    exceeds_cart_limit: bool
    phone_number: str
    coupon_code: str


class OrdersGetQuotationRequest(TypedDict, total=False):
    branch_id: int
    order_type: Literal["delivery", "pickup", "room-service", "digital"]
    payment_type: Literal[
        "cod",
        "payment_link",
        "external_credit_card",
        "third_party",
        "credit_card",
        "card_on_file",
        "bank_transfer",
        "paypal_express",
        "other",
        "none",
    ]
    card: Card
    store_card_info: bool
    products: List[ProductOrder]
    latitude: str
    longitude: float
    address: Address
    is_realtime: bool
    scheduled_date: str
    scheduled_time: str
    comments: str
    customer_tax_id: int
    _3ds_callback_url: str
    exceeds_cart_limit: bool
    phone_number: str
    coupon_code: str


class CustomersOptInServiceAreaEmailRequest(TypedDict, total=False):
    email: str
    latitude: float
    longitude: float
    address1: str


class CustomersStoreGdprPreferencesRequest(TypedDict, total=False):
    device_uuid: str
    accept_all: bool
    accept_performance: bool
    accept_marketing: bool


class CustomersGenerateIntercomHmacRequest(TypedDict, total=False):
    channel: Literal["android", "ios", "web"]
