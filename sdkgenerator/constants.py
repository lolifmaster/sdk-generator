from sdkgenerator.types import Step
import pathlib

MAX_PROMPT_LENGTH = 8192
MODEL = "gpt-4"
MAX_TOKENS = 4096

API_CALLS_DIR = pathlib.Path(__file__).parent.parent.absolute() / "api_calls"

GENERATED_SDK_DIR = pathlib.Path(__file__).parent.parent.absolute() / "generated_sdk"

EDEN_AI_API = "https://api.edenai.run/v2/text/chat"

TEMPERATURE: dict[Step, float] = {
    "types": 0.1,
    "initial_code": 0.2,
    "feedback": 0.2,
    "final_code": 0.1,
}

AGENT: dict[Step, dict[str, str]] = {
    "types": {"openai": "gpt-4"},
    "initial_code": {"openai": "gpt-4"},
    "feedback": {"openai": "gpt-4"},
    "final_code": {"openai": "gpt-4"},
}
