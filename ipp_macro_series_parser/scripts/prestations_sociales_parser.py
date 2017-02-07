#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Parse dénombrements fiscaux to produce the dataframe stroed in a HDF5 file
"""


import argparse
import logging
import os
import sys


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.prestations_sociales.parsers import (
    create_prestations_sociales_data_frames
    )
app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    parser.add_argument('-f', '--force', action = 'store_true', default = False,
        help = "Force overwrite of existing data")

    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    config = Config()
    directory = config.get('data', 'prestations_sociales_directory')
    assert directory != 'None', \
        "Set prestations_sociales_directory in the data section of you config[_local].ini file to a valid directory"

    hdf_file_path = os.path.join(directory, 'prestations_sociales.h5')
    if os.path.exists(hdf_file_path):
        if not args.force:
            log.error("The file {} already exists. Use the --force to overwrite.".format(hdf_file_path))
            return

    create_prestations_sociales_data_frames()


if __name__ == "__main__":
    sys.exit(main())
