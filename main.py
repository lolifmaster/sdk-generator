from sdkgenerator.generate.generate_sdk import generate_sdk
from pathlib import Path


def main():
    api_spec = Path("data/specification-batch/_pdfgeneratorapi.com_3.1.1_openapi.yaml")

    generate_sdk(api_spec, language="python")


if __name__ == "__main__":
    main()
