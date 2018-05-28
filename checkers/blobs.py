from common import Common


def check():
    # check of files
    print("\n=== Blobs")
    import difflib

    d = difflib.Differ()

    def comp_n_diff(cmp1, cmp2, diff1, diff2, note):
        if cmp1 != cmp2:
            print("    Contents of file {} in commit {} do not match!".format(Common.blob_info[o_blob]['path'],
                                                                              Common.blob_info[o_blob]['commit']))
            if Common.args.verbose:
                print("Diff{}:".format(note))
                print(''.join(d.compare(diff1, diff2)))
            exit(1)

    for o_blob, n_blob in Common.blob_mapping.items():
        print("  Blob {}:".format(n_blob))

        if Common.args.ignore_whitespace == 'none':
            comp_n_diff(o_blob, n_blob, Common.original[o_blob].data.splitlines(1), Common.new[n_blob].data.splitlines(1), '')
        elif Common.args.ignore_whitespace == 'leading':
            data1 = [l.strip(' \t') for l in Common.original[o_blob].data.splitlines(1)]
            data2 = [l.strip(' \t') for l in Common.new[n_blob].data.splitlines(1)]
            comp_n_diff(data1, data2, data1, data2, ' (leading whitespace ignored)')
        elif Common.args.ignore_whitespace == 'both':
            data1 = [l.strip() + '\n' for l in Common.original[o_blob].data.splitlines()]
            data2 = [l.strip() + '\n' for l in Common.new[n_blob].data.splitlines()]
            comp_n_diff(data1, data2, data1, data2, ' (whitespace ignored)')

    print("  OK")
    print("\nRepositories match.")
    # check of individual files done
