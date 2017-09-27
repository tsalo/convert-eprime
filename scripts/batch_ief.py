# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 et:
"""
Created on Tue Feb 24 14:49:47 2015
Sample wrapper for index_eprime_files.py.
@author: tsalo
"""

from convert import index_files

csv_file = "C:\\Users\\tsalo\\Desktop\\behav_sheet.csv"
directory = "Z:\\Behavioral_Data\\BehavBehav\\AX-CPT_EP2\\raw_data\\Archive_20141024\\"
task = "bEP2_AX"

ief.main(directory, csv_file, task)
