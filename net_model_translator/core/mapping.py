# core/mapping.py
from pydantic import BaseModel
from typing import Callable, Dict, Any


class Mapping(BaseModel):
    source_key: str
    target_key: str
    transform: Callable[[Any], Any] = None  # Optional transformation function

    def apply(self, data: Dict[str, Any]) -> Any:
        value = data.get(self.source_key)
        if value is not None and self.transform:
            value = self.transform(value)
        return self.target_key, value
