import json
import yaml
from collections import defaultdict
from datetime import datetime, date
import re
import string
from pathlib import Path


# TODO: Check if openapi spec is valid, separate types and endpoints into different files


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


keys_to_keep = {
    "parameters": True,
    "good_responses": False,
    "bad_responses": False,
    "request_bodies": True,
    "schemas": True,
    "endpoint_descriptions": False,
    "endpoint_summaries": True,
    "enums": True,
    "nested_descriptions": False,
    "examples": False,
    "tag_descriptions": False,
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

types_key_abbreviations = {
    "properties": "props",
    "schemaName": "schName",
    "description": "desc",
    "string": "str",
    "number": "num",
    "object": "obj",
    "boolean": "bool",
    "array": "arr",
    "integer": "int",
    "default": "def",
    "required": "req",
    "minLength": "minLen",
    "maxLength": "maxLen",
    "minimum": "min",
    "maximum": "max",
}

methods_to_handle = {"get", "post", "patch", "delete", "put"}


def load_spec(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as file:
        if file_path.suffix == ".json":
            return json.load(file)
        elif file_path.suffix in {".yaml", ".yml"}:
            return yaml.safe_load(file)
        else:
            raise ValueError(f"Unsupported file format for {file_path}")


def resolve_refs_types(openapi_spec, endpoint, types):
    if isinstance(endpoint, dict):
        new_endpoint = {}
        for key, value in endpoint.items():
            if key == "$ref":
                ref_name = value.split("/")[-1]
                if ref_name in types:
                    return ref_name

                ref_path = value.split("/")[1:]
                ref_object = openapi_spec
                for p in ref_path:
                    ref_object = ref_object.get(p, {})

                # Recursively resolve references inside the ref_object
                ref_object = resolve_refs_types(openapi_spec, ref_object, types)

                # Add the resolved object to the types dictionary
                new_endpoint[key] = ref_name
                types[ref_name] = ref_object

            elif key not in {"description", "example"}:
                new_endpoint[key] = resolve_refs_types(openapi_spec, value, types)

        return new_endpoint

    elif isinstance(endpoint, list):
        # Recursively search in lists
        return [resolve_refs_types(openapi_spec, item, types) for item in endpoint]

    else:
        # Base case: return the endpoint as is if it's neither a dictionary nor a list
        return endpoint


def populate_keys(endpoint, path):
    # Gets the main keys from the specs
    extracted_endpoint_data = {"path": path, "operationId": endpoint.get("operationId")}

    if keys_to_keep["parameters"]:
        # Extract parameters from the endpoint and specify if they are required
        extracted_params = endpoint.get("parameters")
        if extracted_params:
            for param in extracted_params:
                if "required" in param:
                    param["required"] = str(param["required"])
                else:
                    param["required"] = "False"
            extracted_endpoint_data["parameters"] = extracted_params
    if keys_to_keep["endpoint_summaries"]:
        extracted_endpoint_data["summary"] = endpoint.get("summary")

    if keys_to_keep["endpoint_descriptions"]:
        extracted_endpoint_data["description"] = endpoint.get("description")

    if keys_to_keep["request_bodies"]:
        request_body = endpoint.get("requestBody")
        if request_body and "content" in request_body:
            # Extract the schema of application/json request body
            reqBody = request_body["content"].get("application/json")
            if reqBody and "schema" in reqBody:
                extracted_endpoint_data["requestBody"] = reqBody["schema"]
            else:
                extracted_endpoint_data["requestBody"] = None

    if keys_to_keep["good_responses"] or keys_to_keep["bad_responses"]:
        extracted_endpoint_data["responses"] = {}

    if keys_to_keep["good_responses"]:
        if "responses" in endpoint and "200" in endpoint["responses"]:
            extracted_endpoint_data["responses"]["200"] = endpoint["responses"].get(
                "200"
            )

    if keys_to_keep["bad_responses"]:
        if "responses" in endpoint:
            # Loop through all the responses
            for status_code, response in endpoint["responses"].items():
                # Check if status_code starts with '4' or '5' (4xx or 5xx)
                if (
                    status_code.startswith("4")
                    or status_code.startswith("5")
                    or "def" in status_code
                ):
                    # Extract the schema or other relevant information from the response
                    bad_response_content = response
                    if bad_response_content is not None:
                        extracted_endpoint_data["responses"][
                            f"{status_code}"
                        ] = bad_response_content

    return extracted_endpoint_data


def remove_empty_keys(endpoint):
    if isinstance(endpoint, dict):
        # Create a new dictionary without empty keys
        new_endpoint = {}
        for key, value in endpoint.items():
            if value is not None and value != "":
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
                if k == "example" and not keys_to_keep["examples"]:
                    del current_data[k]
                if k == "enum" and not keys_to_keep["enums"]:
                    del current_data[k]
                elif (
                    k == "description"
                    and len(parent_keys) > 0
                    and not keys_to_keep["nested_descriptions"]
                ):
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
                    stack.append((item, parent_keys + ["list"]))

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
            abbreviations.get(key, key): abbreviate(
                abbreviations.get(str(value), value), abbreviations
            )
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
        no_html_str = re.sub("<.*?>", "", input_str)
        # Define the characters that should be considered as punctuation
        modified_punctuation = set(string.punctuation) - {
            "/",
            "#",
            "_",
            "-",
            "|",
            ".",
            ",",
        }
        # Remove punctuation characters
        return "".join(
            ch for ch in no_html_str if ch not in modified_punctuation
        ).strip()

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
    return "\n".join(filter(lambda x: x.strip(), formatted_text_parts))


def minify(spec):
    server_url = spec["servers"][0]["url"]
    tag_summary_dict = {}
    types = {}

    if tags := spec.get("tags"):
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
    for path, methods in spec["paths"].items():
        for method, endpoint in methods.items():
            if method not in methods_to_handle or (
                endpoint.get("deprecated", False) and not keys_to_keep["deprecated"]
            ):
                continue

            # Populate output list with desired keys
            extracted_endpoint_data = populate_keys(endpoint, path)

            # Get types from schemas
            if keys_to_keep["schemas"] and "requestBody" in extracted_endpoint_data:
                resolve_refs_types(
                    spec, extracted_endpoint_data.get("requestBody"), types
                )
                types = abbreviate(types, types_key_abbreviations)

            # If key == None or key == ''
            extracted_endpoint_data = remove_empty_keys(extracted_endpoint_data)

            # Remove unwanted keys
            extracted_endpoint_data = remove_unnecessary_keys(extracted_endpoint_data)

            # Flattens to remove nested objects where the dict has only one key
            extracted_endpoint_data = flatten_endpoint(extracted_endpoint_data)

            # Abbreviate keys
            extracted_endpoint_data = abbreviate(
                extracted_endpoint_data, key_abbreviations
            )

            tags = endpoint.get("tags")
            if tags is None:
                tags = ["default"]
            else:
                tags = [tag for tag in tags]

            # For each tag, add the finalized endpoint to the corresponding list in the dictionary
            for tag in tags:
                endpoints_by_tag[tag].append(extracted_endpoint_data)

                operation_id = endpoint.get("operationId", "")

                content_string = write_dict_to_text(extracted_endpoint_data)

                metadata = {
                    "tag": tag,
                    "operation_id": operation_id,
                    "server_url": f"{server_url}{path}",
                }
                endpoint_dict = {"metadata": metadata, "content": content_string}

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
            tag_summary_dict[tag] = ""

    return endpoints_by_tag_metadata, tag_summary_dict, server_url, types


def extract_information(spec):
    endpoints_by_tag_metadata, tag_summary_dict_output, server_url, types = minify(spec)
    output_string = f"base_url:{server_url}!\n"
    for tag, endpoints_with_tag in endpoints_by_tag_metadata.items():
        # If we're adding tag descriptions, and they exist they're added here.
        tag_description = tag_summary_dict_output.get(tag)
        if keys_to_keep["tag_descriptions"] and tag_description:
            tag_description = write_dict_to_text(tag_summary_dict_output.get(tag))
            tag_string = f"{tag}! {tag_description}!\n"
        else:
            tag_string = f"{tag}!\n"

        tag_string += "---\n"

        for endpoint in endpoints_with_tag:
            # operation_id = endpoint.get("metadata", "").get("operation_id", "")
            # tag_string += f"{operation_id}!"
            tag_string += f"{endpoint.get('content')}\n"
            tag_string += "---\n"

        output_string += f"{tag_string}\n"

    return output_string, types


def process_file(file_path: Path):
    """
    Process an openapi specification file and save the minified spec to a text file.
    args: Tuple containing the file path (json or yaml), filename and target directory
    return: None
    """

    spec = load_spec(file_path)
    return extract_information(spec)
