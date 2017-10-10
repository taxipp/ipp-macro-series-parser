# -*- coding: utf-8 -*-


import os
import urllib

from ipp_macro_series_parser.config import Config


parser = Config()
transports_directory = parser.get('data', 'transports_directory')
assert os.path.exists(transports_directory), "{} is not a valid directory".format(transports_directory)


def getunzipped(theurl, thedir, file_name):
    name = os.path.join(thedir, file_name)
    if not os.path.exists(thedir):
        os.makedirs(thedir)
    try:
        name, hdrs = urllib.urlretrieve(theurl, name)
    except IOError as e:
        print("Can't retrieve %r to %r: %s" % (theurl, thedir, e))
        return

to_be_downloaded = [    
    'Annexes_G_-_Bilan_de_la_circulation'
    ]


def transports_downloader():
    for element in to_be_downloaded:
        theurl = 'http://www.statistiques.developpement-durable.gouv.fr/fileadmin/documents/Themes/Transports/Comptes_des_transports/2016/{}.xls'.format(element)
        thedir = os.path.join(transports_directory)
        getunzipped(theurl, thedir, element + '.xls')

transports_downloader()
