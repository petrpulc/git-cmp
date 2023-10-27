"""
Commit level checker (repository structure and commit properties).
"""
import subprocess

from common import Common

def __check_author(o_commit, n_commit):
    if o_commit.author.name != n_commit.author.name:
        Common.add_issue("Commit author name does not match!", f"on commit {n_commit.id}")
    if o_commit.author.email != n_commit.author.email:
        Common.add_issue("Commit author email does not match!", f"on commit {n_commit.id}")


def __check_message(n_commit):
    if Common.reject_msg_regex.search(n_commit.message) is not None:
        Common.add_issue("Commit message contains disallowed content!", f"on commit {n_commit.id}")


def __check_commits_and_return_hint(o_commit, n_commit):
    """
    Compare original and new commits.
    :return: Whether reference graph should be listed or not
    """
    # do not check again, but detect clashes
    if o_commit.id in Common.commits:
        if n_commit.id != Common.commits[o_commit.id]:
            Common.add_issue("Commit mapping clash.", f"of commits {n_commit.id} and {Common.commits[o_commit.id]}")
            return True
        return False

    if Common.args.author:
        __check_author(o_commit, n_commit)
    if Common.reject_msg_regex:
        __check_message(n_commit)

    # check number of parents
    o_parents = o_commit.parents
    n_parents = n_commit.parents
    if len(o_parents) != len(n_parents):
        Common.add_issue(f"Commit {n_commit.id} has bad number of parents.",
                         f"{len(o_parents)} parents expected, {len(n_parents)} present")
        return True

    # store to hash of mapped commits
    Common.commits[o_commit.id] = n_commit.id

    # stop if root
    if not o_parents:
        return False

    # continue in same branch
    if __check_commits_and_return_hint(o_parents[0], n_parents[0]):
        return True

    # check length of subtrees
    for i in range(1, len(o_parents)):
        o_sublen = len(list(Common.original.walk(o_parents[i].id)))
        n_sublen = len(list(Common.new.walk(n_parents[i].id)))
        if o_sublen != n_sublen:
            Common.add_issue(f'Walk from parent {n_parents[i].id} differs in length!',
                             f"walk of length {o_sublen} expected, {n_sublen} found")
            return True

        if __check_commits_and_return_hint(o_parents[i], n_parents[i]):
            return True
    return False


def __print__hint(o_commit, n_commit):
    Common.add_issue('Expecting repository structure:',
                     subprocess.Popen(f"git log --oneline --graph --format=%s {o_commit.id}",
                                      env={'GIT_DIR': Common.original.path},
                                      shell=True, stdout=subprocess.PIPE).stdout.read().decode())
    Common.add_issue('Submitted repository structure:',
                     subprocess.Popen(f"git log --oneline --graph --format=%s {n_commit.id}",
                                      env={'GIT_DIR': Common.new.path},
                                      shell=True, stdout=subprocess.PIPE).stdout.read().decode())


def check():
    """
    Run the checker on commits.
    """
    for reference in Common.references:
        o_commit = Common.original.lookup_reference(reference).peel()
        n_commit = Common.new.lookup_reference(reference).peel()
        if __check_commits_and_return_hint(o_commit, n_commit) and Common.args.verbose:
            __print__hint(o_commit, n_commit)
