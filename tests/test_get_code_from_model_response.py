from utils import get_code_from_model_response


class TestGetCodeFromModelResponse:
    #  Returns the generated code and its file extension when the response contains a single code block.
    def test_extract_code_from_single_block(self):
        response = "Here is some text\n```python\ndef function():\n    print('Hello, World!')\n```\nSome more text"
        expected_code = "def function():\n    print('Hello, World!')"

        actual_code, file_extension = get_code_from_model_response(response)
        assert actual_code == expected_code
        assert file_extension == ".py"

    #  Returns the generated code and its file extension when the response contains multiple code blocks.
    def test_extract_code_from_multiple_blocks(self):
        response = "Here is some text\n```python\ndef function():\n    print('Hello, World!')\n```\nSome more text\n```javascript\nfunction hello() {\n    console.log('Hello, World!');\n}\n```"
        expected_code = "def function():\n    print('Hello, World!')"

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

    #  Returns an empty string and '.txt' when the input response contains a code block with no code and no language identifier.
    def test_return_empty_string_and_when_no_code(self):
        response = "Here is some text\n```python\n```"
        expected_code = ""

        actual_code, file_extension = get_code_from_model_response(response)
        assert actual_code == expected_code
        assert file_extension == ".py"
