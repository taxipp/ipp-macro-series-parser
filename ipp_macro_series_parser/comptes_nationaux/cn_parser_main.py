# -*- coding: utf-8 -*-


# TaxIPP -- A french microsimulation model
# By: IPP <taxipp@oipp.eu>
#
# Copyright (C) 2012, 2013, 2014, 2015 IPP
# https://github.com/taxipp
#
# This file is part of TaxIPP.
#
# TaxIPP is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# TaxIPP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import os
import pandas
import pkg_resources


from ipp_macro_series_parser.config import Config
from ipp_macro_series_parser.comptes_nationaux.cn_parser_tee import tee_df_by_year_generator
from ipp_macro_series_parser.comptes_nationaux.cn_parser_non_tee import non_tee_df_by_filename_generator


log = logging.getLogger(__name__)


parser = Config(
    config_files_directory = os.path.join(pkg_resources.get_distribution('ipp-macro-series-parser').location)
    )
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
    return df_full


def get_comptes_nationaux_data(year, list_years = None, drop_duplicates = True, subset = None, force_recompute = False):
    # TODO: tests that all years are included in list_years
    hdf_file_name = 'comptes_nationaux.h5'
    key = 'test'
    file_path = os.path.join(hdf_directory, hdf_file_name)
    if force_recompute or not os.path.exists(file_path):
        df = cn_df_generator(year, list_years = list_years, drop_duplicates = drop_duplicates, subset = subset)
        save_df_to_hdf(df, hdf_file_name, key)
        return df
    else:
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
