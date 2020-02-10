"""
Commit level checker (repository structure and commit properties).
"""

import re

from common import Common


def __check_author(o_commit, n_commit):
    if not Common.args.author:
        return
    if o_commit.author.name != n_commit.author.name:
        print("      Commit author name does not match!")
        if not Common.args.print_all:
            exit(1)
    if o_commit.author.email != n_commit.author.email:
        print("      Commit author email does not match!")
        if not Common.args.print_all:
            exit(1)


def __check_message(n_commit):
    if not Common.args.reject_msg:
        return
    regexp = re.compile(Common.args.reject_msg)
    if regexp.search(n_commit.message) is not None:
        print("      Commit message contains not allowed content!")
        if Common.args.verbose:
            print("      ({})").format(Common.args.reject_msg)
        if not Common.args.print_all:
            exit(1)


def __browse_commits(o_commit, n_commit):
    if Common.args.verbose:
        print("    ? {} == {}".format(o_commit.id, n_commit.id))
    else:
        print("    Commit {}".format(n_commit.id))

    # do not check again, detect clashes
    if o_commit.id in Common.commits:
        if n_commit.id == Common.commits[o_commit.id]:
            return
        else:
            if Common.args.verbose:
                print("      ! {} -> {}".format(o_commit.id, Common.commits[o_commit.id]))
            print("      Bad structure of repository, commit clash with: {}".
                  format(Common.commits[o_commit.id]))
            if not Common.args.print_all:
                exit(1)

    __check_author(o_commit, n_commit)
    __check_message(n_commit)

    # check number of parents
    o_parents = o_commit.parents
    n_parents = n_commit.parents
    if len(o_parents) != len(n_parents):
        if Common.args.verbose:
            print("      ! {} parents expected, {} present".format(len(o_parents), len(n_parents)))
        print("      Commit does not have same number of parents!")
        if not Common.args.print_all:
            exit(1)

    # store to hash of mapped commits
    Common.commits[o_commit.id] = n_commit.id

    # stop if root
    if not o_parents:
        return

    # continue in same branch
    __browse_commits(o_parents[0], n_parents[0])

    # check length of subtrees
    for i in range(1, len(o_parents)):
        o_sublen = sum(1 for _ in Common.original.walk(o_parents[i].id))
        n_sublen = sum(1 for _ in Common.new.walk(n_parents[i].id))
        if o_sublen != n_sublen:
            if Common.args.verbose:
                print("      ! walk of length {} expected, {} found".format(o_sublen, n_sublen))
            print("      Walk from parent {} differs in length!".format(n_parents[i].id))
            if not Common.args.print_all:
                exit(1)

        __browse_commits(o_parents[i], n_parents[i])


def check():
    """
    Run the checker on commits.
    """
    print("\n=== Commits")

    for reference in Common.references:
        print("  Browsing {}:".format(reference))
        o_commit = Common.original.lookup_reference(reference).peel()
        n_commit = Common.new.lookup_reference(reference).peel()
        __browse_commits(o_commit, n_commit)

    print("  OK")
