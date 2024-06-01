import json
import os
import argparse

import requests
from dotenv import load_dotenv
from openai import OpenAI
from openai.types import FileObject
from pathlib import Path
from pprint import pprint
from prepare_finetune_data import generate_finetune_data

load_dotenv()

file_metadata_path = (
    Path(__file__).parent.parent / "data" / "fine-tuning" / "uploaded_file.json"
)
fine_tune_job_path = (
    Path(__file__).parent.parent / "data" / "fine-tuning" / "fine_tune_job.json"
)

job_details_path = (
    Path(__file__).parent.parent / "data" / "fine-tuning" / "job_details.json"
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

    pprint(f"Fine-tuning job created. Job metadata: {job_metadata}")
    fine_tune_job_path.write_text(json.dumps(job_metadata, indent=4))


def get_fine_tune_job():
    """Retrieves the fine-tuning job metadata."""
    try:
        job_id = json.loads(fine_tune_job_path.read_text())["id"]
    except KeyError:
        raise ValueError("Fine-tuning job metadata does not contain the job ID.")
    job_details = client.fine_tuning.jobs.retrieve(job_id).dict()

    # Checkpoints
    checkpoints = requests.get(
        f"https://api.openai.com/v1/fine_tuning/jobs/{job_id}/checkpoints",
        headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
    ).json()

    details = {
        "job_details": job_details,
        "checkpoints": checkpoints.get("data", []),
    }
    job_details_path.write_text(json.dumps(details, indent=4))


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
    parser.add_argument(
        "--details",
        action="store_true",
        help="Retrieve the fine-tuning job metadata",
    )

    args = parser.parse_args()

    if sum([args.new, args.train, args.details]) > 1:
        parser.error("Only one of --new, --train, or --job can be specified.")

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
    elif args.details:
        get_fine_tune_job()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
