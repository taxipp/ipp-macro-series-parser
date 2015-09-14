#! /usr/bin/env python
# -*- coding: utf-8 -*-


# TAXIPP -- A French microsimulation model
# By: IPP <taxipp@ipp.eu>
#
# Copyright (C) 2012, 2013, 2014, 2015 IPP
# https://github.com/taxipp
#
# This file is part of TAXIPP.
#
# TAXIPP is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# TAXIPP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Download Comptes nationaux files from the INSEE website for specific years and unzip them
INSEE website: http://www.insee.fr/fr/indicateurs/cnat_annu/archives/comptes_annee_YEAR.zip
"""


import argparse
import logging
import os
import pkg_resources
import sys
import urllib


from ipp_macro_series_parser.config import Config


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
demographie_directory = parser.get('data', 'demographie_directory')
assert demographie_directory != 'None', \
    "Set demographie_directory_directory in the data section of you config[_local].ini file to a valid directory"


# Download a the xls file from url and unzipp it in directory thedir
def demographie_downloader(years = None, directory = demographie_directory):
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
        except Exception, e:
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
    demographie_downloader(years = range(args.start, args.end + 1))


if __name__ == "__main__":
    sys.exit(main())
