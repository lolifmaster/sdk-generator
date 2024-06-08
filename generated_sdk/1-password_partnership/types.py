from typing import TypedDict, Optional
from datetime import datetime


class CreatePartnerAccountRequest(TypedDict):
    customer_account_uid: str
    account_type: str
    domain: str
    ends_at: Optional[datetime]


class UpdatePartnerAccountRequest(TypedDict):
    ends_at: datetime
