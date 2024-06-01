import unittest
from pyls.__main__ import list_directory_contents


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
        expected = ['LICENSE', 'README.md', 'ast', 'go.mod', 'lexer', 'main.go', 'parser', 'token']
        result = list_directory_contents(self.structure)
        self.assertEqual(result, expected)

    def test_list_directory_contents_with_dotfiles(self):
        expected = ['.gitignore', 'LICENSE', 'README.md', 'ast', 'go.mod', 'lexer', 'main.go', 'parser', 'token']
        result = list_directory_contents(self.structure, show_all=True)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
