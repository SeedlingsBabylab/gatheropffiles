import os
import sys
import shutil


def correct_name(name):
    if "sparse_code.opf" in name and\
        (name[3:5] == month or month == "--all"):
        return True
    return False

def walk_tree(start):
    for root, dirs, files in os.walk(start):
        if "Video_Annotation" in root:
            for file in files:
                if correct_name(file):
                    shutil.copy(os.path.join(root, file),
                                os.path.join(out, file))

if __name__ == "__main__":

    start = sys.argv[1]
    out = sys.argv[2]

    month = sys.argv[3]

    walk_tree(start)
