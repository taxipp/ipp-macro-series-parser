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
    data_frame['categorie'] = 0
    data_frame['categorie'] = data_frame['index'].str[:3]
    cols = data_frame.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    data_frame = data_frame[cols]
    data_frame.loc[data_frame['categorie'].str[:2] != '07', 'categorie'] = 'autres'
    data_frame.loc[data_frame['categorie'] == '071', 'categorie'] = 'achats_de_vehicules'
    data_frame.loc[data_frame['categorie'] == '072', 'categorie'] = 'depenses_utilisation_vehicules'
    data_frame.loc[data_frame['categorie'] == '073', 'categorie'] = 'services_de_transports'
    data_frame.loc[data_frame['categorie'] == '07 ', 'categorie'] = 'Total'
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


def cleaner_mode_transport(data_frame):
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
    data_frame.loc[data_frame['sous_categorie'] == data_frame['sous_sous_categorie'], 'sous_sous_categorie'] = 'Total'
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


def cleaner_d2g(data_frame):
    data_frame['identification_categ'] = np.nan
    data_frame['identification_categ'] = data_frame['index'].str[:10]
    data_frame['categorie'] = np.nan
    data_frame.loc[data_frame['identification_categ'] == 'Transports', 'categorie'] = \
        data_frame.loc[data_frame['identification_categ'] == 'Transports', 'index']
    data_frame.loc[data_frame['identification_categ'] == 'Transports', 'index'] = 'Total'

    data_frame.loc[data_frame['identification_categ'] == 'Navigation', 'categorie'] = \
        data_frame.loc[data_frame['identification_categ'] == 'Navigation', 'index']
    data_frame.loc[data_frame['identification_categ'] == 'Navigation', 'index'] = 'Total'

    data_frame.loc[data_frame['identification_categ'] == u'Oléoducs (', 'categorie'] = \
        data_frame.loc[data_frame['identification_categ'] == u'Oléoducs (', 'index']
    data_frame.loc[data_frame['identification_categ'] == u'Oléoducs (', 'index'] = 'Total'

    data_frame.loc[data_frame['identification_categ'] == 'Plaisance ', 'categorie'] = \
        data_frame.loc[data_frame['identification_categ'] == 'Plaisance ', 'index']
    data_frame.loc[data_frame['identification_categ'] == 'Plaisance ', 'index'] = 'Total'

    data_frame.loc[data_frame['identification_categ'] == 'Ensemble', 'categorie'] = \
        data_frame.loc[data_frame['identification_categ'] == 'Ensemble', 'index']
    data_frame.loc[data_frame['identification_categ'] == 'Ensemble', 'index'] = 'Total'

    data_frame.loc[data_frame['identification_categ'] == 'Transport ', 'categorie'] = \
        data_frame.loc[data_frame['identification_categ'] == 'Transport ', 'index']
    data_frame.loc[data_frame['identification_categ'] == 'Transport ', 'index'] = 'Total'

    data_frame['categorie'].fillna(method = 'ffill', inplace = True)
    cols = list(data_frame)
    cols.insert(0, cols.pop(cols.index('categorie')))
    data_frame = data_frame.ix[:, cols]
    del data_frame['identification_categ']
    return data_frame


def cleaner_alinea(data_frame):
    data_frame['index'] = data_frame['index'].str.replace(' dont', 'dont')
    data_frame['index'] = data_frame['index'].str.replace('        en', 'en')
    data_frame['index'] = data_frame['index'].str.replace('    D', 'D')
    return data_frame


g1_a1 = cleaner_dont(g1_a1)
g1_b1 = cleaner_dont(g1_b1)
g2_1 = cleaner_dont(g2_1)
g3_c1 = cleaner_dont(g3_c1)

a3_a = cleaner_achat_vehicule(a3_a)
a3_b = cleaner_achat_vehicule(a3_b)

a6_b = cleaner_au_profit(a6_b)

a1_b = cleaner_mode_transport(a1_b)
a1_b = cleaner_depense(a1_b)
a1_b = cleaner_alinea(a1_b)

f1_a = cleaner_f(f1_a)

d2_g = cleaner_d2g(d2_g)

g_3a = cleaner_alinea(g_3a)

# If we want to set the index:
# cols = list(a1_b)
# a1_b.set_index(cols[:4], inplace = True)
