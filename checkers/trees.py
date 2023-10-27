"""
Tree level checker (existence of files and folders).
"""

from common import Common
from utils import check_diff, check_issues_and_exit


def __browse_trees(o_tree, n_tree, commit, path="/"):
    # skip on same ids
    if o_tree.id == n_tree.id:
        return

    o_subtree = set(e.name for e in o_tree if e.type_str == 'tree')
    n_subtree = set(e.name for e in n_tree if e.type_str == 'tree')

    check_diff(o_subtree, n_subtree, "Folder")
    check_issues_and_exit()

    o_blobs = set(e.name for e in o_tree if e.type_str == 'blob')
    n_blobs = set(e.name for e in n_tree if e.type_str == 'blob')

    check_diff(o_blobs, n_blobs, "File")
    check_issues_and_exit()

    for blob in o_blobs:
        Common.blobs[o_tree[blob].id] = n_tree[blob].id
        Common.blobs_info[o_tree[blob].id] = {'commit': commit, 'path': path + blob}

    for tree in o_subtree:
        __browse_trees(Common.original[o_tree[tree].id],
                       Common.new[n_tree[tree].id],
                       commit, path + tree + "/")


def check():
    """
    Run the checker on tree objects.
    """

    for o_comm, n_comm in Common.commits.items():
        o_tree = Common.original[o_comm].tree
        n_tree = Common.new[n_comm].tree
        __browse_trees(o_tree, n_tree, n_comm)
