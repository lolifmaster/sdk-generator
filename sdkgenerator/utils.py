import re
import pathlib
import os
import requests
from dotenv import load_dotenv
from typing import TypedDict, Literal
import yaml
import json
from pathlib import Path
import tiktoken
from sdkgenerator.db import db
from openapi_spec_validator import validate
from openapi_spec_validator.readers import read_from_filename

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
    types: str
    initial_code: str
    feedback: str
    final_code: str
    # test: str


Step = Literal["types", "initial_code", "feedback", "final_code"]

TEMPLATES: dict[Language, Template] = {
    "python": {
        "types": '''Write the types in python specified in the following json (inside triple quotes):
        """{types}"""
        
        - Use TypedDict for objects (not required fields should have NotRequired type).
        - Use Literals for enums.
        - Use other types as needed.
        - Ensure all types are defined.
        - Ensure all types are correct.
        ''',
        "initial_code": '''Write a Python client sdk for the following API (inside triple quotes):
            """{api_spec}"""
            the ref types are found in types.py file (from types import *).
            Sdk must use the requests library to make the requests.
            Sdk must be a class with methods for each endpoint in the API, choose a name for the method based on what it does.
            The requests must handle authenticated request with a _make_authenticated_request\n.
            Use json for the request body.
            The methods must return The requests library Response object.
        
            Ensure implementing all the methods.\n
            No yapping.
        ''',
        "feedback": '''Write feedback on the following generated code (inside triple quotes) context (types are in types.py):
            """{generated_code}"""
            The feedback should be constructive and point out any issues with the code.
            The feedback should be detailed and provide suggestions for improvement.
            The feedback should be written as if you are reviewing the code.
            
            Ensure all issues are addressed.
        ''',
        "final_code": '''Write the final version of the Python client sdk looking at this feedback (inside triple quotes):
            """{feedback}"""
            
            the types needed are in the types file (from types import *).
            Ensure all issues are addressed.
            Give the whole file.
            The ref types are found in types.py file.
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


def log_llm_response(
    payload: dict, response: dict, *, step: Step, sdk_name: str = None
):
    """
    Log the response from the language model to logs file.

    :param sdk_name: The name of the SDK.
    :type sdk_name: str
    :param step: The step in the process.
    :type step: Step
    :param payload: The payload sent to the language model.
    :type payload: dict
    :param response: The response from the language model.
    :type response: dict
    :return: None
    """

    # save the response to the database
    db.insert_one(
        {"step": step, "sdk_name": sdk_name, "payload": payload, "response": response}
    )

    with open(API_CALLS_DIR / "logs.txt", "a+", encoding="utf-8") as file:
        file.write(f"Step: {step}\n")
        file.write(f"Payload: {json.dumps(payload, indent=2)}\n")
        file.write(f"Response: {json.dumps(response, indent=2)}\n-----------\n")


def generate_llm_response(payload: dict, *, step: Step, sdk_name: str):
    """
    Generate code for the API spec via the language model.

    :return: The response from the language model.
    """

    headers = {
        "Authorization": f"Bearer {os.getenv('EDEN_AI_AUTH_TOKEN')}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(EDEN_AI_API, headers=headers, json=payload)
        response.raise_for_status()
        log_llm_response(payload, response.json(), step=step, sdk_name=sdk_name)
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


def count_token(txt: str, model: str):
    encoding = tiktoken.encoding_for_model(model)
    num_token = len(encoding.encode(txt))
    return num_token


def check_step_count(txt: str, *, model: str, max_token: int) -> bool:
    """
    Check if the number of tokens in the text is within the limit for the step.

    :param txt: The text to check.
    :type txt: str
    :param model: The model to use for tokenization.
    :type model: str
    :param max_token: The maximum number of tokens allowed.
    :type max_token: int
    :return: True if the number of tokens is within the limit, False otherwise.
    :rtype: bool
    """
    return count_token(txt, model) <= max_token


def is_all_steps_within_limit(
    open_specs, types_json, *, model: str, max_token: int, lang: Language = "python"
) -> bool:
    """
    Check if all steps are within the token limit.

    :param open_specs: The openapi specs.
    :type open_specs: str
    :param types_json: The types json.
    :type types_json: str
    :param model: The model to use for tokenization.
    :type model: str
    :param max_token: The maximum number of tokens allowed.
    :type max_token: int
    :param lang: The language of the generated code. Default is "python".
    :type lang: Language

    :return: True if all steps are within the limit, False otherwise.

    :rtype: bool
    """

    steps = []
    types_prompt = TEMPLATES[lang]["types"].format(types=types_json)
    initial_code_prompt = TEMPLATES[lang]["initial_code"].format(api_spec=open_specs)

    steps.append(types_prompt)
    steps.append(initial_code_prompt)

    return all(
        check_step_count(step, model=model, max_token=max_token) for step in steps
    )


def validate_openapi_spec(file_path: Path):
    """
    Validate the OpenAPI specification file.

    :param file_path: Path to the OpenAPI specification file.
    :type file_path: Path
    :return: None
    """
    try:
        spec_dict, _ = read_from_filename(str(file_path))
        validate(spec_dict)
    except Exception as e:
        raise Exception(f"Failed to validate OpenAPI spec: {e}")
