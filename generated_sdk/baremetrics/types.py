from typing import TypedDict, List, Optional
from datetime import datetime


class SourceCreatePlanRequest(TypedDict):
    oid: str
    name: str
    currency: str
    amount: int
    interval: str
    interval_count: int
    trial_duration: Optional[int]
    trial_duration_unit: Optional[str]


class SourceUpdatePlanRequest(TypedDict):
    name: str


class SourceCreateCustomerRecordRequest(TypedDict):
    oid: str
    name: Optional[str]
    notes: Optional[str]
    email: Optional[str]
    created: Optional[datetime]


class SourceUpdateCustomerInformationRequest(TypedDict):
    name: Optional[str]
    notes: Optional[str]
    created: Optional[datetime]
    email: Optional[str]


class Addon(TypedDict):
    oid: str
    amount: int
    quantity: int


class SourceCreateSubscriptionRequest(TypedDict):
    oid: str
    started_at: datetime
    canceled_at: Optional[datetime]
    plan_oid: str
    customer_oid: str
    addons: Optional[List[Addon]]
    quantity: Optional[int]
    discount: Optional[int]


class SourceUpdateSubscriptionRequest(TypedDict):
    plan_oid: str
    occurred_at: Optional[datetime]
    addons: Optional[List[Addon]]
    quantity: Optional[int]
    discount: Optional[int]


class SourceCancelSubscriptionRequest(TypedDict):
    canceled_at: datetime


class AnnotationCreateNewRequest(TypedDict):
    metric: str
    annotation: str
    date: datetime
    global_: bool
    user_id: str


class GoalCreateNewGoalRequest(TypedDict):
    metric: str
    start_amount: int
    end_amount: int
    start_date: datetime
    end_date: datetime
    name: str


class SourceCreateChargeOneOffRequest(TypedDict):
    oid: str
    amount: int
    currency: str
    customer_oid: str
    created: Optional[datetime]
    status: Optional[str]
    fee: Optional[int]
    subscription_oid: Optional[str]


class SourceCreateOneOffRefundRequest(TypedDict):
    oid: str
    amount: int
    currency: str
    customer_oid: str
    charge_oid: str
    created: Optional[datetime]


class QueryItem(TypedDict):
    category: str
    field: str
    value: str
    method: str


class SegmentCreateRequestRequest(TypedDict):
    query: List[QueryItem]
    name: Optional[str]


class SegmentUpdateByIdRequest(TypedDict):
    name: Optional[str]
    query: Optional[List[QueryItem]]


class SegmentFindWithoutSaveRequest(TypedDict):
    query: List[QueryItem]


class AttributeSetPropertiesRequest(TypedDict):
    attributes: List[QueryItem]


class AttributeCreateFieldRequest(TypedDict):
    title: str
    field_type: str


class AttributeUpdateFieldRequest(TypedDict):
    title: str


class EventCreateInsightEventRequest(TypedDict):
    reason_id: str
    comment: Optional[str]
    customer_oid: Optional[str]
    subscription_oids: Optional[List[str]]


class EventUpdateEventByIdRequest(TypedDict):
    reason_id: Optional[str]
    comment: Optional[str]


class ReasonUpdateReasonByIdRequest(TypedDict):
    text: str
    sort_key: Optional[int]


class CancellationInsightCreateNewReasonRequest(TypedDict):
    text: str
    sort_key: int
