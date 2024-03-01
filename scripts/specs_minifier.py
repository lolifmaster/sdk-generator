import os
import json
import yaml
from collections import defaultdict
import shutil
from datetime import datetime, date
from tqdm.contrib.concurrent import process_map
import re
import string


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
    # Keys to exclude
    "enums": False,
    "nested_descriptions": False,
    "examples": False,
    "tag_descriptions": True,
    "deprecated": False,
}

key_abbreviations = {
    "operationId": "opid",
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
    "integer": "int",
    "default": "def",
    "required": "req",

}

methods_to_handle = {"get", "post", "patch", "delete", "put"}


def load_spec(file_path, filename):
    with open(file_path, 'r', encoding='utf-8') as file:
        if filename.endswith('.yaml'):
            return yaml.safe_load(file)
        elif filename.endswith('.json'):
            return json.load(file)


def resolve_refs(openapi_spec, endpoint):
    if isinstance(endpoint, dict):
        new_endpoint = {}
        for key, value in endpoint.items():
            if key == '$ref':
                ref_path = value.split('/')[1:]
                ref_object = openapi_spec
                for p in ref_path:
                    ref_object = ref_object.get(p, {})

                # Recursively resolve references inside the ref_object
                ref_object = resolve_refs(openapi_spec, ref_object)

                # Use the last part of the reference path as key
                new_key = ref_path[-1]
                new_endpoint[new_key] = ref_object
            else:
                # Recursively search in nested dictionaries
                new_endpoint[key] = resolve_refs(openapi_spec, value)
        return new_endpoint

    elif isinstance(endpoint, list):
        # Recursively search in lists
        return [resolve_refs(openapi_spec, item) for item in endpoint]

    else:
        # Base case: return the endpoint as is if it's neither a dictionary nor a list
        return endpoint


def populate_keys(endpoint, path):
    # Gets the main keys from the specs
    extracted_endpoint_data = {'path': path, 'operationId': endpoint.get('operationId')}

    if keys_to_keep["parameters"]:
        extracted_endpoint_data['parameters'] = endpoint.get('parameters')

    if keys_to_keep["endpoint_summaries"]:
        extracted_endpoint_data['summary'] = endpoint.get('summary')

    if keys_to_keep["endpoint_descriptions"]:
        extracted_endpoint_data['description'] = endpoint.get('description')

    if keys_to_keep["request_bodies"]:
        extracted_endpoint_data['requestBody'] = endpoint.get('requestBody')

    if keys_to_keep["good_responses"] or keys_to_keep["bad_responses"]:
        extracted_endpoint_data['responses'] = {}

    if keys_to_keep["good_responses"]:
        if 'responses' in endpoint and '200' in endpoint['responses']:
            extracted_endpoint_data['responses']['200'] = endpoint['responses'].get('200')

    if keys_to_keep["bad_responses"]:
        if 'responses' in endpoint:
            # Loop through all the responses
            for status_code, response in endpoint['responses'].items():
                # Check if status_code starts with '4' or '5' (4xx or 5xx)
                if status_code.startswith('4') or status_code.startswith('5') or 'def' in status_code:
                    # Extract the schema or other relevant information from the response
                    bad_response_content = response
                    if bad_response_content is not None:
                        extracted_endpoint_data['responses'][f'{status_code}'] = bad_response_content

    return extracted_endpoint_data


def remove_empty_keys(endpoint):
    if isinstance(endpoint, dict):
        # Create a new dictionary without empty keys
        new_endpoint = {}
        for key, value in endpoint.items():
            if value is not None and value != '':
                # Recursively call the function for nested dictionaries
                cleaned_value = remove_empty_keys(value)
                new_endpoint[key] = cleaned_value
        return new_endpoint
    elif isinstance(endpoint, list):
        # Recursively call the function for elements in a list
        return [remove_empty_keys(item) for item in endpoint]
    else:
        # Return the endpoint if it's not a dictionary or a list
        return endpoint


def remove_unnecessary_keys(endpoint):
    # Stack for storing references to nested dictionaries/lists and their parent keys
    stack = [(endpoint, [])]

    # Continue until there is no more data to process
    while stack:
        current_data, parent_keys = stack.pop()

        # If current_data is a dictionary
        if isinstance(current_data, dict):
            # Iterate over a copy of the keys, as we may modify the dictionary during iteration
            for k in list(current_data.keys()):
                # Check if this key should be removed based on settings and context
                if k == 'example' and not keys_to_keep["examples"]:
                    del current_data[k]
                if k == 'enum' and not keys_to_keep["enums"]:
                    del current_data[k]
                elif k == 'description' and len(parent_keys) > 0 and not keys_to_keep["nested_descriptions"]:
                    del current_data[k]
                # Otherwise, if the value is a dictionary or a list, add it to the stack for further processing
                # Check if the key still exists before accessing it
                if k in current_data and isinstance(current_data[k], (dict, list)):
                    stack.append((current_data[k], parent_keys + [k]))

        # If current_data is a list
        elif isinstance(current_data, list):
            # Add each item to the stack for further processing
            for item in current_data:
                if isinstance(item, (dict, list)):
                    stack.append((item, parent_keys + ['list']))

    return endpoint


def flatten_endpoint(endpoint):
    if not isinstance(endpoint, dict):
        return endpoint

    flattened_endpoint = {}

    # Define the set of keys to keep without unwrapping
    keep_keys = {"responses", "default", "200"}

    for key, value in endpoint.items():
        if isinstance(value, dict):
            # Check if the dictionary has any of the keys that need to be kept
            if key in keep_keys:
                # Keep the inner dictionaries but under the current key
                flattened_endpoint[key] = flatten_endpoint(value)
            else:
                # Keep unwrapping single-key dictionaries
                while isinstance(value, dict) and len(value) == 1:
                    key, value = next(iter(value.items()))
                # Recursively flatten the resulting value
                flattened_endpoint[key] = flatten_endpoint(value)
        else:
            # If the value is not a dictionary, keep it as is
            flattened_endpoint[key] = value

    return flattened_endpoint


def abbreviate(data, abbreviations):
    if isinstance(data, dict):
        # Lowercase keys, apply abbreviations and recursively process values
        return {
            abbreviations.get(key, key): abbreviate(abbreviations.get(str(value), value),
                                                                    abbreviations)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        # Recursively process list items
        return [abbreviate(item, abbreviations) for item in data]
    elif isinstance(data, str):
        # If the data is a string, convert it to lowercase and replace if abbreviation exists
        return abbreviations.get(data, data)
    else:
        # Return data unchanged if it's not a dict, list or string
        return data


def write_dict_to_text(data):
    def remove_html_tags_and_punctuation(input_str):
        # Strip HTML tags
        no_html_str = re.sub('<.*?>', '', input_str)
        # Define the characters that should be considered as punctuation
        modified_punctuation = set(string.punctuation) - {'/', '#'}
        # Remove punctuation characters
        return ''.join(ch for ch in no_html_str if ch not in modified_punctuation).strip()

    # List to accumulate the formatted text parts
    formatted_text_parts = []

    # Check if data is a dictionary
    if isinstance(data, dict):
        # Iterate over items in the dictionary
        for key, value in data.items():
            # Remove HTML tags and punctuation from key
            key = remove_html_tags_and_punctuation(key)

            # Depending on the data type, write the content
            if isinstance(value, (dict, list)):
                # Append the key followed by its sub-elements
                formatted_text_parts.append(key)
                formatted_text_parts.append(write_dict_to_text(value))
            else:
                # Remove HTML tags and punctuation from value
                value = remove_html_tags_and_punctuation(str(value))
                # Append the key-value pair
                formatted_text_parts.append(f"{key}: {value}")
    # Check if data is a list
    elif isinstance(data, list):
        # Append each element in the list
        for item in data:
            formatted_text_parts.append(write_dict_to_text(item))
    # If data is a string or other type
    else:
        # Remove HTML tags and punctuation from data
        data = remove_html_tags_and_punctuation(str(data))
        # Append the data directly
        formatted_text_parts.append(data)

    # Join the formatted text parts with a single newline character
    # but filter out any empty strings before joining
    return '\n'.join(filter(lambda x: x.strip(), formatted_text_parts))


def minify(spec):
    server_url = spec['servers'][0]['url']
    tag_summary_dict = {}

    if tags := spec.get('tags'):
        for tag in tags:
            # Extract name and description
            name = tag.get("name")
            description = tag.get("description")
            # Add to the dictionary
            if name and description:
                tag_summary_dict[name] = description

    # Dictionary with each unique tag as a key, and the value is a list of finalized endpoints with that tag
    endpoints_by_tag = defaultdict(list)
    endpoints_by_tag_metadata = defaultdict(list)
    for path, methods in spec['paths'].items():
        for method, endpoint in methods.items():
            if method not in methods_to_handle or (
                    endpoint.get('deprecated', False) and not keys_to_keep["deprecated"]):
                continue
            # Adds schema to each endpoint
            if keys_to_keep["schemas"]:
                extracted_endpoint_data = resolve_refs(spec, endpoint)
            else:
                extracted_endpoint_data = endpoint
            # Populate output list with desired keys
            extracted_endpoint_data = populate_keys(extracted_endpoint_data, path)
            # If key == None or key == ''
            extracted_endpoint_data = remove_empty_keys(extracted_endpoint_data)

            # Remove unwanted keys
            extracted_endpoint_data = remove_unnecessary_keys(extracted_endpoint_data)

            # Flattens to remove nested objects where the dict has only one key
            extracted_endpoint_data = flatten_endpoint(extracted_endpoint_data)

            # Abbreviate keys
            extracted_endpoint_data = abbreviate(extracted_endpoint_data, key_abbreviations)

            tags = endpoint.get('tags')
            if tags is None:
                tags = ['default']
            else:
                tags = [tag for tag in tags]

            # For each tag, add the finalized endpoint to the corresponding list in the dictionary
            for tag in tags:
                endpoints_by_tag[tag].append(extracted_endpoint_data)

                operation_id = endpoint.get('operationId', '')

                content_string = write_dict_to_text(extracted_endpoint_data)

                metadata = {
                    'tag': tag,
                    'operation_id': operation_id,
                    'server_url': f'{server_url}{path}'
                }
                endpoint_dict = {
                    "metadata": metadata,
                    "content": content_string
                }

                endpoints_by_tag_metadata[tag].append(endpoint_dict)

    # Sort alphabetically by tag name
    sorted_items = sorted(endpoints_by_tag.items())
    endpoints_by_tag = defaultdict(list, sorted_items)
    # Sort alphabetically by tag name
    sorted_items = sorted(endpoints_by_tag_metadata.items())
    endpoints_by_tag_metadata = defaultdict(list, sorted_items)

    # In the case tag_summary_dict is empty or missing tags this adds them here
    for tag in endpoints_by_tag.keys():
        # If the tag is not already in tag_summary_dict, add it with an empty description
        if tag not in tag_summary_dict:
            tag_summary_dict[tag] = ''

    return endpoints_by_tag_metadata, tag_summary_dict


def save_as_txt(spec, target_directory, spec_name):
    output_file_path = os.path.join(target_directory, f'{spec_name}.txt')

    endpoints_by_tag_metadata, tag_summary_dict_output = minify(spec)
    output_string = ''

    for tag, endpoints_with_tag in endpoints_by_tag_metadata.items():
        # If we're adding tag descriptions, and they exist they're added here.
        tag_description = tag_summary_dict_output.get(tag)
        if keys_to_keep["tag_descriptions"] and tag_description:
            tag_description = write_dict_to_text(tag_summary_dict_output.get(tag))
            tag_string = f'{tag}! {tag_description}!!\n'
        else:
            tag_string = f'{tag}!\n'

        for endpoint in endpoints_with_tag:
            operation_id = endpoint.get('metadata', '').get('operation_id', '')
            tag_string += f'{operation_id}!'
            tag_string += endpoint.get('content', '')

        output_string += f'{tag_string}\n'

    # Write sorted info_strings to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(output_string)

    # file_path = os.path.join(target_directory, f'{spec_name}.txt')
    # with open(file_path, 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(minified_spec, indent=2, cls=DateTimeEncoder))


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
    os.makedirs(target_directory)
    tasks = [(os.path.join(input_directory, filename), filename, target_directory) for filename in
             os.listdir(input_directory) if filename.endswith('.yaml') or filename.endswith('.json')]
    process_map(process_file, tasks, max_workers=5)


if __name__ == '__main__':
    main('../data/specification-batch', '../data/simplified-batch-specs')
