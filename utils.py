"""
Various helper functions and utilities.
"""

import pygit2

from common import Common


def load_repository(path):
    """
    Load repository object.
    :param path: Path to repository.
    """
    try:
        return pygit2.Repository(path)
    except pygit2.GitError:
        Common.add_issue("'{}' is not a repository.".format(path))


def check_diff(set1, set2, what):
    """
    Check difference of two sets of values and inform user accordingly.

    :param set1: First set.
    :param set2: Second set.
    :param what: Text description of compared value.
    """
    if (set1 - set2) or (Common.args.pedantic and set1 != set2):
        detail = ""
        if set1 - set2:
            detail = f"{', '.join(set1 - set2)} expected, but not found"
        if set2 - set1:
            detail = f"{', '.join(set2 - set1)} found, but not expected"
        Common.add_issue(f"{what} mismatch!", detail)


def check_issues_and_exit():
    """
    Check if there are any issues and if so, quit.
    """
    if Common.issues:
        print("Found issues:")
        for issue in Common.issues:
            print(f"- {issue[0]}")
            if issue[1] and Common.args.verbose:
                print(f"{issue[1]}")
                print()
        exit(1)
