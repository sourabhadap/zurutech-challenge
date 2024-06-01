import argparse
import json
import os
import time
from typing import List, Dict, Any


def load_json_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)


def list_directory_contents(directory: Dict[str, Any], show_all: bool = False, reverse: bool = False,
                            sort_time: bool = False) -> List[Dict[str, Any]]:
    items = []
    for item in directory.get('contents', []):
        if not show_all and item['name'].startswith('.'):
            continue
        if sort_time:
            item['time_modified'] = time.localtime(item['time_modified'])
        items.append(item)
    if sort_time:
        items = sorted(items, key=lambda t: time.mktime(t['time_modified']))
    if reverse:
        items = items[::-1]
    return items


def format_time(epoch_time: Any) -> str:
    if isinstance(epoch_time, int):
        return time.strftime('%b %d %H:%M', time.localtime(epoch_time))
    else:
        return time.strftime('%b %d %H:%M', epoch_time)


def print_long_format(contents: List[Dict[str, Any]]) -> None:
    for item in contents:
        permissions = item['permissions']
        size = item['size']
        time_modified = format_time(item['time_modified'])
        name = item['name']
        print(f"{permissions} {size:>5} {time_modified} {name}")


def main():
    parser = argparse.ArgumentParser(description="Python ls utility.")
    parser.add_argument('-A', action='store_true', help='Include directory entries whose names begin with a dot (.)')
    parser.add_argument('-l', action='store_true', help='Use a long listing format')
    parser.add_argument('-r', action='store_true', help='List subdirectories reverse', default=False)
    parser.add_argument('-t', action='store_true', help='List subdirectories by modified time', default=False)
    parser.add_argument('path', nargs='?', default='structure.json',
                        help='Path to the JSON file representing the directory structure')

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"error: cannot access '{args.path}': No such file or directory")
        return

    directory_structure = load_json_file(args.path)
    contents = list_directory_contents(directory_structure, show_all=args.A, reverse=args.r, sort_time=args.t)

    if args.l:
        print_long_format(contents)
    else:
        names = [item['name'] for item in contents]
        print(' '.join(names))


if __name__ == '__main__':
    main()
