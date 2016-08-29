#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Build an excel file containing with data parsed from the fiscal revenus files"""


import argparse
import logging
import os
import pkg_resources
import shutil
import sys
import urllib
import zipfile

from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.denombrements_fiscaux.revenus_imposables_parser import build_excel

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)

parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
xls_directory = parser.get('data', 'denombrements_fiscaux_xls')
assert xls_directory != 'None', \
    'Set denombrements_fiscaux_xls in the data section of your config_local.ini file to a valid directory'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--target',
        default = xls_directory,
        help = 'path where to store downloaded files (default to {})'.format(xls_directory)
        )
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)
    build_excel(os.path.join(args.target, 'foyers_imposables_imposes.xls'))

if __name__ == "__main__":
    sys.exit(main())
