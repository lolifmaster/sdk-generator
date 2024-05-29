from sdkgenerator.generate import generate_sdk
from pathlib import Path
import traceback


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
            generate_sdk(file, language="python")
        except Exception as e:
            print(f"Failed to generate SDK for {file.stem}: {e}")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()
