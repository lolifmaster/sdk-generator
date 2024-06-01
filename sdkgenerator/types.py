from typing import TypedDict, Literal


class Template(TypedDict):
    types: str
    initial_code: str
    feedback: str
    final_code: str


class TemplateWithoutTypes(TypedDict):
    initial_code: str
    feedback: str
    final_code: str


Step = Literal["types", "initial_code", "feedback", "final_code"]

Language = Literal["python"]
