# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 et:
"""
Utility functions for testing convert-eprime.

"""

from os.path import abspath, dirname, join, pardir, sep


def get_resource_path():
    """
    Based on function by Yaroslav Halchenko used in Neurosynth Python package.
    """
    return abspath(join(dirname(__file__), pardir, 'resources') + sep)

def get_test_data_path():
    """
    Returns the path to test datasets, terminated with separator.

    Based on function by Yaroslav Halchenko used in Neurosynth Python package.
    """
    return abspath(join(dirname(__file__), 'data') + sep)

def get_config_path():
    """
    Returns the path to test datasets, terminated with separator.

    Based on function by Yaroslav Halchenko used in Neurosynth Python package.
    """
    return abspath(join(dirname(__file__), pardir, pardir, 'config_files') + sep)
