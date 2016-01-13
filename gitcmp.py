#!/usr/bin/env python

import argparse
import pygit2

parser = argparse.ArgumentParser(description='Compare two Git repositories on selected level with selected features.')
parser.add_argument('original', help='path to a repository checked against')
parser.add_argument('new', help='path to a checked repository')
parser.add_argument('-v', action='store_true', help='print detailed information')
parser.add_argument('--level', '-l', choices=['ref','commit','tree','blob'], default='commit', help='level of comparation, default: tree')
parser.add_argument('--pedantic', '-p', action='store_true', help='checked repository must not contain anything in excess')
parser.add_argument('--author', '-a', action='store_true', help='chech authorship details of commits as well (l>=commit)')

args = parser.parse_args()

#construct repos
try:
    original = pygit2.Repository(args.original)
except KeyError:
    print("'{}' is not a reposity.".format(args.original))
    exit(1)

try:
    new = pygit2.Repository(args.new)
except KeyError:
    print("'{}' is not a reposity.".format(args.new))
    exit(1)
    
    
def check_diff(set1, set2, what, offset=0):
    if (set1 - set2 or (args.pedantic and set1 != set2)):
        print("{} mismatch!".format(' '*offset + what))
        if args.v:
            if set1 - set2 != set():
                print("{} expected, but not found".format(' '*offset + ', '.join(set1-set2)))
            if set2 - set1 != set():
                print("{} found, but not expected".format(' '*offset + ', '.join(set2-set1)))
        exit(1)



#check refernces (and filter only heads)
print("=== References")
o_refs = set(ref for ref in original.listall_references() if ref.split('/')[1] == 'heads')
n_refs = set(ref for ref in new.listall_references() if ref.split('/')[1] == 'heads')

check_diff(o_refs, n_refs, "References", 2)

print("  OK")
if args.level == 'ref':
    print("\nRepositories match.")
    exit()
#reference check done


#check commits
print("\n=== Commits")

execfile('browse_commits.py')

commit_mapping = {}

for ref in o_refs:
    print("  Browsing {}:".format(ref))
    browse_commits(original.lookup_reference(ref).peel(), new.lookup_reference(ref).peel())

print("  OK")
if args.level == 'commit':
    print("\nRepositories match.")
    exit()
#commit structure check done


#check file structures
print("\n=== Trees")
execfile('browse_trees.py')

blob_mapping = {}
blob_info = {}

for o_comm, n_comm in commit_mapping.iteritems():
    print("  Commit {}:".format(n_comm))
    browse_trees(original[o_comm].tree, new[n_comm].tree, n_comm)

print("  OK")
if args.level == 'tree':
    print("\nRepositories match.")
    exit()
#check of file structure done


#check of files
print("\n=== Blobs")
import difflib
d = difflib.Differ()

for o_blob, n_blob in blob_mapping.iteritems():
    print("  Blob {}:".format(n_blob))
    if o_blob != n_blob:
        print("    Contents of file {} in commit {} do not match!".format(blob_info[o_blob]['path'], blob_info[o_blob]['commit']))
        if args.v:
            print("Diff:")
            print(''.join(d.compare(original[o_blob].data.splitlines(1), new[n_blob].data.splitlines(1))))
        exit(1)

print("  OK")
print("\nRepositories match.")
exit()
#check of individual files done

