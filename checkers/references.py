from utils import check_diff


def __filter(reference_list):
    return set(reference for reference in
               reference_list if reference.split('/')[1] in ('heads', 'tags'))


def check(args, original, new):
    # check references (and filter only heads and tags)
    print("=== References")
    if args.references is None:
        o_refs = __filter(original.listall_references())
        n_refs = __filter(new.listall_references())
        check_diff(args, o_refs, n_refs, "References", 2)
    else:
        o_refs = set()
        for reference in args.references:
            if reference not in original.listall_references():
                print("  {} does not exist, please report".format(reference))
                exit(1)
            if reference not in new.listall_references():
                print("  {} expected, but not found".format(reference))
                exit(1)
            o_refs.add(reference)

    print("  OK")
    if args.level == 'ref':
        print("\nRepositories match.")
        exit()
    # reference check done

    return o_refs
