# -*- coding: utf-8 -*-
"""
Created on Mon May  5 12:32:17 2014
Converts text file attached to edat to csv.
@author: tsalo
"""

#pylint: disable-msg=C0103
import os
import pickle
import inspect
import csv
import numpy.core.fromnumeric as fn

code_dir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))


op = "/home/tsalo/Desktop/FAST/"
TEXT_FILE = op + "RISE_FMRI_ItemRecoga&bVer1-FASTpilot001-1.txt"
PAIR_FILE = op + "RISE_FMRI_ItemRecoga&bVer1-FASTpilot001-1.edat2"
OUT_FILE = op + "FASTpilot001-1_IR.csv"
WHOLE_TEXT_FILE = '/home/tsalo/Desktop/FAST/stuff.csv'
TASK = "FAST_RISE_IR"

with open(code_dir + "/headers.pickle") as file_:
        [headers, replace_dict, fill_block, merge_cols, merge_col_names,
         null_cols] = pickle.load(file_)

[filename, suffix] = os.path.splitext(PAIR_FILE)

header_list = headers.get(TASK)

replacements = replace_dict.get(TASK).get(suffix)


def try_index(list_, val):
    """
    Indexes a list without throwing an error if the value isn't found.
    """
    try:
        return list_.index(val)
    except:
        print(val)
        pass


def stripped(string):
    """
    Removes unicode characters in string.
    """
    return "".join([val for val in string if 31 < ord(val) < 127])


def merge_lists(lists, option):
    """
    Merges multiple lists into one list, with the default being the values of
    the first list. It either replaces values with NULL if NULL is in that
    position in another list or replaces NULL with values if values are in that
    position in another list.
    """
    if type(lists[0]) != list:
        return lists
    else:
        merged = lists[0]
        for iCol in range(len(lists)):
            if option == "allNull":
                merged = [lists[iCol][iRow] if lists[iCol][iRow] == "NULL" else
                          merged[iRow] for iRow in range(len(merged))]
            elif option == "allElse":
                merged = [lists[iCol][iRow] if lists[iCol][iRow] != "NULL" else
                          merged[iRow] for iRow in range(len(merged))]
        return merged

with open(TEXT_FILE, "r") as text:
    text_list = list(text)

# Remove unicode characters.
filtered = [stripped(x) for x in text_list]

initIdx = [i for i, x in enumerate(filtered) if x == "*** LogFrame Start ***"]
endIdx = [i for i, x in enumerate(filtered) if x == "*** LogFrame End ***"]

if len(initIdx) != len(endIdx) or initIdx[0] >= endIdx[0]:
    raise ValueError("LogFrame Starts and Ends do not match up.")

all_headers = []
unsplit_list = []

# Find column headers and remove duplicates.
for iLog in range(len(initIdx)):
    one_row = filtered[initIdx[iLog]+1:endIdx[iLog]]
    unsplit_list.append(filtered[initIdx[iLog]+1:endIdx[iLog]])
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
tmat = [[row[col] for row in mat] for col in range(len(mat[0]))]

# Replace text headers with edat headers (replacement dict). Unnecessary if
# your processing scripts are built around text files instead of edat files.
tmat[0] = [replacements.get(item, item) for item in tmat[0]]

fo = open(WHOLE_TEXT_FILE, 'wb')
file_ = csv.writer(fo)
for row in tmat:
    file_.writerow(row)
fo.close()

# Pare mat down based on desired headers
# Create list of columns with relevant headers.
main_array = [tmat[0].index(hed) for hed in header_list]

# Create column from which null index will be created.
null_col_names = null_cols.get(TASK)

nullCol = [main_array[header_list.index(colName)] for colName in
           null_col_names]
nullCols = [mat[colNum] for colNum in nullCol]
mergedNulls = merge_lists(nullCols, "allNulls")
null_idx = sorted([iRow for iRow in range(len(mergedNulls)) if
                   mergedNulls[iRow] == "NULL"], reverse=True)

# Merge any columns that need to be merged.
mergeColList = merge_cols.get(TASK)
mergeColNameList = merge_col_names.get(TASK)
mergedCols = []
for iMerge in range(len(mergeColNameList)):
    mergeColNums = [tmat[0].index(hed) for hed in mergeColList[iMerge]]
    mergeCols = [mat[col] for col in mergeColNums]
    mergedCols.append(merge_lists(mergeCols, "allElse"))
    mergedCols[iMerge][0] = mergeColNameList[iMerge]

out_struct = [[tmat[iRow][col] for col in main_array] for iRow in
              range(fn.size(tmat, 0))]

# Transpose mergedCols
if len(mergedCols) != 0:
    tmergedCols = [[row[col] for row in mergedCols] for col in
                   range(len(mergedCols[0]))]
    for iRow in range(len(out_struct)):
        out_struct[iRow] = out_struct[iRow] + tmergedCols[iRow]

# Remove all instances of NULL by creating an index of NULL occurrences
# and removing them from out_struct.
[out_struct.pop(i) for i in null_idx]

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
