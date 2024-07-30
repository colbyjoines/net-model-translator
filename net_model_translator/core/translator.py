# net_model_translator/core/translator.py
from typing import List, Dict, Any, Type, Optional
from pydantic import BaseModel
from net_model_translator.core.mapping import Mapping
from net_model_translator.core.autodetect_schema import AutoDetectSchema
from net_model_translator.core.input_schema import InputSchema
from net_model_translator.models import mapping
from net_model_translator.core.model_list import ModelList


class SchemaDetector:
    @staticmethod
    def detect(raw_data: List[Dict[str, Any]], data_type) -> Type[InputSchema]:
        if raw_data is None or not raw_data:
            raise ValueError("raw_data must be provided if input_schema is None.")
        return AutoDetectSchema.detect_schema(raw_data[0], data_type)


class DataMapper:
    def __init__(self, input_schema: Type[InputSchema]):
        self.input_schema = input_schema

    def apply_mappings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        mapped_data = self._map_defined_fields(data)
        extra_fields = self._extract_extra_fields(data, mapped_data)
        mapped_data.update(extra_fields)
        return mapped_data

    def _map_defined_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        mapped_data = {}
        for field_name, field_info in self.input_schema.__fields__.items():
            mapping: Mapping = field_info.default
            target_key = mapping.target_key or field_name
            source_key = mapping.source_key or field_name
            value = data.get(source_key)
            if value is not None and mapping.transform:
                value = mapping.transform(value)
            mapped_data[target_key] = value
        return mapped_data

    def _extract_extra_fields(
        self, data: Dict[str, Any], mapped_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        combined_schema_source_keys = set(self.input_schema.__fields__.keys())
        combined_schema_source_keys.update(
            mapping.source_key or field_name
            for field_name, field_info in self.input_schema.__fields__.items()
            for mapping in [field_info.default]
        )
        return {
            key: value
            for key, value in data.items()
            if key not in combined_schema_source_keys
        }


class Translator:
    def __init__(
        self,
        data_type: str,
        model: Type[BaseModel] = None,
        raw_data: Optional[List[Dict[str, Any]]] = None,
        input_schema: Optional[Type[InputSchema]] = None,
    ):
        self.data_type = data_type
        self.model = model or mapping[data_type]
        self.raw_data = raw_data
        self.input_schema = input_schema or SchemaDetector.detect(raw_data, data_type)
        self.data_mapper = DataMapper(self.input_schema)

    def translate(self, raw_data: Optional[List[Dict[str, Any]]] = None) -> ModelList:
        self.raw_data = raw_data or self.raw_data
        if not self.raw_data:
            raise ValueError(
                "raw_data must be passed to translate() if not set in the constructor."
            )

        validated_data = [
            self.data_mapper.apply_mappings(data) for data in self.raw_data
        ]
        return ModelList(
            self.model,
            self.data_mapper.input_schema,
            *validated_data,
        )
