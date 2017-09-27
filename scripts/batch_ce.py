# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 et:
"""
Convert an example E-Prime text file to csv.
"""
from convert_eprime import convert
from os.path import join

DATA_DIR = '/Users/salo/Downloads'
TEXT_FILE = join(DATA_DIR, '150609_CART_send5forscanner_withtracking-43-1.txt')
EDAT_FILE = join(DATA_DIR, '150609_CART_send5forscanner_withtracking-43-1.edat2')
OUT_FILE = join(DATA_DIR, 'pilot_subj.csv')

convert.text_to_csv(TEXT_FILE, OUT_FILE)
