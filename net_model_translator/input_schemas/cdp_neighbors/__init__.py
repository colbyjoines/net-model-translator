# net_model_translator/input_schemas/__init__.py
import pkgutil
import inspect
import importlib
from typing import Dict, Type
from net_model_translator.core.input_schema import InputSchema

# def get_all_schemas(package_name: str) -> Dict[str, Type[InputSchema]]:
#     schemas = {}
#     package = importlib.import_module(package_name)
#     for _, module_name, _ in pkgutil.walk_packages(
#         package.__path__, package.__name__ + "."
#     ):
#         module = importlib.import_module(module_name)
#         for class_name, obj in inspect.getmembers(module, inspect.isclass):
#             if issubclass(obj, InputSchema) and obj is not InputSchema:
#                 schemas[class_name.lower()] = obj
#     return schemas
