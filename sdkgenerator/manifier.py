import json
from datetime import datetime, date
import re
import string
from pathlib import Path
import yaml

from sdkgenerator.utils import validate_openapi_spec


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
    "array": "array",
    "integer": "int",
    "default": "def",
    "required": "req",
    "minLength": "minLen",
    "maxLength": "maxLen",
    "minimum": "min",
    "maximum": "max",
}

types_keys_to_remove = {
    "description",
    "example",
    "title",
    "pattern",
}

security_keys_to_remove = {
    "description",
    "example",
    "title",
    "pattern",
}

methods_to_handle = {"get", "post", "patch", "delete", "put"}

security_types_to_handle = {
    "http",
    "apiKey",
    "openIdConnect",
}


def resolve_refs_types(
    openapi_spec, ref, types, keys_to_remove=None, resolving_refs=None
):
    if keys_to_remove is None:
        keys_to_remove = types_keys_to_remove

    if resolving_refs is None:
        resolving_refs = set()

    if isinstance(ref, dict):
        new_ref = {}
        for key, value in ref.items():
            if key == "$ref":
                ref_name = value.split("/")[-1]
                if ref_name in types:
                    return ref_name

                # Check if this reference is currently being resolved
                if ref_name in resolving_refs:
                    return ref_name

                resolving_refs.add(ref_name)

                ref_path = value.split("/")[1:]
                ref_object = openapi_spec
                for p in ref_path:
                    ref_object = ref_object.get(p, {})

                # Recursively resolve references inside the ref_object
                ref_object = resolve_refs_types(
                    openapi_spec, ref_object, types, keys_to_remove, resolving_refs
                )

                # Add the resolved object to the types dictionary
                types[ref_name] = ref_object

                resolving_refs.remove(ref_name)

                return ref_name  # Return the ref_name here instead of new_ref

            elif key not in keys_to_remove:
                new_ref[key] = resolve_refs_types(
                    openapi_spec, value, types, keys_to_remove, resolving_refs
                )

        return new_ref

    elif isinstance(ref, list):
        # Recursively search in lists
        return [
            resolve_refs_types(
                openapi_spec, item, types, keys_to_remove, resolving_refs
            )
            for item in ref
        ]

    else:
        # Base case: return the endpoint as is if it's neither a dictionary nor a list
        return ref


def resolve_refs_request_body(openapi_spec, ref) -> dict:
    ref_path = ref.split("/")[1:]
    ref_object = openapi_spec
    for p in ref_path:
        ref_object = ref_object.get(p, {})

    return ref_object


def populate_keys(endpoint, path, openapi_spec):
    # Gets the main keys from the specs
    extracted_endpoint_data = {
        "path": path,
        "operationId": endpoint.get("operationId"),
    }

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
        elif request_body and "$ref" in request_body:
            reqBody = (
                resolve_refs_request_body(openapi_spec, request_body["$ref"])
                .get("content", {})
                .get("application/json")
            )
        else:
            reqBody = None

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
    stack = [(endpoint, [])]

    while stack:
        current_data, parent_keys = stack.pop()

        if isinstance(current_data, dict):
            for k in list(current_data.keys()):
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
                if k in current_data and isinstance(current_data[k], (dict, list)):
                    stack.append((current_data[k], parent_keys + [k]))

        elif isinstance(current_data, list):
            for item in current_data:
                if isinstance(item, (dict, list)):
                    stack.append((item, parent_keys + ["list"]))

    return endpoint


def flatten(endpoint) -> dict:
    if not isinstance(endpoint, dict):
        return endpoint

    flattened_dict = {}

    for key, value in endpoint.items():
        if isinstance(value, dict):
            # Keep unwrapping single-key dictionaries
            while isinstance(value, dict) and len(value) == 1:
                key, value = next(iter(value.items()))
            # Recursively flatten the resulting value
            flattened_dict[key] = flatten(value)
        else:
            # If the value is not a dictionary, keep it as is
            flattened_dict[key] = value

    return flattened_dict


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
                if key == 'ref':
                    formatted_text_parts.append(f"{key}: #{value.split('/')[-1]}")
                else:
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
    types = {}
    defined_security_schemes = spec.get("components", {}).get("securitySchemes", {})
    security_schemes = {}
    security: list[dict[str, list]] = spec.get("security", [])
    api_security_scopes = {}

    if defined_security_schemes:
        for scheme_name, scheme in defined_security_schemes.items():
            if scheme["type"] in security_types_to_handle:
                current_security = {
                    key: value
                    for key, value in scheme.items()
                    if key not in security_keys_to_remove
                }
                current_security = abbreviate(current_security, key_abbreviations)
                current_security = flatten(current_security)
                security_schemes[scheme_name] = current_security

    if security:
        for item in security:
            for scheme, scopes in item.items():
                api_security_scopes[scheme] = scopes

    endpoints_with_metadata = []
    for path, methods in spec["paths"].items():
        for method, endpoint in methods.items():
            if method not in methods_to_handle or (
                endpoint.get("deprecated", False) and not keys_to_keep["deprecated"]
            ):
                continue

            # Populate output list with desired keys
            extracted_endpoint_data = populate_keys(endpoint, path, spec)

            # Get types from schemas
            if keys_to_keep["schemas"]:
                if request_body := extracted_endpoint_data.get("requestBody"):
                    resolve_refs_types(spec, request_body, types)

                if parameters := extracted_endpoint_data.get("parameters"):
                    resolve_refs_types(spec, parameters, types)

                if types:
                    types = abbreviate(types, types_key_abbreviations)

            # If key == None or key == ''
            extracted_endpoint_data = remove_empty_keys(extracted_endpoint_data)

            # Remove unwanted keys
            extracted_endpoint_data = remove_unnecessary_keys(extracted_endpoint_data)

            # Flattens to remove nested objects where the dict has only one key
            extracted_endpoint_data = flatten(extracted_endpoint_data)

            # Abbreviate keys
            extracted_endpoint_data = abbreviate(
                extracted_endpoint_data, key_abbreviations
            )

            tags = endpoint.get("tags")
            if tags is None:
                tags = ["default"]
            else:
                tags = [tag for tag in tags]

            operation_id = endpoint.get("operationId", "")

            # For each tag, add the finalized endpoint to the corresponding list in the dictionary
            # for tag in tags:
            #     endpoints_by_tag[tag].append(extracted_endpoint_data)
            #
            #     operation_id = endpoint.get("operationId", "")
            #
            #     content_string = write_dict_to_text(extracted_endpoint_data)
            #
            #     metadata = {
            #         "tag": tag,
            #         "operation_id": operation_id,
            #         "server_url": f"{server_url}{path}",
            #     }
            #     endpoint_dict = {"metadata": metadata, "content": content_string}
            #
            #     endpoints_by_tag_metadata[tag].append(endpoint_dict)

            content_string = write_dict_to_text(extracted_endpoint_data)

            metadata = {
                "security": endpoint.get("security"),
                "method": method,
                "tags": tags,
                "operation_id": operation_id,
            }
            endpoint_dict = {"metadata": metadata, "content": content_string}

            endpoints_with_metadata.append(endpoint_dict)

    return (
        endpoints_with_metadata,
        server_url,
        types,
        api_security_scopes,
        security_schemes,
    )


def extract_information(spec):
    (
        endpoints_with_metadata,
        server_url,
        types,
        api_security_scopes,
        security_schemes,
    ) = minify(spec)
    output_string = f"##IMPORTANT: base_url:{server_url}\n---\n"
    # for tag, endpoints_with_tag in endpoints_by_tag_metadata.items():
    #     # If we're adding tag descriptions, and they exist they're added here.
    #     tag_description = tag_summary_dict_output.get(tag)
    #     if keys_to_keep["tag_descriptions"] and tag_description:
    #         tag_description = write_dict_to_text(tag_summary_dict_output.get(tag))
    #         tag_string = f"{tag}! {tag_description}!\n"
    #     else:
    #         tag_string = f"{tag}!\n"
    #
    #     tag_string += "---\n"
    #
    #     for endpoint in endpoints_with_tag:
    #         # operation_id = endpoint.get("metadata", "").get("operation_id", "")
    #         # tag_string += f"{operation_id}!"
    #         tag_string += f"{endpoint.get('content')}\n"
    #         tag_string += "---\n"
    #
    #     output_string += f"{tag_string}\n"

    if security_schemes:
        output_string += f"##SECURITY SCHEMES\n"
        for scheme_name, schema_object in security_schemes.items():
            output_string += f"-{scheme_name}\n"
            for key, value in schema_object.items():
                output_string += f"{key}: {value}\n"

    if api_security_scopes:
        output_string += f"---\n##SECURITY SCOPES\n"
        for scheme, scopes in api_security_scopes.items():
            output_string += f"{scheme}: {scopes}\n"

    output_string += f"---\n##ENDPOINTS\n---\n"

    for endpoint in endpoints_with_metadata:
        metadata = endpoint.get("metadata")
        content = endpoint.get("content")

        output_string += f"-method:{metadata.get('method')}\n"
        security = metadata.get("security")
        if security:
            output_string += f"-security\n"
            for schema in security:
                for name, scopes in schema.items():
                    output_string += f"{name}: {scopes}\n"
        output_string += f"{content}\n---\n"

    return output_string, types


def load_file(file_path: Path | str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        if file_path.suffix == ".json":
            return json.load(file)
        elif file_path.suffix in {".yaml", ".yml"}:
            return yaml.safe_load(file)
        else:
            raise ValueError(f"Unsupported file format for {file_path}")


def process_file(spec: dict) -> tuple[str, dict]:
    """
    Process the OpenAPI spec file.

    :arg spec: The OpenAPI spec as a dictionary.

    :return tuple: The processed OpenAPI spec as a string, and the types as a dict.
    """
    return extract_information(spec)


def get_api_data(file_path: Path) -> tuple[str, dict]:
    """
    Load, validate and process the OpenAPI spec file.

    Args:
    file_path: The file path to the OpenAPI spec.

    Returns:
        tuple[str, str]: The OpenAPI spec as a string, and the types as a string.

    """
    file = load_file(file_path)
    validate_openapi_spec(file)
    api_spec, types_json = process_file(file)

    return api_spec, types_json
