#!/usr/bin/env python3
"""
Main entry point to git repository comparator.
"""

import argparse

from checkers import references, commits, trees, blobs
from common import Common
from utils import load_repository, check_level_and_exit


def parse_arguments():
    """
    Method used to setup argument parser and store parsed data.
    """
    parser = argparse.ArgumentParser(description='Compare two Git repositories on selected level '
                                                 'with selected features.')
    parser.add_argument('original', help='path to a repository checked against')
    parser.add_argument('new', help='path to a checked repository')
    parser.add_argument('--verbose', '-v', action='store_true', help='print detailed information')
    parser.add_argument('--level', '-l', choices=['ref', 'commit', 'tree', 'blob'],
                        default='commit', help='level of comparision, default: commit')
    parser.add_argument('--pedantic', '-p', action='store_true',
                        help='checked repository must not contain anything in excess')
    parser.add_argument('--author', '-a', action='store_true',
                        help='check authorship details of commits as well (l>=commit)')
    parser.add_argument('--references', '-r', metavar='refs', nargs='+',
                        help='check only selected references')
    parser.add_argument('--reject-msg', metavar='regex',
                        help='reject commit when "regex" found in commit message')
    parser.add_argument('--ignore-whitespace', choices=['leading', 'both'], default='none',
                        help='ignore leading whitespace in blobs')

    Common.args = parser.parse_args()


if __name__ == "__main__":
    parse_arguments()

    # load repositories
    Common.original = load_repository(Common.args.original)
    Common.new = load_repository(Common.args.new)

    references.check()
    check_level_and_exit('ref')

    commits.check()
    check_level_and_exit('commit')

    trees.check()
    check_level_and_exit('tree')

    blobs.check()
    check_level_and_exit()
