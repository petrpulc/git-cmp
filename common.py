"""
Common variable and method module.
"""


class Common:
    """
    Singleton storage for variables used during comparison.
    """
    # values from argument parser
    args = None

    # original repository
    original = None
    # compared repository
    new = None

    # references to be checked
    references = None

    # mapping of commits
    commits = {}

    # blob mapping and info
    blobs = {}
    blobs_info = {}
