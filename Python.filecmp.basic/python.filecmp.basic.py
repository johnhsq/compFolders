# import os
import filecmp
# import itertools

dir1="/Users/huang/Documents/Workspace/python.folder.compare/dir1/"
dir2="/Users/huang/Documents/Workspace/python.folder.compare/dir2/"

# compare files
print("===== compare files =====")
print(filecmp.cmp(dir1+'file1.txt',dir2+"file1.txt"))
print(filecmp.cmp(dir1+'file1.txt',dir2+"file1.txt", shallow = False))
print(filecmp.cmp(dir1+'file2.txt',dir2+"file2.txt"))


match, mismatch, errors = filecmp.cmpfiles(dir1,dir2,['file1.txt','file2.txt'])
print(match)
print(mismatch)
print(errors)

# compare dir
print("===== compare dir =====")
result = filecmp.dircmp(dir1, dir2)
result.report()

print("=== folder name ===")
print(result.left)  # folder name
print(result.right)

print("=== files and subfolders  ===")
print(result.left_list) # file and subfolder
print(result.right_list)

print("=== common ===")
print(result.common)    # commom subfolder and files
print(result.common_files) # common files only
print(result.common_dirs) # common subfolders only

print("=== file result ===")
print(result.same_files)
print(result.diff_files)

# recursively compare subfolders and files
print("===== recursively compare subfolders")
def print_diff_files(dcmp):
    for diff_file in dcmp.diff_files:
        print("different files: %s found in %s and %s" % (diff_file, dcmp.left, dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

dcmp = filecmp.dircmp(dir1, dir2) 
print_diff_files(dcmp) 