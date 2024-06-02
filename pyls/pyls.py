from .exceptions import InvalidPath
from .filter_strategy import FilterStrategy
from .sort_strategy import SortStrategy
from .output_format import OutputFormat
import json
from typing import List, Dict, Any


class Pyts:
    def __init__(self, path: str, show_all: bool, filter_strategy: FilterStrategy, sort_strategy: SortStrategy,
                 output_format: OutputFormat):
        self.path = path
        self.show_all = show_all
        self.filter_strategy = filter_strategy
        self.sort_strategy = sort_strategy
        self.output_format = output_format
        self.directory_structure = self.load_json_file('structure.json')

    @staticmethod
    def load_json_file(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data

    def navigate_to_path(self, path: str) -> Dict[str, Any]:
        directory = self.directory_structure
        parts = path.split('/')
        for part in parts:
            found = False
            for item in directory.get('contents', []):
                if item['name'] == part:
                    directory = item
                    found = True
                    break
            if not found:
                raise InvalidPath(f"error: cannot access '{path}': No such file or directory")
        if len(parts) > 1:
            directory["name"] = f" ./{path}"
            directory = {"contents": [directory]}
        return directory

    def list_directory_contents(self, directory: Dict[str, Any]) -> List[Dict[str, Any]]:
        items = []
        for item in directory.get("contents", []):
            if self.show_all or not item["name"].startswith('.'):
                items.append(item)
        return items

    def execute(self) -> None:
        try:
            if self.path:
                self.directory_structure = self.navigate_to_path(self.path)
            contents = self.list_directory_contents(self.directory_structure)
            filtered_contents = self.filter_strategy.filter(contents)
            sorted_contents = self.sort_strategy.sort(filtered_contents)
            output = self.output_format.format(sorted_contents)
            print(output)
        except Exception as e:
            print(str(e))
