# -*- coding: utf-8 -*-
"""
Created on Thu May 22 14:09:37 2014
Designed to check for the existence of paired edat/text files in a folder.
It will flag text files that do not have a paired edat or who have a paired
text (two text files).
@author: tsalo
"""
import os
import glob
import re
import pandas as pd
import time

CSVFILE = "/home/tsalo/AX_Archive_050814/behav_sheet.csv"
DIRECTORY = "/home/tsalo/AX_Archive_050814/"
task = "EP2_AX"
csvData = pd.read_csv(CSVFILE)
colnames = csvData.columns.tolist()

note_dict = {
    "one_text": "One text file- must be recovered.",
    "two_texts": "Two text files- must be merged.",
    "three_files": "One edat and two text files- it's a thinker.",
    "pair": "All good.",
    "uaf": "One edat- unknown problem.",
    }

tp_dict = {
    "EP2_AX": {
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


def get_subject(text_file):
    path_name, sf = os.path.splitext(text_file)
    fname = os.path.basename(path_name)

    all_hyphens = [m.start() for m in re.finditer('-', fname)]
    if len(all_hyphens) == 1:
        beg = fname[:len(fname) - 2].rindex('_')
    elif len(all_hyphens) == 2:
        beg = fname.index('-')
    else:
        raise ValueError("Input file name has too many hyphens :-( .")

    end = fname.rindex('-')
    subj = fname[beg + 1:end]
    subj = subj.lower()
    return subj


def get_timepoint(text_file):
    path_name, sf = os.path.splitext(text_file)
    fname = os.path.basename(path_name)
    last_hyph = fname.rindex('-')
    tp = fname[last_hyph + 1]
    return tp


def add_subject(csvData, subj, timepoint, orged, orgedwhen, conved, convedwhen,
                notes):
    row = pd.DataFrame([dict(Subject=subj, Timepoint=timepoint,
                             Organized=orged, Date_Organized=orgedwhen,
                             Converted=conved, Date_Converted=convedwhen,
                             Notes=notes)])
    csvData = csvData.append(row, ignore_index=False)
    return csvData

edat_files = glob.glob(DIRECTORY + "*.edat*")
text_files = glob.glob(DIRECTORY + "*-*.txt")
all_files = edat_files + text_files
pair = []
p_txt = []

for i in text_files:
    [text_fname, sf] = os.path.splitext(i)
    for j in edat_files:
        [edat_fname, sf] = os.path.splitext(j)
        if text_fname == edat_fname:
            pair.append([i, j])

for i in pair:
    p_txt.append(i[0])

up_txt = list(set(text_files) - set(p_txt))

three_files = []
pop_idx = []

# List of lists
for iText in range(len(up_txt)):
    for jP in range(len(p_txt)):
        if up_txt[iText][:len(up_txt[iText])-6] in p_txt[jP]:
            three_files.append([p_txt[jP], pair[jP][1], up_txt[iText]])
            pop_idx.append(iText)

for rm in reversed(pop_idx):
    up_txt.pop(rm)

# three_files is the text files and edats that form a triad (one edat, two
# similafrom __future__ import print_functionrly named text files).
for rm in three_files:
    for stuff in reversed(range(len(pair))):
        if rm[0:2] == pair[stuff]:
            pair.pop(stuff)

two_text = []
all_tt = []
tt_pr = []

for p1 in range(len(up_txt)):
    for p2 in range(p1 + 1, len(up_txt)):
        if up_txt[p1][:len(up_txt[p1])-6] in up_txt[p2]:
            all_tt.append(p1)
            all_tt.append(p2)
            tt_pr.append([p1, p2])

all_tt = sorted(all_tt, reverse=True)

# two_text is the text files that pair with other text files.
for i in range(len(tt_pr)):
    two_text.append([up_txt[tt_pr[i][0]], up_txt[tt_pr[i][1]]])

for i in all_tt:
    up_txt.pop(i)

# one_text is the remaining un-paired text files.
one_text = [[up_txt[i]] for i in range(len(up_txt))]

ot_subj = [get_subject(one_text[i][0]) for i in range(len(one_text))]
ot_tp = [get_timepoint(one_text[i][0]) for i in range(len(one_text))]
tt_subj = [get_subject(two_text[i][0]) for i in range(len(two_text))]
tt_tp = [get_timepoint(two_text[i][0]) for i in range(len(two_text))]
tf_subj = [get_subject(three_files[i][0]) for i in range(len(three_files))]
tf_tp = [get_timepoint(three_files[i][0]) for i in range(len(three_files))]
p_subj = [get_subject(pair[i][0]) for i in range(len(pair))]
p_tp = [get_timepoint(pair[i][0]) for i in range(len(pair))]

af_files = ([item for sublist in pair for item in sublist] +
            [item for sublist in two_text for item in sublist] +
            [item for sublist in three_files for item in sublist] +
            [item for sublist in one_text for item in sublist])

uaf_files = list(set(all_files) - set(af_files))
uaf_files = [[uaf_files[i]] for i in range(len(uaf_files))]
uaf_subj = [get_subject(uaf_files[i][0]) for i in range(len(uaf_files))]
uaf_tp = [get_timepoint(uaf_files[i][0]) for i in range(len(uaf_files))]

all_subj = ot_subj + tt_subj + tf_subj + p_subj + uaf_subj
all_notetype = ((["one_text"] * len(ot_subj)) +
               (["two_texts"] * len(tt_subj)) +
               (["three_files"] * len(tf_subj)) +
               (["pair"] * len(p_subj)) +
               (["uaf"] * len(uaf_subj)))
all_tp = ot_tp + tt_tp + tf_tp + p_tp + uaf_tp
al_files = one_text + two_text + three_files + pair + uaf_files

for i in range(len(all_subj)):
    # Problem 1- How to make organization section as general as possible.
    month = tp_dict.get(task).get(all_tp[i])
    try:
        print("Successfully organized %s-%s" % (all_subj[i], month))
        print("Moved:")
        for dude in al_files[i]:
            print(dude)
        orged = 1
        orgedwhen = time.strftime("%Y/%m/%d")
    except IOError:
        print("%s-%s couldn't be organized." % (all_subj[i], all_tp[i]))
        orged = 0
        orgedwhen = ""

    try:
        if all_notetype[i] == "pair":
            print("Successfully converted %s-%s" % (all_subj[i], all_tp[i]))
            conved = 1
            convedwhen = time.strftime("%Y/%m/%d")
        else:
            print("%s-%s couldn't be converted." % (all_subj[i], all_tp[i]))
            conved = 0
            convedwhen = ""
    except IOError:
        print("%s-%s couldn't be converted." % (all_subj[i], all_tp[i]))
        conved = 0
        convedwhen = ""

    csvData = add_subject(csvData, all_subj[i], all_tp[i], orged,
                          orgedwhen, conved, convedwhen,
                          note_dict.get(all_notetype[i]))

csvData = csvData[colnames]
