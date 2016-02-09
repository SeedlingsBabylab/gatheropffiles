import sys
import os
from shutil import copy
import os
import csv

start_dir = ""
final_directory = "/Users/andrei/code/work/babylab/opffiles"


empty_vid_anot_folders = []
single_opf_in_dir = []
nofinal_but_consensus = []

no_files = []


single_opf_nofinal=["01_14_coderVL.opf",
                    "01_13_coderSK.opf",
                    "19_11_coderJH.opf",
                    "31_07_coderVL.opf",
                    "17_09_coderEB.opf",
                    "28_07_coderAR.opf",
                    "11_10_coderEB.opf",
                    "27_06_coderJH.opf",
                    "32_06_coderJH.opf",
                    "04_10_coderAS.opf",
                    "04_09_coderSM.opf",
                    "26_06_coderAS.opf",
                    "26_07_coderEB.opf",
                    "26_09_coderEB.opf",
                    "29_07_coderEB.opf",
                    "29_12_coderSD.opf",
                    "42_07_coderSK.opf",
                    "43_07_coderTE.opf",
                    "15_12_coderLN.opf",
                    "07_11_CoderSM.opf"]


personal_dictionary = []
def init_personalinfo_dictionary():
    for i in range(47):
        personal_dictionary.append(["no-pi"]*13)

def walk_tree():
    for root, dirs, files in os.walk(start_dir):
        if os.path.split(root)[1] == "Video_Annotation":
            print "root: {}".format(root)
            print "dirs: {}".format(dirs)
            print "files: {}".format(files)

            for file in files:
                if "_final.opf" in file:
                    copy(os.path.join(root, file), final_directory)


def find_empty_folders():
    for root, dirs, files in os.walk(start_dir):
        if os.path.split(root)[1] == "Video_Annotation":
            print "root: {}".format(root)
            print "dirs: {}".format(dirs)
            print "files: {}".format(files)

            if len(files) == 0:
                empty_vid_anot_folders.append(root)

            opf_files = [x for x in files if ".opf" in x]

            if len(opf_files) == 1:
                single_opf_in_dir.append(opf_files[0])

            if len(opf_files) > 1:
                if any("consensus" in x for x in opf_files):


    with open("empty_vid_annot_dirs", "wb") as file:
        for dir in empty_vid_anot_folders:
            file.write(dir+"\n")

    single_opf_nofinal = [x for x in single_opf_in_dir if 'final' not in x]
    with open("single_opf_in_dir", "wb") as output:
        for dir in single_opf_nofinal:
            output.write(dir+"\n")

def fill_pidictionary_with_nofile():
    subj_prefix = ""
    visit_prefix = ""

    nofile_count = 0
    all_files = list_of_all_files()
    for i, subject in enumerate(personal_dictionary[1:]):
        #print "i: {}".format(i)
        for j, visit in enumerate(subject):
            if i <9:
                subj_prefix = '0'+str(i+1)
            else:
                subj_prefix = str(i+1)

            visit_prefix = str(array_to_prefix(j))

            prefix = subj_prefix+"_"+visit_prefix


            if not any(prefix in x for x in all_files):
                #print "prefix: {}".format(prefix)
                #print "no file"
                no_files.append(prefix)
                personal_dictionary[i+1][j] = "NO-FILE"
                nofile_count += 1

    print "\n\nnofile_count: {}".format(nofile_count)

def check_if_file_exists(prefix):
    for file in list_of_all_files():
        if prefix in file:
            return True
    return False


def prefix_to_array(prefix):
    if prefix == '06':
        return 0
    elif prefix == '07':
        return 1
    elif prefix == '08':
        return 2
    elif prefix == '09':
        return 3
    elif prefix == '10':
        return 4
    elif prefix == '11':
        return 5
    elif prefix == '12':
        return 6
    elif prefix == '13':
        return 7
    elif prefix == '14':
        return 8
    elif prefix == '15':
        return 9
    elif prefix == '16':
        return 10
    elif prefix == '17':
        return 11
    elif prefix == '18':
        return 12

def array_to_prefix(array):
    if array == 0:
        return '06'
    elif array == 1:
        return '07'
    elif array == 2:
        return '08'
    elif array == 3:
        return '09'
    elif array == 4:
        return '10'
    elif array == 5:
        return '11'
    elif array == 6:
        return '12'
    elif array == 7:
        return '13'
    elif array == 8:
        return '14'
    elif array == 9:
        return '15'
    elif array == 10:
        return '16'
    elif array == 11:
        return '17'
    elif array == 12:
        return '18'

def list_of_all_files():
    return os.listdir("data/opf_files") + os.listdir("data/single_opf_nofinal")

def list_of_pinfo_files():
    return os.listdir("data/pinfo_files") + os.listdir("data/single_opf_nofinal/personal_info_files")

def generate_nopersonalinfo_files():

    pinfo_files = list_of_pinfo_files()
    for file in set(pinfo_files):
        if ".DS" in file:
            continue
        prefix = file[0:5].split("_")
        #print "original: {}".format(prefix)
        prefix = [int(prefix[0]), prefix_to_array(prefix[1])]
        #print "new: {}".format(prefix)

        personal_dictionary[prefix[0]][prefix[1]] = "**PI**"
    with open("opf_personalinfo_table.csv", "wb") as table:
        writer = csv.writer(table)
        writer.writerow(["subject-visit", "06", "07", "08", "09", "10",
                         "11", "12", "13", "14", "15", "16", "17", "18"])
        for index, subject in enumerate(personal_dictionary[1:]):
            writer.writerow([index+1] + subject)

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
    #start_dir = sys.argv[1]
    #init_personalinfo_dictionary()
    #fill_pidictionary_with_nofile()
    #generate_nopersonalinfo_files()
    # output_no_files()
    #find_empty_folders()
    empty_folders_to_list()