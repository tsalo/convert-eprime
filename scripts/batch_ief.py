# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 14:49:47 2015
Sample wrapper for index_eprime_files.py.
@author: tsalo
"""

import index_eprime_files as ief

csv_file = "C:\\Users\\tsalo\\Desktop\\behav_sheet.csv"
directory = "Z:\\Behavioral_Data\\BehavBehav\\AX-CPT_EP2\\raw_data\\Archive_20141024\\"
task = "bEP2_AX"

ief.main(directory, csv_file, task)