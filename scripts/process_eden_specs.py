import os
import shutil
from context import process_file
from pathlib import Path


def process_and_save_file(file_path, output_file, target_directory):
    try:
        result = process_file(file_path)
        with open(
            os.path.join(target_directory, output_file), "w", encoding="utf-8"
        ) as f:
            f.write(result)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def main(input_directory: Path, target_directory: Path):
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
    os.makedirs(target_directory, exist_ok=True)

    for file in input_directory.iterdir():
        if file.is_file():
            if file.suffix == ".json" or file.suffix == ".yaml":
                output_file = f"{file.stem}.txt"
                process_and_save_file(file, output_file, target_directory)


if __name__ == "__main__":
    # main("../data/eden/sub-domains", "../data/eden/processed-specs")
    dataFolder = Path(__file__).parent.parent / "data"

    main((dataFolder / "eden" / "sub-domains"), dataFolder / "eden" / "processed-specs")
