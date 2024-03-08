import json
import requests
import pathlib
import os
import dotenv

dotenv.load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('EDEN_AI_AUTH_TOKEN')}",
    "Content-Type": "application/json"
}

url = "https://api.edenai.run/v2/text/chat"

simplified_specs_dir = pathlib.Path(__file__).parent.absolute() / 'data' / 'simplified-batch-specs'

output_dir = pathlib.Path(__file__).parent.absolute() / 'api_calls'

api_spec_name = "_pdfgeneratorapi.txt"

api_spec = simplified_specs_dir / api_spec_name

TEMPLATE = """
Write a Python client sdk for the following API:

---
{API_SPEC}
---

The client sdk should be able to make requests to the API and return the response.
you should use the requests library to make the requests.
the client sdk should be a class with methods for each endpoint in the API.
the requests should be by two methods _make_request or _make_authenticated_request.
"""

payload = {
    "providers": "openai",
    "text": TEMPLATE.format(API_SPEC=api_spec.read_text()),
    "chatbot_global_action": "You are a programmer",
    "previous_history": [],
    "temperature": 0.0,
    "max_tokens": 2000,
    "settings": {
        "openai": "gpt-4"
    },
    "fallback_providers": ""
}


def generate_code():
    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)

    if response.status_code == 200:
        output_file = output_dir / api_spec_name
        output_file.write_text(result['openai']['generated_text'])
        print(f"Output written to {output_file}")


if __name__ == "__main__":
    generate_code()
