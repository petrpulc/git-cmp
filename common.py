class Common:
    # values from argument parser
    args = None

    # original repository
    original = None
    # compared repository
    new = None

    # references to be checked
    references = None

    # mapping of commits
    commit_mapping = None

    # blob mapping and info
    blob_mapping = None
    blob_info = None
