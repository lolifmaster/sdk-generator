import yaml
from sdkgenerator.types import Step, Agent

with open("generator.config.yaml", "r") as file:
    config = yaml.safe_load(file)

TEMPERATURE: dict[Step, float] = config["TEMPERATURE"]
AGENT: dict[Step, Agent] = config["AGENT"]
MAX_PROMPT_LENGTH: dict[Step, int] = config["MAX_PROMPT_LENGTH"]
MAX_TOKENS: dict[Step, int] = config["MAX_TOKENS"]
