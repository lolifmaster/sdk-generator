from sdkgenerator.types import Language
from sdkgenerator.utils import get_code_from_model_response, generate_llm_response
from sdkgenerator.templates import TEMPLATES, TEMPLATES_WITHOUT_TYPES


def generate_types(
    types_json: str, *, language: Language = "python"
) -> tuple[str, str]:
    """
    Generate types for the API spec and return it as a string.

    Args:
    types_file_path: The types.
    language: The language of the generated code. Default is "python".

    Returns:
        tuple[str, str]: The generated types for the API spec, and the file extension.
    """

    print("Generating types")
    message, _ = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["types"].format(types=types_json),
            "chatbot_global_action": f"You are a {language} developer, and you are writing types for an API",
            "previous_history": [],
        },
        step="types",
        sdk_name="types",
    )

    return get_code_from_model_response(message)


def generate_initial_code(
    api_spec: str, types: str, sdk_name: str, rules: str, language: Language = "python"
) -> tuple[str, list]:
    """
    Generate code for the API spec and return it as a string.

    Args:
    api_spec: The API spec.
    sdk_name: The name of the SDK.
    rules: The rules for the SDK.
    language: The language of the generated code. Default is "python".

    Returns:
        tuple[str, list]: The generated code for the API spec and the history of the conversation.
    """

    print("Generating initial code")
    message, history = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["initial_code"].format(
                api_spec=api_spec, rules=rules
            ),
            "chatbot_global_action": f"You are a {language} developer, and you are writing a client sdk for an API",
            "previous_history": [
                {"role": "user", "message": "Generate types needed for the sdk"},
                {
                    "role": "assistant",
                    "message": f"Here are the types needed for the sdk stored in a file called types.py : '''{types}'''",
                },
            ],
        },
        step="initial_code",
        sdk_name=sdk_name,
    )

    code, _ = get_code_from_model_response(message)

    if not code:
        raise Exception("The generated initial code is empty.")

    return code, history


def feedback_on_generated_code(
    generated_code: str,
    previous_history: list,
    *,
    sdk_name: str,
    rules: str,
    language: Language = "python",
) -> str:
    """
    Generate Feedback on the generated code for the API spec and return it as a string.

    Args:
    generated_code: The generated code for the API spec.
    previous_history: The previous history of the conversation.
    language: The language of the generated code. Default is "python".
    sdk_name: The name of the SDK.
    rules: The rules for the SDK.

    Returns:
    str: The feedback on the generated code.
    """

    print("Generating feedback")
    message, _ = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["feedback"].format(
                generated_code=generated_code, rules=rules
            ),
            "chatbot_global_action": f"You are a {language} developer reviewing code for an SDK",
            "previous_history": previous_history,
        },
        step="feedback",
        sdk_name=sdk_name,
    )

    return message


def generate_final_code(
    feedback: str,
    previous_history: list,
    *,
    sdk_name: str,
    rules: str,
    language: Language = "python",
) -> tuple[str, str]:
    """
    Generate final code for the API spec and return it as a string.

    Args:
    initial_code: The initial code for the API spec.
    feedback: The feedback on the initial code.
    language: The language of the generated code. Default is "python".
    sdk_name: The name of the SDK.
    rules: The rules for the SDK.

    Returns:
        tuple[str, str]: The final code for the API spec, and the file extension.
    """

    print("Generating final code")

    message, _ = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["final_code"].format(
                feedback=feedback, rules=rules
            ),
            "chatbot_global_action": f"You are a {language} developer, and you are refining a generated code",
            "previous_history": previous_history,
        },
        step="final_code",
        sdk_name=sdk_name,
    )

    return get_code_from_model_response(message)


def generate_initial_code_without_types(
    api_spec: str, sdk_name: str, rules: str, language: Language = "python"
) -> str:
    """
    Generate code for the API spec and return it as a string.

    Args:
    api_spec: The API spec.
    sdk_name: The name of the SDK.
    rules: The rules for the SDK.
    language: The language of the generated code. Default is "python".

    Returns:
        str: The generated code for the API spec.

    """

    print("Generating initial code")
    message, _ = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES_WITHOUT_TYPES[language]["initial_code"].format(
                api_spec=api_spec,
                rules=rules,
            ),
            "chatbot_global_action": f"You are a {language} developer, and you are writing a client sdk for an API",
            "previous_history": [],
        },
        step="initial_code",
        sdk_name=sdk_name,
    )

    code, _ = get_code_from_model_response(message)

    if not code:
        raise Exception("The generated initial code is empty.")

    return code


def feedback_on_generated_code_without_types(
    generated_code: str,
    previous_history: list,
    *,
    sdk_name: str,
    rules: str,
    language: Language = "python",
) -> str:
    """
    Generate Feedback on the generated code for the API spec and return it as a string.

    Args:
        :arg generated_code: The generated code for the API spec.
        :arg previous_history: The previous history of the conversation.
        :arg sdk_name: The name of the SDK.
        :arg rules: The rules for the SDK.
        :arg language: The language of the generated code. Default is "python".
    Returns: str: The feedback on the generated code.
    """

    print("Generating feedback")
    message, _ = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES_WITHOUT_TYPES[language]["feedback"].format(
                generated_code=generated_code,
                rules=rules,
            ),
            "chatbot_global_action": f"You are a {language} developer reviewing code for an SDK",
            "previous_history": previous_history,
        },
        step="feedback",
        sdk_name=sdk_name,
    )

    return message


def generate_final_code_without_types(
    feedback: str,
    previous_history: list,
    *,
    sdk_name: str,
    rules: str,
    language: Language = "python",
) -> tuple[str, str]:
    """
    Generate final code for the API spec and return it as a string.

    Args:
        :arg feedback: The feedback on the initial code.
        :arg previous_history: The previous history of the conversation.
        :arg sdk_name: The name of the SDK.
        :arg rules: The rules for the SDK.
        :arg language: The language of the generated code. Default is "python".

    Returns:
        tuple[str, str]: The final code for the API spec, and the file extension.
    """

    print("Generating final code")

    message, _ = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES_WITHOUT_TYPES[language]["final_code"].format(
                feedback=feedback,
                rules=rules,
            ),
            "chatbot_global_action": f"You are a {language} developer, and you are refining a generated code",
            "previous_history": previous_history,
        },
        step="final_code",
        sdk_name=sdk_name,
    )

    return get_code_from_model_response(message)
