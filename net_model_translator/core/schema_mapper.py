from pydantic import BaseModel
from typing import Dict, Any

from net_model_translator.core.mapping import Mapping


class SchemaMapper(BaseModel):
    mappings: Dict[str, Mapping]

    def apply_mappings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        mapped_data = {}
        for key, mapping in self.mappings.items():
            key, value = mapping.apply(data)
            mapped_data[key] = value
        return mapped_data
