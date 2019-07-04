#! /usr/bin/env python
# -*- coding: utf-8 -*-


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
    version = '0.1.7',
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
