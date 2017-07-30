# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 et:
"""
Utility functions for convert_eprime.
"""


def remove_unicode(string):
    """
    Removes unicode characters in string.
    """
    return ''.join([val for val in string if 31 < ord(val) < 127])
