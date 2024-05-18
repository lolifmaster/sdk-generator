
from sdkgenerator.utils import get_code_from_model_response


class TestGetCodeFromModelResponse:

    #  Returns the generated code and its file extension when the response contains a single code block.
    def test_extract_code_from_single_block(self):
        response = "Here is some text\n```python\ndef function():\n    print('Hello, World!')\n```\nSome more text"
        expected_code = "def function():\n    print('Hello, World!')"

        actual_code, file_extension = get_code_from_model_response(response)
        assert actual_code == expected_code
        assert file_extension == ".py"

    #  Raise an error if multi-languages are in the same response.
    def test_extract_code_from_multiple_blocks(self):
        response = "Here is some text\n```python\ndef function():\n    print('Hello, World!')\n```\nSome more text\n```javascript\ndef hello():\n    console.log('Hello, World!');\n}\n```"

        try:
            get_code_from_model_response(response)
        except ValueError as e:
            assert str(e) == "Code blocks are in different languages"

    #  Returns none when the input response contains a code block with no code and no language identifier.
    def test_return_none_and_when_no_code(self):
        response = "Here is some text\n```python\n```"
        expected_code = None

        actual_code, file_extension = get_code_from_model_response(response)
        assert actual_code == expected_code
        assert file_extension == None

    #  Returns the generated code and its file extension when the response contains a single code block with an unknown language identifier.
    def test_return_code_and_file_extension_with_unknown_language_identifier(self):
        response = "Here is some text\n```unknown\ndef function():\n    print('Hello, World!')\n```\nSome more text"
        expected_code = "def function():\n    print('Hello, World!')"

        actual_code, file_extension = get_code_from_model_response(response)
        assert actual_code == expected_code
        assert file_extension == ".txt"

    #  Returns the generated code and its file extension when the response contains multiple code blocks with unknown language identifiers.
    def test_return_code_and_file_extension_with_multiple_unknown_language_identifiers(self):
        response = "Here is some text\n```unknown\ndef function():\n    print('Hello, World!')\n```\nSome more text\n```other\ndef hello():\n    console.log('Hello, World!');\n}\n```"
        expected_code = "def function():\n    print('Hello, World!')"

        actual_code, file_extension = get_code_from_model_response(response)
        assert actual_code == expected_code
        assert file_extension == ".txt"

    #  Returns the generated code and its file extension when the response contains multiple code blocks with the same language identifier.
    def test_return_code_and_file_extension_with_same_language_identifier(self):
        response = "Here is some text\n```python\ndef function():\n    print('Hello, World!')\n```\nSome more text\n```python\ndef hello():\n    print('Hello, World!');\n}\n```"
        expected_code = "def function():\n    print('Hello, World!')def hello():\n    print('Hello, World!');"

        actual_code, file_extension = get_code_from_model_response(response)
        assert actual_code == expected_code
        assert file_extension == ".py"

    #  Returns None when the response does not contain a code block.
    def test_return_none_when_no_code_block(self):
        response = "Here is some text without a code block"

        actual_code, file_extension = get_code_from_model_response(response)

        assert actual_code is None
        assert file_extension is None

    #  Returns None, None when the input response is None.
    def test_return_none_when_input_response_is_none(self):
        response = None

        actual_code, file_extension = get_code_from_model_response(response)

        assert actual_code is None
        assert file_extension is None

    #  Returns None, None when the input response is not a string.
    def test_return_none_when_input_response_is_not_string(self):
        response = 123

        actual_code, file_extension = get_code_from_model_response(response)

        assert actual_code is None
        assert file_extension is None

    #  Returns None, None when the input response is an empty string.
    def test_return_none_when_input_response_is_empty_string(self):
        response = ""

        actual_code, file_extension = get_code_from_model_response(response)

        assert actual_code is None
        assert file_extension is None
