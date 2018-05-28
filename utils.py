import pygit2

from common import Common


def load_repository(path):
    try:
        return pygit2.Repository(path)
    except KeyError:
        print("'{}' is not a reposity.".format(path))
        exit(1)


def check_diff(set1, set2, what, offset=0):
    if (set1 - set2) or (Common.args.pedantic and set1 != set2):
        print("{} mismatch!".format(' ' * offset + what))
        if Common.args.verbose:
            if set1 - set2 != set():
                print("{} expected, but not found".format(' ' * offset + ', '.join(set1 - set2)))
            if set2 - set1 != set():
                print("{} found, but not expected".format(' ' * offset + ', '.join(set2 - set1)))
        exit(1)


def check_level_and_exit(level=None):
    if level is None or Common.args.level == level:
        print("\nRepositories match.")
        exit()
