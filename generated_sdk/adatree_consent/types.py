from typing import TypedDict, Literal, Optional

PostUsageAction = Literal["DELETION", "DE_IDENTIFICATION"]


class Grantee(TypedDict):
    name: str
    licenceNumber: str
    id: str


class CreateConsent(TypedDict, total=False):
    consumerEmail: str
    sharingEndDate: str
    dataHolderBrandId: str
    useCaseId: str
    postUsageAction: PostUsageAction
    directMarketingAllowed: bool
    externalId: str
    consumerId: str
    grantee: Grantee
    customData: dict


class UpdateConsentConsumer(TypedDict, total=False):
    postUsageAction: PostUsageAction
    directMarketingAllowed: bool
    sharingEndDate: str


class UpdateConsentMachine(TypedDict, total=False):
    externalId: str


ConsentUpdateViaDashboardRequest = TypedDict(
    "ConsentUpdateViaDashboardRequest",
    {
        "UpdateConsentConsumer": UpdateConsentConsumer,
        "UpdateConsentMachine": UpdateConsentMachine,
    },
    total=False,
)


class Authorization(TypedDict):
    code: str
    state: str
    id_token: str
    response: str
