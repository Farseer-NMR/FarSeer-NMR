# -*- coding: utf-8 -*-
"""Sphinx config file."""
from __future__ import unicode_literals

import os
import mock
import sys


mock_modules = [
    'matplotlib',
    'numpy',
    ]

for modulename in mock_modules:
    sys.modules[modulename] = mock.Mock()

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinxarg.ext',
    'sphinx.ext.autosectionlabel',
    ]

source_suffix = '.rst'
master_doc = 'index'
project = 'farseernmr'
year = '2020'
author = 'FarSeer-NMR'
copyright = '{0}, {1}'.format(year, author)
version = release = '2.0.0-dev'

todo_include_todos = True
pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('https://github.com/Farseer-NMR/FarSeer-NMR/issues/%s', '#'),
    'pr': ('https://github.com/Farseer-NMR/FarSeer-NMR/pull/%s', 'PR #'),
    }
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

linkcheck_ignore = [r'https://codecov.io/*']

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = 'sphinx_rtd_theme'

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
    '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
    }
html_short_title = '%s-%s' % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
