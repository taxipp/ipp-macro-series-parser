# -*- coding: utf-8 -*-
"""
Created on Mon Jul 06 11:55:35 2015

@author: Antoine
"""

import os
import pkg_resources
import shutil
import urllib
import zipfile

from ipp_macro_series_parser.config import Config

parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )

cn_directory = parser.get('data', 'cn_directory')

# to delete:
# cn_directory = 'C:\Users\Antoine\Documents\data_aggregates'


# download a zip file from theurl and unzipp it in directory thedir
def getunzipped(theurl, thedir):
    name = os.path.join(thedir, 'source_insee.zip')
    if not os.path.exists(thedir):
        os.makedirs(thedir)
    try:
        name, hdrs = urllib.urlretrieve(theurl, name)
    except IOError, e:
        print "Can't retrieve %r to %r: %s" % (theurl, thedir, e)
        return
    try:
        z = zipfile.ZipFile(name)
    except zipfile.error, e:
        print "Bad zipfile (from %r): %s" % (theurl, e)
        return
    z.close()

    with zipfile.ZipFile(name) as zip_file:
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue  # go on with next iteration of the loop

            # copy file (taken from zipfile's extract)
            source = zip_file.open(member)
            target = file(os.path.join(thedir, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)


# use getunzipped for INSEE comptabilite national zip file data for a given year
def cn_downloader(years):
    if years is None:
        years = range(1949, 2013 + 1, 1)
    elif type(years) is int:
        years = [years]
    for year in years:
        theurl = 'http://www.insee.fr/fr/indicateurs/cnat_annu/archives/comptes_annee_{}.zip'.format(year)
        thedir = os.path.join(cn_directory, 'comptes_annee_{}'.format(year))
        getunzipped(theurl, thedir)

# maybe: should test wthether the downloaded folder exist / is not empty? does the program first delete the files?

# to be called somewhere else?
cn_downloader(range(2005, 2014))
