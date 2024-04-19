import re
from typing import Literal
import pathlib
import os
import requests
from dotenv import load_dotenv
from typing import TypedDict
import yaml
import json
from pathlib import Path

load_dotenv()

API_CALLS_DIR = pathlib.Path(__file__).parent.parent.absolute() / "api_calls"

GENERATED_SDK_DIR = pathlib.Path(__file__).parent.parent.absolute() / "generated_sdk"

EDEN_AI_API = "https://api.edenai.run/v2/text/chat"

Language = Literal["python"]

# Precompile the regular expression for better performance
code_block_pattern = re.compile(r"```(\w+)([\s\S]+?)```")

language_to_extension = {
    "python": ".py",
}

extension_to_language = {v: k for k, v in language_to_extension.items()}


class Template(TypedDict):
    initial_code: str
    feedback: str
    final_code: str
    # test: str


TEMPLATES: dict[Language, Template] = {
    "python": {
        "initial_code": '''Write a Python client sdk for the following API (inside triple quotes):
            """{api_spec}"""
            Sdk must use the requests library to make the requests.
            Sdk must be a class with methods for each endpoint in the API, choose a name for the method based on what it does.
            Nullable fields must be NotRequired in the method arguments.
            Ensure type hints for arguments and return types.
            Objects typed using TypedDict not required params must be inside NotRequired type.
            Enums typed using Literal.
            The requests must handle authenticated request with a _make_authenticated_request\n.
            Use json for the request body.
            The methods must return The requests library Response object.
        
            Ensure implementing all the methods.\n
            No yapping.
        ''',
        "feedback": '''Write feedback on the following generated code (inside triple quotes):
            """{generated_code}"""
            The feedback should be constructive and point out any issues with the code.
            The feedback should be detailed and provide suggestions for improvement.
            The feedback should be written as if you are reviewing the code.
            
            Ensure all issues are addressed.
        ''',
        "final_code": '''Write the final version of the Python client sdk looking at the feedback provided (inside triple quotes):
            """feedback"""
            Ensure all issues are addressed.
            Ensure type hints, especially for dicts.
            No yapping.''',
        # TODO: Implement test template
        # "test": """
        #     Write unit tests for the following python client sdk class (inside triple quotes):
        #     """{sdk}"""
        #     Use unittest and mock.patch to mock the requests library.
        #     The sdk class must be imported from the sdk file named {sdk_file_name} found in the same directory as the test file.
        #     Write a test for each method in the sdk class.
        #
        #     Ensure all methods are tested.
        #     No yapping.
        # """,
    }
}


def get_code_from_model_response(response):
    """
    Extracts the code from the response and returns it along with the file extension for the code.

    :param response: The response from the model.
    :type response: str
    :return: The generated code and its file extension.
    :rtype: tuple (str or None, str or None)
    """
    if response is None or not isinstance(response, str):
        return None, None

    code_blocks = code_block_pattern.findall(response)

    if not code_blocks:
        return None, None

    language_identifier, _ = code_blocks[0]

    file_extension = language_to_extension.get(language_identifier.lower(), ".txt")

    code = "".join([block[1] for block in code_blocks])

    return code, file_extension


def log_llm_response(payload: dict, response: dict):
    """
    Log the response from the language model to logs file.

    :param payload: The payload sent to the language model.
    :type payload: dict
    :param response: The response from the language model.
    :type response: dict
    :return: None
    """

    with open(API_CALLS_DIR / "logs.txt", "a+", encoding="utf-8") as file:
        file.write(f"Payload: {json.dumps(payload, indent=2)}\n")
        file.write(f"Response: {json.dumps(response, indent=2)}\n-----------\n")


def generate_llm_response(
    payload: dict,
):
    """
    Generate code for the API spec via the language model.

    :return: The response from the language model.
    """
    # TODO: will be in a config file

    headers = {
        "Authorization": f"Bearer {os.getenv('EDEN_AI_AUTH_TOKEN')}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(EDEN_AI_API, headers=headers, json=payload)
        log_llm_response(payload, response.json())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)


def split_openapi_spec(file_path: Path, output_dir_path: Path):
    """
    Split an OpenAPI specification file into separate files for each resource.
    :param file_path: Path to the OpenAPI specification file.
    :param output_dir_path: Path to the directory where the split files will be saved.

    :return: None
    """
    with open(file_path, "r", encoding="utf-8") as file:
        if file_path.suffix == ".yaml" or file_path.suffix == ".yml":
            spec = yaml.safe_load(file)
        elif file_path.suffix == ".json":
            spec = json.load(file)
        else:
            raise ValueError(
                "Unsupported file format. Please provide a YAML or JSON file."
            )

    paths = spec.get("paths", {})
    default_spec = spec.copy()
    del default_spec["paths"]

    specs = {}
    for path, methods in paths.items():
        resource = path.split("/")[1]
        if resource not in specs:
            specs[resource] = default_spec.copy()
            specs[resource]["paths"] = {}

        specs[resource]["paths"][path] = methods

    for resource, spec in specs.items():
        resource = resource.replace("{", "").replace("}", "")
        output_file = output_dir_path / f"{resource}.json"
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(spec, file, indent=2)
