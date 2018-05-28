from utils import check_diff


def __browse_trees(args, original, new, o_tree, n_tree, commit, blob_mapping, blob_info, path="/"):
    print("    Folder: {}".format(path))

    # skip on same ids
    if o_tree.id == n_tree.id:
        print("      Recursive match")
        return

    o_subtree = set(e.name for e in o_tree if e.type == 'tree')
    n_subtree = set(e.name for e in n_tree if e.type == 'tree')

    check_diff(args, o_subtree, n_subtree, "Subfolder", 6)

    o_blobs = set(e.name for e in o_tree if e.type == 'blob')
    n_blobs = set(e.name for e in n_tree if e.type == 'blob')

    check_diff(args, o_blobs, n_blobs, "File", 6)

    for f in o_blobs:
        blob_mapping[o_tree[f].id] = n_tree[f].id
        blob_info[o_tree[f].id] = {'commit': commit, 'path': path + f}

    for f in o_subtree:
        __browse_trees(args, original, new,
                       original[o_tree[f].id], new[n_tree[f].id], commit,
                       blob_mapping, blob_info,
                       path + f + "/")


def check(args, original, new, commit_mapping):
    # check file structures
    print("\n=== Trees")

    blob_mapping = {}
    blob_info = {}

    for o_comm, n_comm in commit_mapping.items():
        print("  Commit {}:".format(n_comm))
        o_tree = original[o_comm].tree
        n_tree = original[n_comm].tree
        __browse_trees(args, original, new, o_tree, n_tree, n_comm, blob_mapping, blob_info)

    print("  OK")
    if args.level == 'tree':
        print("\nRepositories match.")
        exit()
    # check of file structure done

    return blob_mapping, blob_info
