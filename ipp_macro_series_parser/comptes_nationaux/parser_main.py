# -*- coding: utf-8 -*-


import logging
import os
import pandas
import numpy


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.comptes_nationaux.parser_tee import tee_df_by_year_generator
from ipp_macro_series_parser.comptes_nationaux.parser_non_tee import non_tee_df_by_filename_generator


log = logging.getLogger(__name__)


parser = Config()
hdf_directory = parser.get('data', 'cn_hdf_directory')


def cn_df_generator(year, list_years = None, drop_duplicates = True, subset = None):
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
    >>> table2013 = cn_df_generator(2013, list_years = range(1949, 2014))

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
    if not subset:
        subset = [u'code', u'institution', u'ressources', u'value', u'year']
    if drop_duplicates:
        df_full.drop_duplicates(subset = subset, inplace = True)
        if year == 2011:
            df_full['value_rounded'] = numpy.around(df_full['value'].astype('float64'), 3)
        else:
            df_full['value_rounded'] = numpy.around(df_full['value'].astype('float64'), 5)
        df_full = df_full.drop_duplicates(['code', 'institution', 'ressources', 'value_rounded', 'year'])
    return df_full


def get_comptes_nationaux_data(year, list_years = None, drop_duplicates = True, subset = None, force_recompute = False):
    # TODO: tests that all years are included in list_years
    hdf_file_name = 'comptes_nationaux_{}.h5'.format(year)
    key = 'test'
    file_path = os.path.join(hdf_directory, hdf_file_name)
    if force_recompute or not os.path.exists(file_path):
        log.info('Opening HDF5 file {} and (re)generating key {}'.format(hdf_file_name, key))
        df = cn_df_generator(year, list_years = list_years, drop_duplicates = drop_duplicates, subset = subset)
        save_df_to_hdf(df, hdf_file_name, key)
        return df
    else:
        log.info('Opening HDF5 file {} and reading key {}'.format(hdf_file_name, key))
        return import_hdf_to_df(hdf_file_name, key)


def save_df_to_hdf(df, hdf_file_name, key):
    file_path = os.path.join(hdf_directory, hdf_file_name)
    if not os.path.exists(hdf_directory):
        log.info('Directory {} does not exist. Creating it.'.format(hdf_directory))
        os.mkdir(hdf_directory)
    df.to_hdf(file_path, key)


def import_hdf_to_df(hdf_file_name, key):
    file_path = os.path.join(hdf_directory, hdf_file_name)
    log.info('Importing {} form {}'.format(key, file_path))
    store = pandas.HDFStore(file_path)
    df = store[key]
    store.close()
    return df
