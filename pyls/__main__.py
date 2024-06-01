import argparse
import json
import os
from typing import List, Dict, Any


def load_json_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)


def list_directory_contents(directory: Dict[str, Any], show_all: bool) -> List[str]:
    items = []
    for item in directory.get('contents', []):
        if not show_all and item['name'].startswith('.'):
            continue
        items.append(item['name'])
    return items


def main():
    parser = argparse.ArgumentParser(description="Python ls utility.")
    parser.add_argument('-A', action='store_true', help='Include directory entries whose names begin with a dot (.)',
                        default=False)
    parser.add_argument('path', nargs='?', default='structure.json',
                        help='Path to the JSON file representing the directory structure')

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"error: cannot access '{args.path}': No such file or directory")
        return

    directory_structure = load_json_file(args.path)
    contents = list_directory_contents(directory_structure, show_all=args.A)
    print(' '.join(contents))


if __name__ == '__main__':
    main()
