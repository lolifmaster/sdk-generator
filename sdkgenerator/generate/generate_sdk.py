from dotenv import load_dotenv
from sdkgenerator.manifier import process_file
from sdkgenerator.utils import (
    get_code_from_model_response,
    Language,
    API_CALLS_DIR,
    GENERATED_SDK_DIR,
    generate_llm_response,
    TEMPLATES,
)
from pathlib import Path

load_dotenv()


def generate_sdk(file_path: Path, *, language: Language = "python") -> Path:
    """
    Generate code for the API spec and save it to the generated_sdk module.
    """
    api_spec = process_file(file_path)
    api_spec_name = file_path.stem.split(".")[0]

    response = generate_llm_response(
        payload={
            "providers": "openai",
            "text": TEMPLATES[language]["sdk"].format(api_spec=api_spec),
            "chatbot_global_action": f"You are a {language} developer, and you are writing a client sdk for an API",
            "previous_history": [],
            "temperature": 0.0,
            "max_tokens": 4000,
            "settings": {"openai": "gpt-4"},
            "fallback_providers": "",
        },
    )

    if response is None:
        raise Exception("Failed to generate code")

    if "error" in response["openai"]:
        raise Exception(response["openai"]["error"])

    response_output_file = API_CALLS_DIR / f"{api_spec_name}.txt"
    response_output_file.write_text(response["openai"]["generated_text"])

    code, file_extension = get_code_from_model_response(
        response["openai"]["generated_text"]
    )

    if not code or not file_extension:
        raise Exception("The generated code is empty or the file extension is missing.")

    # create a module for the generated sdk
    sdk_module = GENERATED_SDK_DIR / api_spec_name
    sdk_module.mkdir(exist_ok=True)

    # create the sdk file
    sdk_output_file = sdk_module / f"{api_spec_name}{file_extension}"
    sdk_output_file.write_text(code)

    return sdk_output_file
