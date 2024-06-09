from typing import TypedDict, Literal, List, Union


class CreateUnitAttributeModel(TypedDict):
    id: str


class CreateConnectedUnitModel(TypedDict):
    unitId: str


class CreateUnitModel(TypedDict):
    propertyId: str
    name: str
    unitGroupId: str
    maxPersons: int
    condition: Literal["Clean", "CleanToBeInspected", "Dirty"]
    attributes: List[CreateUnitAttributeModel]
    connectedUnits: List[CreateConnectedUnitModel]


class BulkCreateUnitsModel(TypedDict):
    units: List[CreateUnitModel]


class CreateUnitAttributeDefinitionModel(TypedDict):
    name: str


class CreateConnectedUnitGroupModel(TypedDict):
    unitGroupId: str
    memberCount: int


class CreateUnitGroupModel(TypedDict):
    code: str
    propertyId: str
    name: Union[str, dict[str, str]]
    maxPersons: int
    rank: int
    type: Literal["BedRoom", "MeetingRoom", "EventSpace", "ParkingLot"]
    connectedUnitGroups: List[CreateConnectedUnitGroupModel]


class ReplaceConnectedUnitGroupModel(TypedDict):
    unitGroupId: str
    memberCount: int


class ReplaceUnitGroupModel(TypedDict):
    name: Union[str, dict[str, str]]
    maxPersons: int
    rank: int
    connectedUnitGroups: List[ReplaceConnectedUnitGroupModel]
