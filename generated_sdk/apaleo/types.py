from typing import TypedDict, List, Dict, Literal, Optional


class CreateAddressModel(TypedDict, total=False):
    addressLine1: str
    addressLine2: Optional[str]
    postalCode: str
    city: str
    regionCode: str
    countryCode: str


class BankAccountModel(TypedDict, total=False):
    iban: Optional[str]
    bic: Optional[str]
    bank: Optional[str]


class CreatePropertyModel(TypedDict, total=False):
    code: str
    name: Dict[str, str]
    companyName: str
    managingDirectors: Optional[str]
    commercialRegisterEntry: str
    taxId: str
    location: CreateAddressModel
    bankAccount: BankAccountModel
    paymentTerms: Dict[str, str]
    timeZone: str
    defaultCheckInTime: str
    defaultCheckOutTime: str
    currencyCode: Optional[str]


class Operation(TypedDict, total=False):
    value: Dict
    path: str
    op: str
    from_: Optional[str]


class PropertyModifyDetailsRequest(List[Operation]):
    pass


class CreateUnitAttributeModel(TypedDict):
    id: str


class CreateConnectedUnitModel(TypedDict):
    unitId: str


class CreateUnitModel(TypedDict, total=False):
    propertyId: str
    name: str
    unitGroupId: Optional[str]
    maxPersons: int
    condition: Optional[Literal["Clean", "CleanToBeInspected", "Dirty"]]
    attributes: List[CreateUnitAttributeModel]
    connectedUnits: List[CreateConnectedUnitModel]


class BulkCreateUnitsModel(TypedDict):
    units: List[CreateUnitModel]


class CreateUnitAttributeDefinitionModel(TypedDict):
    name: str


class CreateConnectedUnitGroupModel(TypedDict):
    unitGroupId: str
    memberCount: int


class CreateUnitGroupModel(TypedDict, total=False):
    code: str
    propertyId: str
    name: Dict[str, str]
    maxPersons: int
    rank: Optional[int]
    type_: Optional[Literal["BedRoom", "MeetingRoom", "EventSpace", "ParkingLot"]]
    connectedUnitGroups: List[CreateConnectedUnitGroupModel]


class ReplaceConnectedUnitGroupModel(TypedDict):
    unitGroupId: str
    memberCount: int


class ReplaceUnitGroupModel(TypedDict, total=False):
    name: Dict[str, str]
    maxPersons: Optional[int]
    rank: Optional[int]
    connectedUnitGroups: List[ReplaceConnectedUnitGroupModel]
