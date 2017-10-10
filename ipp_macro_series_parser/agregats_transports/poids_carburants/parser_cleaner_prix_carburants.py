# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 13:57:18 2015

@author: thomas.douenne
"""

import pandas as pd

from ipp_macro_series_parser.config import Config

parser = Config()

transports_directory = parser.get('data', 'transports_directory')
prix_annuel_carburants = transports_directory + '/prix_annuel_carburants_90_2016.xls'
prix_mensuel_carburants = transports_directory + '/prix_mensuel_carburants_90_2017.xls'


def prix_carburants_parser(excelfile_name):
    data_frame = pd.read_excel(excelfile_name, header = 2)
    data_frame = data_frame.dropna(how = 'all')
    data_frame['Date'] = data_frame['Date'].astype(str)
    data_frame.fillna('   ', inplace = True)
    data_frame = data_frame[data_frame.ix[:, 1] != '   ']
    data_frame = data_frame[data_frame.ix[:, 0] != 'en euro par litre']
    data_frame.rename(columns = {'Super carburant': 'super_plombe_ht'}, inplace = True)
    data_frame.rename(columns = {'Super carburant.1': 'super_plombe_ttc'}, inplace = True)
    data_frame.rename(columns = {'Gazole': 'diesel_ht'}, inplace = True)
    data_frame.rename(columns = {'Gazole.1': 'diesel_ttc'}, inplace = True)
    data_frame.rename(columns = {'Super SP95': 'super_95_ht'}, inplace = True)
    data_frame.rename(columns = {'Super SP95.1': 'super_95_ttc'}, inplace = True)
    data_frame.rename(columns = {'Super SP98': 'super_98_ht'}, inplace = True)
    data_frame.rename(columns = {'Super SP98.1': 'super_98_ttc'}, inplace = True)
    return data_frame

prix_mensuel_carburants = prix_carburants_parser(prix_mensuel_carburants)
prix_annuel_carburants = prix_carburants_parser(prix_annuel_carburants)


def prix_carburants_cleaner_90_96(data_frame):
    data_frame = data_frame[data_frame['Date'] != 'Date'].copy()
    data_frame.rename(columns = {'Unnamed: 9': 'ident_year'}, inplace = True)
    data_frame['ident_year'] = data_frame['Date'].str[-4:]
    data_frame['ident_year'] = data_frame['ident_year'].astype(float)
    data_frame = data_frame[data_frame['ident_year'] < 1997]
    del data_frame['ident_year']
    del data_frame['Unnamed: 10']
    return data_frame


prix_mensuel_carburants_90_96 = prix_carburants_cleaner_90_96(prix_mensuel_carburants)
prix_carburants_90_96 = prix_carburants_cleaner_90_96(prix_annuel_carburants)


def prix_carburants_cleaner_97_06(data_frame):
    data_frame = data_frame[data_frame['Unnamed: 9'] != '   '].copy()
    data_frame.loc[data_frame['Date'] == 'Date', 'super_plombe_ht'] = 'super_plombe_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ht'] = 'diesel_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ht'] = 'super_95_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ht'] = 'super_98_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_plombe_ttc'] = 'gplc_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ttc'] = 'super_plombe_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ttc'] = 'diesel_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ttc'] = 'super_95_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'Unnamed: 9'] = 'super_98_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'Unnamed: 10'] = 'gplc_ttc'

    data_frame.columns = data_frame.iloc[0]
    data_frame = data_frame[data_frame['Date'] != 'Date']
    data_frame['ident_year'] = 0
    data_frame['ident_year'] = data_frame['Date'].str[-4:]
    data_frame['ident_year'] = data_frame['ident_year'].astype(float)
    data_frame = data_frame[data_frame['ident_year'] < 2013]
    del data_frame['ident_year']
    return data_frame


prix_mensuel_carburants_97_06 = prix_carburants_cleaner_97_06(prix_mensuel_carburants)
prix_carburants_97_06 = prix_carburants_cleaner_97_06(prix_annuel_carburants)


def prix_carburants_cleaner_07_12(data_frame):
    data_frame = data_frame[data_frame['Unnamed: 9'] == '   '].copy()
    data_frame = data_frame[data_frame['super_plombe_ht'] != 'Super carburant']
    data_frame.rename(columns = {'Unnamed: 9': 'ident_year'}, inplace = True)
    data_frame['ident_year'] = data_frame['Date'].str[-4:-2]
    data_frame = data_frame[data_frame['ident_year'] != '19']
    data_frame.loc[data_frame['Date'] == 'Date', 'super_plombe_ht'] = 'diesel_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ht'] = 'super_95_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ht'] = 'super_98_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ht'] = 'gplc_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_plombe_ttc'] = 'diesel_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ttc'] = 'super_95_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ttc'] = 'super_98_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ttc'] = 'gplc_ttc'

    data_frame.columns = data_frame.iloc[0]
    data_frame = data_frame[data_frame['Date'] != 'Date'].copy()
    del data_frame['Da']
    del data_frame['   ']
    return data_frame


prix_mensuel_carburants_07_12 = prix_carburants_cleaner_07_12(prix_mensuel_carburants)
prix_carburants_07_12 = prix_carburants_cleaner_07_12(prix_annuel_carburants)


def prix_carburants_cleaner_13_17(data_frame):
    data_frame = data_frame[data_frame['Unnamed: 9'] != '   ']
    data_frame = data_frame[data_frame['super_plombe_ht'] != 'Super carburant']
    data_frame['ident_year'] = data_frame['Date'].str[-4:]
    data_frame['ident_year'] = data_frame['ident_year'].str[2:3]
    data_frame = data_frame[data_frame['ident_year'] != '9']
    data_frame = data_frame[data_frame['ident_year'] != '0']

    data_frame.loc[data_frame['Date'] == 'Date', 'super_plombe_ht'] = 'diesel_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ht'] = 'super_95_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ht'] = 'super_95_e10_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ht'] = 'super_98_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_plombe_ttc'] = 'gplc_ht'
    data_frame.loc[data_frame['Date'] == 'Date', 'diesel_ttc'] = 'diesel_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_95_ttc'] = 'super_95_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'super_98_ttc'] = 'super_95_e10_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'Unnamed: 9'] = 'super_98_ttc'
    data_frame.loc[data_frame['Date'] == 'Date', 'Unnamed: 10'] = 'gplc_ttc'

    data_frame.columns = data_frame.iloc[0]
    data_frame = data_frame[data_frame['Date'] != 'Date']
    del data_frame['t']
    return data_frame


prix_annuel_carburants_13_16 = prix_carburants_cleaner_13_17(prix_annuel_carburants)
prix_mensuel_carburants_13_17 = prix_carburants_cleaner_13_17(prix_mensuel_carburants)


def prix_mensuel_date_cleaner(data_frame):
    data_frame['annee'] = data_frame['Date'].str[-4:]
    data_frame['mois'] = data_frame['Date'].str[:-4]
    data_frame['mois'] = data_frame['mois'].str.replace('Janvier ', '1')
    data_frame['mois'] = data_frame['mois'].str.replace('Fevrier ', '2')
    data_frame['mois'] = data_frame['mois'].str.replace('Mars ', '3')
    data_frame['mois'] = data_frame['mois'].str.replace('Avril ', '4')
    data_frame['mois'] = data_frame['mois'].str.replace('Mai ', '5')
    data_frame['mois'] = data_frame['mois'].str.replace('Juin ', '6')
    data_frame['mois'] = data_frame['mois'].str.replace('Juillet ', '7')
    data_frame['mois'] = data_frame['mois'].str.replace('Aout ', '8')
    data_frame['mois'] = data_frame['mois'].str.replace('Septembre ', '9')
    data_frame['mois'] = data_frame['mois'].str.replace('Octobre ', '10')
    data_frame['mois'] = data_frame['mois'].str.replace('Novembre ', '11')
    data_frame['mois'] = data_frame['mois'].str.replace('Decembre ', '12')
    data_frame['mois'] = data_frame['mois'].astype(int)
    del data_frame['Date']
    return data_frame


prix_mensuel_carburants_90_96 = prix_mensuel_date_cleaner(prix_mensuel_carburants_90_96)
prix_mensuel_carburants_97_06 = prix_mensuel_date_cleaner(prix_mensuel_carburants_97_06)
prix_mensuel_carburants_07_12 = prix_mensuel_date_cleaner(prix_mensuel_carburants_07_12)
prix_mensuel_carburants_13_17 = prix_mensuel_date_cleaner(prix_mensuel_carburants_13_17)

# Tidy datasets:

prix_annuel_carburants_90_16 = pd.concat([prix_carburants_90_96, prix_carburants_97_06,
    prix_carburants_07_12, prix_annuel_carburants_13_16], axis = 0)


prix_mensuel_carburants_90_17 = pd.concat([prix_mensuel_carburants_90_96, prix_mensuel_carburants_97_06,
    prix_mensuel_carburants_07_12, prix_mensuel_carburants_13_17], axis = 0)
prix_mensuel_carburants_90_17 = prix_mensuel_carburants_90_17.convert_objects(convert_numeric=True)
