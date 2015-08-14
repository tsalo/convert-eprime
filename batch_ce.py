# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 13:21:45 2014

@author: tsalo
"""
import convert_eprime as ce

op = "/home/tsalo/behav/Archive_20150128/"
text_file = op + "EP2_AXCPT_Run1_epc198-3.txt"
edat_file = op + "EP2_AXCPT_Run1_epc198-3.edat2"
out_file = op + "epc198.csv"
task = "EP2_AX"

ce.text_to_csv(text_file, out_file)
