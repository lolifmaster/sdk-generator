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
    pathlib.Path(__file__).parent.absolute() / "data" / "simplified-batch-specs"
)
response_output_dir = pathlib.Path(__file__).parent.absolute() / "api_calls"
sdk_output_dir = pathlib.Path(__file__).parent.absolute() / "generated_sdk"
api_spec_name = "_pdfgeneratorapi.txt"
api_spec = simplified_specs_dir / api_spec_name

payload = {
    "providers": "openai",
    "text": f"Write a Python client sdk for the following API:\n---\n{api_spec.read_text()}\n---\nThe client sdk should be able to make requests to the API and return the response.\nyou should use the requests library to make the requests.\nthe client sdk should be a class with methods for each endpoint in the API.\nthe requests should be by two methods _make_request or _make_authenticated_request.",
    "chatbot_global_action": "You are a programmer",
    "previous_history": [],
    "temperature": 0.0,
    "max_tokens": 2000,
    "settings": {"openai": "gpt-4"},
    "fallback_providers": "",
}


def generate_code():
    """
    Generate code for the API spec and save it to the generated_sdk directory.
    """
    return requests.post(url, json=payload, headers=headers)


def main():
    response = generate_code()
    result = json.loads(response.text)

    if response.status_code == 200:
        response_output_file = response_output_dir / api_spec_name
        response_output_file.write_text(result["openai"]["generated_text"])

        code, file_extension = get_code_from_model_response(
            result["openai"]["generated_text"]
        )
        sdk_output_file = (
            sdk_output_dir / f"{api_spec_name.split('.')[0]}{file_extension}"
        )
        sdk_output_file.write_text(code)

        print(f"Generated code for {api_spec_name} and saved to {sdk_output_file}")
    else:
        print(f"Failed to generate code for {api_spec_name}")
        print(result)


if __name__ == "__main__":
    main()
