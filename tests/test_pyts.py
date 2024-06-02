import unittest
from io import StringIO
import sys
import pyls
from pyls.output_format import OutputFormatFactory
from pyls.sort_strategy import SortStrategyFactory, ReverseSortDecorator
from pyls.filter_strategy import FilterStrategyFactory
from pyls.exceptions import InvalidFilter


class TestPyts(unittest.TestCase):

    def setUp(self):
        output_format = OutputFormatFactory.get_output_format("simple")
        sort_strategy = SortStrategyFactory.get_sort_strategy("")
        filter_strategy = FilterStrategyFactory().get_filter_strategy("")
        self.pyls = pyls.Pyts(
            path='',
            show_all=False,
            output_format=output_format,
            sort_strategy=sort_strategy,
            filter_strategy=filter_strategy,
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
        output_format = OutputFormatFactory.get_output_format("long")
        self.pyls.output_format = output_format
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
        output_format = OutputFormatFactory.get_output_format("long")
        sort_strategy = ReverseSortDecorator(self.pyls.sort_strategy)
        self.pyls.output_format = output_format
        self.pyls.sort_strategy = sort_strategy
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

        output_format = OutputFormatFactory.get_output_format("long")
        sort_strategy = SortStrategyFactory.get_sort_strategy("time")
        sort_strategy = ReverseSortDecorator(sort_strategy)
        self.pyls.output_format = output_format
        self.pyls.sort_strategy = sort_strategy
        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    def test_print_long_format_in_reverse_with_time_modified_dir_filter(self):
        expected_output = (
            "drwxr-xr-x  4.0K Nov 17 12:51 parser\n"
            "drwxr-xr-x  4.0K Nov 14 15:58 ast\n"
            "drwxr-xr-x  4.0K Nov 14 15:21 lexer\n"
            "drwxr-xr-x  4.0K Nov 14 14:57 token\n"
        )

        output_format = OutputFormatFactory.get_output_format("long")
        sort_strategy = SortStrategyFactory.get_sort_strategy("time")
        sort_strategy = ReverseSortDecorator(sort_strategy)
        filter_strategy = FilterStrategyFactory.get_filter_strategy("dir")
        self.pyls.filter_strategy = filter_strategy
        self.pyls.output_format = output_format
        self.pyls.sort_strategy = sort_strategy
        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    def test_print_long_format_in_reverse_with_time_modified_file_filter(self):
        expected_output = (
            "-rw-r--r--    74 Nov 14 13:57 main.go\n"
            "-rw-r--r--    60 Nov 14 13:51 go.mod\n"
            "-rw-r--r--    83 Nov 14 11:27 README.md\n"
            "-rw-r--r--  1.0K Nov 14 11:27 LICENSE\n"
        )

        output_format = OutputFormatFactory.get_output_format("long")
        sort_strategy = SortStrategyFactory.get_sort_strategy("time")
        sort_strategy = ReverseSortDecorator(sort_strategy)
        filter_strategy = FilterStrategyFactory.get_filter_strategy("file")
        self.pyls.filter_strategy = filter_strategy
        self.pyls.output_format = output_format
        self.pyls.sort_strategy = sort_strategy
        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    #
    def test_print_long_format_in_reverse_with_time_modified_invalid_filter(self):
        expected_output = "error: filewsd is not a valid filter criteria. Available filters are 'dir' and 'file'"

        output_format = OutputFormatFactory.get_output_format("long")
        sort_strategy = SortStrategyFactory.get_sort_strategy("time")
        sort_strategy = ReverseSortDecorator(sort_strategy)
        with self.assertRaises(InvalidFilter) as cm:
            filter_strategy = FilterStrategyFactory.get_filter_strategy("filewsd")
            self.pyls.filter_strategy = filter_strategy
            self.pyls.output_format = output_format
            self.pyls.sort_strategy = sort_strategy
            output = self.validate_pyls()
        self.assertEqual(str(cm.exception.__str__()), expected_output)

    def test_handle_paths(self):
        expected_output = (
            "-rw-r--r--   533 Nov 14 16:03 go.mod\n"
            "-rw-r--r--  1.6K Nov 17 12:05 parser.go\n"
            "-rw-r--r--  1.3K Nov 17 12:51 parser_test.go\n"
        )
        output_format = OutputFormatFactory.get_output_format("long")
        sort_strategy = ReverseSortDecorator(self.pyls.sort_strategy)
        self.pyls.output_format = output_format
        self.pyls.sort_strategy = sort_strategy
        self.pyls.path = "parser"
        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    def test_relative_handle_paths(self):
        expected_output = (
            "-rw-r--r--  1.6K Nov 17 12:05  ./parser/parser.go\n"
        )
        output_format = OutputFormatFactory.get_output_format("long")
        sort_strategy = ReverseSortDecorator(self.pyls.sort_strategy)
        self.pyls.output_format = output_format
        self.pyls.sort_strategy = sort_strategy
        self.pyls.path = 'parser/parser.go'
        output = self.validate_pyls()
        self.assertEqual(output.getvalue(), expected_output)

    def test_invalid_handle_paths(self):
        expected_output = (
            "error: cannot access 'parser/parser.go.cscsd': No such file or directory"
        )
        output_format = OutputFormatFactory.get_output_format("long")
        sort_strategy = ReverseSortDecorator(self.pyls.sort_strategy)
        self.pyls.output_format = output_format
        self.pyls.sort_strategy = sort_strategy
        self.pyls.path = 'parser/parser.go.cscsd'
        output = self.validate_pyls()
        self.assertEqual(output.getvalue().strip(), expected_output)


if __name__ == '__main__':
    unittest.main()
