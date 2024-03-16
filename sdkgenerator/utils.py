import re
from typing import Literal

Language = Literal["python", "javascript", "typescript"]


# Precompile the regular expression for better performance
code_block_pattern = re.compile(r"```(\w+)([\s\S]+?)```")

language_to_extension = {
    "python": ".py",
    "javascript": ".js",
    "typescript": ".ts",
}

TEMPLATES: dict[Language, str] = {
    "python": """
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
    """,
    "javascript": """
        Write a JavaScript client sdk for the following API:
        ---{api_spec}---
        Sdk must use the axios library to make the requests.
        Sdk must be a class with methods for each endpoint in the API.
        Nullable fields must be optional in the method arguments.
        Ensure type hints for arguments and return types, with objects typed using interfaces and enums using union types.
        the class name must be the name of the API.
        the requests must be by two methods _makeRequest or _makeAuthenticatedRequest\n.
    
        ensure implementing all the methods.\n
        no yapping.
    """,
    "typescript": """
        Write a TypeScript client sdk for the following API:
        ---{api_spec}---
        Sdk must use the axios library to make the requests.
        Sdk must be a class with methods for each endpoint in the API.
        Nullable fields must be optional in the method arguments.
        Ensure type hints for arguments and return types, with objects typed using interfaces and enums using union types.
        the class name must be the name of the API.
        the requests must be by two methods _makeRequest or _makeAuthenticatedRequest\n.
    
        ensure implementing all the methods.\n
        no yapping.
    """,
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
