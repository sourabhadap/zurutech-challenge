import unittest
from io import StringIO
import sys
from pyls.__main__ import list_directory_contents, print_long_format


class TestPyls(unittest.TestCase):

    def setUp(self):
        self.structure = {
            "name": "interpreter",
            "size": 4096,
            "time_modified": 1699957865,
            "permissions": "-rw-r--r--",
            "contents": [
                {"name": ".gitignore", "size": 8911, "time_modified": 1699941437, "permissions": "drwxr-xr-x"},
                {"name": "LICENSE", "size": 1071, "time_modified": 1699941437, "permissions": "drwxr-xr-x"},
                {"name": "README.md", "size": 83, "time_modified": 1699941437, "permissions": "drwxr-xr-x"},
                {"name": "ast", "size": 4096, "time_modified": 1699957739, "permissions": "-rw-r--r--"},
                {"name": "go.mod", "size": 60, "time_modified": 1699950073, "permissions": "drwxr-xr-x"},
                {"name": "lexer", "size": 4096, "time_modified": 1699955487, "permissions": "drwxr-xr-x"},
                {"name": "main.go", "size": 74, "time_modified": 1699950453, "permissions": "-rw-r--r--"},
                {"name": "parser", "size": 4096, "time_modified": 1700205662, "permissions": "drwxr-xr-x"},
                {"name": "token", "size": 4096, "time_modified": 1699954070, "permissions": "-rw-r--r--"}
            ]
        }

    def test_list_directory_contents_without_dotfiles(self):
        expected = [
            {'name': 'LICENSE', 'size': 1071, 'time_modified': 1699941437, 'permissions': 'drwxr-xr-x'},
            {'name': 'README.md', 'size': 83, 'time_modified': 1699941437, 'permissions': 'drwxr-xr-x'},
            {'name': 'ast', 'size': 4096, 'time_modified': 1699957739, 'permissions': '-rw-r--r--'},
            {'name': 'go.mod', 'size': 60, 'time_modified': 1699950073, 'permissions': 'drwxr-xr-x'},
            {'name': 'lexer', 'size': 4096, 'time_modified': 1699955487, 'permissions': 'drwxr-xr-x'},
            {'name': 'main.go', 'size': 74, 'time_modified': 1699950453, 'permissions': '-rw-r--r--'},
            {'name': 'parser', 'size': 4096, 'time_modified': 1700205662, 'permissions': 'drwxr-xr-x'},
            {'name': 'token', 'size': 4096, 'time_modified': 1699954070, 'permissions': '-rw-r--r--'}
        ]
        result = list_directory_contents(self.structure)
        self.assertEqual(result, expected)

    def test_list_directory_contents_with_dotfiles(self):
        expected = [
            {'name': '.gitignore', 'size': 8911, 'time_modified': 1699941437, 'permissions': 'drwxr-xr-x'},
            {'name': 'LICENSE', 'size': 1071, 'time_modified': 1699941437, 'permissions': 'drwxr-xr-x'},
            {'name': 'README.md', 'size': 83, 'time_modified': 1699941437, 'permissions': 'drwxr-xr-x'},
            {'name': 'ast', 'size': 4096, 'time_modified': 1699957739, 'permissions': '-rw-r--r--'},
            {'name': 'go.mod', 'size': 60, 'time_modified': 1699950073, 'permissions': 'drwxr-xr-x'},
            {'name': 'lexer', 'size': 4096, 'time_modified': 1699955487, 'permissions': 'drwxr-xr-x'},
            {'name': 'main.go', 'size': 74, 'time_modified': 1699950453, 'permissions': '-rw-r--r--'},
            {'name': 'parser', 'size': 4096, 'time_modified': 1700205662, 'permissions': 'drwxr-xr-x'},
            {'name': 'token', 'size': 4096, 'time_modified': 1699954070, 'permissions': '-rw-r--r--'}
        ]
        result = list_directory_contents(self.structure, show_all=True)
        self.assertEqual(result, expected)

    def test_print_long_format(self):
        contents = list_directory_contents(self.structure)
        expected_output = (
            "drwxr-xr-x  1071 Nov 14 11:27 LICENSE\n"
            "drwxr-xr-x    83 Nov 14 11:27 README.md\n"
            "-rw-r--r--  4096 Nov 14 15:58 ast\n"
            "drwxr-xr-x    60 Nov 14 13:51 go.mod\n"
            "drwxr-xr-x  4096 Nov 14 15:21 lexer\n"
            "-rw-r--r--    74 Nov 14 13:57 main.go\n"
            "drwxr-xr-x  4096 Nov 17 12:51 parser\n"
            "-rw-r--r--  4096 Nov 14 14:57 token\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output
        print_long_format(contents)
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
