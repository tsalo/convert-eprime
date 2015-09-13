# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 13:21:45 2014

@author: tsalo
"""
import convert_eprime as ce

op = "/Users/salo/Downloads/"
text_file = op + "150609_CART_send5forscanner_withtracking-43-1.txt"
edat_file = op + "150609_CART_send5forscanner_withtracking-43-1.edat2"
out_file = op + "pilot_subj.csv"

ce.text_to_csv(text_file, out_file)
