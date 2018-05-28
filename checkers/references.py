"""
Reference level checker (existence of given references or all refs/heads ans refs/tags).
"""

from common import Common
from utils import check_diff


def __filter(reference_list):
    return set(reference for reference in
               reference_list if reference.split('/')[1] in ('heads', 'tags'))


def check():
    """
    Run the checker on references.
    """
    print("=== References")
    if Common.args.references is None:
        o_refs = __filter(Common.original.listall_references())
        n_refs = __filter(Common.new.listall_references())
        check_diff(o_refs, n_refs, "References", 2)
    else:
        o_refs = set()
        for reference in Common.args.references:
            if reference not in Common.original.listall_references():
                print("  {} does not exist, please report".format(reference))
                exit(1)
            if reference not in Common.new.listall_references():
                print("  {} expected, but not found".format(reference))
                exit(1)
            o_refs.add(reference)

    print("  OK")
    Common.references = o_refs
