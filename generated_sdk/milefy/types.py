from typing import List, TypedDict, Literal
from datetime import date


class PriceBreakdown(TypedDict, total=False):
    currency: str
    baseFare: float
    total: float
    airlineSurcharges: float
    taxes: float


class FlightSegment(TypedDict):
    id: str
    marketingAirline: str
    operatingAirline: str
    departureAirport: str
    arrivalAirport: str
    departureDate: date
    cabin: Literal["Economy", "PremiumEconomy", "Business", "First"]
    bookingClass: str
    fareBasisCode: str
    fareFamilyName: str
    flightNumber: int
    distance: int


class FlightLeg(TypedDict):
    id: str
    segments: List[FlightSegment]


class Flight(TypedDict):
    id: str
    bookingChannel: Literal["airline", "ota"]
    price: PriceBreakdown
    legs: List[FlightLeg]


class FlightsCalculateAttributesBenefitsRequest(TypedDict):
    flights: List[Flight]


class FlightsCalculateFareAttributesRequest(TypedDict):
    legs: List[FlightLeg]


class TravelersCreateProfileRequest(TypedDict, total=False):
    country: str


class Miles(TypedDict):
    code: Literal[1, 2, 3, 4, 5]
    value: float


class MembershipsCreateFrequentFlyerProgramMembershipRequest(TypedDict):
    program: str
    memberNumber: str
    memberName: str
    mileageEarnings: List[Miles]
    statusTier: Literal[0, 1, 8, 16, 24, 32, 33, 34, 35, 36]
