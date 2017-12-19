#! /usr/bin/env python
# -*- coding: utf-8 -*-


# Aggregates Parser -- A versatile parser for aggregates
# By: IPP <???>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""OpenFisca -- a versatile microsimulation free software

OpenFisca includes a framework to simulate any tax and social system.
"""


from setuptools import setup, find_packages


classifiers = """\
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: POSIX
Programming Language :: Python
Topic :: Scientific/Engineering :: Information Analysis
"""

doc_lines = __doc__.split('\n')


setup(
    name = 'IPP-Macro-Series-Parser',
    version = '0.1.6',
    author = 'IPP',
    author_email = 'taxipp@ipp.eu',
    classifiers = [classifier for classifier in classifiers.split('\n') if classifier],
    description = doc_lines[0],
    keywords = 'macro data aggregates beneficiaries parser',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description = '\n'.join(doc_lines[2:]),
    url = 'https://github.com/taxipp/ipp-macro-series-parser.git',
    entry_points = {
        'console_scripts': [
            'download-prestations-sociales=ipp_macro_series_parser.scripts.prestations_sociales_downloader:main',
            'parse-prestations-sociales=ipp_macro_series_parser.scripts.prestations_sociales_parser:main',
            'parse-prelevements-sociaux=ipp_macro_series_parser.scripts.prelevements_sociaux_parser:main',
            'download-demographic-projections=ipp_macro_series_parser.scripts.demographic_projections_downloader:main',
            ],
        },
    install_requires = [
        'glob2',
        'pandas',
        'py-expression-eval',
        'pyxdg',
        'python-slugify',
        'setuptools',
        'xlrd',
        'xlsxwriter',
        'xlwt',
        ],
    message_extractors = {
        'ipp-macro-series-parser': [
            ('**.py', 'python', None),
            ],
        },
    packages = find_packages(),
    test_suite = 'nose.collector',
    zip_safe = False,
    )
