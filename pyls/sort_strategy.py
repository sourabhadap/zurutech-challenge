from abc import ABC, abstractmethod
from typing import List, Dict, Any


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass


class ReverseSortDecorator(SortStrategy):
    def __init__(self, sort_strategy: SortStrategy):
        self.sort_strategy = sort_strategy

    def sort(self, items: List[Any]) -> List[Any]:
        return self.sort_strategy.sort(items)[::-1]


class TimeSortStrategy(SortStrategy):
    def sort(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(contents, key=lambda item: item["time_modified"])


class NoSortStrategy(SortStrategy):
    def sort(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return contents


class SortStrategyFactory:
    @staticmethod
    def get_sort_strategy(strategy_name: str) -> SortStrategy:
        if strategy_name == "time":
            return TimeSortStrategy()
        else:
            return NoSortStrategy()
