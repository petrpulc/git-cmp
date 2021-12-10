"""
Tree level checker (existence of files and folders).
"""

from common import Common
from utils import check_diff


def __browse_trees(o_tree, n_tree, commit, path="/"):
    Common.lazy_print("    Folder: {}".format(path))

    # skip on same ids
    if o_tree.id == n_tree.id:
        Common.lazy_print("      Recursive match")
        return

    o_subtree = set(e.name for e in o_tree if e.type == 'tree')
    n_subtree = set(e.name for e in n_tree if e.type == 'tree')

    check_diff(o_subtree, n_subtree, "Folder", 6)

    o_blobs = set(e.name for e in o_tree if e.type == 'blob')
    n_blobs = set(e.name for e in n_tree if e.type == 'blob')

    check_diff(o_blobs, n_blobs, "File", 6)

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
    Common.lazy_print("\n=== Trees")

    for o_comm, n_comm in Common.commits.items():
        Common.lazy_print("  Commit {}:".format(n_comm))
        o_tree = Common.original[o_comm].tree
        n_tree = Common.new[n_comm].tree
        __browse_trees(o_tree, n_tree, n_comm)

    Common.lazy_print("  OK")
