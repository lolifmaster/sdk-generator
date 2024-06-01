from pathlib import Path
import os
import shutil


def move_files(source_directory: Path | str, target_directory: Path | str):
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith("swagger.yaml"):
                continue  # Work only with OpenAPI specs
            old_file_path = os.path.join(root, file)
            # Replace source_directory from the old file path and replace path separator with underscore
            new_file_name = old_file_path.replace(source_directory, "").replace(
                os.sep, "_"
            )
            new_file_path = os.path.join(target_directory, new_file_name)
            shutil.copy(str(old_file_path), str(new_file_path))


if __name__ == "__main__":
    source = Path(__file__).parent.parent / "data" / "openapi-directory-main" / "APIs"
    target = Path(__file__).parent.parent / "data" / "specifications"

    if not source.exists():
        raise FileNotFoundError(f"Source directory {source} does not exist.")

    # Create the target directory if it does not exist
    target.mkdir(parents=True, exist_ok=True)

    move_files(source, target)
