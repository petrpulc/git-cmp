"""
Blob level checker (individual files and file contents).
"""

from difflib import unified_diff
from termcolor import colored

from common import Common


def __get_diff(data1, data2, path):
    try:
        diff = list(unified_diff(data1, data2, 'a' + path, 'b' + path))

        buffer = ["Diff:\n"]

        buffer.extend(diff[:2])

        buffer.append(colored(diff[2], "cyan", force_color=True))

        for row in diff[3:]:
            row_buffer = ""

            if row.startswith('+'):
                colour = "green"
            elif row.startswith('-'):
                colour = "red"
            else:
                colour = None

            clean = row.rstrip()
            row_buffer += colored(clean, colour, force_color=True)

            if len(row) > 2 and len(clean) < len(row) - 1:
                row_buffer += colored(row[len(clean):-1], on_color="on_red", force_color=True)
            buffer.append(row_buffer + "\n")

    except TypeError:
        buffer = ["Binary files, no diff to be shown."]

    return ''.join(buffer)


def __comp_n_diff(data1, data2, blob_sha, note):
    if data1 == data2:
        return

    path = Common.blobs_info[blob_sha]['path']

    Common.add_issue(f"Contents of file {path} in commit {Common.blobs_info[blob_sha]['commit']} do not match!{note}",
                     __get_diff(data1, data2, path))


def check():
    """
    Run the checker on blobs.
    """
    for o_blob, n_blob in Common.blobs.items():
        if o_blob == n_blob:
            continue

        try:
            original_lines = [l.decode() for l in Common.original[o_blob].data.splitlines(1)]
            new_lines = [l.decode() for l in Common.new[n_blob].data.splitlines(1)]
        except UnicodeDecodeError:
            original_lines = Common.original[o_blob].data
            new_lines = Common.new[n_blob].data

        if Common.args.ignore_whitespace == 'none' or type(new_lines[0]) is not str:
            __comp_n_diff(original_lines, new_lines, o_blob, '')
        elif Common.args.ignore_whitespace == 'leading':
            data1 = [l.lstrip(' \t') for l in original_lines]
            data2 = [l.lstrip(' \t') for l in new_lines]
            __comp_n_diff(data1, data2, o_blob, ' (leading whitespace ignored)')
        elif Common.args.ignore_whitespace == 'both':
            data1 = [l.strip() + '\n' for l in original_lines]
            data2 = [l.strip() + '\n' for l in new_lines]
            __comp_n_diff(data1, data2, o_blob, ' (whitespace ignored)')
