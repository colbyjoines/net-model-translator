# core/translator.py
from typing import List, Dict, Type
from pydantic import BaseModel, ValidationError
from net_model_translator.core.input_schema import InputSchema
from net_model_translator.core.mapping import Mapping


class Translator:
    def __init__(
        self, device_type: str, input_schema: InputSchema, model: Type[BaseModel]
    ):
        self.device_type = device_type
        self.input_schema = input_schema
        self.model = model

    def translate(self, raw_data: List[Dict]) -> List[BaseModel]:
        validated_data = []
        for data in raw_data:
            try:
                mapped_data = self._map_data(data)
                validated_data.append(mapped_data)
            except ValidationError as e:
                print(f"Validation error: {e.json()}")
                continue

        return [self.model(**data) for data in validated_data]

    def _map_data(self, data: Dict) -> Dict:
        mapped_data = {}
        for field in self.input_schema.model_fields():
            mapping_instance = getattr(self.input_schema, field)
            if isinstance(mapping_instance, Mapping):
                target_key, value = mapping_instance.apply(data)
                if value is None:
                    value = ""  # Set default value to empty string
                mapped_data[target_key] = value
        return mapped_data
