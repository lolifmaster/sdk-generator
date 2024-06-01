import pathlib


API_CALLS_DIR = pathlib.Path(__file__).parent.parent.absolute() / "api_calls"

GENERATED_SDK_DIR = pathlib.Path(__file__).parent.parent.absolute() / "generated_sdk"

EDEN_AI_API = "https://api.edenai.run/v2/text/chat"
OPENAI_API = "https://api.openai.com/v1/chat/completions"
