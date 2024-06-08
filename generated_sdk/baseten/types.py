from typing import TypedDict, Optional

class UpsertSecretRequestV1(TypedDict):
    name: str
    value: str

class ModelId(TypedDict):
    schema: str
    name: str
    in_: str
    req: bool

class DeploymentId(TypedDict):
    schema: str
    name: str
    in_: str
    req: bool

class UpdateAutoscalingSettingsV1(TypedDict):
    min_replica: Optional[int]
    max_replica: Optional[int]
    autoscaling_window: Optional[int]
    scale_down_delay: Optional[int]
    concurrency_target: Optional[int]

class PromoteRequestV1(TypedDict):
    scale_down_previous_production: bool