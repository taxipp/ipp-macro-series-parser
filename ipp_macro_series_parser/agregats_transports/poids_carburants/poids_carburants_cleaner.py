# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 10:06:10 2015

@author: thomas.douenne
"""

import numpy as np

from ipp_macro_series_parser.agregats_transports.poids_carburants.poids_carburants_parser import \
    consommation, parc_auto


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


def cleaner_alinea(data_frame):
    data_frame['index'] = data_frame['index'].str.replace(' dont', 'dont')
    data_frame['index'] = data_frame['index'].str.replace('        en', 'en')
    data_frame['index'] = data_frame['index'].str.replace('    D', 'D')
    return data_frame


parc_auto = cleaner_dont(parc_auto)
consommation = cleaner_alinea(consommation)
