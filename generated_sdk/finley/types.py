from typing import TypedDict, Optional


class SettleRequestBody(TypedDict):
    amount: float
    settlementDate: str


class CollectionsPaydown(TypedDict):
    amount: float
    targetFundingDate: str


class CollectionsRecycle(TypedDict):
    amount: float
    targetFundingDate: str


class CurePaydown(TypedDict):
    amount: float
    targetFundingDate: str


class DrawRequest(TypedDict):
    amount: float
    targetFundingDate: str


class FundingRequestSubmissionRequestBody(TypedDict):
    collectionsPaydown: Optional[CollectionsPaydown]
    collectionsRecycle: Optional[CollectionsRecycle]
    curePaydown: Optional[CurePaydown]
    drawRequest: Optional[DrawRequest]
