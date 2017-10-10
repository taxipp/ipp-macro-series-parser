# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from ipp_macro_series_parser.config import Config

parser = Config()

transports_directory = parser.get('data', 'transports_directory')
g_bilan_circulation = transports_directory + '/Annexes_G_-_Bilan_de_la_circulation.xls'

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


parc_auto = transports_parser(g_bilan_circulation, 4)  # composition moyenne du parc automobile (ess/die)
consommation = transports_parser_categ(g_bilan_circulation, 5)  # consommation en L au 100 par type de véhicule (ess/die)
