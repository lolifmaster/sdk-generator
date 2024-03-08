import json
import requests
import pathlib

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZjJhODdiMTUtMTk0MC00YTE3LTljYzQtN2E1ZWVjZDQ4ZGJkIiwidHlwZSI6ImFwaV90b2tlbiJ9.ChywjC-I1Ksp7KeHi1aASB5Oys1fRPY1AtDwhL0AZrc"}

url = "https://api.edenai.run/v2/text/code_generation"

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
the client sdk should be a class with methods for each endpoint in the API and _make_request, _make_authenticated_request methods.
"""

payload = {
    "providers": "openai",
    "prompt": "",
    "instruction": TEMPLATE.format(API_SPEC=api_spec.read_text()),
    "temperature": 0.1,
    "max_tokens": 500,
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
