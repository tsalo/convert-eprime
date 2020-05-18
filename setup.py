# emacs: -*- mode: python-mode; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 et:
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# fetch version from within gclda module
with open('convert_eprime/version.py') as f:
    exec(f.read())

# fetch requirements from file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

config = {
    'description': 'Python tools for converting E-Prime files',
    'author': 'Taylor Salo',
    'url': 'https://github.com/tsalo/convert-eprime/',
    'download_url': 'https://github.com/tsalo/convert-eprime/',
    'author_email': 'tsalo006@fiu.edu',
    'version': __version__,
    'install_requires': requirements,
    'packages': ['convert_eprime'],
    'name': 'convert_eprime',
    'entry_points': {'console_scripts': ['convert_eprime=convert_eprime.cli:_main']}
}

setup(**config)
