import re

def browse_commits(o_commit, n_commit):
    if args.v:
        print("    ? {} == {}".format(o_commit.id, n_commit.id))
    else:
        print("    Commit {}".format(n_commit.id))
    
    #do not check again, detect clashes
    if o_commit.id in commit_mapping:
        if n_commit.id == commit_mapping[o_commit.id]:
            return
        else:
            if args.v:
                print("      ! {} -> {}".format(o_commit.id, commit_mapping[o_commit.id]))
            print("      Bad structure of repository, commit clash with: {}".format(commit_mapping[o_commit.id]))
            exit(1)
        
    if args.author:
        if o_commit.author.name != n_commit.author.name:
            print("      Commit author name does not match!")
            exit(1)
        if o_commit.author.email != n_commit.author.email:
            print("      Commit author email does not match!")
            exit(1)
    
    if args.reject_msg:
        reg = re.compile(args.reject_msg)
        if reg.search(n_commit.message) != None:
            print("      Commit message contains not allowed content!")
            if args.v:
                print("      ({})").format(args.reject_msg)
            exit(1)
        
    #check number of parents
    o_parents = o_commit.parents
    n_parents = n_commit.parents
    if len(o_parents) != len(n_parents):
        if args.v:
            print("      ! {} parents expected, {} present".format(len(o_parents), len(n_parents)))
        print("      Commit does not have same number of parents!")
        exit(1)
        
    #store to hash f mapped commits
    commit_mapping[o_commit.id] = n_commit.id
    
    #stop if root
    if len(o_parents) == 0:
        return
    
    #continue in same branch
    browse_commits(o_parents[0], n_parents[0])
    
    #check length of subtrees
    for i in range(1,len(o_parents)):
        o_sublen = sum(1 for _ in original.walk(o_parents[i].id))
        n_sublen = sum(1 for _ in new.walk(n_parents[i].id))
        if o_sublen != n_sublen:
            if args.v:
                print("      ! walk of length {} expected, {} found".format(o_sublen, n_sublen))
            print("      Walk from parent {} differs in length!".format(n_parents[i].id))
            exit(1)
        
        browse_commits(o_parents[i], n_parents[i])
