# -*- coding: utf-8 -*-


import numpy
import os
import pandas
import pkg_resources


from ipp_macro_series_parser.config import Config

config_parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
xls_directory = config_parser.get('data', 'denombrements_fiscaux_xls')
# hdf_directory = config_parser.get('data', 'denombrements_fiscaux_hdf')


def df_by_year_generator():
    df = pandas.read_excel(os.path.join(xls_directory, '2042_national.xls'), sheetname = 'montant')

    assert df.dtypes.apply(lambda x: numpy.issubdtype(x, numpy.float)).all(), df.dtypes
    df = df.stack()
    df = df.reset_index()
    df.rename(columns = {'level_0': 'code', 'level_1': 'year', 0: 'value'}, inplace = True)
    return df


def denombrements_fiscaux_df_generator(year = None, years = None):
    """
    Generates the table with all the data from Dénombrements Fiscaux .

    Parameters
    ----------
    year : int
        year of DGFIP data (coincides with year of declaration)
    years : list of integers
        list of years of interest. Optional.

    Example
    --------
    >>> table_2013 = denombrements_fiscaux_df_generator(year = 2013)

    Returns the main table of dénombrements fiscaux for the year 2013.
    """
    if year is not None and years is None:
        years = [year]
    df = df_by_year_generator()
    df[['year']] = df[['year']].astype(int)
    return df.loc[df.year.isin(years)].copy() if years is not None else df.copy()


def save_df_to_hdf(df, hdf_file_name, key):
    file_path = os.path.join(hdf_directory, hdf_file_name)
    df.to_hdf(file_path, key)
    pandas.DataFrame().to_hdf


def import_hdf_to_df(hdf_file_name, key):
    file_path = os.path.join(hdf_directory, hdf_file_name)
    store = pandas.HDFStore(file_path)
    df = store[key]
    return df
