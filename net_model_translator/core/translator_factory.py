from typing import Dict, Type

from pydantic import BaseModel

from net_model_translator.models.arp import ARPModel
from net_model_translator.models.cdp_neighbors import CDPNeighborsModel


class TranslatorFactory:
    _translators: Dict[str, Type[BaseModel]] = {
        "cdp_neighbors": CDPNeighborsModel,
        "arp": ARPModel,
        # Add other translators here
    }

    @classmethod
    def get_translator(cls, command_definition: str):
        if command_definition in cls._translators:
            return cls._translators[command_definition]
        raise ValueError(f"Unsupported command: {command_definition}")

    @classmethod
    def register_translator(cls, command_definition: str, model_class: Type[BaseModel]):
        cls._translators[command_definition] = model_class
