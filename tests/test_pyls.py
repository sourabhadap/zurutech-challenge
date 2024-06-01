import unittest
from io import StringIO
import sys
import pyls


class TestPyls(unittest.TestCase):

    def setUp(self):
        self.pyls = pyls.Pyls(
            path='',
            show_all=False,
            long_format=False,
            reverse=False,
            sort_by_time=False,
            filter_option=''
        )

    def validate_pyls(self):
        self.maxDiff = None
        captured_output = StringIO()
        sys.stdout = captured_output
        self.pyls.execute()
        sys.stdout = sys.__stdout__
        return captured_output

    def test_list_directory_contents_without_dotfiles(self):
        expected = ['LICENSE', 'README.md', 'ast', 'go.mod', 'lexer', 'main.go', 'parser', 'token']
        output = self.validate_pyls()
        result = output.getvalue().split(" ")
        resul = [i.strip() for i in result]
        self.assertEqual(resul, expected)

    def test_list_directory_contents_with_dotfiles(self):
        expected = ['.gitignore', 'LICENSE', 'README.md', 'ast', 'go.mod', 'lexer', 'main.go', 'parser', 'token']
        self.pyls.show_all = True
        output = self.validate_pyls()
        result = output.getvalue().split(" ")
        resul = [i.strip() for i in result]
        self.assertEqual(resul, expected)

    def test_print_long_format(self):
        expected_output = (
            "-rw-r--r--  1.0K Nov 14 11:27 LICENSE\n"
            "-rw-r--r--    83 Nov 14 11:27 README.md\n"
            "drwxr-xr-x  4.0K Nov 14 15:58 ast\n"
            "-rw-r--r--    60 Nov 14 13:51 go.mod\n"
            "drwxr-xr-x  4.0K Nov 14 15:21 lexer\n"
            "-rw-r--r--    74 Nov 14 13:57 main.go\n"
            "drwxr-xr-x  4.0K Nov 17 12:51 parser\n"
            "drwxr-xr-x  4.0K Nov 14 14:57 token\n"
        )

        self.pyls.long_format = True
        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    def test_print_long_format_in_reverse(self):
        expected_output = (
            "drwxr-xr-x  4.0K Nov 14 14:57 token\n"
            "drwxr-xr-x  4.0K Nov 17 12:51 parser\n"
            "-rw-r--r--    74 Nov 14 13:57 main.go\n"
            "drwxr-xr-x  4.0K Nov 14 15:21 lexer\n"
            "-rw-r--r--    60 Nov 14 13:51 go.mod\n"
            "drwxr-xr-x  4.0K Nov 14 15:58 ast\n"
            "-rw-r--r--    83 Nov 14 11:27 README.md\n"
            "-rw-r--r--  1.0K Nov 14 11:27 LICENSE\n"
        )

        self.pyls.long_format = True
        self.pyls.reverse = True
        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    def test_print_long_format_in_reverse_with_time_modified(self):

        expected_output = (
            "drwxr-xr-x  4.0K Nov 17 12:51 parser\n"
            "drwxr-xr-x  4.0K Nov 14 15:58 ast\n"
            "drwxr-xr-x  4.0K Nov 14 15:21 lexer\n"
            "drwxr-xr-x  4.0K Nov 14 14:57 token\n"
            "-rw-r--r--    74 Nov 14 13:57 main.go\n"
            "-rw-r--r--    60 Nov 14 13:51 go.mod\n"
            "-rw-r--r--    83 Nov 14 11:27 README.md\n"
            "-rw-r--r--  1.0K Nov 14 11:27 LICENSE\n"
        )

        self.pyls.long_format = True
        self.pyls.sort_by_time = True
        self.pyls.reverse = True
        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    def test_print_long_format_in_reverse_with_time_modified_dir_filter(self):
        expected_output = (
            "drwxr-xr-x  4.0K Nov 17 12:51 parser\n"
            "drwxr-xr-x  4.0K Nov 14 15:58 ast\n"
            "drwxr-xr-x  4.0K Nov 14 15:21 lexer\n"
            "drwxr-xr-x  4.0K Nov 14 14:57 token\n"
        )

        self.pyls.long_format = True
        self.pyls.sort_by_time = True
        self.pyls.reverse = True
        self.pyls.filter_option = 'dir'
        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    def test_print_long_format_in_reverse_with_time_modified_file_filter(self):
        expected_output = (
            "-rw-r--r--    74 Nov 14 13:57 main.go\n"
            "-rw-r--r--    60 Nov 14 13:51 go.mod\n"
            "-rw-r--r--    83 Nov 14 11:27 README.md\n"
            "-rw-r--r--  1.0K Nov 14 11:27 LICENSE\n"
        )

        self.pyls.long_format = True
        self.pyls.sort_by_time = True
        self.pyls.reverse = True
        self.pyls.filter_option = 'file'
        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)
    #
    def test_print_long_format_in_reverse_with_time_modified_invalid_filter(self):
        self.pyls.long_format = True
        self.pyls.sort_time = True
        self.pyls.show_all = True
        self.pyls.filter_option = 'filewsd'
        expected_output = "error: filewsd is not a valid filter criteria. Available filters are 'dir' and 'file'"

        output = self.validate_pyls()
        self.assertEqual(output.getvalue().strip(), expected_output)

    def test_handle_paths(self):
        self.pyls.long_format = True
        self.pyls.reverse = True
        self.pyls.path = 'parser'
        expected_output = (
            "-rw-r--r--   533 Nov 14 16:03 go.mod\n"
            "-rw-r--r--  1.6K Nov 17 12:05 parser.go\n"
            "-rw-r--r--  1.3K Nov 17 12:51 parser_test.go\n"
        )

        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    def test_relative_handle_paths(self):
        self.pyls.long_format = True
        self.pyls.reverse = True
        self.pyls.path = 'parser/parser.go'
        expected_output = (
            "-rw-r--r--  1.6K Nov 17 12:05  ./parser/parser.go\n"
        )

        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    def test_invalid_handle_paths(self):
        self.pyls.long_format = True
        self.pyls.reverse = True
        self.pyls.path = 'parser/parser.go.cscsd'
        expected_output = (
            "error: cannot access 'parser/parser.go.cscsd': No such file or directory"
        )
        output = self.validate_pyls()
        self.assertEqual(output.getvalue().strip(), expected_output)


if __name__ == '__main__':
    unittest.main()
