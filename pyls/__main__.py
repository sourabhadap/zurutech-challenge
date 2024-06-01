import argparse
from pyls.pyls import Pyls

parser = argparse.ArgumentParser(description="Python ls utility.", usage="python -m pyls [options] [path]",
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-A', action='store_true', help='Include directory entries whose names begin with a dot (.)',
                    default=False)
parser.add_argument('-l', action='store_true', help='Use a long listing format', default=False)
parser.add_argument('-r', action='store_true', help='List subdirectories reverse', default=False)
parser.add_argument('-t', action='store_true', help='List subdirectories by modified time', default=False)
parser.add_argument('--filter', type=str, help='Filter files by specific criteria: files, directories')
parser.add_argument('path', nargs='?', default=None,
                    help='Path to the JSON file representing the directory structure')

args = parser.parse_args()
pyls = Pyls(
    path=args.path,
    show_all=args.A,
    long_format=args.l,
    reverse=args.r,
    sort_by_time=args.t,
    filter_option=args.filter
)
pyls.execute()
