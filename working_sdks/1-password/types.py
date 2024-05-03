
from typing import TypedDict, List, Literal, Union
from enum import Enum

class Category(Enum):
    LOGIN = 'LOGIN'
    PASSWORD = 'PASSWORD'
    API_CREDENTIAL = 'API_CREDENTIAL'
    SERVER = 'SERVER'
    DATABASE = 'DATABASE'
    CREDIT_CARD = 'CREDIT_CARD'
    MEMBERSHIP = 'MEMBERSHIP'
    PASSPORT = 'PASSPORT'
    SOFTWARE_LICENSE = 'SOFTWARE_LICENSE'
    OUTDOOR_LICENSE = 'OUTDOOR_LICENSE'
    SECURE_NOTE = 'SECURE_NOTE'
    WIRELESS_ROUTER = 'WIRELESS_ROUTER'
    BANK_ACCOUNT = 'BANK_ACCOUNT'
    DRIVER_LICENSE = 'DRIVER_LICENSE'
    IDENTITY = 'IDENTITY'
    REWARD_PROGRAM = 'REWARD_PROGRAM'
    DOCUMENT = 'DOCUMENT'
    EMAIL_ACCOUNT = 'EMAIL_ACCOUNT'
    SOCIAL_SECURITY_NUMBER = 'SOCIAL_SECURITY_NUMBER'
    MEDICAL_RECORD = 'MEDICAL_RECORD'
    SSH_KEY = 'SSH_KEY'
    CUSTOM = 'CUSTOM'

class State(Enum):
    ARCHIVED = 'ARCHIVED'
    DELETED = 'DELETED'

class CharacterSets(Enum):
    LETTERS = 'LETTERS'
    DIGITS = 'DIGITS'
    SYMBOLS = 'SYMBOLS'

class FieldPurpose(Enum):
    USERNAME = 'USERNAME'
    PASSWORD = 'PASSWORD'
    NOTES = 'NOTES'

class Field(Enum):
    STRING = 'STRING'
    EMAIL = 'EMAIL'
    CONCEALED = 'CONCEALED'
    URL = 'URL'
    TOTP = 'TOTP'
    DATE = 'DATE'
    MONTH_YEAR = 'MONTH_YEAR'
    MENU = 'MENU'

class PatchOp(Enum):
    ADD = 'add'
    REMOVE = 'remove'
    REPLACE = 'replace'

class Vault(TypedDict):
    id: str

class Urls(TypedDict, total=False):
    label: str
    primary: bool
    href: str

class GeneratorRecipe(TypedDict, total=False):
    length: int
    characterSets: List[CharacterSets]
    excludeCharacters: str

class Field(TypedDict, total=False):
    id: str
    section: Vault
    type: Field
    purpose: FieldPurpose
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
    section: Vault
    content: str

class FullItem(TypedDict):
    sections: List[Vault]
    fields: List[Field]
    files: List[File]

class Patch(TypedDict):
    op: PatchOp
    path: str
    value: dict

class Item(TypedDict, total=False):
    tags: List[str]
    title: str
    version: int
    id: str
    vault: Vault
    category: Category
    urls: List[Urls]
    favorite: bool
    state: State
    createdAt: str
    updatedAt: str
    lastEditedBy: str

class GeneratorRecipe(TypedDict, total=False):
    length: int
    characterSets: List[CharacterSets]
    excludeCharacters: str

class Field(TypedDict, total=False):
    id: str
    section: Vault
    type: Field
    purpose: FieldPurpose
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
    section: Vault
    content: str

class FullItem(TypedDict):
    sections: List[Vault]
    fields: List[Field]
    files: List[File]

class Patch(TypedDict):
    op: PatchOp
    path: str
    value: dict
