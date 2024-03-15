import os
import json
import requests
import pathlib
from utils import get_code_from_model_response
from dotenv import load_dotenv

load_dotenv()

# TODO: will be in a config file

headers = {
    "Authorization": f"Bearer {os.getenv('EDEN_AI_AUTH_TOKEN')}",
    "Content-Type": "application/json",
}

url = "https://api.edenai.run/v2/text/chat"
simplified_specs_dir = (
    pathlib.Path(__file__).parent.absolute() / "data" / "eden" / "processed-specs"
)
response_output_dir = pathlib.Path(__file__).parent.absolute() / "api_calls"
sdk_output_dir = pathlib.Path(__file__).parent.absolute() / "generated_sdk"
api_spec_name = "aiproducts.txt"
api_spec = simplified_specs_dir / api_spec_name

TEMPLATE = """
    Write a Python client sdk for the following API:
    ---{api_spec}---
    Sdk must use the requests library to make the requests.
    Sdk must be a class with methods for each endpoint in the API.
    Nullable fields must be NotRequired in the method arguments.
    Ensure type hints for arguments and return types, with objects typed using TypedDict and enums using Literal.
    the class name must be the name of the API.
    the requests must be by two methods _make_request or _make_authenticated_request\n.
    
    ensure implementing all the methods.\n
    no yapping.
"""

payload = {
    "providers": "openai",
    "text": TEMPLATE.format(api_spec=api_spec.read_text()),
    "chatbot_global_action": "You are a python developer, and you are writing a client sdk for an API",
    "previous_history": [],
    "temperature": 0.0,
    "max_tokens": 3000,
    "settings": {"openai": "gpt-4"},
    "fallback_providers": "",
}


def generate_code():
    """
    Generate code for the API spec and save it to the generated_sdk directory.
    """
    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(payload)
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to generate code for {api_spec_name}")
        print(e)


def main():
    response = generate_code()

    if response is None:
        return

    if 'error' in response['openai']:
        print(f"Failed to generate code for {api_spec_name}")
        print(response)
        return

    response_output_file = response_output_dir / api_spec_name
    response_output_file.write_text(response["openai"]["generated_text"])

    code, file_extension = get_code_from_model_response(
        response["openai"]["generated_text"]
    )
    sdk_output_file = (
            sdk_output_dir / f"{api_spec_name.split('.')[0]}{file_extension}"
    )
    sdk_output_file.write_text(code)

    print(f"Generated code for {api_spec_name} and saved to {sdk_output_file}")


if __name__ == "__main__":
    main()
