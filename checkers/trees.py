from common import Common
from utils import check_diff


def __browse_trees(o_tree, n_tree, commit, path="/"):
    print("    Folder: {}".format(path))

    # skip on same ids
    if o_tree.id == n_tree.id:
        print("      Recursive match")
        return

    o_subtree = set(e.name for e in o_tree if e.type == 'tree')
    n_subtree = set(e.name for e in n_tree if e.type == 'tree')

    check_diff(o_subtree, n_subtree, "Subfolder", 6)

    o_blobs = set(e.name for e in o_tree if e.type == 'blob')
    n_blobs = set(e.name for e in n_tree if e.type == 'blob')

    check_diff(o_blobs, n_blobs, "File", 6)

    for f in o_blobs:
        Common.blobs[o_tree[f].id] = n_tree[f].id
        Common.blobs_info[o_tree[f].id] = {'commit': commit, 'path': path + f}

    for f in o_subtree:
        __browse_trees(Common.original[o_tree[f].id], Common.new[n_tree[f].id], commit, path + f + "/")


def check():
    # check file structures
    print("\n=== Trees")

    Common.blobs = {}
    Common.blobs_info = {}

    for o_comm, n_comm in Common.commits.items():
        print("  Commit {}:".format(n_comm))
        o_tree = Common.original[o_comm].tree
        n_tree = Common.new[n_comm].tree
        __browse_trees(o_tree, n_tree, n_comm)

    print("  OK")
    if Common.args.level == 'tree':
        print("\nRepositories match.")
        exit()
