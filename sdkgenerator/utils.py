import re
from typing import Literal
import pathlib
import os
import requests
from dotenv import load_dotenv
from typing import TypedDict

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
    sdk: str
    test: str


TEMPLATES: dict[Language, Template] = {
    "python": {
        "sdk": """
        Write a Python client sdk for the following API (inside triple quotes):
        \"\"\"{api_spec}\"\"\"
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
    """,
        "test": """
        Write unit tests for the following python client sdk class (inside triple quotes):
        \"\"\"{sdk}\"\"\"
        Use unittest and mock.patch to mock the requests library.
        The sdk class must be imported from the sdk file named {sdk_file_name} found in the same directory as the test file.
        Write a test for each method in the sdk class.
        
        Ensure all methods are tested.
        No yapping.
        """,
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
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)
