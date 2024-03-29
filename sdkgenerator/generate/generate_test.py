from dotenv import load_dotenv
from sdkgenerator.utils import (
    get_code_from_model_response,
    Language,
    API_CALLS_DIR,
    GENERATED_SDK_DIR,
    generate_llm_response,
    TEMPLATES,
    extension_to_language,
)
from pathlib import Path

load_dotenv()


def generate_test(sdk_file: Path) -> Path:
    """
    Generate test generated sdk and save it to the generated_sdk module.
    """
    sdk_name = sdk_file.stem
    sdk_code = sdk_file.read_text()
    language: Language = extension_to_language[sdk_file.suffix]

    payload = {
        "providers": "openai",
        "text": TEMPLATES[language]["test"].format(sdk=sdk_code, sdk_file_name=sdk_file.name),
        "chatbot_global_action": f"You are a {language} developer, and you are writing tests for an SDK.",
        "previous_history": [
            {
                "role": "user",
                "message": f"Write a test for the following {language} sdk:",
            },
            {
                "role": "assistant",
                "message": f'---{(API_CALLS_DIR / f"{sdk_name}.txt").read_text()}---',
            },
        ],
        "temperature": 0.0,
        "max_tokens": 4000,
        "settings": {"openai": "gpt-4"},
        "fallback_providers": "",
    }

    response = generate_llm_response(payload)

    if response is None:
        raise Exception("Failed to generate test.")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    response_output_file = API_CALLS_DIR / f"{sdk_name}_test.txt"
    response_output_file.write_text(response["openai"]["generated_text"])

    code, file_extension = get_code_from_model_response(
        response["openai"]["generated_text"]
    )

    if code is None or file_extension is None:
        raise Exception("Generated test code is empty.")

    # create the test file
    test_output_file = GENERATED_SDK_DIR / sdk_name / f"test_{sdk_name}{file_extension}"
    test_output_file.write_text(code)

    return test_output_file
