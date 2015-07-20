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

transports_directory = parser.get('data', 'transports_directory')
a_activite_economique = parser.get('data', 'a_activite_economique')
d_developpement_durable = parser.get('data', 'd_developpement_durable')
f_voyageurs = parser.get('data', 'f_voyageurs')
g_bilan_circulation = parser.get('data', 'g_bilan_circulation')


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
    cols = data_frame.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    data_frame = data_frame[cols]
    return data_frame


a3_a = transports_parser(a_activite_economique, 14)  # OK
a3_b = transports_parser(a_activite_economique, 15)  # OK
a6_b = transports_parser(a_activite_economique, 30)  # OK
d2_f = transports_parser(d_developpement_durable, 10)  # OK

g1_a1 = transports_parser(g_bilan_circulation, 1)  # OK
g1_b1 = transports_parser(g_bilan_circulation, 3)  # OK
g2_1 = transports_parser(g_bilan_circulation, 7)  # OK
g3_c1 = transports_parser(g_bilan_circulation, 11)  # OK

d2_g = transports_parser(d_developpement_durable, 11)  # compliqué
f1_a = transports_parser(f_voyageurs, 1)  # compliqué

a1_b = transports_parser_categ(a_activite_economique, 2)  # compliqué
g_3a = transports_parser_categ(g_bilan_circulation, 9)
