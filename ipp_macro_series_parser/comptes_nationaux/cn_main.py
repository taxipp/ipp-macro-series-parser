# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:14:31 2015

@author: Antoine
"""

import pandas
# import functions from other files:
from ipp_macro_series_parser.comptes_nationaux.cn_parser_tee import tee_df_generator
from ipp_macro_series_parser.comptes_nationaux.cn_parser_non_tee import non_tee_df_generator


def cn_df_generator(year, list_years = None):
    tee_df_dict = tee_df_generator(year, list_years)  # arguments: (year, [years_list])
    non_tee_df_dict = non_tee_df_generator(year)  # arguement: (year)

    df_full = pandas.DataFrame()

    for key, value in tee_df_dict.items():
        df_full = df_full.append(value, ignore_index = True)

    for key, value in non_tee_df_dict.items():
        df_full = df_full.append(value, ignore_index = True)

    return df_full


table = cn_df_generator(2013)
