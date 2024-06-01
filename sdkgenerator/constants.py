from sdkgenerator.types import Step
import pathlib
from typing import TypedDict


class Agent(TypedDict):
    model: str
    custom: bool


MODEL = "gpt-4"

API_CALLS_DIR = pathlib.Path(__file__).parent.parent.absolute() / "api_calls"

GENERATED_SDK_DIR = pathlib.Path(__file__).parent.parent.absolute() / "generated_sdk"

EDEN_AI_API = "https://api.edenai.run/v2/text/chat"

TEMPERATURE: dict[Step, float] = {
    "types": 0.1,
    "initial_code": 0.2,
    "feedback": 0.2,
    "final_code": 0.1,
}

AGENT: dict[Step, Agent] = {
    "types": {
        "model": "gpt-4",
        "custom": False,
    },
    "initial_code": {
        "model": "gpt-4",
        "custom": False,
    },
    "feedback": {
        "model": "gpt-4",
        "custom": False,
    },
    "final_code": {
        "model": "gpt-4",
        "custom": False,
    },
}

MAX_PROMPT_LENGTH: dict[Step, int] = {
    "types": 8192,
    "initial_code": 8192,
    "feedback": 8192,
    "final_code": 8192,
}

MAX_TOKENS: dict[Step, int] = {
    "types": 4096,
    "initial_code": 4096,
    "feedback": 4096,
    "final_code": 4096,
}
