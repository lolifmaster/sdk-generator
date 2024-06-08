from typing import TypedDict, List, Union, Optional, Literal
from datetime import datetime


class Vault(TypedDict):
    id: str


class Url(TypedDict, total=False):
    label: str
    primary: bool
    href: str


class Item(TypedDict, total=False):
    version: int
    id: str
    vault: Vault
    category: Literal[
        "LOGIN",
        "PASSWORD",
        "API_CREDENTIAL",
        "SERVER",
        "DATABASE",
        "CREDIT_CARD",
        "MEMBERSHIP",
        "PASSPORT",
        "SOFTWARE_LICENSE",
        "OUTDOOR_LICENSE",
        "SECURE_NOTE",
        "WIRELESS_ROUTER",
        "BANK_ACCOUNT",
        "DRIVER_LICENSE",
        "IDENTITY",
        "REWARD_PROGRAM",
        "DOCUMENT",
        "EMAIL_ACCOUNT",
        "SOCIAL_SECURITY_NUMBER",
        "MEDICAL_RECORD",
        "SSH_KEY",
        "CUSTOM",
    ]
    urls: List[Url]
    favorite: bool
    state: Literal["ARCHIVED", "DELETED"]
    createdAt: datetime
    updatedAt: datetime
    lastEditedBy: str


class GeneratorRecipe(TypedDict, total=False):
    length: int
    characterSets: List[Literal["LETTERS", "DIGITS", "SYMBOLS"]]
    excludeCharacters: str


class Section(TypedDict, total=False):
    id: str


class Field(TypedDict, total=False):
    id: str
    section: Section
    type: Literal[
        "STRING", "EMAIL", "CONCEALED", "URL", "TOTP", "DATE", "MONTH_YEAR", "MENU"
    ]
    purpose: Literal["", "USERNAME", "PASSWORD", "NOTES"]
    label: str
    value: str
    generate: bool
    recipe: GeneratorRecipe
    entropy: float


class File(TypedDict, total=False):
    id: str
    name: str
    size: int
    content_path: str
    section: Section
    content: str


class FullItemSection(TypedDict):
    id: str
    label: str


class FullItem(Item, total=False):
    sections: List[FullItemSection]
    fields: List[Field]
    files: List[File]


class PatchOperation(TypedDict):
    op: Literal["add", "remove", "replace"]
    path: str
    value: object


Patch = List[PatchOperation]
