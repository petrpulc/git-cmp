"""
Blob level checker (individual files and file contents).
"""

import sys
from difflib import unified_diff

from common import Common


def __comp_n_diff(data1, data2, blob_sha, note):
    if data1 == data2:
        return

    path = Common.blobs_info[blob_sha]['path']

    print("    Contents of file {} in commit {} do not match!".
          format(path, Common.blobs_info[blob_sha]['commit']))
    if Common.args.verbose:
        try:
            diff = unified_diff(data1, data2, 'a' + path, 'b' + path)

            print("Diff{}:".format(note))
            print(''.join(diff))

        except TypeError:
            print("Binary files, no diff to be shown.")

    exit(1)


def check():
    """
    Run the checker on blobs.
    """
    print("\n=== Blobs")

    for o_blob, n_blob in Common.blobs.items():
        print("  Blob {}:".format(n_blob))

        try:
            original_lines = [l.decode() for l in Common.original[o_blob].data.splitlines(1)]
            new_lines = [l.decode() for l in Common.new[n_blob].data.splitlines(1)]
        except UnicodeDecodeError:
            original_lines = Common.original[o_blob].data
            new_lines = Common.new[n_blob].data

        if Common.args.ignore_whitespace == 'none':
            __comp_n_diff(original_lines, new_lines, o_blob, '')
        elif Common.args.ignore_whitespace == 'leading':
            data1 = [l.lstrip(' \t') for l in original_lines]
            data2 = [l.lstrip(' \t') for l in new_lines]
            __comp_n_diff(data1, data2, o_blob, ' (leading whitespace ignored)')
        elif Common.args.ignore_whitespace == 'both':
            data1 = [l.strip() + '\n' for l in original_lines]
            data2 = [l.strip() + '\n' for l in new_lines]
            __comp_n_diff(data1, data2, o_blob, ' (whitespace ignored)')

    print("  OK")
