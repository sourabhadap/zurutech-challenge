from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .exceptions import InvalidFilter


class FilterStrategy(ABC):
    @abstractmethod
    def filter(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass


class FileFilter(FilterStrategy):
    def filter(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [item for item in contents if item['permissions'] == "-rw-r--r--"]


class DirectoryFilter(FilterStrategy):
    def filter(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [item for item in contents if item['permissions'] == "drwxr-xr-x"]


class NoFilterStrategy(FilterStrategy):
    def filter(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return contents


class FilterStrategyFactory:
    @staticmethod
    def get_filter_strategy(strategy_name: str) -> FilterStrategy:
        if strategy_name == 'file':
            return FileFilter()
        elif strategy_name == 'dir':
            return DirectoryFilter()
        elif strategy_name == '':
            return NoFilterStrategy()
        else:
            raise InvalidFilter(
                f"error: {strategy_name} is not a valid filter criteria. Available filters are 'dir' "
                f"and 'file'")
