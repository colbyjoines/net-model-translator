from pydantic import BaseModel, ValidationError, ConfigDict
from typing import Any, Dict, Type, Optional
import logging


class CoreModel(BaseModel):
    """
    A base model with extended configuration and utility methods.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: Optional[bool] = None,
        from_attributes: Optional[bool] = None,
        context: Any = None,
    ) -> "CoreModel":
        """
        Validate a pydantic model instance.
        """
        return super().model_validate(
            obj, strict=strict, from_attributes=from_attributes, context=context
        )

    @classmethod
    def model_validate_json(
        cls, json_data: str, *, strict: Optional[bool] = None, context: Any = None
    ) -> "CoreModel":
        """
        Validate the given JSON data against the Pydantic model.
        """
        return super().model_validate_json(json_data, strict=strict, context=context)

    def model_dump(self, **kwargs) -> dict:
        """
        Returns a dictionary representation of the model, optionally specifying which fields to include or exclude.
        """
        return super().model_dump(**kwargs)

    def model_dump_json(self, **kwargs) -> str:
        """
        Returns a JSON string representation of the model.
        """
        return super().model_dump_json(**kwargs)

    @classmethod
    def parse_json(cls, json_str: str) -> "CoreModel":
        """
        Parses a JSON string to create an instance of the model.
        """
        return cls.model_validate_json(json_str)

    @classmethod
    def parse_obj(cls, obj: Any) -> "CoreModel":
        """
        Parses a dict-like object to create an instance of the model.
        """
        return cls.model_validate(obj)

    @classmethod
    def construct(cls, **values: Any) -> "CoreModel":
        """
        Creates a new instance of the model without validation.
        """
        return cls.model_construct(**values)

    @classmethod
    def schema(cls, **kwargs) -> dict:
        """
        Generates a JSON schema for the model.
        """
        return cls.model_json_schema(**kwargs)

    @classmethod
    def detect_schema(
        cls, raw_data: Dict[str, Any], data_type: str
    ) -> Type["CoreModel"]:
        """
        Detects the appropriate schema for the given raw data and data type.
        """
        from net_model_translator.core.autodetect_schema import AutoDetectSchema

        return AutoDetectSchema.detect_schema(raw_data, data_type)

    @classmethod
    def extract_fields(
        cls, raw_data: Dict[str, Any], schema: Type[BaseModel]
    ) -> Dict[str, Any]:
        """
        Extracts fields from raw data based on the input schema.
        """
        extracted_data = {}
        for field in schema.__fields__:
            if field in raw_data:
                extracted_data[field] = raw_data[field]
        return extracted_data

    @classmethod
    def apply_transformations(
        cls, data: Dict[str, Any], transformations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Applies transformations to the data.
        """
        transformed_data = data.copy()
        for field, transform in transformations.items():
            if field in transformed_data and callable(transform):
                transformed_data[field] = transform(transformed_data[field])
        return transformed_data

    @classmethod
    def translate(
        cls,
        raw_data: Dict[str, Any],
        data_type: str,
        transformations: Optional[Dict[str, Any]] = None,
    ) -> "CoreModel":
        """
        Translates raw data into a structured model.
        """
        try:
            schema = cls.detect_schema(raw_data, data_type)
            extracted_data = cls.extract_fields(raw_data, schema)
            if transformations:
                extracted_data = cls.apply_transformations(
                    extracted_data, transformations
                )
            model_instance = schema(**extracted_data)
            logging.info(f"Successfully translated data into model: {model_instance}")
            return model_instance
        except ValidationError as e:
            logging.error(f"Validation error during translation: {e}")
            raise
