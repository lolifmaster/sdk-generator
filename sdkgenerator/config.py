from sdkgenerator.types import Step, Agent

TEMPERATURE: dict[Step, float] = {
    "types": 0.1,
    "initial_code": 0.2,
    "feedback": 0.2,
    "final_code": 0.1,
}

AGENT: dict[Step, Agent] = {
    "types": {
        "model": "gpt-4-32k-0314",
        "custom": False,
    },
    "initial_code": {
        "model": "ft:gpt-3.5-turbo-0125:eden-ai::9UxoYDO3",
        "custom": True,
    },
    "feedback": {
        "model": "gpt-4-32k-0314",
        "custom": False,
    },
    "final_code": {
        "model": "ft:gpt-3.5-turbo-0125:eden-ai::9UxoYDO3",
        "custom": True,
    },
}

MAX_PROMPT_LENGTH: dict[Step, int] = {
    "types": 8192,
    "initial_code": 8192,
    "feedback": 8192,
    "final_code": 8192,
}

MAX_TOKENS: dict[Step, int] = {
    "types": 4096,
    "initial_code": 4096,
    "feedback": 4096,
    "final_code": 4096,
}
