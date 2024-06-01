from pathlib import Path

from sdkgenerator.manifier import process_file


def get_api_data(file_path: Path) -> tuple[str, dict]:
    """
    Load, validate and process the OpenAPI spec file.

    Args:
    file_path: The file path to the OpenAPI spec.

    Returns:
        tuple[str, str]: The OpenAPI spec as a string, and the types as a string.

    """
    api_spec, types_json = process_file(file_path)

    return api_spec, types_json
