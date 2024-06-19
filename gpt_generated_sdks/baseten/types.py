from typing import Optional, Dict, Union


# Define types for each object


class UpsertSecretRequestV1:
    name: str
    value: str

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class UpdateAutoscalingSettingsV1:
    min_replica: Optional[int]
    max_replica: Optional[int]
    autoscaling_window: Optional[int]
    scale_down_delay: Optional[int]
    concurrency_target: Optional[int]


class PromoteRequestV1:
    scale_down_previous_production: bool


# Define a type for model_id and deployment_id
PathParameter = str

# Define a type for the entire schema
SchemaTypes = Union[
    UpsertSecretRequestV1, UpdateAutoscalingSettingsV1, PromoteRequestV1, PathParameter
]

# Mapping of schema names to their corresponding types
schema_types: Dict[str, SchemaTypes] = {
    "UpsertSecretRequestV1": UpsertSecretRequestV1,
    "model_id": PathParameter,
    "deployment_id": PathParameter,
    "UpdateAutoscalingSettingsV1": UpdateAutoscalingSettingsV1,
    "PromoteRequestV1": PromoteRequestV1,
}
