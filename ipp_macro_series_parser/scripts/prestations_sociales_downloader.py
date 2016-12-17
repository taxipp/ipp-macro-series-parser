#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Download data from data.caf.fr
"""


import argparse
import logging
import os
import sys
import urllib
import urllib2

from ipp_macro_series_parser.config import Config


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)

parser = Config()
prestations_sociales_directory = parser.get('data', 'prestations_sociales_directory')
assert prestations_sociales_directory != 'None', \
    "Set prestations_sociales_directory in the data section of you config[_local].ini file to a valid directory"
prestations_sociales_raw = os.path.join(
    prestations_sociales_directory,
    'raw',
    )


def minimum_vieillesse_downloader(directory = prestations_sociales_raw):
    if not os.path.exists(directory):
        log.info('Creating directory {} since it does not exist.'.format(directory))
        os.makedirs(directory)
    # http://www.statistiques-recherches.cnav.fr/le-minimum-vieillesse.html
    statistiques_recherches_cnav_fr = os.path.join(directory, 'statistiques_recherches_cnav_fr')
    if not os.path.exists(statistiques_recherches_cnav_fr):
        log.info('Creating directory {} since it does not exist.'.format(statistiques_recherches_cnav_fr))
        os.makedirs(statistiques_recherches_cnav_fr)
    urls = [
        'http://www.statistiques-recherches.cnav.fr/images/donnees-statistiques/serie-labellisee/Minimum-vieillesse-au-31-decembre-serie-labellisee.xls',
        'http://www.statistiques-recherches.cnav.fr/images/donnees-statistiques/pensions/Les%20allocataires%20du%20minimum%20vieillesse%20en%20stock%20depuis%201994.xls'
        ]

    for url in urls:
        target = os.path.join(statistiques_recherches_cnav_fr, os.path.basename(url))
        log.info('Downloading {}'.format(url))
        try:
            source = urllib2.urlopen(url)
        except Exception as e:
            print("Can't retrieve {} to save it to {}:\n {}".format(url, target, e))
        with open(target, "wb") as local_file:
            local_file.write(source.read())
    return


def prestations_sociales_downloader(years = None, directory = prestations_sociales_raw):
    if years is not None:
        if type(years) is int:
            years = [years]
    if not os.path.exists(directory):
        log.info('Creating directory {} since it does not exist.'.format(directory))
        os.makedirs(directory)
    caf_data_fr = os.path.join(directory, 'caf_data_fr')
    if not os.path.exists(caf_data_fr):
        log.info('Creating directory {} since it does not exist.'.format(caf_data_fr))
        os.makedirs(caf_data_fr)

    base_url = 'http://data.caf.fr/dataset/'

    file_by_year_by_section = {
        'les-beneficiaires-tous-regimes-de-prestations-familiales-et-sociales': {
            'doc': '63a91700-45c7-456f-aa6c-7bcbf3734f0c/resource/c5f02f7e-5966-4581-b745-efc9d2db6ce9/download/DescriptiffichierbenTR.txt',
            '2013': '63a91700-45c7-456f-aa6c-7bcbf3734f0c/resource/381a49ce-6ddb-4fdd-9b59-a1e25edc5cfd/download/BenTR2013.csv',
            '2014': '63a91700-45c7-456f-aa6c-7bcbf3734f0c/resource/79258bba-6a5e-46cb-adda-26be49247784/download/BenTR2014.csv',
            '2015': '63a91700-45c7-456f-aa6c-7bcbf3734f0c/resource/e4256d93-5225-48ec-b050-c35b000c0365/download/BenTR2015.csv'
            },
        'les-depenses-tous-regimes-de-prestations-familiales-et-sociales': {
            'doc': '854be851-a74f-410e-b261-3d40324426aa/resource/07d5b1ea-a977-4821-83dc-101c3a58a1e7/download/DescriptiffichierdepTR.txt',
            '2013': '854be851-a74f-410e-b261-3d40324426aa/resource/f01a4674-5e97-4018-9517-bd6de9b5ba37/download/DepTR2013.csv',
            '2014': '854be851-a74f-410e-b261-3d40324426aa/resource/64f6f137-4a74-4ab9-abd2-82f64c44eee4/download/DepTR2014.csv',
            '2015': '854be851-a74f-410e-b261-3d40324426aa/resource/e40fcf1c-8b0e-41ee-9101-4c7e55b3d675/download/DepTR2015.csv',
            }
        }
    for section, file_by_year in file_by_year_by_section.iteritems():
        for year, filename in file_by_year.iteritems():
            section_directory = os.path.join(directory, section)
            if not os.path.exists(section_directory):
                log.info('Creating directory {} since it does not exist.'.format(section_directory))
                os.makedirs(section_directory)

            target = os.path.join(section_directory, os.path.basename(filename))
            url = base_url + filename
            try:
                log.info('Downloading {}/{}'.format(url, filename))
                source, hdrs = urllib.urlretrieve(url, target)  # TODO: use urlib2.urlopen
            except Exception as e:
                log.info("Can't retrieve %r to %r: %s" % (url, directory, e))
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', default = prestations_sociales_raw,
        help = 'path where to store downloaded files')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)
    minimum_vieillesse_downloader()
    prestations_sociales_downloader(years = None)


if __name__ == "__main__":
    sys.exit(main())
