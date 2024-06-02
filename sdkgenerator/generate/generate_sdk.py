import json
import os
from pathlib import Path
from dotenv import load_dotenv

from sdkgenerator.manifier import get_api_data
from sdkgenerator.utils import (
    is_all_steps_within_limit,
    split_openapi_spec,
)
from sdkgenerator.types import Language
from sdkgenerator.constants import (
    GENERATED_SDK_DIR,
)
from sdkgenerator.generators import (
    generate_types,
    generate_initial_code,
    feedback_on_generated_code,
    generate_final_code,
    generate_initial_code_without_types,
    feedback_on_generated_code_without_types,
    generate_final_code_without_types,
)

load_dotenv()


def pipeline_with_types(
    api_spec: str,
    types_json: dict,
    *,
    user_rules: list[str],
    sdk_module: Path,
    language: Language = "python",
    api_spec_name: str,
):
    types_code, file_extension = generate_types(str(types_json), language=language)

    # create the types file
    types_file = sdk_module / f"types{file_extension}"
    types_file.write_text(types_code)

    rules = "#RULES\n" + "\n".join(user_rules) if user_rules else ""

    initial_code, history = generate_initial_code(
        api_spec,
        types=types_code,
        sdk_name=api_spec_name,
        rules=rules,
        language=language,
    )

    history = history[:-1]

    feedback = feedback_on_generated_code(
        initial_code, history, sdk_name=api_spec_name, rules=rules, language=language
    )

    final_code_prev_history = [
        {"role": "user", "message": "Write me an sdk for my api"},
        {
            "role": "assistant",
            "message": f"Here is the generated code for the sdk: '''{initial_code}'''",
        },
    ]

    code, file_extension = generate_final_code(
        feedback,
        final_code_prev_history,
        rules=rules,
        sdk_name=api_spec_name,
        language=language,
    )

    return code, file_extension


def pipeline_without_types(
    api_spec: str,
    *,
    api_spec_name: str,
    user_rules: list[str],
    language: Language = "python",
):
    rules = "#RULES\n" + "\n".join(user_rules) if user_rules else ""

    initial_code = generate_initial_code_without_types(
        api_spec, language=language, sdk_name=api_spec_name, rules=rules
    )

    feedback_prev_history = [
        {
            "role": "user",
            "message": f"I have this specification for an API spec: '''{api_spec}'''",
        },
        {
            "role": "assistant",
            "message": f"Okay, let me generate the code for the sdk",
        },
    ]

    # we can add user rules here
    feedback = feedback_on_generated_code_without_types(
        initial_code,
        feedback_prev_history,
        language=language,
        sdk_name=api_spec_name,
        rules=rules,
    )

    final_code_prev_history = [
        {"role": "user", "message": "Write me an sdk for my api"},
        {
            "role": "assistant",
            "message": f"Here is the generated code for the sdk: '''{initial_code}'''",
        },
    ]

    code, file_extension = generate_final_code_without_types(
        feedback,
        final_code_prev_history,
        language=language,
        sdk_name=api_spec_name,
        rules=rules,
    )

    return code, file_extension


def generate_sdk(
    file_path: Path,
    /,
    *,
    output_dir: Path = GENERATED_SDK_DIR,
    language: Language = "python",
    user_rules: list[str],
) -> Path:
    """
    Generate full SDK for the API spec and return the path to the generated SDK file.
    """
    api_spec, types_json = get_api_data(file_path)

    api_spec_name = file_path.stem

    # create a module for the generated sdk
    sdk_module = output_dir / api_spec_name
    sdk_module.mkdir(exist_ok=True)

    if not is_all_steps_within_limit(
        api_spec,
        types_json,
        user_rules=user_rules,
        lang=language,
    ):
        if os.environ.get("ENV") == "development":
            raise Exception("The api specs are too long, skipping in for training...")
        else:
            print("The api specs are too long, splitting the sdk into submodules...")
            sub_docs_dir = sdk_module / "sub_docs"
            sub_docs_dir.mkdir(exist_ok=True)
            split_openapi_spec(file_path, output_dir_path=sub_docs_dir)

            # sdks directory
            sub_sdks_dir = sdk_module / "sdks"
            sub_sdks_dir.mkdir(exist_ok=True)

            for sub_spec in sub_docs_dir.iterdir():
                print(f"Generating SDK for {sub_spec.stem}...")
                generate_sdk(
                    sub_spec,
                    output_dir=sub_sdks_dir,
                    user_rules=user_rules,
                    language=language,
                )

            return sub_docs_dir

    # save the api spec and types to a file
    if os.environ.get("ENV") == "development":
        api_spec_file = output_dir / api_spec_name
        api_spec_file.mkdir(exist_ok=True)
        api_spec_file = api_spec_file / "api_spec.txt"
        api_spec_file.write_text(api_spec)

        types_file = output_dir / api_spec_name
        types_file = types_file / "types.json"
        types_file.write_text(json.dumps(types_json, indent=4))

    if types_json:
        code, file_extension = pipeline_with_types(
            api_spec,
            types_json,
            sdk_module=sdk_module,
            api_spec_name=api_spec_name,
            user_rules=user_rules,
            language=language,
        )
    else:
        code, file_extension = pipeline_without_types(
            api_spec,
            api_spec_name=api_spec_name,
            user_rules=user_rules,
            language=language,
        )

    # create the sdk file
    sdk_output_file = sdk_module / f"{api_spec_name}{file_extension}"
    sdk_output_file.write_text(code)

    return sdk_output_file
