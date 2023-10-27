"""
Common variable and method module.
"""
import re


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
    # message refusal regex
    reject_msg_regex = None

    # blob mapping and info
    blobs = {}
    blobs_info = {}

    # issues collected along the way
    issues = []

    @classmethod
    def add_issue(cls, msg, detail=""):
        cls.issues.append((msg, detail))

    @classmethod
    def compile_args(cls, args):
        cls.args = args
        if cls.args.reject_msg:
            cls.reject_msg_regex = re.compile(args.reject_msg)
