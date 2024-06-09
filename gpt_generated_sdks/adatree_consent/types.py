from typing import TypedDict, Literal, Union, NotRequired


class Grantee(TypedDict, total=False):
    name: str
    licenceNumber: str
    id: str


PostUsageAction = Literal["DELETION", "DE_IDENTIFICATION"]


class CreateConsent(TypedDict):
    sharingEndDate: str
    dataHolderBrandId: str
    useCaseId: str
    consumerEmail: NotRequired[str]
    postUsageAction: NotRequired[PostUsageAction]
    directMarketingAllowed: NotRequired[bool]
    externalId: NotRequired[str]
    consumerId: NotRequired[str]
    grantee: NotRequired[Grantee]
    customData: NotRequired[dict]


class UpdateConsentConsumer(TypedDict, total=False):
    postUsageAction: PostUsageAction
    directMarketingAllowed: bool
    sharingEndDate: str


class UpdateConsentMachine(TypedDict, total=False):
    externalId: str


ConsentUpdateViaDashboardRequest = Union[UpdateConsentConsumer, UpdateConsentMachine]


class Authorization(TypedDict, total=False):
    code: str
    state: str
    id_token: str
    response: str
