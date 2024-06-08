from typing import Literal, TypedDict, Optional
from typing_extensions import NotRequired


class BookingStatusType(TypedDict):
    enum: Literal["ALL", "BOOKED", "PENDING"]
    type: Literal["str"]


class BankIdIdentifyDto(TypedDict):
    type: Literal["obj"]
    props: NotRequired[{"personalNumber": {"type": "str", "nullable": True}}]


class QrDataRequest(TypedDict):
    req: ["qrStartSecret", "qrStartToken", "qrTime"]
    type: Literal["obj"]
    props: {
        "qrStartSecret": {"minLen": 1, "type": "str"},
        "qrStartToken": {"minLen": 1, "type": "str"},
        "qrTime": {"type": "int", "format": "int32"},
    }


class UserDataDto(TypedDict):
    type: Literal["obj"]
    props: NotRequired[
        {
            "authorizationId": {"type": "str", "nullable": True},
            "personalId": {"type": "str", "nullable": True},
            "corporateId": {"type": "str", "nullable": True},
            "name": {"type": "str", "nullable": True},
            "givenName": {"type": "str", "nullable": True},
            "surname": {"type": "str", "nullable": True},
            "email": {"type": "str", "nullable": True},
            "phoneNumber": {"type": "str", "nullable": True},
        }
    ]


class Providers(TypedDict):
    enum: Literal[
        "fi-op",
        "fi-op-sand",
        "fi-spankki",
        "fi-spankki-sand",
        "fi-nordea",
        "fi-nordea-sand",
        "fi-danskebank",
        "fi-danskebank-sand",
        "fi-handelsbanken",
        "fi-handelsbanken-sand",
        "fi-norwegian",
        "fi-norwegian-sand",
        "fi-revolut",
        "fi-revolut-sand",
        "fi-alandsbanken",
        "fi-alandsbanken-sand",
        "fi-morrowbank",
        "fi-morrowbank-sand",
        "fi-poppankki",
        "fi-poppankki-sand",
        "fi-saastopankki",
        "fi-saastopankki-sand",
        "fi-omasaastopankki",
        "fi-omasaastopankki-sand",
        "dk-nordea",
        "dk-nordea-sand",
        "dk-sparekassendanmark-sand",
        "dk-sparekassendanmark",
        "dk-lansparbank-sand",
        "dk-lansparbank",
        "dk-sparekassenkronjylland-sand",
        "dk-sparekassenkronjylland",
        "dk-folkesparekassen-sand",
        "dk-folkesparekassen",
        "dk-ikanobank-sand",
        "dk-ikanobank",
        "dk-basisbank-sand",
        "dk-basisbank",
        "dk-norwegian",
        "dk-norwegian-sand",
        "dk-danskebank",
        "dk-danskebank-sand",
        "dk-swedbank-sand",
        "dk-swedbank",
        "dk-sparnordbank-sand",
        "dk-sparnordbank",
        "dk-arbejderneslandsbank-sand",
        "dk-arbejderneslandsbank",
        "dk-nykreditbank-sand",
        "dk-nykreditbank",
        "dk-vestjyskbank-sand",
        "dk-vestjyskbank",
        "dk-coopbank-sand",
        "dk-coopbank",
        "dk-monsbank-sand",
        "dk-monsbank",
        "dk-andelskassenfelleskassen-sand",
        "dk-andelskassenfelleskassen",
        "dk-jyskebank",
        "dk-jyskebank-sand",
        "dk-ringkjobinglandbobank",
        "dk-ringkjobinglandbobank-sand",
        "dk-kreditbanken",
        "dk-kreditbanken-sand",
        "dk-revolut",
        "dk-revolut-sand",
    ]
    type: Literal["str"]


# ... and so on for the rest of the types
