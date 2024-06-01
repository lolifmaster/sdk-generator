import re
import os

import requests
from dotenv import load_dotenv
import yaml
import json
from pathlib import Path
import tiktoken

# from openapi_spec_validator import validate // TOO STRICT VALIDATION
# from openapi_spec_validator.readers import read_from_filename

from sdkgenerator.logger import log_llm_response
from sdkgenerator.constants import (
    EDEN_AI_API,
    OPENAI_API,
)
from sdkgenerator.templates import TEMPLATES, TEMPLATES_WITHOUT_TYPES
from sdkgenerator.types import Language, Step
from sdkgenerator.config import AGENT, MAX_TOKENS, TEMPERATURE

load_dotenv()

code_block_pattern = re.compile(r"```(\w+)([\s\S]+?)```")

language_to_extension = {
    "python": ".py",
}

extension_to_language = {v: k for k, v in language_to_extension.items()}


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


def generate_llm_response(
    payload: dict, *, step: Step, sdk_name: str
) -> tuple[str, list]:
    """
    Generate code for the API spec via the language model.

    :return: The response from the language model.
    """
    if AGENT[step]["custom"]:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        }

        prev_history = [
            {
                "role": step["role"],
                "content": step["message"],
            }
            for step in payload["previous_history"]
        ]

        body = {
            "model": AGENT[step]["model"],
            "max_tokens": MAX_TOKENS[step],
            "temperature": TEMPERATURE[step],
            "top_p": 1,
            "messages": [
                {
                    "role": "system",
                    "content": payload["chatbot_global_action"],
                }
            ]
            + prev_history
            + [
                {
                    "role": "user",
                    "content": payload["text"],
                }
            ],
        }

        response = requests.post(
            OPENAI_API,
            headers=headers,
            json=body,
        )
        response.raise_for_status()
        log_llm_response(body, response.json(), step=step, sdk_name=sdk_name)

        data = response.json()

        message = data["choices"][0]["message"]["content"]
        history = [
            {
                "role": "user",
                "message": payload["text"],
            },
            {
                "role": "assistant",
                "message": message,
            },
        ]

    else:
        headers = {
            "Authorization": f"Bearer {os.getenv('EDEN_AI_AUTH_TOKEN')}",
            "Content-Type": "application/json",
        }

        body = payload | {
            "temperature": TEMPERATURE[step],
            "max_tokens": MAX_TOKENS[step],
            "settings": {"openai": AGENT[step]["model"]},
        }

        response = requests.post(
            EDEN_AI_API,
            headers=headers,
            json=body,
        )

        response.raise_for_status()
        log_llm_response(body, response.json(), step=step, sdk_name=sdk_name)

        data = response.json()

        if "error" in data["openai"]:
            raise Exception(data["openai"]["error"])

        message = data["openai"]["generated_text"]
        history = data["openai"]["message"]

    return message, history


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
    lang: Language = "python",
) -> bool:
    """
    Check if all steps are within the token limit.

    :param open_specs: The OpenAPI specification as a string.
    :param types_json: The types as a JSON string.
    :param user_rules: The rules to apply.
    :param lang: The language to use.

    :return: True if all steps are within the limit, False otherwise.

    :rtype: bool
    """
    rules = "#RULES\n" + "\n".join(user_rules) if user_rules else ""
    with_types = not not types_json

    if with_types:
        steps: list[dict] = [
            {
                "name": "types",
                "prompt": TEMPLATES[lang]["types"].format(
                    types=types_json, rules=rules
                ),
            },
            {
                "name": "initial_code",
                "prompt": TEMPLATES[lang]["initial_code"].format(
                    api_spec=open_specs, rules=rules
                ),
            },
            {
                "name": "feedback",
                "prompt": TEMPLATES[lang]["feedback"].format(
                    generated_code="#" * MAX_TOKENS["feedback"], rules=rules
                ),
            },
            {
                "name": "final_code",
                "prompt": TEMPLATES[lang]["final_code"].format(
                    feedback="#" * MAX_TOKENS["final_code"], rules=rules
                ),
            },
        ]
    else:
        steps: list[dict] = [
            {
                "name": "initial_code",
                "prompt": TEMPLATES_WITHOUT_TYPES[lang]["initial_code"].format(
                    api_spec=open_specs, rules=rules
                ),
            },
            {
                "name": "feedback",
                "prompt": TEMPLATES_WITHOUT_TYPES[lang]["feedback"].format(
                    generated_code="#" * MAX_TOKENS["feedback"], rules=rules
                ),
            },
            {
                "name": "final_code",
                "prompt": TEMPLATES_WITHOUT_TYPES[lang]["final_code"].format(
                    feedback="#" * MAX_TOKENS["final_code"], rules=rules
                ),
            },
        ]

    return all(
        check_step_count(
            step["prompt"],
            model=AGENT[step["name"]]["model"],
            max_token=MAX_TOKENS[step["name"]],
        )
        for step in steps
    )


def validate_openapi_spec(openapi_spec: dict, allowed_methods=None):
    """
    Validate the OpenAPI specification file.

    :param openapi_spec: The OpenAPI specification as a dictionary.
    :type openapi_spec: dict
    :param allowed_methods: The allowed HTTP methods.

    :return: None
    """
    if allowed_methods is None:
        allowed_methods = {
            "get",
            "post",
            "put",
            "delete",
            "patch",
            "head",
            "options",
            "trace",
            "connect",
        }
    if not openapi_spec:
        raise ValueError("Empty OpenAPI spec file.")

    if not isinstance(openapi_spec, dict):
        raise ValueError("Invalid OpenAPI spec file. Must be a dictionary.")

    server = openapi_spec.get("servers", []).pop().get("url", "")
    if not server:
        raise ValueError("Invalid OpenAPI spec file. Missing server URL.")

    paths = openapi_spec.get("paths", {})
    if not paths:
        raise ValueError("Invalid OpenAPI spec file. Missing paths.")

    for path, methods in paths.items():
        for method, details in methods.items():
            if method not in allowed_methods:
                raise ValueError(
                    f"Invalid OpenAPI spec file. Invalid method {method} for {path}."
                )
            if not details.get("operationId"):
                raise ValueError(
                    f"Invalid OpenAPI spec file. Missing operationId for {method} {path}."
                )

            if params := details.get("parameters"):
                for param in params:
                    if not param.get("name") and not param.get("$ref"):
                        raise ValueError(
                            f"Invalid OpenAPI spec file. Missing name for parameter in {method} {path}."
                        )

            if request_body := details.get("requestBody"):
                if not request_body.get("content") and not request_body.get("$ref"):
                    raise ValueError(
                        f"Invalid OpenAPI spec file. Missing content for requestBody in {method} {path}."
                    )

                for content_type, content in request_body.get("content", {}).items():
                    if not content.get("schema"):
                        raise ValueError(
                            f"Invalid OpenAPI spec file. Missing schema for requestBody in {method} {path}."
                        )

    return True


def load_file(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        if file_path.suffix == ".json":
            return json.load(file)
        elif file_path.suffix in {".yaml", ".yml"}:
            return yaml.safe_load(file)
        else:
            raise ValueError(f"Unsupported file format for {file_path}")


def load_spec(file_path: Path) -> dict:
    """
    Load and verify the OpenAPI spec file.

    :param file_path: The file path to the OpenAPI spec.
    :type file_path: Path
    :return: The OpenAPI spec as a string.
    :rtype: str
    """

    file = load_file(file_path)

    if not validate_openapi_spec(file):
        raise ValueError("Invalid OpenAPI spec file.")

    return file
