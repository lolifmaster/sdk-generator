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


# constants

MAX_PROMPT_LENGTH = 4096
MODEL = "gpt-4"
MAX_TOKENS = 3500

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


class TemplateWithoutTypes(TypedDict):
    initial_code: str
    feedback: str
    final_code: str


Step = Literal["types", "initial_code", "feedback", "final_code"]

TEMPLATES: dict[Language, Template] = {
    "python": {
        "types": '''Write the types in python specified in the following openapi specification types (inside triple quotes):
        """{types}"""
        ##IMPORTANT:
        - Use TypedDict for objects (not required fields should have NotRequired type).
        - Use Literals for enums.
        - Use other types as needed.
        - Ensure all types are defined.
        - Ensure all types are correct.
        - the code must be in this format ```(lang)\n (code``` example: ```python\n def hello():\nprint('hello)```
        - No yapping just code!''',
        "initial_code": '''Write a Python client sdk for the following API (inside triple quotes):
            """{api_spec}"""
            
            
            ##RULES:
            {rules}
        
            ##IMPORTANT:
            - The ref types are found in types.py file (from types import *).
            - Ensure implementing all the methods.
            - Dont give usage examples.
            - the code must be in this format ```(lang)\n (code``` example: ```python\n def hello():\nprint('hello)```
            - No yapping just code!
            
            import requests
            from types import *
            ''',
        "feedback": '''Write feedback on the following generated code:
            code: """{generated_code}"""
            The feedback should be constructive and point out any issues with the code.
            The feedback should be detailed and provide suggestions for improvement.
            The feedback should be written as if you are reviewing the code.
            Include any suggestions for improvement.
            
            ##RULES:
            {rules}
            
            ##IMPORTANT:
            - Ensure all methods are implemented.
            - Ensure all methods are correct.
            - Ensure all types are correct.
            - I want docstrings for all methods (a small oneline docstring)
            - I will use this feedback to improve the code.
            - Ensure all issues are addressed.
            - Ensure all suggestions are implemented.''',
        "final_code": '''with the old initial code and the feedback, write the final code,
            feedback: """{feedback}"""
            
            ##RULES:
            {rules}
            
            ##IMPORTANT:
            - Ensure all methods are implemented.
            - Ensure all methods are correct.
            - Ensure all types are correct.
            - I want docstrings for all methods (a small oneline docstring)
            - The ref types are found in types.py file (from types import *).
            - Rewrite the whole code.
            - Docstrings must be small and oneline.
            - Ensure all issues are addressed.
            - Dont give usage examples.
            - the code must be in this format ```(lang)\n (code``` example: ```python\n def hello():\nprint('hello)```
            - give whole new file!!.
            - No yapping just code
            
            import requests
            from types import *
            ''',
    }
}

TEMPLATES_WITHOUT_TYPES: dict[Language, TemplateWithoutTypes] = {
    "python": {
        "initial_code": '''Write a Python client sdk for the following API
            specs: """{api_spec}"""
           
            - Sdk must use the requests library to make the requests.
            - Sdk must be a class with methods for each endpoint in the API, choose a name for the method based on what it does.
            - The requests must handle authenticated request with a _make_authenticated_request\n.
            - Use json for the request body.
            - The methods must return The requests library Response object.
        
            ##IMPORTANT:
            - Ensure implementing all the methods.
            - Dont give usage examples.
            - the code must be in this format ```(lang)\n (code``` example: ```python\n def hello():\nprint('hello)```
            - No yapping just code!''',
        "feedback": '''Write feedback on the following generated code (inside triple quotes) context:
            """{generated_code}"""
            The feedback should be constructive and point out any issues with the code.
            The feedback should be detailed and provide suggestions for improvement.
            The feedback should be written as if you are reviewing the code.
            Include any suggestions for improvement.
            
            ##RULES:
            - Ensure all methods are implemented.
            - Ensure all methods are correct.
            - Ensure all types are correct.
            - I want docstrings for all methods (a small oneline docstring).
            
            ##IMPORTANT:
            - I will use this feedback to improve the code.
            - Ensure all issues are addressed.
            - Ensure all suggestions are implemented.''',
        "final_code": '''with the old initial code and the feedback, write the final code, here's the feedback:
            """{feedback}"""
                
                ##IMPORTANT:
                - Rewrite the whole code.
                - Docstrings must be small and oneline.
                - Ensure all issues are addressed.
                - Dont give usage examples.
                - Give the whole new file!!.
                - the code must be in this format ```(lang)\n (code``` example: ```python\n def hello():\nprint('hello)```
                - No yapping just code!''',
    }
}


def get_code_from_model_response(response) -> tuple[str, str]:
    """
    Extracts the code from the response and returns it along with the file extension for the code.

    :param response: The response from the model.
    :type response: str
    :return: The generated code and its file extension.
    :rtype: tuple (str, str)
    """
    if response is None or not isinstance(response, str):
        raise ValueError("Invalid response. Response must be a non-empty string.")

    code_blocks = code_block_pattern.findall(response)

    if not code_blocks:
        raise ValueError("No code blocks found in the response.")

    language_identifier, _ = code_blocks[0]

    file_extension = language_to_extension.get(language_identifier.lower(), ".txt")

    code = "".join([block[1] for block in code_blocks]).strip()

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

    max_level = 0
    for path in paths:
        level = len(path.split("/"))
        if level > max_level:
            max_level = level

    specs = {}
    level = 1
    while len(specs) < 2 and level < max_level:
        specs = {}
        for path, methods in paths.items():
            resource = path.split("/")[level]
            if resource not in specs:
                specs[resource] = default_spec.copy()
                specs[resource]["paths"] = {}

            specs[resource]["paths"][path] = methods

        level += 1

    if not specs or len(specs) < 2:
        raise ValueError("Failed to split the OpenAPI spec.")

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
    open_specs,
    types_json,
    rules,
    *,
    model: str,
    max_token: int,
    lang: Language = "python",
) -> bool:
    """
    Check if all steps are within the token limit.

    :param rules: The rules for the task.
    :type rules: str
    :param open_specs: The openapi specs.
    :type open_specs: str
    :param types_json: The types json.
    :type types_json: dict
    :param model: The model to use for tokenization.
    :type model: str
    :param max_token: The maximum number of tokens allowed.
    :type max_token: int
    :param lang: The language of the generated code. Default is "python".
    :type lang: Language

    :return: True if all steps are within the limit, False otherwise.

    :rtype: bool
    """

    steps = [
        TEMPLATES[lang]["types"].format(types=types_json, rules=rules),
        TEMPLATES[lang]["initial_code"].format(api_spec=open_specs, rules=rules),
        TEMPLATES[lang]["feedback"].format(generated_code="#" * MAX_TOKENS, rules=rules),
        TEMPLATES[lang]["final_code"].format(feedback="#" * MAX_TOKENS, rules=rules),
    ]

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
