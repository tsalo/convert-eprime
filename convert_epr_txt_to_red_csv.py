# -*- coding: utf-8 -*-
"""
Created on Mon May  5 12:32:17 2014
Converts text file attached to edat to csv.
@author: tsalo
"""

#pylint: disable-msg=C0103
#import edit_csv as ec
import os
import pickle
import inspect
import csv
import numpy.core.fromnumeric as fn

code_dir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))

TEXT_FILE = "/home/tsalo/eprime_files_140801/EP2_AXCPT_Run1_epc164-4.txt"
PAIR_FILE = "/home/tsalo/eprime_files_140801/EP2_AXCPT_Run1_epc164-4.edat2"
OUT_FILE = "/home/tsalo/eprime_files_140801/epc164_4.csv"
TASK = "EP2_AX"

with open(code_dir + "/headers.pickle") as file_:
        [headers, replace_dict, fill_block] = pickle.load(file_)

[filename, suffix] = os.path.splitext(PAIR_FILE)

header_list = headers.get(TASK)

replacements = replace_dict.get(suffix)


def try_index(list_, val):
    """
    Indexes a list without throwing an error if the value isn't found.
    """
    try:
        return list_.index(val)
    except:
        pass


def stripped(string):
    """
    Removes unicode characters in string.
    """
    return "".join([val for val in string if 31 < ord(val) < 127])

with open(TEXT_FILE, "r") as text:
    text_list = list(text)

# Remove unicode characters.
filtered2 = [stripped(x) for x in text_list]

initIdx = [i for i, x in enumerate(filtered2) if x == "*** LogFrame Start ***"]
endIdx = [i for i, x in enumerate(filtered2) if x == "*** LogFrame End ***"]

if len(initIdx) != len(endIdx) or initIdx[0] >= endIdx[0]:
    raise ValueError("LogFrame Starts and Ends do not match up.")

all_headers = []
unsplit_list = []

# Find column headers and remove duplicates.
for iLog in range(len(initIdx)):
    one_row = filtered2[initIdx[iLog]+1:endIdx[iLog]]
    unsplit_list.append(filtered2[initIdx[iLog]+1:endIdx[iLog]])
    for jCol in range(len(one_row)):
        splitIdx = one_row[jCol].index(": ")
        all_headers.append(one_row[jCol][:splitIdx])

unique_headers = list(set(all_headers))

# Preallocate list of lists comprised of NULLs.
arr = ["NULL"] * (len(initIdx)+1)
mat = [arr[:] for i in range(len(unique_headers))]

# Fill list of lists with relevant data from unsplit_list and unique_headers.
for iCol in range(len(unique_headers)):
    mat[iCol][0] = unique_headers[iCol]

for iRow in range(len(initIdx)):
    for jCol in range(len(unsplit_list[iRow])):
        splitIdx = unsplit_list[iRow][jCol].index(": ")
        for kHead in range(len(unique_headers)):
            if unsplit_list[iRow][jCol][:splitIdx] == unique_headers[kHead]:
                mat[kHead][iRow+1] = unsplit_list[iRow][jCol][splitIdx+2:]

# If a column is all NULLs except for the header and one value at the bottom,
# fill the column up with that bottom value.
for iCol in range(len(mat)):
    nullIdx = [i for i, x in enumerate(mat[iCol]) if x != "NULL"]
    if len(nullIdx) == 2 and (nullIdx[1] == len(mat[iCol])-1
                              or nullIdx[1] == len(mat[iCol])-2):
        mat[iCol][1:len(mat[iCol])] = ([mat[iCol][nullIdx[1]]] *
                                      (len(mat[iCol])-1))
    elif any([header in mat[iCol][0] for header in fill_block]):
        for s in range(1, len(nullIdx)):
            mat[iCol][nullIdx[s-1]+1:nullIdx[s]] = (mat[iCol][nullIdx[s]] *
                                                    len(range(nullIdx[s-1]+1,
                                                              nullIdx[s])))

    mat[iCol] = mat[iCol][:len(mat[iCol])-2]

# Transpose mat.
mat = [[row[col] for row in mat] for col in range(len(mat[0]))]

# Replace text headers with edat headers (replacement dict). Unnecessary if
# your processing scripts are built around text files instead of edat files.
mat[0] = [replacements.get(item, item) for item in mat[0]]

# Pare mat down based on desired headers
# Create list of columns with relevant headers.
main_array = [try_index(mat[0], hed) for hed in header_list if
              try_index(mat[0], hed) is not None]

# Make empty (zeros) list of lists and fill with relevant data from
# wholefile.
out_struct = [[mat[iRow][col] for col in main_array]
              for iRow in range(fn.size(mat, 0))]

# Remove all instances of NULL by creating an index of NULL occurrences
# and removing them from out_struct.
null_idx = [list(set([iRow for col in out_struct[iRow] if col == "NULL"]))
            for iRow in range(fn.size(out_struct, 0))]
null_idx = sorted([val for sublist in null_idx for val in sublist],
                  reverse=True)
[out_struct.pop(i) for i in null_idx]

# Write out csv.
#ec.write(out_struct, OUT_FILE)

try:
    fo = open(OUT_FILE, 'wb')
    file_ = csv.writer(fo)
    for row in out_struct:
        file_.writerow(row)

    print("Output file successfully created- %s" % OUT_FILE)
except IOError:
    print("Can't open output file- %s" % OUT_FILE)
finally:
    fo.close()

#print("saved " + OUT_FILE)
