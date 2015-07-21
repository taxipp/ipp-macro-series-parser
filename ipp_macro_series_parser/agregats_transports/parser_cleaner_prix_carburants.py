# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 13:57:18 2015

@author: thomas.douenne
"""

import os
import pkg_resources
import pandas as pd
import numpy as np
from pandas import concat

from ipp_macro_series_parser.config import Config

parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )

transports_directory = parser.get('data', 'transports_directory')
prix_annuel_carburants = parser.get('data', 'prix_annuel_carburants_90_2014')


def prix_carburants_parser(excelfile_name):
    data_frame = pd.read_excel(excelfile_name, header = 2)
    data_frame = data_frame.dropna(how = 'all')
    data_frame['Date'] = data_frame['Date'].astype(str)
    data_frame.fillna('   ', inplace = True)
    data_frame = data_frame[data_frame.ix[:, 1] != '   ']
    data_frame = data_frame[data_frame.ix[:, 0] != 'en euro par litre']
    data_frame.rename(columns = {'Super carburant': 'super_ht'}, inplace = True)
    data_frame.rename(columns = {'Super carburant.1': 'super_ttc'}, inplace = True)
    data_frame.rename(columns = {'Gazole': 'diesel_ht'}, inplace = True)
    data_frame.rename(columns = {'Gazole.1': 'diesel_ttc'}, inplace = True)
    data_frame.rename(columns = {'Super SP95': 'super_95_ht'}, inplace = True)
    data_frame.rename(columns = {'Super SP95.1': 'super_95_ttc'}, inplace = True)
    data_frame.rename(columns = {'Super SP98': 'super_98_ht'}, inplace = True)
    data_frame.rename(columns = {'Super SP98.1': 'super_98_ttc'}, inplace = True)
    return data_frame

prix_annuel_carburants = prix_carburants_parser(prix_annuel_carburants)


def prix_carburants_cleaner_90_96(data_frame):
    data_frame = data_frame[data_frame['Date'] != 'Date']
    data_frame['Date'] = data_frame['Date'].astype(float)
    data_frame = data_frame[data_frame['Date'] < 1997]
    del data_frame['Unnamed: 9']
    del data_frame['Unnamed: 10']
    return data_frame

prix_carburants_90_96 = prix_carburants_cleaner_90_96(prix_annuel_carburants)


def prix_carburants_cleaner_97_06(data_frame):
    data_frame = data_frame[data_frame['Unnamed: 9'] != '   ']
    data_frame.loc[data_frame['Date'] == 'Date', 'super_ht'] = 'super_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ht'] = 'diesel_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ht'] = 'super_95_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ht'] = 'super_98_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_ttc'] = 'gplc_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ttc'] = 'super_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ttc'] = 'diesel_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ttc'] = 'super_95_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'Unnamed: 9'] = 'super_98_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'Unnamed: 10'] = 'gplc_ttc'

    data_frame.columns = data_frame.iloc[0]
    data_frame = data_frame[data_frame['Date'] != 'Date']
    data_frame = data_frame.astype(float)
    data_frame = data_frame[data_frame['Date'] < 2013]
    return data_frame

prix_carburants_97_06 = prix_carburants_cleaner_97_06(prix_annuel_carburants)


def prix_carburants_cleaner_07_12(data_frame):
    data_frame = data_frame[data_frame['Unnamed: 9'] == '   ']
    data_frame = data_frame[data_frame['super_ht'] != 'Super carburant']
    data_frame['Unnamed: 9'] = data_frame['Date'].str[:2]
    data_frame = data_frame[data_frame['Unnamed: 9'] != '19']
    data_frame.loc[data_frame['Date'] == 'Date', 'super_ht'] = 'diesel_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ht'] = 'super_95_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ht'] = 'super_98_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ht'] = 'gplc_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_ttc'] = 'diesel_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ttc'] = 'super_95_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ttc'] = 'super_98_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ttc'] = 'gplc_ttc'

    data_frame.columns = data_frame.iloc[0]
    data_frame = data_frame[data_frame['Date'] != 'Date']
    del data_frame['Da']
    del data_frame['   ']
    data_frame['Date'] = data_frame['Date'].astype(float)
    return data_frame

prix_carburants_07_12 = prix_carburants_cleaner_07_12(prix_annuel_carburants)


def prix_carburants_cleaner_13_14(data_frame):
    data_frame = data_frame[data_frame['Unnamed: 9'] != '   ']
    data_frame = data_frame[data_frame['super_ht'] != 'Super carburant']
    data_frame['identification'] = data_frame['Date'].str[2:3]
    data_frame = data_frame[data_frame['identification'] != '9']
    data_frame = data_frame[data_frame['identification'] != '0']

    data_frame.loc[data_frame['Date'] == 'Date', 'super_ht'] = 'diesel_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ht'] = 'super_95_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ht'] = 'super_95_e10_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ht'] = 'super_98_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_ttc'] = 'gplc_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ttc'] = 'diesel_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ttc'] = 'super_95_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ttc'] = 'super_95_e10_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'Unnamed: 9'] = 'super_98_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'Unnamed: 10'] = 'gplc_ttc'

    data_frame.columns = data_frame.iloc[0]
    data_frame = data_frame[data_frame['Date'] != 'Date']
    del data_frame['t']
    data_frame['Date'] = data_frame['Date'].astype(float)
    return data_frame

prix_carburants_13_14 = prix_carburants_cleaner_13_14(prix_annuel_carburants)

prix_carburants_90_14 = pd.concat([prix_carburants_90_96, prix_carburants_97_06, \
    prix_carburants_07_12, prix_carburants_13_14], axis = 0)
carburants = list(prix_carburants_90_14)
prix_carburants_90_14 = pd.melt(prix_carburants_90_14, id_vars = ['Date'], value_vars = carburants[1:], \
    value_name = 'prix', var_name = 'carburant')

prix_carburants_90_14['Date'] = prix_carburants_90_14['Date'].astype(int)
prix_carburants_90_14 = prix_carburants_90_14.set_index(['Date'])
