# net_model_translator/core/autodetect_schema.py
from typing import Type, Any, Dict
from pydantic import BaseModel
from net_model_translator.input_schemas import get_all_schemas


class AutoDetectSchema:
    @staticmethod
    def detect_schema(raw_data: Dict[str, Any], data_type) -> Type[BaseModel]:
        all_schemas = get_all_schemas(data_type)

        for schema_name, schema in all_schemas.items():
            proposed_model_keys = {
                (field.default.source_key if field.default.source_key else field_name)
                for field_name, field in schema.__fields__.items()
            }

            if proposed_model_keys.issubset(raw_data.keys()):
                return schema

        raise ValueError("No matching schema found for the provided data.")

    @staticmethod
    def get_schema_by_type(data_type: str) -> Dict[str, Type[BaseModel]]:
        return get_all_schemas()
