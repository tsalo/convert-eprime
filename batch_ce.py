# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 13:21:45 2014

@author: tsalo
"""

import convert_eprime_text_to_csv as ce

op = "/home/tsalo/Desktop/FAST/"
text_file = op + "RISE_FMRI_ItemRecoga&bVer1-FASTpilot001-1.txt"
out_file = op + "FASTpilot001-1_IR.csv"

ce.main(text_file, out_file)
