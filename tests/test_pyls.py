import unittest
from io import StringIO
import sys
from pyls.__main__ import list_directory_contents, print_long_format, filter_contents


class TestPyls(unittest.TestCase):

    def setUp(self):
        self.structure = {
            "name": "interpreter",
            "size": 4096,
            "time_modified": 1699957865,
            "permissions": "-rw-r--r--",
            "contents": [
                {"name": ".gitignore", "size": 8911, "time_modified": 1699941437, "permissions": "drwxr-xr-x"},
                {"name": "LICENSE", "size": 1071, "time_modified": 1699941437, "permissions": "-rw-r--r--"},
                {"name": "README.md", "size": 83, "time_modified": 1699941437, "permissions": "-rw-r--r--"},
                {"name": "ast", "size": 4096, "time_modified": 1699957739, "permissions": "drwxr-xr-x"},
                {"name": "go.mod", "size": 60, "time_modified": 1699950073, "permissions": "-rw-r--r--"},
                {"name": "lexer", "size": 4096, "time_modified": 1699955487, "permissions": "drwxr-xr-x"},
                {"name": "main.go", "size": 74, "time_modified": 1699950453, "permissions": "-rw-r--r--"},
                {"name": "parser", "size": 4096, "time_modified": 1700205662, "permissions": "drwxr-xr-x"},
                {"name": "token", "size": 4096, "time_modified": 1699954070, "permissions": "drwxr-xr-x"}
            ]
        }

    def test_list_directory_contents_without_dotfiles(self):
        expected = [
            {'name': 'LICENSE', 'size': 1071, 'time_modified': 1699941437, 'permissions': '-rw-r--r--'},
            {'name': 'README.md', 'size': 83, 'time_modified': 1699941437, 'permissions': '-rw-r--r--'},
            {'name': 'ast', 'size': 4096, 'time_modified': 1699957739, 'permissions': 'drwxr-xr-x'},
            {'name': 'go.mod', 'size': 60, 'time_modified': 1699950073, 'permissions': '-rw-r--r--'},
            {'name': 'lexer', 'size': 4096, 'time_modified': 1699955487, 'permissions': 'drwxr-xr-x'},
            {'name': 'main.go', 'size': 74, 'time_modified': 1699950453, 'permissions': '-rw-r--r--'},
            {'name': 'parser', 'size': 4096, 'time_modified': 1700205662, 'permissions': 'drwxr-xr-x'},
            {'name': 'token', 'size': 4096, 'time_modified': 1699954070, 'permissions': 'drwxr-xr-x'}
        ]
        result = list_directory_contents(self.structure)
        self.assertEqual(result, expected)

    def test_list_directory_contents_with_dotfiles(self):
        expected = [
            {'name': '.gitignore', 'size': 8911, 'time_modified': 1699941437, 'permissions': 'drwxr-xr-x'},
            {'name': 'LICENSE', 'size': 1071, 'time_modified': 1699941437, 'permissions': '-rw-r--r--'},
            {'name': 'README.md', 'size': 83, 'time_modified': 1699941437, 'permissions': '-rw-r--r--'},
            {'name': 'ast', 'size': 4096, 'time_modified': 1699957739, 'permissions': 'drwxr-xr-x'},
            {'name': 'go.mod', 'size': 60, 'time_modified': 1699950073, 'permissions': '-rw-r--r--'},
            {'name': 'lexer', 'size': 4096, 'time_modified': 1699955487, 'permissions': 'drwxr-xr-x'},
            {'name': 'main.go', 'size': 74, 'time_modified': 1699950453, 'permissions': '-rw-r--r--'},
            {'name': 'parser', 'size': 4096, 'time_modified': 1700205662, 'permissions': 'drwxr-xr-x'},
            {'name': 'token', 'size': 4096, 'time_modified': 1699954070, 'permissions': 'drwxr-xr-x'}
        ]
        result = list_directory_contents(self.structure, show_all=True)
        self.assertEqual(result, expected)

    def test_print_long_format(self):
        contents = list_directory_contents(self.structure)
        expected_output = (
            "-rw-r--r--  1071 Nov 14 11:27 LICENSE\n"
            "-rw-r--r--    83 Nov 14 11:27 README.md\n"
            "drwxr-xr-x  4096 Nov 14 15:58 ast\n"
            "-rw-r--r--    60 Nov 14 13:51 go.mod\n"
            "drwxr-xr-x  4096 Nov 14 15:21 lexer\n"
            "-rw-r--r--    74 Nov 14 13:57 main.go\n"
            "drwxr-xr-x  4096 Nov 17 12:51 parser\n"
            "drwxr-xr-x  4096 Nov 14 14:57 token\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output
        print_long_format(contents)
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_print_long_format_in_reverse(self):
        contents = list_directory_contents(self.structure, reverse=True)
        expected_output = (
            "drwxr-xr-x  4096 Nov 14 14:57 token\n"
            "drwxr-xr-x  4096 Nov 17 12:51 parser\n"
            "-rw-r--r--    74 Nov 14 13:57 main.go\n"
            "drwxr-xr-x  4096 Nov 14 15:21 lexer\n"
            "-rw-r--r--    60 Nov 14 13:51 go.mod\n"
            "drwxr-xr-x  4096 Nov 14 15:58 ast\n"
            "-rw-r--r--    83 Nov 14 11:27 README.md\n"
            "-rw-r--r--  1071 Nov 14 11:27 LICENSE\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output
        print_long_format(contents)
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_print_long_format_in_reverse_with_time_modified(self):
        contents = list_directory_contents(self.structure, reverse=True, sort_time=True)
        expected_output = (
            "drwxr-xr-x  4096 Nov 17 12:51 parser\n"
            "drwxr-xr-x  4096 Nov 14 15:58 ast\n"
            "drwxr-xr-x  4096 Nov 14 15:21 lexer\n"
            "drwxr-xr-x  4096 Nov 14 14:57 token\n"
            "-rw-r--r--    74 Nov 14 13:57 main.go\n"
            "-rw-r--r--    60 Nov 14 13:51 go.mod\n"
            "-rw-r--r--    83 Nov 14 11:27 README.md\n"
            "-rw-r--r--  1071 Nov 14 11:27 LICENSE\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output
        print_long_format(contents)
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_print_long_format_in_reverse_with_time_modified_dir_filter(self):
        contents = list_directory_contents(self.structure, reverse=True, sort_time=True)
        contents = filter_contents(contents, 'dir')
        expected_output = (
            "drwxr-xr-x  4096 Nov 17 12:51 parser\n"
            "drwxr-xr-x  4096 Nov 14 15:58 ast\n"
            "drwxr-xr-x  4096 Nov 14 15:21 lexer\n"
            "drwxr-xr-x  4096 Nov 14 14:57 token\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output
        print_long_format(contents)
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_print_long_format_in_reverse_with_time_modified_file_filter(self):
        contents = list_directory_contents(self.structure, reverse=True, sort_time=True)
        contents = filter_contents(contents, 'file')
        expected_output = (
            "-rw-r--r--    74 Nov 14 13:57 main.go\n"
            "-rw-r--r--    60 Nov 14 13:51 go.mod\n"
            "-rw-r--r--    83 Nov 14 11:27 README.md\n"
            "-rw-r--r--  1071 Nov 14 11:27 LICENSE\n"
        )

        captured_output = StringIO()
        sys.stdout = captured_output
        print_long_format(contents)
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_print_long_format_in_reverse_with_time_modified_invalid_filter(self):
        contents = list_directory_contents(self.structure, reverse=True, sort_time=True)
        contents = filter_contents(contents, 'filewsd')

        self.assertEqual(len(contents), 0)


if __name__ == '__main__':
    unittest.main()
