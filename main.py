from sdkgenerator.generate import generate_sdk
from pathlib import Path
import traceback

# Mock user rules
user_rules = "1. Use the requests library: All HTTP requests within the SDK must be made using the 'requests' library.\n2. Class structure: The SDK must be a class, with each method representing an endpoint in the API. Choose method names that reflect the action or resource they interact with.\n3. Authenticated requests: Implement a method '_make_authenticated_request' to handle authenticated requests.\n4. JSON request body: Use JSON format for the body of all requests.\n5. Return type: All methods must return the 'Response' object from the 'requests' library."


def main():
    training_specs_dir = Path(__file__).parent / "data" / "specification-batch"
    for file in training_specs_dir.iterdir():
        if not file.is_file():
            print(f"Skipping {file.stem} because it is not a file.")
            continue

        if not (file.suffix == ".json" or file.suffix == ".yaml"):
            print(f"Skipping {file.stem} because it is not a JSON or YAML file.")
            continue

        print(f"Generating SDK for {file.stem}...")

        try:
            generate_sdk(file, user_rules=user_rules, language="python")
        except Exception as e:
            print(f"Failed to generate SDK for {file.stem}: {e}")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()
