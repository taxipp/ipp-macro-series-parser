#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Download Comptes nationaux files from the INSEE website for specific years and unzip them
INSEE website: http://www.insee.fr/fr/indicateurs/cnat_annu/archives/comptes_annee_YEAR.zip
"""


import argparse
import logging
import os
import shutil
import sys
import urllib
import zipfile

from ipp_macro_series_parser.config import Config

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)

parser = Config()
cn_directory = parser.get('data', 'cn_directory')
assert cn_directory != 'None', 'Set cn_directory in the data section of your config_local.ini file to a valid directory'


# Download a zip file from theurl and unzip it in directory thedir
def getunzipped(url = None, directory = None):
    assert url and directory
    name = os.path.join(directory, 'source_insee.zip')
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        log.info('Downloading {}/{}'.format(url, name))
        name, hdrs = urllib.urlretrieve(url, name)
    except IOError as e:
        log.info("Can't retrieve %r to %r: %s" % (url, directory, e))
        return
    try:
        log.info('Unzipping {}'.format(name))
        z = zipfile.ZipFile(name)
    except zipfile.error as e:
        log.info("Bad or nonexistent zipfile (from %r): %s" % (url, e))
        return
    z.close()

    with zipfile.ZipFile(name) as zip_file:
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue

            source = zip_file.open(member)
            target = file(os.path.join(directory, filename), "wb")
            with source, target:
                log.info('Copying to {}'.format(target))
                shutil.copyfileobj(source, target)


def cn_downloader(years = None):
    if years is None:
        years = range(2003, 2013 + 1, 1)
    elif type(years) is int:
        years = [years]
    for year in years:
        directory = os.path.join(cn_directory, 'comptes_annee_{}'.format(year))
        getunzipped(
            url = 'http://www.insee.fr/fr/indicateurs/cnat_annu/archives/comptes_annee_{}.zip'.format(year),
            directory = directory
            )
        assert os.path.exists(directory), 'comptes_annee_{} was not downloaded'.format(year)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--end', default = 2013, type = int, help = 'ending year to be downloaded')
    parser.add_argument('-s', '--start', default = 2013, type = int, help = 'starting year to be downloaded')
    parser.add_argument('-t', '--target', default = cn_directory, help = 'path where to store downloaded files')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)
    cn_downloader(years = range(args.start, args.end + 1))


if __name__ == "__main__":
    sys.exit(main())
