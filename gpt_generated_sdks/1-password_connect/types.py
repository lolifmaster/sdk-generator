from typing import TypedDict, NotRequired, Literal, List


class Vault(TypedDict):
    id: str


class URLItem(TypedDict):
    href: str
    label: NotRequired[str]
    primary: NotRequired[bool]


class Item(TypedDict):
    version: NotRequired[int]
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
    urls: NotRequired[List[URLItem]]
    favorite: NotRequired[bool]
    state: NotRequired[Literal["ARCHIVED", "DELETED"]]
    createdAt: NotRequired[str]
    updatedAt: NotRequired[str]
    lastEditedBy: NotRequired[str]


class GeneratorRecipe(TypedDict):
    length: NotRequired[int]
    characterSets: NotRequired[List[Literal["LETTERS", "DIGITS", "SYMBOLS"]]]
    excludeCharacters: NotRequired[str]


class Section(TypedDict):
    id: NotRequired[str]


class Field(TypedDict):
    id: str
    type: Literal[
        "STRING", "EMAIL", "CONCEALED", "URL", "TOTP", "DATE", "MONTH_YEAR", "MENU"
    ]
    section: NotRequired[Section]
    purpose: NotRequired[Literal["", "USERNAME", "PASSWORD", "NOTES"]]
    label: NotRequired[str]
    value: NotRequired[str]
    generate: NotRequired[bool]
    recipe: NotRequired[GeneratorRecipe]
    entropy: NotRequired[float]


class File(TypedDict):
    id: str
    name: NotRequired[str]
    size: NotRequired[int]
    content_path: NotRequired[str]
    section: NotRequired[Section]
    content: NotRequired[str]


class FullItem(TypedDict):
    version: NotRequired[int]
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
    urls: NotRequired[List[URLItem]]
    favorite: NotRequired[bool]
    state: NotRequired[Literal["ARCHIVED", "DELETED"]]
    createdAt: NotRequired[str]
    updatedAt: NotRequired[str]
    lastEditedBy: NotRequired[str]
    sections: NotRequired[List[Section]]
    fields: NotRequired[List[Field]]
    files: NotRequired[List[File]]


class PatchItem(TypedDict):
    op: Literal["add", "remove", "replace"]
    path: str
    value: NotRequired[dict]


Patch = List[PatchItem]
