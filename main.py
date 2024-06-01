from sdkgenerator.generate import generate_sdk
from pathlib import Path
import traceback

# Mock user rules
RULES = [
    "Sdk must use the requests library to make the requests.",
    "Sdk must be a class with methods for each endpoint in the API, choose a name for the method based on what it does.",
    "The requests must handle authenticated request with a _make_authenticated_request.",
    "Use json for the request body.",
    "The methods must return The requests library Response object.",
]


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
            generate_sdk(file, user_rules=RULES, language="python")
        except Exception as e:
            print(f"Failed to generate SDK for {file.stem}: {e}")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()
