from sdkgenerator.db import db


def log_llm_response(
    payload: dict, response: dict, *, step: Step, sdk_name: str = None
):
    """
    Log the response from the language model to logs file.

    :param sdk_name: The name of the SDK.
    :type sdk_name: str
    :param step: The step in the process.
    :type step: Step
    :param payload: The payload sent to the language model.
    :type payload: dict
    :param response: The response from the language model.
    :type response: dict
    :return: None
    """

    # save the response to the database
    db.insert_one(
        {"step": step, "sdk_name": sdk_name, "payload": payload, "response": response}
    )

    with open(API_CALLS_DIR / "logs.txt", "a+", encoding="utf-8") as file:
        file.write(f"Step: {step}\n")
        file.write(f"Payload: {json.dumps(payload, indent=2)}\n")
        file.write(f"Response: {json.dumps(response, indent=2)}\n-----------\n")