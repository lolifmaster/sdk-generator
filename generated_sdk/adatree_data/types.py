from typing import TypedDict, List, Literal


class QueryUseCaseIds(TypedDict):
    useCaseIds: List[str]


class QueryCdrArrangementIds(TypedDict):
    cdrArrangementIds: List[str]


class QueryConsentIds(TypedDict):
    consentIds: List[str]


class QueryConsumerIds(TypedDict):
    consumerIds: List[str]


class QueryAccountIds(TypedDict, total=False):
    accountIds: List[str]


class QueryDataHolderBrandIds(TypedDict):
    dataHolderBrandIds: List[str]


class QueryAccountIsOwned(TypedDict):
    isOwned: bool


class QueryAccountOpenStatus(TypedDict, total=False):
    openStatus: Literal["OPEN", "CLOSED"]


class QueryProductCategory(TypedDict, total=False):
    productCategories: List[
        Literal[
            "BUSINESS_LOANS",
            "CRED_AND_CHRG_CARDS",
            "LEASES",
            "MARGIN_LOANS",
            "OVERDRAFTS",
            "PERS_LOANS",
            "REGULATED_TRUST_ACCOUNTS",
            "RESIDENTIAL_MORTGAGES",
            "TERM_DEPOSITS",
            "TRADE_FINANCE",
            "TRAVEL_CARDS",
            "TRANS_AND_SAVINGS_ACCOUNTS",
        ]
    ]


class QueryPage(TypedDict):
    page: int


class QueryPageSize(TypedDict):
    pageSize: int


class HeaderConsumerAuthDate(TypedDict):
    Adatree_Consumer_Auth_Date: str


class HeaderConsumerIpAddress(TypedDict):
    Adatree_Consumer_Ip_Address: str


class HeaderUserAgent(TypedDict):
    Adatree_Consumer_User_Agent: str


class QueryTransactionTypes(TypedDict):
    types: List[str]


class QueryTransactionStatuses(TypedDict):
    statuses: List[str]


class QueryTransactionMinimumAmount(TypedDict):
    minimumAmount: float


class QueryTransactionMaximumAmount(TypedDict):
    maximumAmount: float


class QueryTransactionOldestRetrievalTime(TypedDict):
    oldestRetrievalTime: str


class QueryTransactionNewestRetrievalTime(TypedDict):
    newestRetrievalTime: str


class QueryTransactionOldestTime(TypedDict):
    oldestTime: str


class QueryTransactionNewestTime(TypedDict):
    newestTime: str


class QueryPayeeTypes(TypedDict):
    types: List[str]


class QueryPayeeIds(TypedDict, total=False):
    payeeIds: List[str]


class QueryProductIds(TypedDict):
    productIds: List[str]


class QueryCustomerUTypes(TypedDict, total=False):
    customerUTypes: List[Literal["person", "organisation"]]


class QueryPlanIds(TypedDict):
    planIds: List[str]


class QueryPlanTypes(TypedDict):
    planTypes: List[Literal["STANDING", "MARKET", "REGULATED"]]


class QueryPlanFuelTypes(TypedDict):
    fuelTypes: List[Literal["ELECTRICITY", "GAS", "DUAL"]]


class QueryPlanEffective(TypedDict):
    effective: Literal["CURRENT", "FUTURE"]


class QueryPlanUpdatedSince(TypedDict):
    updatedSince: str


class QueryInvoiceIds(TypedDict):
    invoiceIds: List[str]


class QueryBillingIds(TypedDict):
    billingIds: List[str]


class QueryServicePointIds(TypedDict):
    servicePointIds: List[str]


class QueryOldestDate(TypedDict):
    oldestDate: str


class QueryNewestDate(TypedDict):
    newestDate: str
