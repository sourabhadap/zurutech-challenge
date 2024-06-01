import json
import time
from typing import List, Dict, Any


class Pyls:
    def __init__(self, path: str, show_all: bool, long_format: bool, reverse: bool, sort_by_time: bool,
                 filter_option: str):
        self.path = path
        self.show_all = show_all
        self.long_format = long_format
        self.reverse = reverse
        self.sort_by_time = sort_by_time
        self.filter_option = filter_option
        self.directory_structure = self.load_json_file('structure.json')

    @staticmethod
    def load_json_file(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r') as file:
            return json.load(file)

    def navigate_to_path(self, directory: Dict[str, Any], path: str) -> Dict[str, Any]:
        parts = path.split('/')
        for part in parts:
            found = False
            for item in directory.get('contents', []):
                if item['name'] == part:
                    directory = item
                    found = True
                    break
            if not found:
                raise FileNotFoundError(f"error: cannot access '{path}': No such file or directory")
        if len(parts) > 1:
            directory["name"] = f"{path}"
            directory = {"contents": [directory]}
        return directory

    def filter_contents(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self.filter_option == 'file':
            return [item for item in contents if item['permissions'] == "-rw-r--r--"]
        elif self.filter_option == 'dir':
            return [item for item in contents if item['permissions'] == "drwxr-xr-x"]
        else:
            print(
                f"error: {self.filter_option} is not a valid filter criteria. Available filters are 'dir' "
                f"and 'file'")
            return []

    def list_directory_contents(self, directory: Dict[str, Any]) -> List[Dict[str, Any]]:
        items = []
        for item in directory.get('contents', []):
            if not self.show_all and item['name'].startswith('.'):
                continue
            if self.sort_by_time:
                item['time_modified'] = time.localtime(item['time_modified'])
            items.append(item)
        if self.sort_by_time:
            items = sorted(items, key=lambda t: time.mktime(t['time_modified']))
        if self.reverse:
            items = items[::-1]
        return items

    @staticmethod
    def format_time(epoch_time: Any) -> str:
        if isinstance(epoch_time, int):
            return time.strftime('%b %d %H:%M', time.localtime(epoch_time))
        else:
            return time.strftime('%b %d %H:%M', epoch_time)

    def print_long_format(self, contents: List[Dict[str, Any]]) -> None:
        for item in contents:
            permissions = item['permissions']
            size = item['size']
            time_modified = self.format_time(item['time_modified'])
            name = item['name']
            print(f"{permissions} {size:>5} {time_modified} {name}")

    def execute(self):

        # if self.path:
        #     try:
        # directory_structure = self.navigate_to_path(self.directory_structure, self.path)
        # except FileNotFoundError as e:
        #     print(e)
        #     return

        contents = self.list_directory_contents(self.directory_structure)
        if self.filter_option:
            contents = self.filter_contents(contents)
        if self.long_format:
            self.print_long_format(contents)
        else:
            names = [item['name'] for item in contents]
            print(' '.join(names))
