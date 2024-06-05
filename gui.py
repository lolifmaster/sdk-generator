from pathlib import Path
import zipfile
import gradio as gr
from gradio.utils import NamedString
from sdkgenerator.generate import generate_sdk
from sdkgenerator.types import Language


def process_openapi_file(openapi_file: NamedString, user_input: str, language: Language = "python"):
    UPLOAD_DIR = Path(__file__).parent / "GUI_uploads"
    UPLOAD_DIR.mkdir(exist_ok=True)

    COMPRESSED_SDKS = Path(__file__).parent / "compressed_sdks"
    COMPRESSED_SDKS.mkdir(exist_ok=True)
    with open(openapi_file.name, "rb") as file:
        openapi_content = file.read()

    uploaded_file_path = UPLOAD_DIR / Path(openapi_file.name).name
    uploaded_file_path.write_text(openapi_content.decode("utf-8"))

    sdk_folder, sdk_output_file, types_file = generate_sdk(
        uploaded_file_path, user_rules=user_input, language=language
    )

    sdk_path = COMPRESSED_SDKS / f"{sdk_folder.stem}_sdk.zip"
    zipped_sdk = zipfile.ZipFile(sdk_path, "w")

    for file in sdk_folder.rglob("*"):
        zipped_sdk.write(file, file.relative_to(sdk_folder))

    if not sdk_folder.is_dir():
        raise Exception("No sdk returned")

    zipped_sdk = zipfile.ZipFile(UPLOAD_DIR / "sdk.zip", "w")

    for file in sdk_folder.rglob("*"):
        zipped_sdk.write(file, file.relative_to(sdk_folder))

    sdk_code = sdk_output_file.read_text()

    if types_file and types_file.is_file():
        types_code = types_file.read_text()

        return sdk_code, types_code, str(sdk_path.absolute())

    return sdk_code, "No shared types generated.", str(sdk_path.absolute())


# Create the Gradio interface
interface = gr.Interface(
    fn=process_openapi_file,
    inputs=["file", "text", gr.Dropdown(
        label="Language", choices=["python"], value='python'
    )],
    outputs=[
        gr.TextArea(
            label="SDK Code",
        )
        ,
        gr.TextArea(
            label="Shared Types"
        )
        ,
        gr.File(
            label="Generated sdk zip file"
        )
    ],
    title="SDK Generator",
    description="Generate SDKs from OpenAPI specifications.",
)

# Launch the interface
if __name__ == "__main__":
    interface.launch()
