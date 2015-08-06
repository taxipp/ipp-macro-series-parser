# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:14:31 2015

@author: Antoine
"""
import os
import pandas
import pkg_resources


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.comptes_nationaux.cn_parser_tee import tee_df_by_year_generator
from ipp_macro_series_parser.comptes_nationaux.cn_parser_non_tee import non_tee_df_by_filename_generator

parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
hdf_directory = parser.get('data', 'cn_hdf_directory')



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
    >>> list_years = None
    >>> table2013 = cn_df_generator(2013)

    Returns the main table of comptabilite nationale data for all years from 1949 to 2013.
    """
    tee_df_by_year = tee_df_by_year_generator(year, list_years)  # arguments: (year, [years_list])
    non_tee_df_by_filename = non_tee_df_by_filename_generator(year)  # arguement: (year)

    df_full = pandas.DataFrame()

    for key, value in tee_df_by_year.items():
        df_full = df_full.append(value, ignore_index = True)

    for key, value in non_tee_df_by_filename.items():
        df_full = df_full.append(value, ignore_index = True)

    df_full[['year']] = df_full[['year']].astype(int)

    return df_full


def save_df_to_hdf(df, hdf_file_name, key):
    file_path = os.path.join(hdf_directory, hdf_file_name)
    df.to_hdf(file_path, key)
    pandas.DataFrame().to_hdf


def import_hdf_to_df(hdf_file_name, key):
    file_path = os.path.join(hdf_directory, hdf_file_name)
    store = pandas.HDFStore(file_path)
    df = store[key]
    return df
