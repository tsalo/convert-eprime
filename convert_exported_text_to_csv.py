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

HEADERS = {
    'EP_AX': ['Subject', 'Group', 'ExperimentName', 'Session', 'Age',
              'Handedness', 'Sex', 'Block', 'Cue.RT', 'Cue.ACC',
              'Probe.RT', 'Probe.ACC', 'TrialType', 'Cue.OnsetTime',
              'Probe.OnsetTime', 'Cue', 'SessionDate'],
    'EP2_AX': ['Subject', 'Group', 'Session', 'Age', 'ExperimentName',
               'Handedness', 'Sex', 'BlockNum', 'Cue.RT', 'Cue.ACC',
               'Probe.RT', 'Probe.ACC', 'TrialType', 'Cue.OnsetTime',
               'Probe.OnsetTime', 'CueStim[Block]', 'SessionDate'],
    'PACT_AX': ['Subject', 'Group', 'ExperimentName', 'Session', 'Age',
                'Handedness', 'Sex', 'BlockList', 'Cue.RT', 'Cue.ACC',
                'Probe.RT', 'Probe.ACC', 'TrialType', 'Cue.OnsetTime',
                'Probe.OnsetTime', 'Cue', 'SessionDate'],
    'EP2_ICET': ['Subject', 'BlockNum', 'ExperimentName', 'TrialNum',
                 'Probe.ACC', 'IsSame', 'CueStim[Block]',
                 'TrialType', 'Cue.OnsetTime', 'Probe.OnsetTime',
                 'Probe.RT', 'Feedback', 'Feedback.OnsetTime'],
    }

import os
import eprime_convert as ec


def main(in_file, task):
    header_list = HEADERS.get(task)
    ec._convert(in_file, header_list)


def try_index(list_, val):
    try:
        return list_.index(val)
    except:
        pass


def _det_file_type(in_file):
    [fn, sf] = os.path.splitext(in_file)
    if sf == ".csv":
        delimiter_ = ','
        rem_lines = 0
    elif sf == ".txt":
        delimiter_ = '\t'
        rem_lines = 3
    elif len(in_file) == 0:
        raise ValueError("Input file name is empty.")
    else:
        raise ValueError("Input file name is not .csv or .txt.")

    return delimiter_, rem_lines


def _convert(infile, header_list):
    import csv
    import numpy.core.fromnumeric as fn

    delimiter_, rem_lines = ec._det_file_type(infile)
    try:
        wholefile = list(csv.reader(open(infile, 'rb'),
                                    delimiter=delimiter_))
        main_array = []
    except IOError:
        print("Can't open input file- %s" % infile)

    # Remove first three rows.
    for iRow in range(rem_lines):
        wholefile.pop(0)

    # Create list of columns with relevant headers.
    main_array = [try_index(wholefile[0], hed) for hed in header_list if
                  try_index(wholefile[0], hed) is not None]

    # Make empty (zeros) list of lists and fill with relevant data from
    # wholefile.
    out_struct = [[wholefile[iRow][col] for col in main_array]
                  for iRow in range(fn.size(wholefile, 0))]

    # Remove all instances of NULL by creating an index of NULL occurrences
    # and removing them from wholefile.
    null_idx = [list(set([iRow for col in out_struct[iRow] if col == "NULL"]))
                for iRow in range(fn.size(out_struct, 0))]
    null_idx = sorted([val for sublist in null_idx for val in sublist],
                      reverse=True)
    [out_struct.pop(i) for i in null_idx]

    # Write out and save csv file.
    outfile = infile[:len(infile)-4] + "_clean_ett.csv"
    try:
        fo = open(outfile, 'wb')
        file_ = csv.writer(fo)
        for row in out_struct:
            file_.writerow(row)

        print("Output file successfully created- %s" % outfile)
    except IOError:
        print("Can't open output file- %s" % outfile)
    finally:
        fo.close()
