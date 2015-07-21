# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:14:31 2015

@author: Antoine
"""

import pandas


from ipp_macro_series_parser.comptes_nationaux.cn_parser_tee import tee_df_by_year_generator
from ipp_macro_series_parser.comptes_nationaux.cn_parser_non_tee import non_tee_df_by_filename_generator


def cn_df_generator(year, list_years = None):
    tee_df_by_year = tee_df_by_year_generator(year, list_years)  # arguments: (year, [years_list])
    non_tee_df_by_filename = non_tee_df_by_filename_generator(year)  # arguement: (year)

    df_full = pandas.DataFrame()

    for key, value in tee_df_by_year.items():
        df_full = df_full.append(value, ignore_index = True)

    for key, value in non_tee_df_by_filename.items():
        df_full = df_full.append(value, ignore_index = True)

    return df_full


table = cn_df_generator(2013, range(2010, 2014))
