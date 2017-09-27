# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 et:
from os import remove
from os.path import join

import pandas as pd
from convert_eprime import convert
from convert_eprime.tests.utils import get_test_data_path


def test_etext_to_rcsv():
    """Test convert_eprime.convert.etext_to_rcsv.
    """
    etext_file = join(get_test_data_path(), 'PILOT_cuetask_exported.txt')
    param_file = join(get_test_data_path(), 'test_cue.json')
    out_file = join(get_test_data_path(), 'out_rcsv.csv')

    convert.etext_to_rcsv(etext_file, param_file, out_file)
    df = pd.read_csv(out_file)
    assert df.shape == (72, 8)

    remove(out_file)


def test_text_to_csv():
    """Test convert_eprime.convert.text_to_csv.
    """
    text_file = join(get_test_data_path(), 'Cuetask-PILOT-1.txt')
    out_file = join(get_test_data_path(), 'out_csv.csv')

    convert.text_to_csv(text_file, out_file)
    df = pd.read_csv(out_file)
    assert df.shape == (81, 98)

    remove(out_file)


def test_text_to_rcsv():
    """Test convert_eprime.convert.text_to_rcsv.
    """
    text_file = join(get_test_data_path(), 'Cuetask-PILOT-1.txt')
    edat_file = join(get_test_data_path(), 'Cuetask-PILOT-1.edat2')
    param_file = join(get_test_data_path(), 'test_cue.json')
    out_file = join(get_test_data_path(), 'out_rcsv.csv')

    convert.text_to_rcsv(text_file, edat_file, param_file, out_file)
    df = pd.read_csv(out_file)
    assert df.shape == (72, 8)

    remove(out_file)
