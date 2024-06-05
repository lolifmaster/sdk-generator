from context import db
from pathlib import Path
import json


pipeline = [
    {"$match": {"response.openai.status": "success"}},
    {
        "$group": {
            "_id": "$sdk_name",
            "steps": {
                "$push": {
                    "step": "$step",
                    "text": "$payload.text",
                    "response": "$response.openai.generated_text",
                }
            },
        }
    },
    {
        "$project": {
            "sdk_name": "$_id",
            "_id": 0,
            "history": {
                "$reduce": {
                    "input": "$steps",
                    "initialValue": [],
                    "in": {
                        "$concatArrays": [
                            "$$value",
                            [
                                {"role": "user", "content": "$$this.text"},
                                {
                                    "role": "assistant",
                                    "content": "$$this.response",
                                    "weight": {
                                        "$cond": {
                                            "if": {"$eq": ["$$this.step", "feedback"]},
                                            "then": 0,
                                            "else": 1,
                                        }
                                    },
                                },
                            ],
                        ]
                    },
                }
            },
        }
    },
]


def generate_finetune_data():
    data = list(db["train_data"].aggregate(pipeline))

    output_file = Path(__file__).parent.parent / "data" / "finetune_data.jsonl"

    DEFAULT_SYSTEM_PROMPT = (
        "You are a python developer. You should write client sdks to consume apis."
    )

    with output_file.open("w") as f:
        for doc in data:
            # check if any content is empty
            for item in doc["history"]:
                if not item.get("content"):
                    raise ValueError(f"Empty content found in {doc['sdk_name']}")
            row = {
                "messages": [{"role": "system", "content": DEFAULT_SYSTEM_PROMPT}]
                + doc["history"]
            }
            f.write(json.dumps(row) + "\n")

    return output_file


if __name__ == "__main__":
    generate_finetune_data()
