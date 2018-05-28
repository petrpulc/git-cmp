#!/usr/bin/env python

import argparse

from checkers import *
from utils import load_repository


def parse_arguments():
    parser = argparse.ArgumentParser(description='Compare two Git repositories on selected level '
                                                 'with selected features.')
    parser.add_argument('original', help='path to a repository checked against')
    parser.add_argument('new', help='path to a checked repository')
    parser.add_argument('-v', action='store_true', help='print detailed information')
    parser.add_argument('--level', '-l', choices=['ref', 'commit', 'tree', 'blob'], default='commit',
                        help='level of comparision, default: tree')
    parser.add_argument('--pedantic', '-p', action='store_true',
                        help='checked repository must not contain anything in excess')
    parser.add_argument('--author', '-a', action='store_true',
                        help='check authorship details of commits as well (l>=commit)')
    parser.add_argument('--references', '-r', metavar='refs', nargs='+', help='check only selected references')
    parser.add_argument('--reject-msg', metavar='regex', help='reject commit when "regex" found in commit message')
    parser.add_argument('--ignore-whitespace', choices=['leading', 'both'], default='none',
                        help='ignore leading whitespace in blobs')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    # load repositories
    original = load_repository(args.original)
    new = load_repository(args.new)

    references = references.check(args, original, new)
    commit_mapping = commits.check(args, original, new, references)
    blob_mapping, blob_info = trees.check(args, original, new, commit_mapping)
    blobs.check(args, original, new, blob_mapping, blob_info)
