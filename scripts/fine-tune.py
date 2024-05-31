import json
import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from openai.types import FileObject
from pathlib import Path
from pprint import pprint
from prepare_finetune_data import generate_finetune_data

load_dotenv()

# Define the path to store files
file_metadata_path = (
    Path(__file__).parent.parent / "data" / "fine-tuning" / "uploaded_file.json"
)
fine_tune_job_path = (
    Path(__file__).parent.parent / "data" / "fine-tuning" / "fine_tune_job.json"
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_fine_tune_file():
    """Generates and uploads fine-tuning data to OpenAI."""
    print("Creating fine-tuning data")

    train_file = generate_finetune_data()

    print(f"Uploading file {train_file} to OpenAI for fine-tuning")

    with open(train_file, "rb") as f:
        response: FileObject = client.files.create(file=f, purpose="fine-tune")

    file_metadata = response.json()

    pprint(f"File uploaded. File metadata: {file_metadata}")

    file_metadata_path.write_text(json.dumps(file_metadata, indent=4))


def create_fine_tune_model():
    """Creates a fine-tuning job using the uploaded file."""
    file_metadata = json.loads(file_metadata_path.read_text())
    try:
        training_file_id = file_metadata["id"]
    except KeyError:
        raise ValueError("File metadata does not contain the file ID.")

    response = client.fine_tuning.jobs.create(
        training_file=training_file_id,
        model="gpt-3.5-turbo-0125",
    )

    job_metadata = response.json()

    pprint(f'Fine-tuning job created. Job metadata: {job_metadata}')
    fine_tune_job_path.write_text(json.dumps(job_metadata, indent=4))


def main():
    parser = argparse.ArgumentParser(description="Fine-tuning script for OpenAI models")
    parser.add_argument(
        "--new",
        action="store_true",
        help="Generate and upload new fine-tuning data, then start fine-tuning",
    )
    parser.add_argument(
        "--train",
        action="store_true",
        help="Start fine-tuning using existing fine-tuning data",
    )

    args = parser.parse_args()

    if args.new and args.train:
        parser.error("Arguments --new and --train are mutually exclusive.")

    if args.new:
        create_fine_tune_file()
        create_fine_tune_model()
    elif args.train:
        # Check if the file metadata exists
        if not file_metadata_path.exists():
            parser.error(
                "File metadata does not exist. Please run the script with --new to generate fine-tuning data."
            )
        create_fine_tune_model()
    else:
        parser.error("One of --new or --train must be specified.")


if __name__ == "__main__":
    main()
