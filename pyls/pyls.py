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

    @staticmethod
    def human_readable_size(size_in_bytes: int) -> str:
        """
        Convert a file size in bytes to a human-readable string with appropriate units.

        Args:
        size_in_bytes (int): The file size in bytes.

        Returns:
        str: A human-readable string representing the file size with appropriate units.
        """
        if size_in_bytes < 0:
            raise ValueError("Size must be non-negative")

        # Define the units and their corresponding thresholds
        units = ["B", "K", "MB", "GB", "TB", "PB", "EB"]
        threshold = 1024
        if size_in_bytes < threshold:
            return f"{size_in_bytes}"

        size = float(size_in_bytes)
        unit = units.pop(0)

        while size >= threshold and units:
            size /= threshold
            unit = units.pop(0)

        return f"{size:.1f}{unit}"

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
                print(f"error: cannot access '{path}': No such file or directory")
                return {"contents": []}
        if len(parts) > 1:
            directory["name"] = f" ./{path}"
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
            item['size'] = self.human_readable_size(item['size'])
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
        if self.path:
            self.directory_structure = self.navigate_to_path(self.path)
        contents = self.list_directory_contents(self.directory_structure)
        if self.filter_option:
            contents = self.filter_contents(contents)
        if self.long_format:
            self.print_long_format(contents)
        else:
            names = [item['name'] for item in contents]
            print(' '.join(names))
