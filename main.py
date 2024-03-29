from sdkgenerator.generate.generate_sdk import generate_sdk
from pathlib import Path


def main():
    eden_repo_path = Path(__file__).parent / "data" / "eden" / "sub-domains"
    for file in eden_repo_path.iterdir():
        if file.is_file():
            if file.suffix == ".json" or file.suffix == ".yaml":
                generate_sdk(file, language="python")


if __name__ == "__main__":
    main()
