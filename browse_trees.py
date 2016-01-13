def browse_trees(o_tree, n_tree, commit, path = "/"):
    print("    Folder: {}".format(path))
    
    #skip on same ids
    if o_tree.id == n_tree.id:
        print("      Recursive match")
        return
    
    o_subt = set([e.name for e in o_tree if e.type == 'tree'])
    n_subt = set([e.name for e in n_tree if e.type == 'tree'])
    
    check_diff(o_subt, n_subt, "Subfolder", 6)
    
    o_blobs = set([e.name for e in o_tree if e.type == 'blob'])
    n_blobs = set([e.name for e in n_tree if e.type == 'blob'])
    
    check_diff(o_blobs, n_blobs, "File", 6)
    
    for f in o_blobs:
        blob_mapping[o_tree[f].id] = n_tree[f].id
        blob_info[o_tree[f].id] = {'commit': commit, 'path': path+f}
    
    for f in o_subt:
        browse_trees(original[o_tree[f].id], new[n_tree[f].id], commit, path+f+"/")
