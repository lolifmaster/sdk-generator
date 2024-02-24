import os
import json
import yaml
from collections import defaultdict
import shutil
from multiprocessing import Pool
from datetime import datetime, date


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()  # Convert date to string in ISO 8601 format
        else:
            return json.JSONEncoder.default(self, obj)


keys_to_keep = {
    "parameters": True,
    "good_responses": True,
    "bad_responses": False,
    "request_bodies": True,
    "schemas": True,
    "endpoint_descriptions": True,
    "endpoint_summaries": True,
    "enums": False,
    "nested_descriptions": True,
    "examples": False,
    "tag_descriptions": True,
    "deprecated": False,
}

key_abbreviations = {
    "operationId": "opId",
    "parameters": "params",
    "requestBody": "reqBody",
    "properties": "props",
    "schemaName": "schName",
    "description": "desc",
    "summary": "sum",
    "string": "str",
    "number": "num",
    "object": "obj",
    "boolean": "bool",
    "array": "arr",
}

methods_to_handle = {"get", "post", "patch", "delete"}


def load_spec(file_path, filename):
    with open(file_path, 'r', encoding='utf-8') as file:
        if filename.endswith('.yaml'):
            return yaml.safe_load(file)
        elif filename.endswith('.json'):
            return json.load(file)


def minify_and_reformat(spec):
    minified_spec = defaultdict(list)
    if "paths" in spec and type(spec["paths"]) is dict:
        for path, methods in spec['paths'].items():
            methods_items = methods.items()
            for method, endpoint in methods_items:
                if method not in methods_to_handle or (
                        endpoint.get('deprecated', False) and not keys_to_keep["deprecated"]):
                    continue

                minified_endpoint = {key: endpoint.get(key) for key in
                                     ['operationId', 'parameters', 'summary', 'description', 'requestBody', 'responses']
                                     if key in endpoint}
                minified_spec[path].append(minified_endpoint)
    if tags := spec.get('tags'):
        minified_spec['tags'] = [{tag['name']: tag.get('description')} for tag in tags if
                                 'name' in tag and 'description' in tag]
    return minified_spec


def save_as_txt(spec, target_directory, spec_name):
    os.makedirs(target_directory, exist_ok=True)
    minified_spec = minify_and_reformat(spec)
    file_path = os.path.join(target_directory, f'{spec_name}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(minified_spec, indent=2, cls=DateTimeEncoder))


def process_file(args):
    file_path, filename, target_directory = args
    try:
        spec = load_spec(file_path, filename)
        save_as_txt(spec, target_directory, filename)
    except Exception as e:
        print(f'Error processing file {filename}: {e}')


def main(input_directory, target_directory):
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
    else:
        os.makedirs(target_directory)
    with Pool() as p:
        r = p.imap(process_file,
                   [(os.path.join(input_directory, filename), filename, target_directory) for filename in
                    os.listdir(input_directory) if
                    filename.endswith('.yaml') or filename.endswith('.json')], chunksize=10)

        for _ in r:
            pass


if __name__ == '__main__':
    main('../data/specifications', '../data/simplified-specs')
