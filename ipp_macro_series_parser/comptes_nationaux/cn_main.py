# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:14:31 2015

@author: Antoine
"""

import os
import pandas


from ipp_macro_series_parser.comptes_nationaux.cn_parser_tee import tee_df_by_year_generator
from ipp_macro_series_parser.comptes_nationaux.cn_parser_non_tee import non_tee_df_by_filename_generator
from ipp_macro_series_parser.comptes_nationaux.cn_extract_data import extractor


def cn_df_generator(year, list_years = None):
    tee_df_by_year = tee_df_by_year_generator(year, list_years)  # arguments: (year, [years_list])
    non_tee_df_by_filename = non_tee_df_by_filename_generator(year)  # arguement: (year)

    df_full = pandas.DataFrame()

    for key, value in tee_df_by_year.items():
        df_full = df_full.append(value, ignore_index = True)

    for key, value in non_tee_df_by_filename.items():
        df_full = df_full.append(value, ignore_index = True)

    return df_full


def excel_table_generator(folder_year, entry_by_index_list, output_path):  # to add: argument list_years
    df = cn_df_generator(folder_year)
    extractor(df, entry_by_index_list, output_path)


# This is a test of most of the methods
year = 2013
entry_by_index_list = [{'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIB'},
             {'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIN'}]
output_path = "table_for_IPP.xlsx"

excel_table_generator(year, entry_by_index_list, output_path)
os.system('start excel.exe {}'.format(output_path))
