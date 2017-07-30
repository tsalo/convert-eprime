# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 et:
"""
convert_eprime: A Python package for converting and cleaning up E-Prime output files.
"""
from .convert import etext_to_rcsv, text_to_csv, text_to_rcsv
from .version import __version__

__all__ = ['convert', 'utils']
