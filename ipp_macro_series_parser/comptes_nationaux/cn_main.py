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
    """
    Generates the table with all the data from Comptabilite Nationale.

    Parameters
    ----------
    year : int
        year of INSEE data realease
    list_years : list of integers
        list of years of interest. Optional.

    Example
    --------
    >>> year = 2013
    >>> entry_by_index_list = [{'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIB'},
             {'code': None, 'institution': 'S1', 'ressources': False, 'description': 'PIN'}]
    >>> output_path = "table_for_IPP.xlsx"
    >>> table2013  = cn_df_generator(2013)

    Returns the main table of comptabilite nationale data for years from all years from 1949 to 2013.
    """
    tee_df_by_year = tee_df_by_year_generator(year, list_years)  # arguments: (year, [years_list])
    non_tee_df_by_filename = non_tee_df_by_filename_generator(year)  # arguement: (year)

    df_full = pandas.DataFrame()

    for key, value in tee_df_by_year.items():
        df_full = df_full.append(value, ignore_index = True)

    for key, value in non_tee_df_by_filename.items():
        df_full = df_full.append(value, ignore_index = True)

    return df_full


def excel_table_generator(folder_year, entry_by_index_list, output_path):  # to add: argument list_years
    """
    Save the dataframe into an excel file with appropriate formating.

    Parameters
    ----------
    year : int
        year of INSEE data realease
    entry_by_index_list : list of dictionaries
        Dictionnaries should have keys 'code', 'institution', 'ressources', 'year', 'description', but not necesarily
        all of them.
    output_path : path
        Path to the excel file.

    Example
    --------
    >>> excel_table_generator(year, entry_by_index_list, output_path)
    >>> os.system('start excel.exe {}'.format(output_path))
    >>> table2013 = cn_df_generator(2013)
    >>> dico = {'code': 'B1g/PIB', 'institution': 'S1', 'ressources': False, 'year': None, 'description': 'PIB'}
    >>> df0 = look_up(table2013, dico)


    Returns a slice of cn_df_generator(2013) containing only the gross product (PIB) of the whole economy (S1),
    for all years.
    """
    df = cn_df_generator(folder_year)
    extractor(df, entry_by_index_list, output_path)
