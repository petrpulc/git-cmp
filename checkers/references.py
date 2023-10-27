"""
Reference level checker (existence of given references or all refs/heads ans refs/tags).
"""

from common import Common
from utils import check_diff


def __filter(reference_list):
    """
    Filter out only heads and tags.
    """
    return set(reference for reference in
               reference_list if reference.split('/')[1] in ('heads', 'tags'))


def check():
    """
    Run the checker on references.
    """
    if Common.args.references is None:
        o_refs = __filter(Common.original.listall_references())
        n_refs = __filter(Common.new.listall_references())
        check_diff(o_refs, n_refs, "References")
    else:
        o_refs = set()
        for reference in Common.args.references:
            if reference not in Common.original.listall_references():
                Common.add_issue(f"Reference {reference} does not exist, please report.")
            if reference not in Common.new.listall_references():
                Common.add_issue(f"Reference {reference} expected, but not found")
            o_refs.add(reference)

    Common.references = o_refs
