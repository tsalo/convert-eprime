# -*- coding: utf-8 -*-
"""
Created on Mon May  5 12:32:17 2014
Converts text file attached to edat to csv.
@author: tsalo
"""

#pylint: disable-msg=C0103
import csv
import sys


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


def main(text_file, out_file):
    # Load the text file as a list.
    with open(text_file, "r") as text:
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

    # Preallocate list of lists composed of NULLs.
    null_col = ["NULL"] * (len(row_start_idx)+1)
    data_matrix = [null_col[:] for i_col in range(len(unique_headers))]

    # Fill list of lists with relevant data from data_by_rows and
    # unique_headers.
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

    # If a column is all NULLs except for the header and one value at the
    # bottom, fill the column up with that bottom value.
    for i_col in range(len(data_matrix)):
        null_row_idx = [i for i, x in enumerate(data_matrix[i_col]) if x != "NULL"]
        if len(null_row_idx) == 2 and (null_row_idx[1] == len(data_matrix[i_col]) - 1 or null_row_idx[1] == len(data_matrix[i_col]) - 2):
            data_matrix[i_col][1:len(data_matrix[i_col])] = ([data_matrix[i_col][null_row_idx[1]]] * (len(data_matrix[i_col]) - 1))

        data_matrix[i_col] = data_matrix[i_col][:len(data_matrix[i_col]) - 2]

    # Transpose data_matrix.
    transposed_data_matrix = [[row[col] for row in data_matrix] for col in
                              range(len(data_matrix[0]))]

    try:
        fo = open(out_file, 'wb')
        file_ = csv.writer(fo)
        for row in transposed_data_matrix:
            file_.writerow(row)

        print("Output file successfully created- %s" % out_file)
    except IOError:
        print("Can't open output file- %s" % out_file)
    finally:
        fo.close()

    print("Saved " + out_file)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
