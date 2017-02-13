#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Parse dénombrements fiscaux to produce the dataframe stroed in a HDF5 file
"""


import argparse
import logging
import os
import sys


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.prelevements_sociaux.parser import main_parse

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
    prelevements_sociaux_source = config.get('data', 'prelevements_sociaux_source')
    prelevements_sociaux_directory = config.get('data', 'prelevements_sociaux_directory')
    assert prelevements_sociaux_source != 'None', \
        "Set prelevements_sociaux_source in the data section of you config[_local].ini file to a valid directory"
    assert prelevements_sociaux_directory != 'None', \
        "Set prelevements_sociaux_directory in the data section of you config[_local].ini file to a valid directory"

    clean_directory = os.path.join(prelevements_sociaux_directory, 'clean')
    if not os.path.exists(clean_directory):
        os.makedirs(clean_directory)

    file_path1 = os.path.join(clean_directory, 'recette_csg_crds.csv')
    file_path2 = os.path.join(clean_directory, 'recette_csg_by_type.csv')

    if os.path.exists(file_path1) or os.path.exists(file_path2):
        if not args.force:
            log.error("The files {} and/or {} already exist. Use the --force to overwrite.".format(file_path1, file_path2))
            return

    main_parse()


if __name__ == "__main__":
    sys.exit(main())
