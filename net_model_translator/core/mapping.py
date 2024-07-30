from typing import Optional, Callable, Any, Dict
from pydantic import BaseModel


class Mapping(BaseModel):
    source_key: Optional[str] = None
    target_key: Optional[str] = None
    transform: Optional[Callable[[Any], Any]] = None  # Optional transformation function

    def __init__(self, **data):
        super().__init__(**data)
        if not self.source_key:
            self.source_key = self.source_key
        if not self.target_key:
            self.target_key = self.target_key

    def apply(self, data: Dict[str, Any]) -> Any:
        key = self.source_key
        value = data.get(key)
        if value is not None and self.transform:
            value = self.transform(value)
        return self.target_key, value
