import os
import shutil
from tqdm.contrib.concurrent import process_map
from context import process_file


def main(input_directory, target_directory):
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
    os.makedirs(target_directory, exist_ok=True)
    tasks = [
        (os.path.join(input_directory, filename), filename, target_directory)
        for filename in os.listdir(input_directory)
        if filename.endswith(".yaml") or filename.endswith(".json")
    ]
    process_map(process_file, tasks, max_workers=5)


if __name__ == "__main__":
    main("../data/eden/sub-domains", "../data/eden/processed-specs")
