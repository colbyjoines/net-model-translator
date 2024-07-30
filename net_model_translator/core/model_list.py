from collections.abc import MutableSequence
from typing import List, Dict, Any, Type, Optional, Iterator
from pydantic import BaseModel
import pandas as pd
from tabulate import tabulate
import json
import yaml
from net_model_translator.core.input_schema import InputSchema


class ModelList(MutableSequence):
    """
    A custom list-like container for Pydantic models with extended functionalities
    such as filtering, serialization, and statistics.

    Attributes:
        model_cls (Type[BaseModel]): The Pydantic model class.
        input_schema_cls (Type[InputSchema]): The input schema class.
    """

    def __init__(
        self,
        model_cls: Type[BaseModel],
        input_schema_cls: Type[InputSchema] = InputSchema,
        *args: List[Dict[str, Any]],
    ):
        """
        Initializes a ModelList instance with the specified model and input schema classes.

        Args:
            model_cls (Type[BaseModel]): The Pydantic model class.
            input_schema_cls (Type[InputSchema], optional): The input schema class.
            *args (List[Dict[str, Any]]): The initial list of dictionaries to populate the ModelList.
        """
        self.model_cls = model_cls
        self.input_schema_cls = input_schema_cls
        self._list = []
        self.extend(args)

    def __len__(self) -> int:
        return len(self._list)

    def __getitem__(self, index: int) -> BaseModel:
        return self._list[index]

    def __setitem__(self, index: int, value: Dict[str, Any]):
        if not isinstance(value, self.model_cls):
            value = self.model_cls(**value)
        self._list[index] = value

    def __delitem__(self, index: int):
        del self._list[index]

    def insert(self, index: int, value: Dict[str, Any]):
        if not isinstance(value, self.model_cls):
            value = self.model_cls(**value)
        self._list.insert(index, value)

    def __iter__(self) -> Iterator[BaseModel]:
        return iter(self._list)

    def filter(self, **kwargs) -> "ModelList":
        filtered_items = [
            item
            for item in self._list
            if all(getattr(item, k) == v for k, v in kwargs.items())
        ]
        return ModelList(
            self.model_cls,
            self.input_schema_cls,
            *[item.dict() for item in filtered_items],
        )

    def find(self, **kwargs) -> Optional[BaseModel]:
        for item in self._list:
            if all(getattr(item, k) == v for k, v in kwargs.items()):
                return item
        return None

    def to_dict(self) -> List[Dict[str, Any]]:
        return [item.dict() for item in self._list]

    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(self.to_dict())

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_yaml(self) -> str:
        return yaml.dump(self.to_dict(), sort_keys=False, indent=2)

    @classmethod
    def from_json(
        cls,
        json_str: str,
        model_cls: Type[BaseModel],
        input_schema_cls: Type[InputSchema] = InputSchema,
    ):
        data = json.loads(json_str)
        return cls(model_cls, input_schema_cls, *data)

    @classmethod
    def from_yaml(
        cls,
        yaml_str: str,
        model_cls: Type[BaseModel],
        input_schema_cls: Type[InputSchema] = InputSchema,
    ):
        data = yaml.load(yaml_str, Loader=yaml.FullLoader)
        return cls(model_cls, input_schema_cls, *data)

    def sum(self, field: str) -> float:
        return sum(
            getattr(item, field, 0)
            for item in self._list
            if isinstance(getattr(item, field, 0), (int, float))
        )

    def average(self, field: str) -> float:
        values = [
            getattr(item, field, 0)
            for item in self._list
            if isinstance(getattr(item, field, 0), (int, float))
        ]
        return sum(values) / len(values) if values else 0

    def count(self, field: str, value: Any) -> int:
        return sum(1 for item in self._list if getattr(item, field) == value)

    def sort_by(self, field: str, reverse: bool = False):
        self._list.sort(key=lambda item: getattr(item, field), reverse=reverse)

    def group_by(self, field: str) -> Dict[Any, "ModelList"]:
        groups = {}
        for item in self._list:
            key = getattr(item, field)
            if key not in groups:
                groups[key] = []
            groups[key].append(item.dict())
        return {
            k: ModelList(self.model_cls, self.input_schema_cls, *v)
            for k, v in groups.items()
        }

    def get_metadata(self) -> Dict[str, str]:
        """
        Retrieves metadata information about the model and input schema.

        Returns:
            Dict[str, str]: A dictionary containing the model and input schema names.
        """
        parent_cls_name = self.input_schema_cls.__bases__[0].__name__
        return {
            "Model": self.model_cls.__name__,
            "InputSchema": f"{parent_cls_name}({self.input_schema_cls.__name__})",
        }

    def to_table(self) -> str:
        """
        Generates a tabulated representation of the ModelList.

        Returns:
            str: A string representing the ModelList in tabular form.
        """
        if not self._list:
            return f"ModelList({self.model_cls.__name__}): []"

        headers = list(self.model_cls.__fields__.keys())
        rows = [[getattr(item, field) for field in headers] for item in self._list]

        table = tabulate(
            rows,
            headers=headers,
            tablefmt="fancy_grid",
            colalign=("center",) * len(headers),
        )

        metadata = self.get_metadata()

        result = f"ModelList({metadata['Model']})\n\nInputSchema: {metadata['InputSchema']}\n\n{table}"
        return result

    def __repr__(self) -> str:
        return f"ModelList({self.model_cls.__name__}, {len(self._list)} items)"

    def __str__(self) -> str:
        return self.__repr__()
