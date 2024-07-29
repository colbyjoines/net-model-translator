from pydantic import BaseModel
from typing import Callable, Dict, Any

class Mapping(BaseModel):
    source_key: str
    target_key: str
    transform: Callable[[Any], Any] = None  # Optional transformation function

    def apply(self, data: Dict[str, Any]) -> Any:
        value = data.get(self.source_key)
        if self.transform:
            value = self.transform(value)
        return self.target_key, value

class SchemaMapper(BaseModel):
    mappings: Dict[str, Mapping]

    def apply_mappings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        mapped_data = {}
        for key, mapping in self.mappings.items():
            key, value = mapping.apply(data)
            mapped_data[key] = value
        return mapped_data

