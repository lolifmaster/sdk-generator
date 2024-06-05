import gradio as gr
import time
from sdkgenerator.manifier import get_api_data
from pathlib import Path
from gradio.utils import NamedString


def generate_sdk(message):
    for step in range(5):
        time.sleep(1)
        yield f"step {step + 1} of 5"
    yield f"done! {message}"


# Define a function to process the OpenAPI specification file
def process_openapi_file(openapi_file_name: NamedString, user_input: str):
    UPLOAD_DIR = Path(__file__).parent / "GUI_uploads"
    UPLOAD_DIR.mkdir(exist_ok=True)

    GENERATED_SDK_DIR = Path(__file__).parent / "GUI_generated_sdks"
    GENERATED_SDK_DIR.mkdir(exist_ok=True)

    uploaded_file_path = UPLOAD_DIR / Path(openapi_file_name.name).name

    api_specs, types = get_api_data(uploaded_file_path)

    generated_sdk_path = GENERATED_SDK_DIR / f"{uploaded_file_path.stem}.txt"
    generated_sdk_path.write_text(api_specs)

    return api_specs, f"SDK generated at {user_input}"


# Create the Gradio interface
interface = gr.Interface(
    fn=process_openapi_file,
    inputs=["file", "text"],
    outputs=["text", "text"],
    title="OpenAPI Processor",
    description="Upload an OpenAPI specification file to process it.",  # Optional: Description
)

# Launch the interface
if __name__ == "__main__":
    interface.launch()
