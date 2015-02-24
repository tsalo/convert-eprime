# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:03:47 2014
Input: path to edat text file, task/study ID.
Output: none, but creates and saves a csv file in same directory with same
name as input (with csv extension, obviously).

Converts edat text file to csv containing only relevant data. Meant to replace
series of perl scripts currently in use. To add a new task/study, simply add
an entry to the dictionary headers with the task/study ID as the key and the
list of relevant column names as the definition. The headers must be an exact
match for those found in the edat text for the function to work.
@author: salo
"""
import os
import sys
import csv
import numpy.core.fromnumeric as fn
import pickle
import inspect

code_dir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
with open(code_dir + "/headers.pickle") as file_:
    [headers, remnulls, _, _, _, _, _] = pickle.load(file_)

def main(in_file, task):
    header_list = headers.get(task)
    delimiter_, rem_lines = _det_file_type(in_file)
    try:
        wholefile = list(csv.reader(open(in_file, "rb"),
                                    delimiter=delimiter_))
        main_array = []
    except IOError:
        print("Can't open input file- %s" % in_file)

    # Remove first three rows.
    for iRow in range(rem_lines):
        wholefile.pop(0)

    # Create list of columns with relevant headers.
    main_array = [try_index(wholefile[0], hed) for hed in header_list if
                  try_index(wholefile[0], hed) is not None]

    # Make empty (zeros) list of lists and fill with relevant data from
    # wholefile.
    out_arr = [[wholefile[iRow][col] for col in main_array]
               for iRow in range(fn.size(wholefile, 0))]

    # Either remove all instances of NULL or convert all instances of NULL to
    # NaN.
    if remnulls.get(task):
        null_idx = [list(set([iRow for col in out_arr[iRow] if col == "NULL"]))
                    for iRow in range(fn.size(out_arr, 0))]
        null_idx = sorted([val for sublist in null_idx for val in sublist],
                          reverse=True)
        [out_arr.pop(i) for i in null_idx]
    else:
        out_arr = [[word.replace("NULL", "NaN") for word in row]
                   for row in out_arr]

    # Write out and save csv file.
    outfile = in_file[:len(in_file)-3] + "csv"
    try:
        fo = open(outfile, "wb")
        file_ = csv.writer(fo)
        for row in out_arr:
            file_.writerow(row)

        print("Output file successfully created- %s" % outfile)
    except IOError:
        print("Can't open output file- %s" % outfile)
    finally:
        fo.close()


def try_index(list_, val):
    try:
        return list_.index(val)
    except:
        pass


def _det_file_type(in_file):
    [fn, sf] = os.path.splitext(in_file)
    if sf == ".csv":
        delimiter_ = ","
        rem_lines = 0
    elif sf == ".txt":
        delimiter_ = "\t"
        rem_lines = 3
    elif len(in_file) == 0:
        raise ValueError("Input file name is empty.")
    else:
        raise ValueError("Input file name is not .csv or .txt.")

    return delimiter_, rem_lines


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
