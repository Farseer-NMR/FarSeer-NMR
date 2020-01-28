"""
Installation setup.

Read the full installation instructions at:

    https://farseernmr.readthedocs.io/en/latest/installation.html

To install farseernmr run:

    >>> python setup.py

To install farseernmr in developer mode run:

    >>> python setup.py develop

To install farseernmr without ANY of its dependencies:

    >>> python setup.py --no-deps
"""
from __future__ import absolute_import, print_function

import io
import os
import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


install_requires = [
    # 'bioplottemplates>0.1',
    ]

if os.getenv('READTHEDOCS'):
    install_requires = []

# support deps
supdeps = [
    'matplotlib>=3,<4',
    'numpy>=1,<2',
    ]

alldeps = supdeps


def _read(*names, **kwargs):
    with io.open(
            join(dirname(__file__), *names),
            encoding=kwargs.get('encoding', 'utf8')
            ) as fh:
        return fh.read()


setup(
    name='farseernmr',
    version='2.0.0-dev',
    license='GNU GPLv3+',
    description='A software suite for automatic treatment, analysis and plotting of large and multivariable datasets of bioNMR peaklists.',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', _read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', _read('CHANGELOG.rst'))
        ),
    author='FarSeer-NMR',
    author_email='farseer.nmr@gmail.com',
    url='https://github.com/Farseer-NMR/FarSeer-NMR',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 4 - Beta',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        ],
    project_urls={
        'Documentation': 'https://farseernmr.readthedocs.io/',
        'Changelog': 'https://farseernmr.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/FarSeer-NMR/FarSeer-NMR/issues',
        },
    keywords=[
        'Proteins',
        'DNA',
        'RNA',
        'Structural Biology',
        'Molecular Biology',
        'Biochemistry',
        'Nuclear Magnetic Resonance',
        ],
    python_requires='>=3.6, <=3.9',
    install_requires=install_requires,
    extras_require={
        'sup': supdeps,
        },
    entry_points={
        'console_scripts': [
            'farseernmr = farseernmr.cli:maincli',
            ]
        },
    )
