#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Download http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/bilan-demo/fichiers-xls/
"""


import argparse
import logging
import os
import sys
import urllib


from ipp_macro_series_parser.config import Config


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


parser = Config()
demographie_directory = parser.get('data', 'demographie_directory')
assert demographie_directory != 'None', \
    "Set demographie_directory in the data section of you config[_local].ini file to a valid directory"


# Download a the xls file from url and unzipp it in directory
def age_structure_downloader(years = None, directory = demographie_directory):
    assert years is not None
    if type(years) is int:
        years = [years]
    if not os.path.exists(directory):
        os.makedirs(directory)

    base_url = 'http://www.insee.fr/fr/ppp/bases-de-donnees/donnees-detaillees/bilan-demo/fichiers-xls/'

    for year in years:
        filename = 'pyramide-des-ages-{}.xls'.format(year)
        target = os.path.join(directory, 'xls', filename)
        url = base_url + filename
        try:
            log.info('Downloading {}/{}'.format(url, filename))
            source, hdrs = urllib.urlretrieve(url, target)  # TODO: use urlib2.urlopen
        except Exception as e:
            log.info("Can't retrieve %r to %r: %s" % (url, directory, e))
            return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--end', default = 2015, help = 'ending year to be downloaded')
    parser.add_argument('-s', '--start', default = 2008, help = 'starting year to be downloaded')
    parser.add_argument('-t', '--target', default = demographie_directory,
        help = 'path where to store downloaded files')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)
    age_structure_downloader(years = range(args.start, args.end + 1))


if __name__ == "__main__":
    sys.exit(main())
