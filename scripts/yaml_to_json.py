import os
import yaml
import json
from datetime import datetime, date
from typing import override
from tqdm import tqdm


class DateTimeEncoder(json.JSONEncoder):
    @override
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def convert_yaml_to_json(yaml_file, json_file):
    """
    Converts a YAML file to a JSON file.

    Args:
      yaml_file: Path to the YAML file.
      json_file: Path to the output JSON file.
    """
    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, cls=DateTimeEncoder)


def convert_folder(yaml_folder, json_folder):
    """
    Converts all YAML files in a folder to JSON files in another folder.

    Args:
      yaml_folder: Path to the folder containing YAML files.
      json_folder: Path to the folder to store the JSON files.
    """
    os.makedirs(json_folder, exist_ok=True)

    for filename in tqdm(os.listdir(yaml_folder)):
        if filename.endswith(".yaml"):
            yaml_path = os.path.join(yaml_folder, filename)
            json_path = os.path.join(
                json_folder, os.path.splitext(filename)[0] + ".json"
            )
            convert_yaml_to_json(yaml_path, json_path)


input_yaml_folder = "../data/specifications"
output_json_folder = "../data/specifications-json"
convert_folder(input_yaml_folder, output_json_folder)

print("YAML files converted to JSON successfully!")
