


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
    'a-transport-et-activite-economique',
    'b-entreprises-francaises-de-transport',
    'c-transport-emploi-remuneration',
    'd-transport-developpement-durable',
    'e-transport-de-marchandises',
    'f-transport-de-voyageurs',
    'g-bilan-de-circulation'
    ]


def transports_downloader():
    for element in to_be_downloaded:
        theurl = 'http://www.statistiques.developpement-durable.gouv.fr/fileadmin/documents/Produits_editoriaux/Publications/References/2014/comptes-transports/annexes-{}-2013.xls'.format(element)
        thedir = os.path.join(transports_directory)
        getunzipped(theurl, thedir, element + '.xls')


transports_downloader()
