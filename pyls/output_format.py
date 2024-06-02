from typing import List, Dict, Any
from abc import abstractmethod, ABC
import time


class OutputFormat(ABC):
    @abstractmethod
    def format(self, contents: List[Dict[str, Any]]) -> str:
        pass


class LongFormatOutput(OutputFormat):
    @staticmethod
    def human_readable_size(size_in_bytes: int) -> str:
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

    def format(self, items: List[Dict[str, Any]]) -> str:
        formatted_output = []
        for item in items:
            permissions = item['permissions']
            size = self.human_readable_size(item['size'])
            time_modified = time.strftime('%b %d %H:%M', time.localtime(item["time_modified"]))
            name = item["name"]
            formatted_output.append(f"{permissions} {size:>5} {time_modified} {name}")
        return "\n".join(formatted_output)


class SimpleOutput(OutputFormat):
    def format(self, items: List[Dict[str, Any]]) -> str:
        return ' '.join(item['name'] for item in items)


class OutputFormatFactory:
    @staticmethod
    def get_output_format(format_name: str) -> OutputFormat:
        if format_name == 'long':
            return LongFormatOutput()
        elif format_name == 'simple':
            return SimpleOutput()
        else:
            raise ValueError(f"error: {format_name} is not a valid output format. Available formats are 'long' "
                             f"and 'simple'")
