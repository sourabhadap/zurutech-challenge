import argparse
from .pyls import Pyts
from .filter_strategy import FilterStrategyFactory
from .sort_strategy import SortStrategyFactory, ReverseSortDecorator
from .output_format import OutputFormatFactory

parser = argparse.ArgumentParser(description="Python ls utility.", usage="python -m pyls [options] [path]",
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-A', action='store_true', help='Include directory entries whose names begin with a dot (.)',
                    default=False)
parser.add_argument('-l', action='store_true', help='Use a long listing format', default=False)
parser.add_argument('-r', action='store_true', help='List subdirectories reverse', default=False)
parser.add_argument('-t', action='store_true', help='List subdirectories by modified time', default=False)
parser.add_argument('--filter', type=str, help='Filter files by specific criteria: files, directories', default='')
parser.add_argument('path', nargs='?', default='',
                    help='Path to the JSON file representing the directory structure')

args = parser.parse_args()

try:
    output_format = OutputFormatFactory.get_output_format("simple")
    sort_strategy = SortStrategyFactory.get_sort_strategy("")
    filter_strategy = FilterStrategyFactory().get_filter_strategy(args.filter)
    if args.l:
        output_format = OutputFormatFactory.get_output_format("long")
    if args.t:
        sort_strategy = SortStrategyFactory().get_sort_strategy("time")
    if args.r:
        sort_strategy = ReverseSortDecorator(sort_strategy)
    if args.filter:
        filter_strategy = FilterStrategyFactory().get_filter_strategy(args.filter)

    manager = Pyts(path=args.path, show_all=args.A, filter_strategy=filter_strategy,
                   sort_strategy=sort_strategy, output_format=output_format)
    manager.execute()
except Exception as e:
    print(str(e))
