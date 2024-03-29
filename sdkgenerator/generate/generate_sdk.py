import os
import json
import requests
import pathlib
from dotenv import load_dotenv
from sdkgenerator.manifier import process_file
from sdkgenerator.utils import get_code_from_model_response, Language, TEMPLATES
from pathlib import Path


load_dotenv()

# TODO: will be in a config file

headers = {
    "Authorization": f"Bearer {os.getenv('EDEN_AI_AUTH_TOKEN')}",
    "Content-Type": "application/json",
}

url = "https://api.edenai.run/v2/text/chat"

response_output_dir = (
    pathlib.Path(__file__).parent.parent.parent.absolute() / "api_calls"
)

sdk_output_dir = (
    pathlib.Path(__file__).parent.parent.parent.absolute() / "generated_sdk"
)


def generate_llm_response(
    api_spec: str, api_spec_name: str, language: Language = "python"
):
    """
    Generate code for the API spec via the language model.

    :return: The response from the language model.
    """

    payload = {
        "providers": "openai",
        "text": TEMPLATES.get(language).format(api_spec=api_spec),
        "chatbot_global_action": f"You are a {language} developer, and you are writing a client sdk for an API",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 3000,
        "settings": {"openai": "gpt-4"},
        "fallback_providers": "",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to generate code for {api_spec_name}")
        print(e)


def generate_sdk(file_path: Path, *, language: Language = "python"):
    """
    Generate code for the API spec and save it to the generated_sdk directory.
    """
    api_spec = process_file(file_path)
    api_spec_name = file_path.stem.split(".")[0]

    response = generate_llm_response(api_spec, api_spec_name, language)

    if response is None:
        return

    if "error" in response["openai"]:
        print(f"Failed to generate code for {api_spec_name}")
        print(response)
        return

    response_output_file = response_output_dir / f"{api_spec_name}.txt"
    response_output_file.write_text(response["openai"]["generated_text"])

    code, file_extension = get_code_from_model_response(
        response["openai"]["generated_text"]
    )
    sdk_output_file = sdk_output_dir / f"{api_spec_name}{file_extension}"
    sdk_output_file.write_text(code)
    print(
        f"Generated code for {api_spec_name} in {language} and saved to {sdk_output_file}"
    )
    return sdk_output_file
