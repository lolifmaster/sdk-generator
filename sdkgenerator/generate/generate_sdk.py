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


def generate_initial_code(api_spec: str, *, language: Language = "python") -> str:
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
            "settings": {"openai": "gpt-4"}

        },
    )

    if response is None:
        raise Exception("Failed to generate code")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    code, _ = get_code_from_model_response(response["openai"]["generated_text"])

    if not code:
        raise Exception("The generated code is empty.")

    return code


def feedback_on_generated_code(
    api_spec: str, generated_code: str, *, language: Language = "python"
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
            "chatbot_global_action": f"You are a {language} developer, and you are reviewing a generated code",
            "previous_history": [
                {
                    'role': 'user',
                    'message': f'generate code for this API spec: {api_spec}',
                },
            ],
            "temperature": 0.2,
            "max_tokens": 4000,
            "settings": {'openai': "gpt-4"},

        },
    )

    if response is None:
        raise Exception("Failed to generate feedback")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    return response["openai"]["generated_text"]


def generate_final_code(
    api_spec: str, initial_code: str, feedback: str, *, language: Language = "python"
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
            "text": TEMPLATES[language]["final_code"].format(
                initial_code=initial_code, feedback=feedback
            ),
            "chatbot_global_action": f"You are a {language} developer, and you are refining a generated code",
            "previous_history": [
                {
                    'role': 'user',
                    'message': f'generate code for this API spec: {api_spec}',
                },
                {
                    'role': 'assistant',
                    'message': initial_code,
                },
                {
                    'role': 'user',
                    'message': feedback,
                },
            ],
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


def generate_tests(
    api_spec: str, generated_code: str, *, language: Language = "python"
) -> str:
    """
    Generate tests for the API spec and return them as a string.

    Args:
    generated_code: The generated code for the API spec.
    language: The language of the generated code. Default is "python".

    Returns:
    str: The generated tests for the API spec.
    """
    response = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["test"],
            "chatbot_global_action": f"You are a {language} developer, and you are writing tests for an SDK",
            "previous_history": [
                {
                    'role': 'user',
                    'message': f'generate sdk for this API spec: {api_spec}',
                },
                {
                    'role': 'assistant',
                    'message': generated_code,
                },
            ],
            "temperature": 0.0,
            "max_tokens": 4000,
            "settings": {"openai": "gpt-4"},

        },
    )

    if response is None:
        raise Exception("Failed to generate tests")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    code, _ = get_code_from_model_response(response["openai"]["generated_text"])

    if not code:
        raise Exception("The generated tests are empty.")

    return code


def generate_sdk(file_path: Path, *, language: Language = "python") -> Path:
    """
    Generate full SDK for the API spec and return the path to the generated SDK file.
    """
    api_spec = process_file(file_path)
    api_spec_name = file_path.stem.split(".")[0]

    initial_code = generate_initial_code(api_spec, language=language)

    feedback = feedback_on_generated_code(api_spec, initial_code, language=language)

    final_code = generate_final_code(api_spec, initial_code, feedback, language=language)

    code, file_extension = get_code_from_model_response(final_code)

    tests = generate_tests(api_spec, code, language=language)
    test_code, _ = get_code_from_model_response(tests)

    # create a module for the generated sdk
    sdk_module = GENERATED_SDK_DIR / api_spec_name
    sdk_module.mkdir(exist_ok=True)

    # create the sdk file
    sdk_output_file = sdk_module / f"{api_spec_name}{file_extension}"
    sdk_output_file.write_text(code)

    # create the test file
    test_output_file = sdk_module / f"test_{api_spec_name}{file_extension}"
    test_output_file.write_text(test_code)

    return sdk_output_file
