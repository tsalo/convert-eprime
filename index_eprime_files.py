# -*- coding: utf-8 -*-
"""
Created on Thu May 22 14:09:37 2014
Designed to check for the existence of paired edat/text files in a folder.
It will flag text files that do not have a paired edat or which have a paired
text (two text files).
Somewhat functional, but barely readable, as of 150209.
@author: tsalo
"""
import os
import glob
import re
import pandas as pd
import time
import shutil
import sys

note_dict = {
    "one_text": "One text file- must be recovered.",
    "two_texts": "Two text files- must be merged.",
    "three_files": "One edat and two text files- it's a thinker.",
    "pair": "All good.",
    "one_edat": "One edat- unknown problem.",
    }

timepoint_dict = {
    "EP2_AX": {
        "1": "00_MONTH",
        "2": "06_MONTH",
        "3": "12_MONTH",
        "4": "24_MONTH",
        },
    "bEP2_AX": {
        "1": "00_MONTH",
        "2": "06_MONTH",
        "3": "12_MONTH",
        "4": "24_MONTH",
        },
    "EP2_ICET": {
        "1": "00_MONTH",
        "2": "12_MONTH",
        "3": "24_MONTH",
        }
    }

org_dir_dict = {"EP2_AX": "Z:\\Behavioral_Data\\3.0T\\AX-CPT_EP2\\organized\\",
                "bEP2_AX": "Z:\\Behavioral_Data\\BehavBehav\\AX-CPT_EP2\\organized\\",
                "EP2_ICET": "Z:\\Behavioral_Data\\3.0T\\ICE-T_EP2\\organized\\",}

global note_dict, timepoint_dict, org_dir_dict


def add_subject(csv_data, subj, timepoint, orged, orgedwhen, orgedby, conved,
                convedwhen, convedby, notes):
    """
    Adds information about subject's data to spreadsheet.
    """
    row = pd.DataFrame([dict(Subject=subj, Timepoint=timepoint,
                             Organized=orged, Date_Organized=orgedwhen,
                             Organized_by=orgedby, Converted=conved,
                             Date_Converted=convedwhen, Converted_by=convedby,
                             Notes=notes)])
    csv_data = csv_data.append(row, ignore_index=False)
    return csv_data


def get_subject(text_file):
    """
    Splits file name by hyphens to determine subject ID.
    """
    path_name, sf = os.path.splitext(text_file)
    fname = os.path.basename(path_name)
    fname = fname.replace("-Left_Handed", "")
    all_hyphens = [m.start() for m in re.finditer('-', fname)]
    if len(all_hyphens) == 1:
        beg = fname[:len(fname)-2].rindex('_')
    else:
        beg = all_hyphens[-2]

    end = all_hyphens[-1]
    subj = fname[beg+1:end]
    subj = subj.lower()

    return subj


def get_timepoint(text_file):
    """
    Splits file name by hyphens to determine timepoint.
    """
    path_with_filename, sf = os.path.splitext(text_file)
    fname = os.path.basename(path_with_filename)
    fname = fname.replace("-Left_Handed", "")

    # I forget what this does.
    all_underscores = [m.start() for m in re.finditer('_', fname)]
    last_hyphen = fname.rindex('-')
    if not all_underscores:
        tp = fname[-1]
    elif all_underscores[-1] < last_hyphen:
        tp = fname[-1]
    else:
        tp = fname[all_underscores[-1]]

    return tp


def organize_files(subject_id, timepoint, files, organized_dir):
    """
    If there are no problems, copies edat and text files with known subject ID
    and timepoint to organized directory and moves those files in the raw data dir
    to a "done" subfolder.
    
    If the file already exists in the destination directory, it does not copy or
    move the file and returns a note to that effect.
    """
    note = ""
    for file_ in files:
        orig_dir, file_name = os.path.split(file_)
        
        # Create the destination dir if it doesn't already exist.
        org_dir = os.path.join(organized_dir, subject_id, timepoint)
        if not os.path.exists(org_dir):
            os.makedirs(org_dir)

        # If the file does not exist in the destination dir, copy it there and
        # move the original to a "done" subdir.
        # If it does, return a note saying that the file exists.
        if os.path.isfile(org_dir + file_name):
            note += "File {0} already exists in {1}. ".format(file_name, org_dir)
        else:
            shutil.copy(file_, org_dir)
            out_dir = os.path.join(orig_dir, "done", os.sep)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            shutil.move(file_, out_dir)

    return note


def main(directory, csv_file, task_name):
    """
    This does so much. It needs to be documented and thoroughly commented.
    """
    csv_data = pd.read_csv(csv_file)
    colnames = csv_data.columns.tolist()

    edat_files = glob.glob(directory + "*.edat*")
    text_files = glob.glob(directory + "*-*.txt")
    all_files = edat_files + text_files
    pairs = []
    paired_texts = []

    for text_file in text_files:
        [text_fname, _] = os.path.splitext(text_file)
        for edat_file in edat_files:
            [edat_fname, _] = os.path.splitext(edat_file)
            if text_fname == edat_fname:
                pairs.append([text_file, edat_file])

    for pair in pairs:
        paired_texts.append(pair[0])

    unpaired_texts = list(set(text_files) - set(paired_texts))
    three_files = []
    pop_idx = []

    # List of lists
    for i_file in range(len(unpaired_texts)):
        for j_pair in range(len(paired_texts)):
            if (unpaired_texts[i_file][:len(unpaired_texts[i_file])-6] in paired_texts[j_pair]):
                three_files.append([paired_texts[j_pair], pairs[j_pair][1],
                                    unpaired_texts[i_file]])
                pop_idx.append(i_file)

    for rm in reversed(pop_idx):
        unpaired_texts.pop(rm)

    # three_files is the text files and edats that form a triad (one edat, two
    # similarly named text files).
    for triad in three_files:
        for i_pair in reversed(range(len(pairs))):
            if triad[0:2] == pairs[i_pair]:
                pairs.pop(i_pair)

    two_texts = []
    all_two_texts = []
    two_text_pairs = []

    for i_file in range(len(unpaired_texts)):
        for j_file in range(i_file + 1, len(unpaired_texts)):
            if (unpaired_texts[i_file][:len(unpaired_texts[i_file])-6] in unpaired_texts[j_file]):
                all_two_texts.append(i_file)
                all_two_texts.append(j_file)
                two_text_pairs.append([i_file, j_file])

    all_two_texts = sorted(all_two_texts, reverse=True)

    # two_texts is the text files that pair with other text files.
    for i_pair in range(len(two_text_pairs)):
        two_texts.append([unpaired_texts[two_text_pairs[i_pair][0]],
                         unpaired_texts[two_text_pairs[i_pair][1]]])

    for i_file in all_two_texts:
        unpaired_texts.pop(i_file)

    # one_text is the remaining un-paired text files.
    one_text = [[unpaired_texts[i_file]] for i_file in range(len(unpaired_texts))]

    # Determine subject IDs and timepoints for all files.
    # Assumes that files will be named according to convention
    # blahblahblah_[subj]-[tp].txt or blahblahblah-[subj]-[tp].txt.
    one_text_subjects = [get_subject(file_[0]) for file_ in one_text]
    one_text_timepoints = [get_timepoint(file_[0]) for file_ in one_text]
    two_text_subjects = [get_subject(pair[0]) for pair in two_texts]
    two_text_timepoints = [get_timepoint(pair[0]) for pair in two_texts]
    three_file_subjects = [get_subject(triad[0]) for triad in three_files]
    three_file_timepoints = [get_timepoint(triad[0]) for triad in three_files]
    pair_subjects = [get_subject(pair[0]) for pair in pairs]
    pair_timepoints = [get_timepoint(pair[0]) for pair in pairs]

    af_files = ([item for sublist in pairs for item in sublist] +
                [item for sublist in two_texts for item in sublist] +
                [item for sublist in three_files for item in sublist] +
                [item for sublist in one_text for item in sublist])

    one_edat = list(set(all_files) - set(af_files))
    one_edat = [[edat] for edat in one_edat]
    one_edat_subjects = [get_subject(file_[0]) for file_ in one_edat]
    one_edat_timepoints = [get_timepoint(file_[0]) for file_ in one_edat]

    all_subjects = (one_text_subjects + two_text_subjects + three_file_subjects +
                    pair_subjects + one_edat_subjects)
    all_notetype = ((["one_text"] * len(one_text_subjects)) +
                    (["two_texts"] * len(two_text_subjects)) +
                    (["three_files"] * len(three_file_subjects)) +
                    (["pair"] * len(pair_subjects)) +
                    (["one_edat"] * len(one_edat_subjects)))
    all_timepoints = (one_text_timepoints + two_text_timepoints +
                      three_file_timepoints + pair_timepoints +
                      one_edat_timepoints)
    all_file_sets = one_text + two_texts + three_files + pairs + one_edat

    organized_dir = org_dir_dict.get(task_name)

    for i_subj in range(len(all_subjects)):
        month = timepoint_dict.get(task_name).get(all_timepoints[i_subj])
        files_note = note_dict.get(all_notetype[i_subj])
        if len(all_subjects) > 4:
            try:
                print("Successfully organized %s-%s" % (all_subjects[i_subj], month))
                print("Moved:")
                subject_id = all_subjects[i_subj]
                files = all_file_sets[i_subj]
                note = organize_files(subject_id, month, files, organized_dir)
                note.append(files_note)
                orged = 1
                orgedwhen = time.strftime("%Y/%m/%d")
                orgedby = "PY"
            except IOError:
                print("%s-%s couldn't be organized." % (all_subjects[i_subj], all_timepoints[i_subj]))
                note = files_note
                orged = 0
                orgedwhen = ""
                orgedby = ""

            try:
                if all_notetype[i_subj] == "pair":
                    print("Successfully converted %s-%s" % (all_subjects[i_subj], all_timepoints[i_subj]))
                    conved = 1
                    convedwhen = time.strftime("%Y/%m/%d")
                    convedby = "PY"
                else:
                    print("%s-%s couldn't be converted." % (all_subjects[i_subj], all_timepoints[i_subj]))
                    conved = 0
                    convedwhen = ""
                    convedby = ""
            except IOError:
                print("%s-%s couldn't be converted." % (all_subjects[i_subj], all_timepoints[i_subj]))
                conved = 0
                convedwhen = ""
                convedby = ""
        else:
            print("%s-%s couldn't be organized." % (all_subjects[i_subj], all_timepoints[i_subj]))
            note = files_note
            orged = 0
            orgedwhen = ""
            orgedby = ""
            print("%s-%s couldn't be converted." % (all_subjects[i_subj], all_timepoints[i_subj]))
            conved = 0
            convedwhen = ""
            convedby = ""

        csv_data = add_subject(csv_data, all_subjects[i_subj],
                               all_timepoints[i_subj], orged, orgedwhen, orgedby,
                               conved, convedwhen, convedby, note)

    csv_data = csv_data[colnames]
    csv_data.to_csv(csv_file, index=False)


if __name__ == "__main__":
    """
    If you call this function from the shell, the arguments are assumed
    to be the raw data directory, the organization csv file, and the
    task_name, in that order.
    """
    main(sys.argv[1], sys.argv[2], sys.argv[3])
