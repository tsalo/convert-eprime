# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 et:
from convert_eprime import utils


def test_remove_unicode():
    """Test convert_eprime.utils.remove_unicode.
    """
    test_str = 'Test string. Will add unicode characters later.'
    test_str = utils.remove_unicode(test_str)
    true_str = 'Test string. Will add unicode characters later.'
    assert test_str == true_str
