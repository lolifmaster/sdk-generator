from sdkgenerator.types import Language, Template, TemplateWithoutTypes

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


            {rules}

            ##IMPORTANT:
            - Use the requests library: All HTTP requests within the SDK must be made using the 'requests' library.
            - Class structure: The SDK must be a class, with each method representing an endpoint in the API. Choose method names that reflect the action or resource they interact with.
            - Authenticated requests: Implement a method '_make_authenticated_request' to handle authenticated requests.
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
            {rules}

            ##IMPORTANT:
            - Use the requests library: All HTTP requests within the SDK must be made using the 'requests' library.
            - Class structure: The SDK must be a class, with each method representing an endpoint in the API. Choose method names that reflect the action or resource they interact with.
            - Authenticated requests: Implement a method '_make_authenticated_request' to handle authenticated requests.
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

            {rules}

            ##IMPORTANT:
            - I will use this feedback to improve the code.
            - Ensure all issues are addressed.
            - Ensure all suggestions are implemented.''',
        "final_code": '''with the old initial code and the feedback, write the final code, here's the feedback:
            """{feedback}"""
            
            {rules}

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
