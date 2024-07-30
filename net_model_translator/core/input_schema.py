# core/input_schema.py
from pydantic import BaseModel


class InputSchema(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
