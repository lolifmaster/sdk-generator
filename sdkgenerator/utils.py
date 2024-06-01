import re
import os
import requests
from dotenv import load_dotenv
import yaml
import json
from pathlib import Path
import tiktoken
from openapi_spec_validator import validate
from openapi_spec_validator.readers import read_from_filename

from sdkgenerator.logger import log_llm_response
from sdkgenerator.manifier import process_file
from sdkgenerator.constants import MAX_TOKENS, EDEN_AI_API
from sdkgenerator.templates import TEMPLATES, TEMPLATES_WITHOUT_TYPES
from sdkgenerator.types import Language, Step

load_dotenv()

code_block_pattern = re.compile(r"```(\w+)([\s\S]+?)```")

language_to_extension = {
    "python": ".py",
}

extension_to_language = {v: k for k, v in language_to_extension.items()}


def load_openapi_spec(file_path: Path) -> tuple[str, dict]:
    """
    Load, validate and process the OpenAPI spec file.

    Args:
    file_path: The file path to the OpenAPI spec.

    Returns:
        tuple[str, str]: The OpenAPI spec as a string, and the types as a string.

    """
    api_spec, types_json = process_file(file_path)

    return api_spec, types_json


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
        open_specs: str,
        types_json: dict,
        *,
        user_rules: list[str],
        with_types: bool,
        model: str,
        max_token: int,
        lang: Language = "python",
) -> bool:
    """
    Check if all steps are within the token limit.

    :param open_specs: The OpenAPI specification as a string.
    :param types_json: The types as a JSON string.
    :param with_types: Whether to include types in the generated code.
    :param user_rules: The rules to apply.
    :param model: The model to use for tokenization.
    :param max_token: The maximum number of tokens allowed.
    :param lang: The language to use.

    :return: True if all steps are within the limit, False otherwise.

    :rtype: bool
    """
    rules = "#RULES\n" + "\n".join(user_rules) if user_rules else ""

    if with_types:
        steps = [
            TEMPLATES[lang]["types"].format(types=types_json, rules=rules),
            TEMPLATES[lang]["initial_code"].format(api_spec=open_specs, rules=rules),
            TEMPLATES[lang]["feedback"].format(
                generated_code="#" * MAX_TOKENS, rules=rules
            ),
            TEMPLATES[lang]["final_code"].format(
                feedback="#" * MAX_TOKENS, rules=rules
            ),
        ]
    else:
        steps = [
            TEMPLATES_WITHOUT_TYPES[lang]["initial_code"].format(
                api_spec=open_specs, rules=rules
            ),
            TEMPLATES_WITHOUT_TYPES[lang]["feedback"].format(
                generated_code="#" * MAX_TOKENS, rules=rules
            ),
            TEMPLATES_WITHOUT_TYPES[lang]["final_code"].format(
                feedback="#" * MAX_TOKENS, rules=rules
            ),
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
