import yaml
from sdkgenerator.types import Step, Agent
from pathlib import Path

# Load the configuration file
config_path = Path(__file__).parent.parent / "generator.config.yaml"

with open(config_path, "r") as file:
    config = yaml.safe_load(file)

TEMPERATURE: dict[Step, float] = config["TEMPERATURE"]
AGENT: dict[Step, Agent] = config["AGENT"]
MAX_PROMPT_LENGTH: dict[Step, int] = config["MAX_PROMPT_LENGTH"]
MAX_TOKENS: dict[Step, int] = config["MAX_TOKENS"]
TESTING: bool = config["TESTING"]
