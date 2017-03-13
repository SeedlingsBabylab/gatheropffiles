import sys
import os
from shutil import copy
import os
import csv

start_dir = ""
final_directory = ""


empty_vid_anot_folders = []
single_opf_in_dir = []
nofinal_but_consensus = []

no_files = []


def walk_tree(month=None):
    for root, dirs, files in os.walk(start_dir):
        if os.path.split(root)[1] == "Video_Annotation":
            for file in files:
                if "_final.opf" in file:
                    if month:
                        if right_month(file, month):
                            copy(os.path.join(root, file), final_directory)
                    else:
                        copy(os.path.join(root, file), final_directory)

def right_month(file, month):
    if file[3:5] == month:
        return True
    return False


def find_empty_folders():
    for root, dirs, files in os.walk(start_dir):
        if os.path.split(root)[1] == "Video_Annotation":
            # print "root: {}".format(root)
            # print "dirs: {}".format(dirs)
            # print "files: {}".format(files)

            if len(files) == 0:
                empty_vid_anot_folders.append(root)

            opf_files = [x for x in files if ".opf" in x]

            if len(opf_files) == 1:
                single_opf_in_dir.append(opf_files[0])

            if len(opf_files) > 1:
                consensus = False
                final = False
                consensus_files = []
                for file in opf_files:
                    if "consensus" in file and "final" not in file:
                        consensus = True
                        consensus_files.append(file)
                    if "final" in file:
                        final = True

                if not final and consensus:
                    if len(consensus_files) > 1:
                        print "there were a bunch of consensus files: {}".format(consensus_files)
                    nofinal_but_consensus.append(consensus_files[0])

    with open("empty_vid_annot_dirs", "wb") as file:
        for dir in empty_vid_anot_folders:
            file.write(dir+"\n")

    single_opf_nofinal = [x for x in single_opf_in_dir if 'final' not in x]
    with open("single_opf_in_dir", "wb") as output:
        for dir in single_opf_nofinal:
            output.write(dir+"\n")

    with open("nofinal_but_consensus", "wb") as consensus:
        for entry in nofinal_but_consensus:
            consensus.write(entry+"\n")


def output_no_files():

    without_18 = [x for x in no_files if x[3:] != '18']
    with open("no_files", "wb") as file:
        for entry in without_18:
            file.write(entry+"\n")
    print "without_18 count: {}".format(len(without_18))


def empty_folders_to_list():
    paths = []
    with open("empty_vid_annot_dirs", "rU") as input:
        for line in input:
            paths.append(line)

    split_paths = [x.split("/") for x in paths]
    subj_visit = [x[-4] for x in split_paths]

    print subj_visit

if __name__ == "__main__":
    start_dir = sys.argv[1]
    final_directory = sys.argv[2]

    if len(sys.argv) > 3:
        month = sys.argv[3]
        walk_tree(month)
    else:
        walk_tree()


    # output_no_files()
    # find_empty_folders()
    # empty_folders_to_list()
