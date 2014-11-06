# -*- coding: utf-8 -*-
"""
Created on Mon May  5 12:32:17 2014
Converts text file attached to edat to csv. Will be converted to function after
it's been thoroughly debugged.
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
        for i_col in range(len(lists)):
            if option == "allNull":
                merged = [lists[i_col][i_row] if lists[i_col][i_row] == "NULL"
                          else merged[i_row] for i_row in range(len(merged))]
            elif option == "allElse":
                merged = [lists[i_col][i_row] if lists[i_col][i_row] != "NULL"
                          else merged[i_row] for i_row in range(len(merged))]
        return merged

# Load the text file as a list.
with open(TEXT_FILE, "r") as text:
    text_list = list(text)

# Remove unicode characters.
filtered_text_list = [stripped(x) for x in text_list]

# Determine where rows begin and end.
row_start_idx = [i for i, x in enumerate(filtered_text_list)
                 if x == "*** LogFrame Start ***"]
row_end_idx = [i for i, x in enumerate(filtered_text_list)
               if x == "*** LogFrame End ***"]

if (len(row_start_idx) != len(row_end_idx) or
        row_start_idx[0] >= row_end_idx[0]):
    raise ValueError("LogFrame Starts and Ends do not match up.")

# Find column headers and remove duplicates.
all_headers = []
data_by_rows = []

for iLog in range(len(row_start_idx)):
    one_row = filtered_text_list[row_start_idx[iLog]+1:row_end_idx[iLog]]
    data_by_rows.append(filtered_text_list[row_start_idx[iLog] + 1:
                                           row_end_idx[iLog]])
    for j_col in range(len(one_row)):
        split_header_idx = one_row[j_col].index(": ")
        all_headers.append(one_row[j_col][:split_header_idx])

unique_headers = list(set(all_headers))

# Preallocate list of lists comprised of NULLs.
null_col = ["NULL"] * (len(row_start_idx)+1)
data_matrix = [null_col[:] for i_col in range(len(unique_headers))]

# Fill list of lists with relevant data from data_by_rows and unique_headers.
for i_col in range(len(unique_headers)):
    data_matrix[i_col][0] = unique_headers[i_col]

for i_row in range(len(row_start_idx)):
    for j_col in range(len(data_by_rows[i_row])):
        split_header_idx = data_by_rows[i_row][j_col].index(": ")
        for kHead in range(len(unique_headers)):
            if (data_by_rows[i_row][j_col][:split_header_idx] ==
                    unique_headers[kHead]):
                data_matrix[kHead][i_row + 1] = (data_by_rows[i_row][j_col]
                                                 [split_header_idx + 2:])

# If a column is all NULLs except for the header and one value at the bottom,
# fill the column up with that bottom value.
for i_col in range(len(data_matrix)):
    null_row_idx = [i for i, x in enumerate(data_matrix[i_col]) if x != "NULL"]
    if len(null_row_idx) == 2 and (null_row_idx[1] == len(data_matrix[i_col]) - 1 or null_row_idx[1] == len(data_matrix[i_col]) - 2):
        data_matrix[i_col][1:len(data_matrix[i_col])] = ([data_matrix[i_col][null_row_idx[1]]] * (len(data_matrix[i_col]) - 1))
    elif any([header in data_matrix[i_col][0] for header in fill_block]):
        for null_row in range(1, len(null_row_idx)):
            data_matrix[i_col][null_row_idx[null_row - 1] + 1:null_row_idx[null_row]] = (data_matrix[i_col][null_row_idx[null_row]] * len(range(null_row_idx[null_row - 1] + 1, null_row_idx[null_row])))

    data_matrix[i_col] = data_matrix[i_col][:len(data_matrix[i_col]) - 2]

# Transpose data_matrix.
transposed_data_matrix = [[row[col] for row in data_matrix] for col in
                          range(len(data_matrix[0]))]

# Replace text headers with edat headers (replacement dict). Unnecessary if
# your processing scripts are built around text files instead of edat files.
transposed_data_matrix[0] = [replacements.get(item, item) for item in
                             transposed_data_matrix[0]]

# Pare data_matrix down based on desired headers
# Create list of columns with relevant headers.
main_array = [transposed_data_matrix[0].index(hed) for hed in header_list]

# Create column from which null index will be created.
null_col_names = null_cols.get(TASK)

nullCol = [main_array[header_list.index(colName)] for colName in
           null_col_names]
nullCols = [data_matrix[colNum] for colNum in nullCol]
mergedNulls = merge_lists(nullCols, "allNulls")
null_idx = sorted([i_row for i_row in range(len(mergedNulls)) if
                   mergedNulls[i_row] == "NULL"], reverse=True)

# Merge any columns that need to be merged.
merge_col_list = merge_cols.get(TASK)
merge_col_names_list = merge_col_names.get(TASK)
merged_cols = []
for i_merge in range(len(merge_col_names_list)):
    merge_col_nums = [transposed_data_matrix[0].index(hed) for hed in
                      merge_col_list[i_merge]]
    merge_cols = [data_matrix[col] for col in merge_col_nums]
    merged_cols.append(merge_lists(merge_cols, "allElse"))
    merged_cols[i_merge][0] = merge_col_names_list[i_merge]

out_struct = [[transposed_data_matrix[i_row][col] for col in main_array] for
              i_row in range(fn.size(transposed_data_matrix, 0))]

# Transpose merged_cols and append them to out_struct.
if len(merged_cols) != 0:
    transposed_merged_cols = [[row[col] for row in merged_cols] for col in
                              range(len(merged_cols[0]))]
    for i_row in range(len(out_struct)):
        out_struct[i_row] = out_struct[i_row] + transposed_merged_cols[i_row]

# Remove all instances of NULL by creating an index of NULL occurrences
# and removing them from out_struct.
[out_struct.pop(null_row) for null_row in null_idx]

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

print("saved " + OUT_FILE)
