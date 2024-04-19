from dotenv import load_dotenv
from sdkgenerator.manifier import process_file
from sdkgenerator.utils import (
    get_code_from_model_response,
    Language,
    GENERATED_SDK_DIR,
    generate_llm_response,
    TEMPLATES,
)
from pathlib import Path

load_dotenv()


def generate_initial_code(
    api_spec: str, *, language: Language = "python"
) -> tuple[str, list]:
    """
    Generate code for the API spec and return it as a string.

    Args:
    file_path: The path to the API spec file.
    language: The language of the generated code. Default is "python".

    Returns:
    str: The generated code for the API spec.
    """

    response = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["initial_code"].format(api_spec=api_spec),
            "chatbot_global_action": f"You are a {language} developer, and you are writing a client sdk for an API",
            "previous_history": [],
            "temperature": 0.0,
            "max_tokens": 4000,
            "settings": {"openai": "gpt-4"},
        },
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
    generated_code: str, previous_history: list, *, language: Language = "python"
) -> str:
    """
    Generate Feedback on the generated code for the API spec and return it as a string.

    Args:
    generated_code: The generated code for the API spec.
    language: The language of the generated code. Default is "python".

    Returns:
    str: The feedback on the generated code.
    """
    response = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["feedback"].format(
                generated_code=generated_code
            ),
            "chatbot_global_action": f"You are a {language} developer reviewing code for an SDK",
            "previous_history": previous_history,
            "temperature": 0.3,
            "max_tokens": 2000,
            "settings": {"openai": "gpt-4"},
        },
    )

    if response is None:
        raise Exception("Failed to generate feedback")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    return response["openai"]["generated_text"]


def generate_final_code(
    feedback: str, previous_history: list, *, language: Language = "python"
) -> str:
    """
    Generate final code for the API spec and return it as a string.

    Args:
    initial_code: The initial code for the API spec.
    feedback: The feedback on the initial code.
    language: The language of the generated code. Default is "python".

    Returns:
    str: The final code for the API spec.
    """

    response = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["final_code"].format(feedback=feedback),
            "chatbot_global_action": f"You are a {language} developer, and you are refining a generated code",
            "previous_history": previous_history,
            "temperature": 0.2,
            "max_tokens": 4000,
            "settings": {"openai": "gpt-4"},
        },
    )

    if response is None:
        raise Exception("Failed to generate final code")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    return response["openai"]["generated_text"]


def generate_sdk(file_path: Path, *, language: Language = "python") -> Path:
    """
    Generate full SDK for the API spec and return the path to the generated SDK file.
    """
    api_spec = process_file(file_path)
    api_spec_name = file_path.stem.split(".")[0]

    initial_code, history = generate_initial_code(api_spec, language=language)

    feedback = feedback_on_generated_code(initial_code, history, language=language)

    final_code = generate_final_code(feedback, history, language=language)

    code, file_extension = get_code_from_model_response(final_code)

    # create a module for the generated sdk
    sdk_module = GENERATED_SDK_DIR / api_spec_name
    sdk_module.mkdir(exist_ok=True)

    # create the sdk file
    sdk_output_file = sdk_module / f"{api_spec_name}{file_extension}"
    sdk_output_file.write_text(code)

    return sdk_output_file
