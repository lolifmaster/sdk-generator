import json
import os
from pathlib import Path

from dotenv import load_dotenv

from sdkgenerator.manifier import process_file
from sdkgenerator.utils import (
    get_code_from_model_response,
    Language,
    GENERATED_SDK_DIR,
    generate_llm_response,
    TEMPLATES,
    is_all_steps_within_limit,
    validate_openapi_spec,
)

load_dotenv()


def generate_types(types_json: str, *, language: Language = "python") -> str:
    """
    Generate types for the API spec and return it as a string.

    Args:
    types_file_path: The types.
    language: The language of the generated code. Default is "python".

    Returns:
        str: The generated types for the API spec.
    """

    print("Generating types")
    response = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["types"].format(types=types_json),
            "chatbot_global_action": f"You are a {language} developer, and you are writing types for an API",
            "previous_history": [],
            "temperature": 0.0,
            "max_tokens": 5000,
            "settings": {"openai": "gpt-4"},
        },
        step="types",
        sdk_name="types",
    )

    if response is None:
        raise Exception("Failed to generate types")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    return response["openai"]["generated_text"]


def generate_initial_code(
    api_spec: str, types: str, sdk_name: str, language: Language = "python"
) -> tuple[str, list]:
    """
    Generate code for the API spec and return it as a string.

    Args:
    api_spec: The API spec.
    sdk_name: The name of the SDK.
    language: The language of the generated code. Default is "python".

    Returns:
        tuple[str, list]: The generated code for the API spec and the history of the conversation.
    """

    print("Generating initial code")
    response = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["initial_code"].format(api_spec=api_spec),
            "chatbot_global_action": f"You are a {language} developer, and you are writing a client sdk for an API",
            "previous_history": [
                {"role": "user", "message": "Generate types needed for the sdk"},
                {
                    "role": "assistant",
                    "message": f"Here are the types needed for the sdk stored in a file called types.py : '''{types}'''",
                },
            ],
            "temperature": 0.0,
            "max_tokens": 5000,
            "settings": {"openai": "gpt-4"},
        },
        step="initial_code",
        sdk_name=sdk_name,
    )

    if response is None:
        raise Exception("Failed to generate code")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    code, _ = get_code_from_model_response(response["openai"]["generated_text"])

    if not code:
        raise Exception("The generated code is empty.")

    return code, response["openai"]["message"]


def feedback_on_generated_code(
    generated_code: str,
    previous_history: list,
    *,
    sdk_name: str,
    language: Language = "python",
) -> str:
    """
    Generate Feedback on the generated code for the API spec and return it as a string.

    Args:
    generated_code: The generated code for the API spec.
    previous_history: The previous history of the conversation.
    language: The language of the generated code. Default is "python".
    sdk_name: The name of the SDK.

    Returns:
    str: The feedback on the generated code.
    """

    print("Generating feedback")
    response = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["feedback"].format(
                generated_code=generated_code
            ),
            "chatbot_global_action": f"You are a {language} developer reviewing code for an SDK",
            "previous_history": previous_history,
            "temperature": 0.2,
            "max_tokens": 2000,
            "settings": {"openai": "gpt-4"},
        },
        step="feedback",
        sdk_name=sdk_name,
    )

    if response is None:
        raise Exception("Failed to generate feedback")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    return response["openai"]["generated_text"]


def generate_final_code(
    feedback: str,
    previous_history: list,
    *,
    sdk_name: str,
    language: Language = "python",
) -> str:
    """
    Generate final code for the API spec and return it as a string.

    Args:
    initial_code: The initial code for the API spec.
    feedback: The feedback on the initial code.
    language: The language of the generated code. Default is "python".
    sdk_name: The name of the SDK.

    Returns:
    str: The final code for the API spec.
    """

    print("Generating final code")

    response = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["final_code"].format(feedback=feedback),
            "chatbot_global_action": f"You are a {language} developer, and you are refining a generated code",
            "previous_history": previous_history,
            "temperature": 0.2,
            "max_tokens": 5000,
            "settings": {"openai": "gpt-4"},
        },
        step="final_code",
        sdk_name=sdk_name,
    )

    if response is None:
        raise Exception("Failed to generate final code")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    return response["openai"]["generated_text"]


def load_openapi_spec(
    file_path: Path, *, language: Language = "python"
) -> tuple[str, dict]:
    """
    Load, validate and process the OpenAPI spec file.

    Args:
    file_path: The file path to the OpenAPI spec.

    Returns:
        tuple[str, str]: The OpenAPI spec as a string, and the types as a string.

    """
    # validate_openapi_spec(file_path)
    api_spec, types_json = process_file(file_path)

    if not is_all_steps_within_limit(
        api_spec, types_json, model="gpt-4", max_token=8_192, lang=language
    ):
        raise Exception("The token limit has been exceeded.")

    return api_spec, types_json


def generate_sdk(file_path: Path, *, language: Language = "python") -> Path:
    """
    Generate full SDK for the API spec and return the path to the generated SDK file.
    """
    api_spec, types_json = load_openapi_spec(file_path, language=language)

    api_spec_name = file_path.stem.split(".")[0]

    # save the api spec and types to a file
    if os.environ.get("ENV") == 'development':
        api_spec_file = GENERATED_SDK_DIR / api_spec_name
        api_spec_file.mkdir(exist_ok=True)
        api_spec_file = api_spec_file / "api_spec.txt"
        api_spec_file.write_text(api_spec)

        types_file = GENERATED_SDK_DIR / api_spec_name
        types_file = types_file / "types.json"
        types_file.write_text(
            json.dumps(types_json, indent=4)
        )

    types = generate_types(str(types_json), language=language)
    types_code, file_extension = get_code_from_model_response(types)

    # create a module for the generated sdk
    sdk_module = GENERATED_SDK_DIR / api_spec_name
    sdk_module.mkdir(exist_ok=True)

    # create the types file
    types_file = sdk_module / f"types{file_extension}"
    types_file.write_text(types_code)

    initial_code, history = generate_initial_code(
        api_spec, types=types, language=language, sdk_name=api_spec_name
    )

    # check if the generated code is empty (maybe will create a sup function later but for now it works)
    get_code_from_model_response(initial_code)
    history = history[:-1]

    feedback = feedback_on_generated_code(
        initial_code, history, language=language, sdk_name=api_spec_name
    )

    final_code_prev_history = [
        {"role": "user", "message": "Write me an sdk for my api"},
        {"role": "assistant", "message": f"Here is the generated code for the sdk: '''{initial_code}'''"},
    ]

    final_code = generate_final_code(
        feedback, final_code_prev_history, language=language, sdk_name=api_spec_name
    )

    code, file_extension = get_code_from_model_response(final_code)

    # create the sdk file
    sdk_output_file = sdk_module / f"{api_spec_name}{file_extension}"
    sdk_output_file.write_text(code)

    return sdk_output_file
