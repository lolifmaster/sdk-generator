from sdkgenerator.generate import generate_sdk
from pathlib import Path
import traceback


def main():
    test_repo_path = Path(__file__).parent / "data" / "eden"
    for file in test_repo_path.iterdir():
        if not file.is_file():
            print(f"Skipping {file.stem} because it is not a file.")
            continue

        if not (file.suffix == ".json" or file.suffix == ".yaml"):
            print(f"Skipping {file.stem} because it is not a JSON or YAML file.")
            continue

        try:
            generate_sdk(file, language="python")
        except Exception as e:
            print(f"Failed to generate SDK for {file.stem}: {e}")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()
