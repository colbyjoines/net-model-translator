# core/input_schema.py
from pydantic import BaseModel


class InputSchema(BaseModel):
    class Config:
        arbitrary_types_allowed = True
