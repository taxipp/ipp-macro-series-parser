#! /usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import logging
import os
import sys
import urllib

from ipp_macro_series_parser.config import Config

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def grab_data(url, output_dir):

    if not os.path.exists(output_dir):
        log.info("Creating missng directory {}".format(output_dir))
        os.makedirs(output_dir)

    filepath = os.path.join(
        output_dir,
        url.rsplit('/', 1)[-1]
        )

    urllib.urlretrieve(url, filepath)


def main():
    config = Config()
    parser = argparse.ArgumentParser()

    files = ['insee_projections', 'drees_dependance']

    output_dirs_by_file = {file_path: config.get('data', file_path) for file_path in files}

    for name, directory in output_dirs_by_file.iteritems():
        assert directory != 'None', \
            'Set {}in the data section of your config_local.ini file to a valid directory'.format(name)

    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args, garbage = parser.parse_known_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    urls_by_file = {
        'insee_projections':
            'https://www.insee.fr/fr/statistiques/fichier/2517722/projpop0760_FECcentESPcentMIGcent.xls',
        'drees_dependance':
            'http://drees.solidarites-sante.gouv.fr/IMG/xls/dss43_horizon_2060.xls'
        }

    assert {a for a in files} == {b for b in urls_by_file}

    for file in files:
        grab_data(urls_by_file[file], output_dirs_by_file[file])


if __name__ == "__main__":
    sys.exit(main())
