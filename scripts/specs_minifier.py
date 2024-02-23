import os
import json
import yaml
from collections import defaultdict
import shutil

keys_to_keep = {
    # Root level keys to populate
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


def load_specs(input_directory):
    documents = []
    for filename in os.listdir(input_directory):
        if filename.endswith('.yaml') or filename.endswith('.json'):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r') as file:
                if filename.endswith('.yaml'):
                    documents.append(yaml.safe_load(file))
                elif filename.endswith('.json'):
                    documents.append(json.load(file))
    return documents


def minify_and_reformat(specs):
    minified_specs = []
    for spec in specs:
        minified_spec = defaultdict(list)
        for path, methods in spec['paths'].items():
            for method, endpoint in methods.items():
                if method not in methods_to_handle:
                    continue

                if endpoint.get('deprecated', False) and not keys_to_keep["deprecated"]:
                    continue

                minified_endpoint = {key: endpoint[key] for key in
                                     ['operationId', 'parameters', 'summary', 'description', 'requestBody', 'responses']
                                     if key in endpoint}
                minified_spec[path].append(minified_endpoint)
        if tags := spec.get('tags'):
            minified_spec['tags'] = [{tag['name']: tag['description']} for tag in tags if 'name' in tag and 'description' in tag]
        minified_specs.append(minified_spec)
    return minified_specs


def save_as_txt(minified_specs, target_directory):
    os.makedirs(target_directory, exist_ok=True)
    for i, minified_spec in enumerate(minified_specs):
        file_path = os.path.join(target_directory, f'spec_{i}.txt')
        with open(file_path, 'w') as file:
            file.write(json.dumps(minified_spec, indent=2))


def main(input_directory, target_directory):
    # Clear target directory if it exists or create it
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
    else:
        os.makedirs(target_directory)
    specs = load_specs(input_directory)
    minified_specs = minify_and_reformat(specs)
    save_as_txt(minified_specs, target_directory)


# Usage
main('../data/specification-batch', '../data/simplified-specs')
