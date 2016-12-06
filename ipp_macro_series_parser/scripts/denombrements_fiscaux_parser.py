#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Parse dénombrements fiscaux to produce the dataframe stroed in a HDF5 file
"""


import argparse
import logging
import os
import sys


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.denombrements_fiscaux.denombrements_parsers import (
    create_denombrements_fiscaux_data_frame
    )
app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


parser = Config()
denombrements_fiscaux_xls_directory = parser.get('data', 'denombrements_fiscaux_xls')
denombrements_fiscaux_hdf_directory = parser.get('data', 'denombrements_fiscaux_hdf')

assert denombrements_fiscaux_xls_directory != 'None', \
    "Set denombrements_fiscaux_xls in the data section of you config[_local].ini file to a valid directory"

assert os.path.exists(os.path.join(denombrements_fiscaux_xls_directory, 'D2042Nat')), \
    "The D2042Nat containing the DGFiP files doesn't exist"
assert os.path.exists(os.path.join(denombrements_fiscaux_xls_directory, '2042_national.xls')), \
    "The 2042_national.xls containing the openfisca data doesn't exist"
assert os.path.exists(os.path.join(denombrements_fiscaux_xls_directory, 'Agrégats IPP - Données fiscales.xls')), \
    "Agrégats IPP - Données fiscales.xls containing the openfisca data doesn't exist"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--end', default = 2013, help = 'ending year to be downloaded')
    parser.add_argument('-s', '--start', default = 2009, help = 'starting year to be downloaded')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    parser.add_argument('-f', '--force', action = 'store_true', default = False,
        help = "Force overwrite of existing data")

    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)
    years = range(args.start, args.end + 1)
    assert denombrements_fiscaux_hdf_directory != 'None', \
        "Set denombrements_fiscaux_hdf in the data section of you config[_local].ini file to a valid directory"
    if not os.path.exists(denombrements_fiscaux_hdf_directory):
        log.info("We create the directory {} which doesn't exists")
    hdf_file_path = os.path.join(denombrements_fiscaux_hdf_directory, 'denombrements_fiscaux.h5')
    if os.path.exists(hdf_file_path):
        if not args.force:
            log.error("The file {} already exists. Use the --force to overwrite.".format(hdf_file_path))
            return

    create_denombrements_fiscaux_data_frame(year = None, years = years, overwrite = True)


if __name__ == "__main__":
    sys.exit(main())
