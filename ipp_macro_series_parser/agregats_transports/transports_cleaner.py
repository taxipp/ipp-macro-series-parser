# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 10:06:10 2015

@author: thomas.douenne
"""

import numpy as np

from ipp_macro_series_parser.agregats_transports.transports_parser import *


def cleaner_dont(data_frame):
    data_frame['identification_categ'] = 0
    data_frame['identification_categ'] = data_frame['identification_categ'].astype(str)
    data_frame['identification_categ'] = data_frame['index'].str[:4]
    data_frame['categorie'] = data_frame['index']
    data_frame.loc[data_frame['identification_categ'] == 'dont', 'categorie'] = np.nan
    data_frame['categorie'].fillna(method='ffill', inplace = True)
    data_frame.loc[data_frame['identification_categ'] != 'dont', 'index'] = 'Total'

    cols = data_frame.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    data_frame = data_frame[cols]
    del data_frame['identification_categ']
    return data_frame


def cleaner_achat_vehicule(data_frame):
    data_frame['identification_categ'] = 0
    data_frame['identification_categ'] = data_frame['index'].str[:3]
    cols = data_frame.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    data_frame = data_frame[cols]
    return data_frame


def cleaner_au_profit(data_frame):
    data_frame['identification_categ'] = 0
    data_frame['identification_categ'] = data_frame['index'].str[:9]
    data_frame['categorie'] = data_frame['index']
    data_frame.loc[data_frame['identification_categ'] == 'Au profit', 'categorie'] = np.nan
    data_frame['categorie'].fillna(method='ffill', inplace = True)
    data_frame.loc[data_frame['identification_categ'] != 'Au profit', 'index'] = 'Total'

    cols = data_frame.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    data_frame = data_frame[cols]
    del data_frame['identification_categ']

    return data_frame


def cleaner_alinea(data_frame):
    data_frame['identification_categ'] = 0
    data_frame['identification_categ'] = data_frame['index'].str[:1]
    data_frame['sous_sous_categorie'] = data_frame['index']
    data_frame.loc[data_frame['identification_categ'] == ' ', 'sous_sous_categorie'] = np.nan
    data_frame['categorie'].fillna(method='ffill', inplace = True)
    data_frame.loc[data_frame['identification_categ'] != ' ', 'index'] = 'Total'
    return data_frame


def cleaner_depense(data_frame):
    data_frame['identification_categ2'] = 0
    data_frame['identification_categ2'] = data_frame['sous_sous_categorie'].str[:7]
    data_frame['sous_categorie'] = data_frame['sous_sous_categorie']
    data_frame.loc[data_frame['identification_categ2'] != u'Dépense', 'sous_categorie'] = np.nan
    data_frame['sous_categorie'].fillna(method='ffill', inplace = True)
    data_frame['sous_sous_categorie'].fillna(method = 'ffill', inplace = True)
    cols = data_frame.columns.tolist()
    cols = cols[-4:] + cols[:-4]
    data_frame = data_frame[cols]
    del data_frame['identification_categ']
    del data_frame['identification_categ2']

    cols = list(data_frame)
    cols.insert(0, cols.pop(cols.index('sous_categorie')))
    cols.insert(0, cols.pop(cols.index('categorie')))
    data_frame = data_frame.ix[:, cols]
    return data_frame


def cleaner_f(data_frame):
    data_frame['categorie'] = np.nan
    data_frame.loc[data_frame['index'] == u'Véhicules particuliers (1)', 'categorie'] = 'vehicules_particuliers'
    data_frame.loc[data_frame['index'] == 'Transports collectifs', 'categorie'] = 'transports_collectifs'
    data_frame.loc[data_frame['index'] == 'Ensemble', 'categorie'] = 'ensemble'
    data_frame['categorie'].fillna(method = 'ffill', inplace = True)

    data_frame['sous_categorie'] = np.nan
    data_frame.loc[data_frame['index'] == u'Véhicules particuliers (1)', 'sous_categorie'] = 'Total'
    data_frame.loc[data_frame['index'] == 'Transports collectifs', 'sous_categorie'] = 'Total'
    data_frame.loc[data_frame['index'] == 'Ensemble', 'sous_categorie'] = 'Total'
    data_frame.loc[data_frame['index'] == 'Autobus, autocars et tramways', 'sous_categorie'] = 'bus_car_tram'
    data_frame.loc[data_frame['index'] == u'Transports ferrés (5)', 'sous_categorie'] = 'transports_ferres'
    data_frame.loc[data_frame['index'] == u'Transports aériens (13)', 'sous_categorie'] = 'transports_aeriens'
    data_frame['sous_categorie'].fillna(method = 'ffill', inplace = True)

    cols = list(data_frame)
    cols.insert(0, cols.pop(cols.index('sous_categorie')))
    cols.insert(0, cols.pop(cols.index('categorie')))
    data_frame = data_frame.ix[:, cols]
    return data_frame


g1_a1 = cleaner_dont(g1_a1)
g1_b1 = cleaner_dont(g1_b1)
g2_1 = cleaner_dont(g2_1)
g3_c1 = cleaner_dont(g3_c1)

a3_a = cleaner_achat_vehicule(a3_a)
a3_b = cleaner_achat_vehicule(a3_b)

a6_b = cleaner_au_profit(a6_b)

a1_b = cleaner_alinea(a1_b)
a1_b = cleaner_depense(a1_b)

f1_a = cleaner_f(f1_a)

# d2_f does not need to be cleaned. We still have to clean d2_g and g_3a.
