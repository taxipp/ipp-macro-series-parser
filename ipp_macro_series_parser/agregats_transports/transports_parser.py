# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 15:01:56 2015

@author: thomas.douenne
"""

import os
import pkg_resources
import pandas as pd
import numpy as np

from ipp_macro_series_parser.config import Config

parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
cn_directory = parser.get('data', 'cn_directory')


def transports_parser(excelfile_name, onglet):
    data_frame = pd.read_excel(excelfile_name, sheetname = onglet, skiprows = 2)
    data_frame.rename(columns = {'Unnamed: 0': 'index'}, inplace = True)
    data_frame = data_frame.dropna(thresh = 3)
    data_frame.fillna('-', inplace = True)
    return data_frame


def transports_parser_categ(excelfile_name, onglet):
    data_frame = pd.read_excel(excelfile_name, sheetname = onglet, skiprows = 2)
    data_frame.rename(columns = {'Unnamed: 0': 'index'}, inplace = True)
    data_frame['categorie'] = np.nan
    data_frame.loc[data_frame[2005].isnull(), 'categorie'] = \
        data_frame.loc[data_frame[2005].isnull(), 'index']
    data_frame['categorie'].fillna(method='ffill', inplace = True)
    data_frame = data_frame.dropna(thresh = 3)
    return data_frame


def transports_parser_souscateg(excelfile_name, onglet):
    data_frame = pd.read_excel(excelfile_name, sheetname = onglet, skiprows = 2)
    data_frame.rename(columns = {'Unnamed: 0': 'index'}, inplace = True)
    data_frame = data_frame.dropna(thresh = 3)
    return data_frame


a_a3_a = transports_parser('C:/Users/thomas.douenne/Documents/GitHub/ipp-macro-series-parser/agregats_comptes_transports/a-transport-et-activite-economique.xls',
    14)
a_a3_b = transports_parser('C:/Users/thomas.douenne/Documents/GitHub/ipp-macro-series-parser/agregats_comptes_transports/a-transport-et-activite-economique.xls',
    15)
a_a6_b = transports_parser('C:/Users/thomas.douenne/Documents/GitHub/ipp-macro-series-parser/agregats_comptes_transports/a-transport-et-activite-economique.xls',
    30)
d_d2_f = transports_parser('C:/Users/thomas.douenne/Documents/GitHub/ipp-macro-series-parser/agregats_comptes_transports/d-transport-developpement-durable.xls',
    10)

a_a1_b = transports_parser_categ('C:/Users/thomas.douenne/Documents/GitHub/ipp-macro-series-parser/agregats_comptes_transports/a-transport-et-activite-economique.xls',
    2)
g_3a = transports_parser_categ('C:/Users/thomas.douenne/Documents/GitHub/ipp-macro-series-parser/agregats_comptes_transports/g-bilan-de-circulation.xls',
    9)

# Sous categories : il y a moyen d'identifier plus précisémment les variables, ce sont toutes les mêmes.
# Faire un split pour identifier Véhicule et le mettre en index
g1_a1 = transports_parser_souscateg('C:/Users/thomas.douenne/Documents/GitHub/ipp-macro-series-parser/agregats_comptes_transports/g-bilan-de-circulation.xls',
    1)
g1_b1 = transports_parser_souscateg('C:/Users/thomas.douenne/Documents/GitHub/ipp-macro-series-parser/agregats_comptes_transports/g-bilan-de-circulation.xls',
    3)
g2_1 = transports_parser_souscateg('C:/Users/thomas.douenne/Documents/GitHub/ipp-macro-series-parser/agregats_comptes_transports/g-bilan-de-circulation.xls',
    7)
g3_c1 = transports_parser_souscateg('C:/Users/thomas.douenne/Documents/GitHub/ipp-macro-series-parser/agregats_comptes_transports/g-bilan-de-circulation.xls',
    11)

# Il reste une dernière catégorie de fichiers à parser.
