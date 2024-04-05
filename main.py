from sdkgenerator.generate import generate_sdk, generate_test
from pathlib import Path


def main():
    eden_repo_path = Path(__file__).parent / "data" / "eden" / "sub-domains"
    for file in eden_repo_path.iterdir():
        if not file.is_file():
            print(f"Skipping {file.stem} because it is not a file.")
            continue

        if not (file.suffix == ".json" or file.suffix == ".yaml"):
            print(f"Skipping {file.stem} because it is not a JSON or YAML file.")
            continue

        try:
            sdk_file_path = generate_sdk(file, language="python")
            # test_file_path = generate_test(sdk_file_path)
            # if test_file_path:
            #     print(f"Generated both SDK and Test for {file.stem}")
            # else:
            #     print(f"Failed to generate Test for {file.stem}")
        except Exception as e:
            print(f"Failed to generate SDK and Test for {file.stem}: {e}")


if __name__ == "__main__":
    main()
