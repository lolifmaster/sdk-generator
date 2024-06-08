from typing import List, Union, TypedDict, Any, Dict
from typing_extensions import Literal


class Interval(TypedDict):
    start: str
    end: str


class Preset(TypedDict):
    value: str


PeriodFilter = Union[Interval, Preset]


class Filter(TypedDict, total=False):
    attribute: str
    values: List[str]


class GetMetricDataInput(TypedDict, total=False):
    id: str
    periodFilter: PeriodFilter
    filters: List[Filter]
    aggregations: List[str]
    timezone: str


class GetMetricRecordsDataInput(TypedDict, total=False):
    id: str
    periodFilter: PeriodFilter
    filters: List[Filter]
    timezone: str


class BulkUpdateAgentInput(TypedDict, total=False):
    id: str
    displayName: str
    phoneNumber: str
    additionalEmails: List[str]
    additionalPhoneNumbers: List[str]
    firstName: str
    lastName: str
    middleNames: List[str]
    avatarUrl: str


AgentsUpdateBulkRequest = List[BulkUpdateAgentInput]


class CreateAgentInput(TypedDict, total=False):
    displayName: str
    email: str
    phoneNumber: str
    additionalEmails: List[str]
    additionalPhoneNumbers: List[str]
    firstName: str
    lastName: str
    middleNames: List[str]
    avatarUrl: str


class BulkPatchAgentInput(TypedDict, total=False):
    id: str
    displayName: str
    phoneNumber: str
    additionalEmails: List[str]
    additionalPhoneNumbers: List[str]
    firstName: str
    lastName: str
    middleNames: List[str]
    avatarUrl: str


AgentsBulkPatchRequest = List[BulkPatchAgentInput]


class CreateAgentsInput(TypedDict):
    data: List[CreateAgentInput]


class UpdateAgentInput(TypedDict, total=False):
    displayName: str
    phoneNumber: str
    additionalEmails: List[str]
    additionalPhoneNumbers: List[str]
    firstName: str
    lastName: str
    middleNames: List[str]
    avatarUrl: str


class PatchAgentInput(TypedDict, total=False):
    displayName: str
    phoneNumber: str
    additionalEmails: List[str]
    additionalPhoneNumbers: List[str]
    firstName: str
    lastName: str
    middleNames: List[str]
    avatarUrl: str


class BulkUpdateEndUserInput(TypedDict, total=False):
    id: str
    displayName: str
    email: str
    phoneNumber: str
    additionalEmails: List[str]
    additionalPhoneNumbers: List[str]
    firstName: str
    lastName: str
    middleNames: List[str]
    avatarUrl: str
    externalId: str


BulkUpdateEndUsersInput = List[BulkUpdateEndUserInput]


class CreateEndUserInput(TypedDict, total=False):
    displayName: str
    email: str
    phoneNumber: str
    additionalEmails: List[str]
    additionalPhoneNumbers: List[str]
    firstName: str
    lastName: str
    middleNames: List[str]
    avatarUrl: str
    externalId: str


class BulkPatchEndUserInput(TypedDict, total=False):
    id: str
    displayName: str
    email: str
    phoneNumber: str
    additionalEmails: List[str]
    additionalPhoneNumbers: List[str]
    firstName: str
    lastName: str
    middleNames: List[str]
    avatarUrl: str
    externalId: str


BulkPatchEndUsersInput = List[BulkPatchEndUserInput]


class CreateEndUsersInput(TypedDict):
    data: List[CreateEndUserInput]


class UpdateEndUserInput(TypedDict, total=False):
    displayName: str
    email: str
    phoneNumber: str
    additionalEmails: List[str]
    additionalPhoneNumbers: List[str]
    firstName: str
    lastName: str
    middleNames: List[str]
    avatarUrl: str
    externalId: str


class PatchEndUserInput(TypedDict, total=False):
    displayName: str
    email: str
    phoneNumber: str
    additionalEmails: List[str]
    additionalPhoneNumbers: List[str]
    firstName: str
    lastName: str
    middleNames: List[str]
    avatarUrl: str
    externalId: str


Map_UUID_Option_AttributeValue = Dict[str, Union[List[str], str]]


class CreateTeamInput(TypedDict):
    name: str


class DeleteAgentsFromTeamInput(TypedDict, total=False):
    agentIds: List[str]


class AgentsToTeamInput(TypedDict, total=False):
    agentIds: List[str]


class CloseConversationInput(TypedDict, total=False):
    userId: str


class ReopenConversationInput(TypedDict, total=False):
    userId: str


class TransferConversationInput(TypedDict, total=False):
    queueId: str
    userId: str


class CreateInternalNoteInput(TypedDict, total=False):
    message: str
    agentId: str
    createdAt: str


BulkCreateInternalNoteInput = List[CreateInternalNoteInput]


class Html(TypedDict):
    value: str


class Text(TypedDict):
    value: str


Content = Union[Html, Text]


class File(TypedDict):
    url: str
    prettyName: str


class Inbound(TypedDict, total=False):
    content: Content
    attachments: List[File]
    integrationEmail: str
    externalId: str


class Outbound(TypedDict, total=False):
    content: Content
    agentId: str
    attachments: List[File]
    integrationEmail: str
    externalId: str
    cc: List[str]
    bcc: List[str]


CreateMessageInput = Union[Inbound, Outbound]


class Callback(TypedDict):
    requesterId: str
    direction: str
    contactEndpointId: str
    queueId: str


class BrowserInfo(TypedDict, total=False):
    version: str
    name: str
    ipAddress: str
    originatingUrl: str


class Chat(TypedDict):
    requesterId: str
    widgetId: str
    message: CreateMessageInput
    browserInfo: BrowserInfo
    language: str


class ContactForm(TypedDict):
    requesterId: str
    emailIntegrationId: str
    subject: str
    message: CreateMessageInput
    language: str


class Email(TypedDict):
    requesterId: str
    emailIntegrationId: str
    subject: str
    message: CreateMessageInput
    language: str


class Sms(TypedDict):
    requesterId: str
    contactEndpointId: str
    message: CreateMessageInput


CreateConversationInput = Union[Callback, Chat, ContactForm, Email, Sms]


class ClaimConversationInput(TypedDict, total=False):
    agentId: str
    force: bool


Map_QueueThreshold_Int = Dict[str, int]

Map_ConversationChannel_Int = Dict[str, int]


class CreateOrUpdateQueueRequest(TypedDict, total=False):
    name: str
    callFunctionality: bool
    isDefault: bool
    queueThresholds: Map_QueueThreshold_Int
    offerTimeout: int
    offerAlgorithm: str
    wrapupTimeout: int
    priority: int
    offerAbandonedConversations: bool
    doNotOfferTimeouts: Map_ConversationChannel_Int
    isDoNotOfferEnabled: bool
    preferredAgentTimeouts: Map_ConversationChannel_Int
    isPreferredAgentEnabled: bool
    preferredAgentOfflineTimeout: int
    personalAgentOfflineTimeout: int


class CreateQueueInput(TypedDict):
    request: CreateOrUpdateQueueRequest


class BulkQueueEndpointInput(TypedDict, total=False):
    agentIds: List[str]


class CreateTagInput(TypedDict, total=False):
    name: str
    color: str


class BasicAuth(TypedDict):
    username: str
    password: str


class NoAuth(TypedDict):
    pass


class TokenAuth(TypedDict):
    value: str


WebhookAuthorization = Union[BasicAuth, NoAuth, TokenAuth]


class PatchWebhookSubscriptionInput(TypedDict, total=False):
    name: str
    events: List[str]
    url: str
    authorization: WebhookAuthorization
    enabled: bool


class CreateWebhookSubscriptionInput(TypedDict, total=False):
    name: str
    events: List[str]
    url: str
    authorization: WebhookAuthorization
    enabled: bool
